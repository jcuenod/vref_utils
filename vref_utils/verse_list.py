from typing import Callable, Generator, Union

from .verse import Verse


class VerseList:
    # vref_generator is a callable that returns a Generator[Verse, None, None]
    def __init__(self, vref_generator: Callable[[], Generator[Verse, None, None]]):
        self.vref_generator = vref_generator
        self.length = len(list(vref_generator()))

    def __getitem__(self, slice_or_index) -> Union[Verse, "VerseList"]:
        if isinstance(slice_or_index, slice):
            return VerseList(lambda: self._get_slice(slice_or_index))

        for index, verse in enumerate(self):
            if index == slice_or_index:
                return verse

    def __iter__(self):
        return self.vref_generator()

    def _get_slice(self, slice):
        for index, verse in enumerate(self):
            if index < slice.start:
                continue
            if index >= slice.stop:
                break
            yield verse

    def __len__(self):
        return self.length

    def __repr__(self):
        return f"VerseList({list(self)})"
