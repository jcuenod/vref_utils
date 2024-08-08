import linecache
from .verse import Verse
from .versification import get_versification_mapping, get_versification_range
from typing import List

class Vref:
    def __init__(self, vref_file, versification_vref_path=None):
        self.vref_file = vref_file
        self.verse_to_line_mappings = get_versification_mapping() if versification_vref_path is None else get_versification_mapping(versification_vref_path)

    def __getitem__(self, key: str) -> List[Verse]:
        """
        Returns a list of Verse objects based on the key provided. The key
        can be a single verse reference, a comma-separated list of verse
        references, or a range of verse references. The verse references
        can be in the format "GEN 1:1" or "GEN 1:1-3". The verse references
        must be in the USFM book name format and books and chapters must be
        explicitly stated (no implicit books or chapters).

        Supported formats:
        - "GEN 1:1"
        - "GEN 1:1,GEN 1:2-GEN 1:3"
        - "GEN 1:1-3"

        Args:
            key (str): The verse reference or references to retrieve.

        Returns:
            list[Verse]: A list of Verse objects for the requested verses.
        """
        if "," in key or "-" in key:
            return self._get_ranges_and_selections(key)
        return [self._get_verse(key)]
    
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