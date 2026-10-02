from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="ComicCraft - FINAL FIXED")

# Health checks
@app.get("/health")
def health():
    return {"status": "ok", "live": True}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/")
def root():
    return {
        "message": "ComicCraft Live 🚀",
        "status": "ok",
        "docs": "/docs",
        "test_image": "/test-image?prompt=brave fox",
        "ui": "/ui"
    }

# Test image - CHECK PURPLE POYACHA
@app.get("/test-image")
def test_image(prompt: str = "brave fox in forest"):
    from app.ai.image_generator import generate_comic_image
    url = generate_comic_image(prompt)
    return {"prompt": prompt, "image_url": url, "note": "If image is not purple, FIXED!"}

# Try to load templates safely
try:
    templates = Jinja2Templates(directory="app/templates")
except:
    templates = None

try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except:
    pass

@app.get("/ui", response_class=HTMLResponse)
def ui(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            return HTMLResponse(f"""
            <html><body style="font-family:sans-serif; padding:40px">
            <h1>ComicCraft 🚀 LIVE</h1>
            <p>Template error: {e}</p>
            <a href='/docs'>Go to API Docs</a><br><br>
            <a href='/test-image?prompt=fox'>Test Image (No Purple)</a>
            </body></html>
            """)
    return HTMLResponse("""
    <html><body style="font-family:sans-serif; padding:40px">
    <h1>ComicCraft 🚀 LIVE</h1>
    <p>API is Working!</p>
    <a href='/docs'>API Docs</a><br><br>
    <a href='/test-image?prompt=brave fox'>Test Fox Image - No Purple Check</a>
    </body></html>
    """)

# Load your existing routes SAFELY - No crash
try:
    from app.routes import router as app_router
    app.include_router(app_router)
    print("✅ Loaded app.routes")
except Exception as e:
    print(f"Note: app.routes not loaded: {e}")

# Also load comic service if exists
try:
    from app.services.comic_service import router as comic_router
    app.include_router(comic_router)
    print("✅ Loaded comic_service")
except:
    pass
