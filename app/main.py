import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(title="ComicCraft")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return {"pong": True}

# --- FIXED IMPORTS - CORRECT PATH ---
# routes.py is at app/routes.py, not app.core.routes
try:
    from routes import router as main_router
    app.include_router(main_router)
    print("✅ Loaded: routes.router")
except Exception as e:
    print(f"⚠️ routes failed: {e}")
    try:
        from app.routes import router as main_router
        app.include_router(main_router)
        print("✅ Loaded: app.routes.router")
    except Exception as e2:
        print(f"⚠️ app.routes failed: {e2}")

# Also try services
try:
    from services.comic_service import router as service_router
    app.include_router(service_router)
except:
    pass

# Templates & Static
try:
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except:
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except:
        pass

templates = None
try:
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
except:
    pass

@app.get("/")
def root(request: Request = None):
    # Try to serve UI
    try:
        if templates:
            return templates.TemplateResponse("index.html", {"request": request})
    except:
        pass
    try:
        return FileResponse("app/templates/index.html")
    except:
        return {"message": "ComicCraft Live 🚀", "status": "ok", "go_to": "/docs"}

@app.get("/ui")
def ui(request: Request = None):
    try:
        if templates:
            return templates.TemplateResponse("index.html", {"request": request})
    except:
        pass
    return {"message": "API Live, UI template not found, but /docs works"}

# Direct image gen test
from app.ai.image_generator import generate_comic_image

@app.get("/test-image")
def test_image(prompt: str = "brave fox"):
    url = generate_comic_image(prompt)
    return {"prompt": prompt, "image_url": url}
