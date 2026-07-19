import json
import os
from typing import Optional, Dict


SAVE_PATH = os.path.join(os.path.dirname(__file__), "pet_save.json")


class Storage:
    """
    Simulated persistent storage for Pixel Pet.
    Uses a JSON file as a stand-in for EEPROM/flash.
    """

    def load_pet_data(self) -> Optional[Dict]:
        if not os.path.exists(SAVE_PATH):
            return None
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def save_pet_data(self, data: Dict):
        try:
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            # In a real embedded system you'd log this somewhere
            pass