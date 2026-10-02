from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="ComicCraft")

# 1. HOME + HEALTH - Render ku mukkiyam
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    return {"status": "ok", "message": "ComicCraft API Running - Go to /docs for API"}

@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {"status": "ok"}

# 2. Static folder
if os.path.exists("static"):
    try:
        app.mount("/static", StaticFiles(directory="static"), name="static")
    except:
        pass

if os.path.exists("app/static"):
    try:
        app.mount("/app_static", StaticFiles(directory="app/static"), name="app_static")
    except:
        pass

# 3. YOUR ORIGINAL ROUTES - CORRECT
try:
    from app.routes import router as comic_router
    app.include_router(comic_router)
    print("✅ Comic router loaded from app.routes")
except Exception as e:
    print(f"❌ Router load failed: {e}")
    import traceback
    traceback.print_exc()

print("✅ App startup complete")
