from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="ComicCraft")

# 1. HEALTH ONLY - / vida koodathu
@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {"status": "ok"}

# 2. YOUR ORIGINAL UI - FIRST LOAD
try:
    from app.routes import router as comic_router
    app.include_router(comic_router)
    print("✅ Comic router loaded - UI will be at /")
except Exception as e:
    print(f"❌ Router load failed: {e}")
    import traceback
    traceback.print_exc()

# 3. Static folders
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

print("✅ App startup complete")
