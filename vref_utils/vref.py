import linecache
import os
from collections import Counter

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
        self._stats_cache = None

    @property
    def stats(self):
        if self._stats_cache is None:
            self._stats_cache = self._get_stats()
        return self._stats_cache

    def _get_stats(self):
        # 1. Count the number of verses in each book and the total number of verses.
        book_verse_totals = Counter(
            ref.split(" ")[0] for ref in self._verse_to_line_mappings.keys()
        )
        books_unique = list(book_verse_totals.keys())
        total_possible_verses = len(self._verse_to_line_mappings)

        # 2. Create a reverse mapping from line number to verse reference.
        line_to_verse_mapping = {v: k for k, v in self._verse_to_line_mappings.items()}

        # 3. Iterate through the vref file ONCE, line by line.
        #    This avoids loading the whole file into memory and allows us to
        #    calculate all stats in a single pass.
        verses_in_vref_file = 0
        book_verse_completed = Counter()
        with open(self._vref_file, "r") as f:
            for line_num, line in enumerate(f, 1):
                if line.strip():
                    verses_in_vref_file += 1
                    # Find the verse ref for this line number
                    verse_ref = line_to_verse_mapping.get(line_num)
                    if verse_ref:
                        # Increment the completed count for the correct book
                        book = verse_ref.split(" ")[0]
                        book_verse_completed[book] += 1

        # 4. Calculate final stats using the pre-computed data.
        progress_percentage = (
            round(verses_in_vref_file / total_possible_verses, 1)
            if total_possible_verses > 0
            else 0
        )

        def aggregate_progress(corpus_books):
            count = sum(book_verse_completed[book] for book in corpus_books)
            total = sum(book_verse_totals[book] for book in corpus_books)
            return round(count / total, 1) if total > 0 else 0

        return {
            "verses": verses_in_vref_file,
            "progress": progress_percentage,
            "summary": {
                "whole_bible": progress_percentage,
                "old_testament": aggregate_progress(ot_books),
                "new_testament": aggregate_progress(nt_books),
                "deuterocanonical": aggregate_progress(dt_books),
            },
            "details": {
                book: (
                    round(book_verse_completed[book] / book_verse_totals[book] * 100, 1)
                    if book_verse_totals[book] > 0
                    else 0
                )
                for book in books_unique
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
