import linecache
import os

from .book_lists import dt_books, nt_books, ot_books
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

        self._vref_file = vref_file
        self._verse_to_line_mappings = (
            get_versification_mapping()
            if versification_vref_path is None
            else get_versification_mapping(versification_vref_path)
        )
        self.stats = self._get_stats()

    def _get_stats(self):
        all_verses = self._verse_to_line_mappings.keys()
        books = [v.split(" ")[0] for v in all_verses]
        books_unique = list(dict.fromkeys(books))

        def verses_in_book(book):
            return [v for v in all_verses if v.split(" ")[0] == book]

        def progress(verse_list):
            count = 0
            for ref in verse_list:
                v = self._get_verse(ref)
                if len(v.text) > 0:
                    count += 1
            return count, len(verse_list)

        def aggregate_progress(verses_complete, corpus):
            total = 0
            count = 0
            for book in corpus:
                book_count, book_total = verses_complete[book]
                count += book_count
                total += book_total
            return count / total

        verses_in_vref_file = len(self)
        progress_percentage = round(
            verses_in_vref_file / len(self._verse_to_line_mappings), 1
        )
        verses_complete = {b: progress(verses_in_book(b)) for b in books_unique}

        return {
            "verses": verses_in_vref_file,
            "progress": progress_percentage,
            "summary": {
                "whole_bible": progress_percentage,
                "old_testament": round(
                    aggregate_progress(verses_complete, ot_books), 1
                ),
                "new_testament": round(
                    aggregate_progress(verses_complete, nt_books), 1
                ),
                "deuterocanonical": round(
                    aggregate_progress(verses_complete, dt_books), 1
                ),
            },
            "details": {
                b: round(verses_complete[b][0] / verses_complete[b][1], 1)
                for b in books_unique
            },
        }

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
        for verse_key in self._verse_to_line_mappings.keys():
            yield self._get_verse(verse_key)

    def __len__(self):
        count = 0
        for verse in self:
            if len(verse.text) > 0:
                count += 1
        return count

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
                    start.strip(), end.strip(), self._verse_to_line_mappings
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
        line_number = self._verse_to_line_mappings[ref]
        return Verse(ref, linecache.getline(self._vref_file, line_number).strip())
