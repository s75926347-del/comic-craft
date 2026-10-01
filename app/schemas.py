from pydantic import BaseModel
from typing import List, Optional

class PanelOutline(BaseModel):
    panel: int
    description: str
    dialogue: str
    title: Optional[str] = None

class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str

class ComicLayout(BaseModel):
    panel_number: int
    title: str
    description: str
    dialogue: str
    image_path: str
    narration: str