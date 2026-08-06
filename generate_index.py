"""
generate_index.py

Scans the current directory tree for `index.html` files (i.e. individual
frontend pages/projects) and generates a polished root-level `index.html`
that links to each one.

Usage:
    python generate_index.py
"""

from __future__ import annotations

import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_FILE = BASE_DIR / "index.html"

EXCLUDED_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
}

# A small rotating palette so each card gets a distinct accent color.
ACCENT_COLORS = [
    "#6366f1",  # indigo
    "#8b5cf6",  # violet
    "#ec4899",  # pink
    "#f59e0b",  # amber
    "#10b981",  # emerald
    "#06b6d4",  # cyan
    "#ef4444",  # red
]


@dataclass(frozen=True)
class Page:
    name: str
    url: str
    accent: str


def discover_pages() -> list[Page]:
    """Find every index.html in the tree (excluding the generated root one)."""
    found: list[tuple[str, str]] = []

    for index in BASE_DIR.rglob("index.html"):
        rel = index.relative_to(BASE_DIR)

        # Skip the generated root index itself.
        if rel == Path("index.html"):
            continue

        # Skip excluded folders anywhere in the path.
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue

        folder = rel.parent
        name = folder.as_posix()
        url = urllib.parse.quote(name) + "/"
        found.append((name, url))

    found.sort(key=lambda item: item[0].lower())

    return [
        Page(name=name, url=url, accent=ACCENT_COLORS[i % len(ACCENT_COLORS)])
        for i, (name, url) in enumerate(found)
    ]


def humanize(name: str) -> str:
    """Turn a folder path like 'my-cool-app' into 'My Cool App'."""
    label = name.rsplit("/", 1)[-1]
    label = label.replace("-", " ").replace("_", " ")
    return label.strip().title() or name


def render_card(page: Page) -> str:
    display_name = humanize(page.name)
    initial = display_name[:1].upper() or "?"
    return f"""        <a class="card" href="{page.url}" style="--accent:{page.accent}">
          <span class="card-icon" aria-hidden="true">{initial}</span>
          <span class="card-body">
            <span class="card-title">{display_name}</span>
            <span class="card-path">/{page.url}</span>
          </span>
          <span class="card-arrow" aria-hidden="true">&rarr;</span>
        </a>"""


def render_empty_state() -> str:
    return """        <div class="empty">
          <p>No pages found yet.</p>
          <p class="empty-sub">Add a folder containing an <code>index.html</code> and regenerate.</p>
        </div>"""


def build_html(pages: list[Page]) -> str:
    cards_html = "\n".join(render_card(p) for p in pages) if pages else render_empty_state()
    count = len(pages)
    count_label = "page" if count == 1 else "pages"
    generated_at = datetime.now().strftime("%B %d, %Y at %H:%M")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Project Index</title>
<style>
  :root {{
    --bg-1: #0f172a;
    --bg-2: #1e1b4b;
    --surface: rgba(255, 255, 255, 0.06);
    --surface-hover: rgba(255, 255, 255, 0.1);
    --border: rgba(255, 255, 255, 0.1);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --radius: 16px;
  }}

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    font-family: "Segoe UI", "Inter", system-ui, -apple-system, sans-serif;
    min-height: 100vh;
    color: var(--text-primary);
    background:
      radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.25), transparent 40%),
      radial-gradient(circle at 85% 80%, rgba(236, 72, 153, 0.2), transparent 45%),
      linear-gradient(160deg, var(--bg-1), var(--bg-2));
    background-attachment: fixed;
    display: flex;
    justify-content: center;
    padding: 64px 20px;
  }}

  .container {{
    width: 100%;
    max-width: 760px;
  }}

  header {{
    text-align: center;
    margin-bottom: 40px;
  }}

  .eyebrow {{
    display: inline-block;
    font-size: 12px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--text-secondary);
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 6px 14px;
    border-radius: 999px;
    margin-bottom: 18px;
  }}

  h1 {{
    font-size: clamp(28px, 5vw, 40px);
    font-weight: 700;
    letter-spacing: -0.02em;
    margin-bottom: 10px;
  }}

  .subtitle {{
    color: var(--text-secondary);
    font-size: 15px;
  }}

  .cards {{
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}

  .card {{
    --accent: #6366f1;
    position: relative;
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 18px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    text-decoration: none;
    color: var(--text-primary);
    overflow: hidden;
    transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease;
  }}

  .card::before {{
    content: "";
    position: absolute;
    inset: 0;
    left: 0;
    width: 4px;
    background: var(--accent);
  }}

  .card:hover {{
    background: var(--surface-hover);
    border-color: color-mix(in srgb, var(--accent) 50%, var(--border));
    transform: translateY(-2px);
  }}

  .card-icon {{
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 16px;
    color: var(--bg-1);
    background: var(--accent);
  }}

  .card-body {{
    display: flex;
    flex-direction: column;
    min-width: 0;
    flex: 1;
  }}

  .card-title {{
    font-weight: 600;
    font-size: 15.5px;
  }}

  .card-path {{
    font-size: 12.5px;
    color: var(--text-secondary);
    font-family: "SFMono-Regular", Consolas, monospace;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  .card-arrow {{
    flex-shrink: 0;
    color: var(--text-secondary);
    font-size: 18px;
    transition: transform 0.18s ease, color 0.18s ease;
  }}

  .card:hover .card-arrow {{
    transform: translateX(4px);
    color: var(--text-primary);
  }}

  .empty {{
    text-align: center;
    padding: 48px 24px;
    background: var(--surface);
    border: 1px dashed var(--border);
    border-radius: var(--radius);
    color: var(--text-secondary);
  }}

  .empty p {{
    margin-bottom: 6px;
  }}

  .empty-sub {{
    font-size: 13px;
  }}

  .empty code {{
    background: rgba(255, 255, 255, 0.08);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "SFMono-Regular", Consolas, monospace;
  }}

  footer {{
    text-align: center;
    margin-top: 40px;
    font-size: 12.5px;
    color: var(--text-secondary);
  }}
</style>
</head>
<body>
  <div class="container">
    <header>
      <span class="eyebrow">{count} {count_label} found</span>
      <h1>Project Index</h1>
      <p class="subtitle">Every page discovered under this directory, ready to open.</p>
    </header>

    <main class="cards">
{cards_html}
    </main>

    <footer>Generated on {generated_at}</footer>
  </div>
</body>
</html>
"""


def main() -> None:
    pages = discover_pages()
    html = build_html(pages)
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with {len(pages)} page(s) linked.")


if __name__ == "__main__":
    main()