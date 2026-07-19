from __future__ import annotations

from enum import Enum

from pet import Pet


class PetOSState(Enum):
    BOOT = "boot"
    HOME = "home"
    CARE_MENU = "care_menu"
    MINI_GAME = "mini_game"
    MEMORY_BOOK = "memory_book"


class PetOSStateMachine:
    """
    Simple state machine for PetOS.
    Does NOT import Display to avoid circular imports.
    """

    def __init__(self, pet: Pet, display) -> None:
        self.pet = pet
        self.display = display
        self.current_state: PetOSState = PetOSState.BOOT

    def set_state(self, new_state: PetOSState) -> None:
        self.current_state = new_state

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
        # Optional: decay hunger/fun over time later
        pass
