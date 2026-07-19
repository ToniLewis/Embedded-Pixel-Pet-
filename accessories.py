from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Accessory:
    name: str
    cost: int


ACCESSORY_CATALOG: Dict[str, Accessory] = {
    "Bow": Accessory("Bow", 10),
    "Sun Hat": Accessory("Sun Hat", 15),
    "Glasses": Accessory("Glasses", 12),
    "Flower Crown": Accessory("Flower Crown", 20),
    "Scarf": Accessory("Scarf", 8),
}


def list_accessories() -> List[Accessory]:
    return list(ACCESSORY_CATALOG.values())
