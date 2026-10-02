from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Request
import os

app = FastAPI()

# Fix for Render HEAD health check
@app.api_route("/", methods=["GET", "HEAD"])
async def root(request: Request):
    return FileResponse("app/templates/index.html")

@app.get("/health")
@app.head("/health")
async def health():
    return {"status": "ok"}

# Mount static
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Import routers if you have
try:
    from app.routes import comic
    app.include_router(comic.router)
except Exception as e:
    print(f"Router load failed: {e}")
