import linecache
from .versification import get_versification_mapping, get_versification_range

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

class Vref:
    def __init__(self, vref_file):
        self.vref_file = vref_file
        self.verse_to_line_mappings = get_versification_mapping()

    # Supports ["GEN 1:1"], ["GEN 1:1,GEN 1:2-GEN 1:3"], ["GEN 1:1-3"] etc.
    # Requires , for multiple selections and - for ranges.
    # Requires USFM book names.
    # No implicit books or chapters. 
    def __getitem__(self, key: str):
        if "," in key or "-" in key:
            return self._get_ranges_and_selections(key)
        
        return [Verse(key, self._get_verse(key))]
    
    def _get_ranges_and_selections(self, key):
        selections = key.split(",")
        lines = []
        for selection in selections:
            if "-" in selection:
                start, end = selection.split("-")
                verse_keys = get_versification_range(start.strip(), end.strip(), self.verse_to_line_mappings)
                lines.extend([self._get_verse(v) for v in verse_keys])
            else:
                verse_key = selection.strip()
                lines.append(self._get_verse(verse_key))
        return lines
    
    def _get_verse(self, ref):
        line_number = self.verse_to_line_mappings[ref]
        return Verse(ref, linecache.getline(self.vref_file, line_number).strip())