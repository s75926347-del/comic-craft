import os
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ping")
def ping():
    return {"pong": True}

@app.get("/")
def home():
    return {"message": "ComicCraft Live", "status": "ok"}

# Try to load real app AFTER health checks
try:
    from app.core.routes import router as core_router
    app.include_router(core_router)
    print("✅ Core routes loaded")
except Exception as e:
    print(f"⚠️ Core routes failed: {e}")

try:
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory="app/static"), name="static")
except:
    pass

@app.get("/ui")
def ui():
    try:
        return FileResponse("app/templates/index.html")
    except:
        return {"ui": "not found but app is live"}
