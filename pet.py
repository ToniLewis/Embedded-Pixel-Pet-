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
    LOVED = "loved"
    SICK = "sick"
    SLEEPY = "sleepy"


class PetAccessory(Enum):
    NONE = "none"
    BOW = "bow"
    SUN_HAT = "sun_hat"
    GLASSES = "glasses"
    FLOWER_CROWN = "flower_crown"
    SCARF = "scarf"


@dataclass
class Pet:
    name: str
    mood: PetMood = PetMood.HAPPY
    accessory: PetAccessory = PetAccessory.NONE
    days_together: int = 0
    is_sleeping: bool = False

    hunger: int = 30
    fun: int = 50

    def __post_init__(self) -> None:
        self.memory_book = MemoryBook()

    # ---- Gameplay helpers ----

    def add_memory(self, text: str, emoji: str = "♡") -> None:
        self.memory_book.add_memory(day=self.days_together, text=text, emoji=emoji)

    def toggle_sleep(self) -> None:
        self.is_sleeping = not self.is_sleeping
        self.mood = PetMood.SLEEPY if self.is_sleeping else PetMood.HAPPY

    def set_mood(self, mood: PetMood) -> None:
        self.mood = mood

    def set_accessory_index(self, index: int) -> None:
        mapping = {
            1: PetAccessory.BOW,
            2: PetAccessory.SUN_HAT,
            3: PetAccessory.GLASSES,
            4: PetAccessory.FLOWER_CROWN,
            5: PetAccessory.SCARF,
        }
        self.accessory = mapping.get(index, PetAccessory.NONE)

    def feed(self) -> None:
        self.hunger = max(0, self.hunger - 20)
        if self.hunger <= 20:
            self.mood = PetMood.HAPPY
        else:
            self.mood = PetMood.HUNGRY

    def play(self) -> None:
        self.fun = min(100, self.fun + 20)
        if self.fun >= 70:
            self.mood = PetMood.EXCITED
        else:
            self.mood = PetMood.HAPPY

    # ---- Serialization ----

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "mood": self.mood.value,
            "accessory": self.accessory.value,
            "days_together": self.days_together,
            "is_sleeping": self.is_sleeping,
            "hunger": self.hunger,
            "fun": self.fun,
            "memory_book": self.memory_book.to_dict(),
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Pet":
        mood_value = data.get("mood", PetMood.HAPPY.value)
        acc_value = data.get("accessory", PetAccessory.NONE.value)
        try:
            mood = PetMood(mood_value)
        except ValueError:
            mood = PetMood.HAPPY
        try:
            accessory = PetAccessory(acc_value)
        except ValueError:
            accessory = PetAccessory.NONE

        pet = Pet(
            name=data.get("name", "Pixel"),
            mood=mood,
            accessory=accessory,
            days_together=data.get("days_together", 0),
            is_sleeping=data.get("is_sleeping", False),
            hunger=data.get("hunger", 30),
            fun=data.get("fun", 50),
        )
        pet.memory_book = MemoryBook.from_dict(data.get("memory_book", {}))
        return pet
