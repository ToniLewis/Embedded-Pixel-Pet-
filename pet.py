from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any

from memory_book import MemoryBook


class PetMood(Enum):
    HAPPY = "happy"
    GRUMPY = "grumpy"
    EXCITED = "excited"
    HUNGRY = "hungry"
    LONELY = "lonely"
    LOVE = "love"
    SICK = "sick"
    SLEEPY = "sleepy"


@dataclass
class Pet:
    name: str
    mood: PetMood = PetMood.HAPPY
    days_together: int = 0
    is_sleeping: bool = False

    def __post_init__(self) -> None:
        self.memory_book = MemoryBook()
        # You can track more stats later (hunger, energy, etc.)

    # ---- Gameplay helpers ----

    def add_memory(self, text: str, emoji: str = "♡") -> None:
        self.memory_book.add_memory(day=self.days_together, text=text, emoji=emoji)

    def toggle_sleep(self) -> None:
        self.is_sleeping = not self.is_sleeping
        self.mood = PetMood.SLEEPY if self.is_sleeping else PetMood.HAPPY

    def set_mood(self, mood: PetMood) -> None:
        self.mood = mood

    # ---- Serialization ----

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mood": self.mood.value,
            "days_together": self.days_together,
            "is_sleeping": self.is_sleeping,
            "memory_book": self.memory_book.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Pet":
        mood_value = data.get("mood", PetMood.HAPPY.value)
        try:
            mood = PetMood(mood_value)
        except ValueError:
            mood = PetMood.HAPPY

        pet = Pet(
            name=data.get("name", "Pixel"),
            mood=mood,
            days_together=data.get("days_together", 0),
            is_sleeping=data.get("is_sleeping", False),
        )
        pet.memory_book = MemoryBook.from_dict(data.get("memory_book", {}))
        return pet
