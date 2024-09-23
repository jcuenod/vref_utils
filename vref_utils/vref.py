import linecache
import os

from .verse import Verse
from .verse_list import VerseList
from .versification import get_versification_mapping, get_versification_range


def exists_or_raise(file_path, message):
    if not os.path.exists(file_path):
        raise FileNotFoundError(message)


class Vref:
    def __init__(self, vref_file, versification_vref_path=None):
        exists_or_raise(vref_file, f"Vref file not found: {vref_file}")
        exists_or_raise(
            versification_vref_path,
            f"File not found (versification_vref_path): {versification_vref_path}",
        ) if versification_vref_path is not None else None

        self.vref_file = vref_file
        self.verse_to_line_mappings = (
            get_versification_mapping()
            if versification_vref_path is None
            else get_versification_mapping(versification_vref_path)
        )

    def __getitem__(self, verse_range_and_or_selections: str) -> VerseList:
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
        if "," in verse_range_and_or_selections or "-" in verse_range_and_or_selections:
            return self._get_verse_list_for_ranges_and_selections(
                verse_range_and_or_selections
            )

        return self._get_verse_list_for_one_verses(verse_range_and_or_selections)

    def __iter__(self):
        for verse_key in self.verse_to_line_mappings.keys():
            yield self._get_verse(verse_key)

    def __len__(self):
        return len(self.verse_to_line_mappings)

    def _get_verse_list_for_ranges_and_selections(
        self, verse_range_and_or_selections: str
    ):
        return VerseList(
            lambda: self._get_ranges_and_selections(verse_range_and_or_selections)
        )

    def _get_ranges_and_selections(self, verse_range_and_or_selections: str):
        selections = verse_range_and_or_selections.split(",")
        for selection in selections:
            if "-" in selection:
                start, end = selection.split("-")
                verse_keys = get_versification_range(
                    start.strip(), end.strip(), self.verse_to_line_mappings
                )
                for verse_key in verse_keys:
                    yield self._get_verse(verse_key)
            else:
                verse_key = selection.strip()
                yield self._get_verse(verse_key)

    def _get_verse_list_for_one_verses(self, verse_range: str):
        return VerseList(lambda: self._yield_one_verse(verse_range))

    def _yield_one_verse(self, verse_key: str):
        yield self._get_verse(verse_key)

    def _get_verse(self, ref: str):
        line_number = self.verse_to_line_mappings[ref]
        return Verse(ref, linecache.getline(self.vref_file, line_number).strip())
