from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  
from app.routes import router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="ComicCraft API",
    description="AI Comic Story Creator",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routes
app.include_router(router)

templates = Jinja2Templates(directory="app/templates")

@app.get("/health")
def health():
    return {"status": "ok"}