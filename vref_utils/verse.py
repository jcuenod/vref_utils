class Verse:
    def __init__(self, reference, text):
        self.reference = reference
        self.text = text

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"""Verse(verse="{self.reference}", text="{self.text}")"""

    def __getattr__(self, name):
        if name == "verse":
            return self.reference
        if name == "text":
            return self.text
        raise AttributeError(f"Verse object has no attribute {name}")
