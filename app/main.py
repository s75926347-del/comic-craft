from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="ComicCraft")

# 1. Health check for Render - MOST IMPORTANT
@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {"status": "ok"}

# 2. Mount static if exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Load your actual router - CORRECT IMPORT
try:
    from app.routes import router as comic_router
    app.include_router(comic_router)
    print("✅ Comic router loaded from app.routes")
except Exception as e:
    print(f"❌ Router load failed: {e}")
    import traceback
    traceback.print_exc()

# 4. Also mount templates static
if os.path.exists("app/templates"):
    # This is handled inside routes.py
    pass

print("✅ App startup complete")
