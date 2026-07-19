from __future__ import annotations

from enum import Enum
from typing import Optional

from pet import Pet


class PetOSState(Enum):
    BOOT = "boot"
    HOME = "home"
    CARE_MENU = "care_menu"
    MINI_GAME = "mini_game"
    MEMORY_BOOK = "memory_book"


class PetOSStateMachine:
    def __init__(self, pet: Pet, display) -> None:
        self.pet = pet
        # display is any object with .show_notification() etc.
        self.display = display
        self.current_state: PetOSState = PetOSState.BOOT

    def set_state(self, new_state: PetOSState) -> None:
        self.current_state = new_state

    # High-level actions called from input/gpio

    def handle_action(self, action: str) -> None:
        if action == "feed":
            self.set_state(PetOSState.CARE_MENU)
        elif action == "play":
            self.set_state(PetOSState.MINI_GAME)
        elif action == "view_memory":
            self.set_state(PetOSState.MEMORY_BOOK)
        elif action == "sleep_toggle":
            self.pet.toggle_sleep()
            self.set_state(PetOSState.HOME)
        elif action == "home":
            self.set_state(PetOSState.HOME)

    def update(self) -> None:
        # You can grow this later: mood changes, timers, etc.
        pass
