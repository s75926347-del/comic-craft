from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import os

from app.routes import router

app = FastAPI(title="ComicCraft", version="1.0")

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "ComicCraft Live 🚀",
        "status": "ok",
        "docs": "/docs",
        "ui": "/ui",
        "test_image": "/test-image?prompt=brave fox"
    }

# FIXED UI ROUTE - NO JINJA ERROR!
@app.get("/ui", response_class=HTMLResponse)
async def ui_page():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
        # fallback check
        if not os.path.exists(file_path):
            file_path = os.path.join("app", "templates", "index.html")
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading template: {e}</h1><a href='/docs'>Go to Docs</a>")
