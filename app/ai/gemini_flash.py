def generate_outline(prompt: str):
    class Panel:
        def __init__(self, title, description, dialogue):
            self.title=title; self.description=description; self.dialogue=dialogue
    return [
        Panel("Panel 1: The Beginning", f"{prompt} in enchanted forest, bright morning", "Wow! What a beautiful day!"),
        Panel("Panel 2: The Challenge", f"{prompt} sees a big problem, dramatic", "Oh no! What to do?"),
        Panel("Panel 3: The Plan", f"{prompt} gets a clever idea, closeup", "I have an idea!"),
        Panel("Panel 4: The Action", f"{prompt} doing heroic action, dynamic", "Let's go!"),
        Panel("Panel 5: The Happy Ending", f"{prompt} happy celebration, sunset", "We did it!")
    ]