from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
import os

app = FastAPI()

# 1. Health check - Render ku romba mukkiyam
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return JSONResponse({"status": "ok", "message": "ComicCraft is Live!"})

@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {"status": "ok"}

# 2. Static folder iruntha mount pannu
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. App routes - un original comic routes
try:
    from app.routes.comic import router as comic_router
    app.include_router(comic_router)
    print("Comic router loaded")
except Exception as e:
    print(f"Comic router failed: {e}")

try:
    from app.core import exporter
    print("Exporter loaded")
except Exception as e:
    print(f"Exporter failed: {e}")

# 4. Frontend - HTML file enga irukku nu thedu
@app.api_route("/app", methods=["GET", "HEAD"])
async def serve_frontend():
    possible_paths = [
        "app/templates/index.html",
        "templates/index.html",
        "static/index.html",
        "frontend/index.html",
        "index.html"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            with open(p, 'r') as f:
                return HTMLResponse(f.read())
    return JSONResponse({"detail": "Frontend not found, but API is running. Go to /docs"})
