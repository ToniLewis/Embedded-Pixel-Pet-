from dataclasses import dataclass
from typing import Dict


@dataclass
class Event:
    """
    Simple event container for PetOS.

    type: high-level event name (e.g., 'FeedEvent', 'DialogueEvent').
    payload: dict of extra data (e.g., snack_name, mood, timestamp).
    """
    type: str
    payload: Dict