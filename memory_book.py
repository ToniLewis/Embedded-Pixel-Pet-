from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class MemoryEntry:
    day: int
    text: str
    emoji: str = "♡"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MemoryEntry":
        return MemoryEntry(
            day=data.get("day", 0),
            text=data.get("text", ""),
            emoji=data.get("emoji", "♡"),
        )


class MemoryBook:
    """
    A cozy log of your pet's memories.
    Stores entries and provides simple paging for the UI.
    """

    def __init__(self) -> None:
        self._entries: List[MemoryEntry] = []
        # For paging / scrolling in the UI
        self.page_size: int = 6
        self.current_page: int = 0

    @property
    def entries(self) -> List[MemoryEntry]:
        return self._entries

    def add_memory(self, day: int, text: str, emoji: str = "♡") -> None:
        entry = MemoryEntry(day=day, text=text, emoji=emoji)
        self._entries.append(entry)

    def clear(self) -> None:
        self._entries.clear()
        self.current_page = 0

    def page_count(self) -> int:
        if not self._entries:
            return 1
        return ((len(self._entries) - 1) // self.page_size) + 1

    def get_page(self, page_index: int) -> List[MemoryEntry]:
        if page_index < 0:
            page_index = 0
        if page_index >= self.page_count():
            page_index = self.page_count() - 1

        start = page_index * self.page_size
        end = start + self.page_size
        return self._entries[start:end]

    def next_page(self) -> None:
        if self.current_page < self.page_count() - 1:
            self.current_page += 1

    def prev_page(self) -> None:
        if self.current_page > 0:
            self.current_page -= 1

    # Serialization for save data
    def to_dict(self) -> Dict[str, Any]:
        return {
            "entries": [e.to_dict() for e in self._entries],
            "page_size": self.page_size,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "MemoryBook":
        book = MemoryBook()
        book.page_size = data.get("page_size", 6)
        entries_data = data.get("entries", [])
        for e in entries_data:
            book.entries.append(MemoryEntry.from_dict(e))
        return book
