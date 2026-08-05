from pathlib import Path
import urllib.parse

# Folder containing your frontend pages
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


def build_html():
    pages = []

    for index in BASE_DIR.rglob("index.html"):
        rel = index.relative_to(BASE_DIR)

        # Skip the generated root index
        if rel == Path("index.html"):
            continue

        # Skip excluded folders
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue

        folder = rel.parent
        url = urllib.parse.quote(folder.as_posix()) + "/"

        pages.append((folder.as_posix(), url))

    pages.sort()

    links = "\n".join(
        f'                <a href="{url}">{name}</a>'
        for name, url in pages
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Frontend Index</title>

<style>
* {{
    margin:0;
    padding:0;
    box-sizing:border-box;
    font-family:Arial,sans-serif;
}}

body {{
    background:linear-gradient(135deg,#f5f7fa,#c3cfe2);
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px;
}}

.container {{
    background:white;
    padding:40px;
    border-radius:12px;
    width:100%;
    max-width:700px;
    box-shadow:0 10px 30px rgba(0,0,0,.1);
}}

h1 {{
    text-align:center;
    margin-bottom:25px;
}}

a {{
    display:block;
    padding:12px;
    margin:8px 0;
    background:#4f46e5;
    color:white;
    text-decoration:none;
    border-radius:8px;
    transition:.2s;
}}

a:hover {{
    background:#6366f1;
}}
</style>
</head>
<body>
<div class="container">
<h1>Frontend Index</h1>

{links if links else "<p>No pages found.</p>"}

</div>
</body>
</html>
"""


def main():
    html = build_html()
    OUTPUT_FILE.write_text(html, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()