from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from src import generate_index
app = FastAPI()
BASE_DIR = Path(__file__).parent.parent
STATIC_PATH = BASE_DIR / "static" 
INDEX_PATH = STATIC_PATH / "index.html"
ALLOWED_EXTENSIONS = {".html", ".css", ".js",".png"}
generate_index.main(STATIC_PATH,INDEX_PATH)
# -----------------------------
# FILE SERVER (FIXED FOR VERCEL)
# -----------------------------
@app.get("{path:path}")
async def serve_static(path: str):
    # if path == '/':# this oterwise destrois the static path with pathlib 
    #     path = '.' 
    print(f"path: {path}")
    expanded_path = path
    # Case 1: /extract-colors/ → /extract-colors/index.html
    if path.endswith("/"):
        print("full path is dir")
        expanded_path = path + "index.html"

    # Case 2: no extension → assume html page
    elif '.' not in path: #and path.split('.')[-1] == :
        print("full path has no siffix then html")
        expanded_path = path + ".html"

    print("expanded_path:",expanded_path)
    print("STATIC_PATH:",STATIC_PATH)
    os_path_str = str(STATIC_PATH) + expanded_path
    print("os_path_str:",os_path_str)
    os_path = Path(os_path_str)
    print("os_path:",os_path)
    print("os_path resolved:",os_path.resolve())

    # Security + existence check
    if (not os_path.exists()):
        raise HTTPException(status_code=404, detail="File not found v0")
    if os_path.suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=403, detail="Not allowed")
        # or STATIC_PATH not in full_path.parents

    return FileResponse(os_path)