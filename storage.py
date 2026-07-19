import json
import os
from typing import Dict, Any, Optional


SAVE_FILE = os.path.join(os.path.dirname(__file__), "save.json")


class Storage:
    """
    Very simple JSON-based storage for the pet state.
    """

    def load(self) -> Optional[Dict[str, Any]]:
        if not os.path.exists(SAVE_FILE):
            return None
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            # If anything goes wrong, start fresh
            return None

    def save(self, data: Dict[str, Any]) -> None:
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            # You can log this or ignore for now
            pass
