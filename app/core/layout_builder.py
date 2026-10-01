def build_comic_layout(panels, images, story_text):
    layout = []
    for i, panel in enumerate(panels):
        layout.append({
            "panel_number": panel.panel if hasattr(panel, 'panel') else i+1,
            "title": f"Panel {i+1}: {panel.description[:30] if hasattr(panel, 'description') else 'Scene'}",
            "description": panel.description if hasattr(panel, 'description') else str(panel),
            "dialogue": panel.dialogue if hasattr(panel, 'dialogue') else "",
            "image_path": images[i] if i < len(images) else "",
            "narration": story_text # full story
        })
    return layout