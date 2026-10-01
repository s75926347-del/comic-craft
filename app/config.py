from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    gemini_api_key: str = ""
    hf_token: str = ""
    demo_mode: bool = False
    static_dir: Path = Path("app/static")
    
    gemini_outline_model: str = "gemini-2.0-flash"
    gemini_story_model: str = "gemini-2.0-flash"
    hf_image_model: str = "black-forest-labs/FLUX.1-schnell"
    image_width: int = 768
    image_height: int = 768

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

def get_settings():
    return Settings()