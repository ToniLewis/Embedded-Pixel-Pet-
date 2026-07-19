from dataclasses import dataclass, field
from enum import Enum, auto
import time
from typing import List, Dict

from accessories import ACCESSORY_CATALOG


class Mood(Enum):
    HAPPY = auto()
    SLEEPY = auto()
    LONELY = auto()
    HUNGRY = auto()
    SICK = auto()
    EXCITED = auto()
    GRUMPY = auto()
    LOVED = auto()


@dataclass
class MemoryEntry:
    day: int
    text: str
    emoji: str = "♡"


@dataclass
class Pet:
    name: str
    hunger: int = 20
    energy: int = 80
    affection: int = 50
    health: int = 100
    boredom: int = 20
    days_together: int = 1
    last_interaction_time: float = field(default_factory=time.time)
    snacks: Dict[str, int] = field(default_factory=lambda: {
        "Strawberry": 3,
        "Cupcake": 1,
        "Carrot": 3,
        "Cookie": 2,
        "Rice Ball": 2,
        "Tea": 2,
    })
    accessories: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)
    memories: List[MemoryEntry] = field(default_factory=list)
    mood: Mood = Mood.HAPPY
    coins: int = 0
    equipped_accessory: str | None = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "hunger": self.hunger,
            "energy": self.energy,
            "affection": self.affection,
            "health": self.health,
            "boredom": self.boredom,
            "days_together": self.days_together,
            "last_interaction_time": self.last_interaction_time,
            "snacks": self.snacks,
            "accessories": self.accessories,
            "achievements": self.achievements,
            "memories": [
                {"day": m.day, "text": m.text, "emoji": m.emoji}
                for m in self.memories
            ],
            "coins": self.coins,
            "equipped_accessory": self.equipped_accessory,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Pet":
        pet = cls(
            name=data.get("name", "Mochi"),
            hunger=data.get("hunger", 20),
            energy=data.get("energy", 80),
            affection=data.get("affection", 50),
            health=data.get("health", 100),
            boredom=data.get("boredom", 20),
            days_together=data.get("days_together", 1),
            last_interaction_time=data.get("last_interaction_time", time.time()),
            snacks=data.get("snacks", {}),
            accessories=data.get("accessories", []),
            achievements=data.get("achievements", []),
            coins=data.get("coins", 0),
        )
        pet.equipped_accessory = data.get("equipped_accessory")
        pet.memories = [
            MemoryEntry(day=m["day"], text=m["text"], emoji=m.get("emoji", "♡"))
            for m in data.get("memories", [])
        ]
        pet.update_mood()
        return pet

    def feed(self, snack_name: str):
        if snack_name not in self.snacks or self.snacks[snack_name] <= 0:
            return

        self.snacks[snack_name] -= 1

        if snack_name == "Strawberry":
            self.hunger = max(0, self.hunger - 15)
            self.affection = min(100, self.affection + 5)
        elif snack_name == "Cupcake":
            self.hunger = max(0, self.hunger - 25)
            self.health = max(0, self.health - 5)
            self.affection = min(100, self.affection + 10)
        elif snack_name == "Carrot":
            self.hunger = max(0, self.hunger - 20)
            self.health = min(100, self.health + 10)
        elif snack_name == "Cookie":
            self.hunger = max(0, self.hunger - 15)
            self.affection = min(100, self.affection + 8)
            self.boredom = max(0, self.boredom - 5)
        elif snack_name == "Rice Ball":
            self.hunger = max(0, self.hunger - 18)
            self.health = min(100, self.health + 5)
        elif snack_name == "Tea":
            self.energy = min(100, self.energy + 10)
            self.affection = min(100, self.affection + 3)

        self.last_interaction_time = time.time()
        self.update_mood()

    def play(self):
        self.energy = max(0, self.energy - 10)
        self.boredom = max(0, self.boredom - 20)
        self.affection = min(100, self.affection + 10)
        self.last_interaction_time = time.time()
        self.update_mood()

    def tick_idle(self, dt: float):
        # Simple decay/growth over time
        self.hunger = min(100, self.hunger + dt * 0.2)
        self.energy = max(0, self.energy - dt * 0.05)
        self.boredom = min(100, self.boredom + dt * 0.1)

        # Affection and health decay slowly
        self.affection = max(0, self.affection - dt * 0.01)
        self.health = max(0, self.health - dt * 0.005)

        self.update_mood()

    def update_mood(self):
        if self.health < 30 and self.hunger > 60:
            self.mood = Mood.SICK
        elif self.hunger > 60:
            self.mood = Mood.HUNGRY
        elif self.energy < 30:
            self.mood = Mood.SLEEPY
        elif self.affection < 30 and self.boredom > 60:
            self.mood = Mood.LONELY
        elif self.boredom > 70:
            self.mood = Mood.GRUMPY
        elif self.affection > 80 and self.health > 70 and self.energy > 50:
            self.mood = Mood.LOVED
        elif self.affection > 60 and self.energy > 60:
            self.mood = Mood.EXCITED
        else:
            self.mood = Mood.HAPPY

    def add_accessory(self, accessory_name: str):
        if accessory_name not in self.accessories:
            self.accessories.append(accessory_name)
            self.add_memory(f"You bought me a {accessory_name.lower()}.", "🌸")

    def add_achievement(self, title: str):
        if title not in self.achievements:
            self.achievements.append(title)

    def add_memory(self, text: str, emoji: str = "♡"):
        entry = MemoryEntry(day=self.days_together, text=text, emoji=emoji)
        self.memories.append(entry)

    def earn_coins(self, amount: int):
        self.coins = max(0, self.coins + amount)

    def buy_accessory(self, name: str) -> bool:
        acc = ACCESSORY_CATALOG.get(name)
        if acc is None:
            return False
        if self.coins < acc.cost:
            return False

        self.coins -= acc.cost
        if name not in self.accessories:
            self.accessories.append(name)
            self.add_memory(f"You unlocked a {name.lower()}!", "🎀")
        return True

    def equip_accessory(self, name: str):
        if name in self.accessories:
            self.equipped_accessory = name
            self.add_memory(f"You equipped my {name.lower()}!", "🌸")
