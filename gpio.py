import pygame

from state_machine import PetOSStateMachine, PetOSState
from pet import Pet


class GPIOController:
    """
    Simulated GPIO/input layer for PetOS.
    Right now it uses keyboard keys, but you can later swap
    in real Raspberry Pi GPIO pin reads.
    """

    def __init__(self, pet: Pet, state_machine: PetOSStateMachine) -> None:
        self.pet = pet
        self.state_machine = state_machine

    def poll_input(self) -> None:
        """
        Called once per frame from the main loop.
        Checks current keyboard state and sends actions to the state machine.
        """
        keys = pygame.key.get_pressed()  # continuous key state[web:159][web:153]

        # Global actions (these will repeat while key held; fine for now)
        if keys[pygame.K_f]:
            # Go to care menu and log a memory
            self.state_machine.handle_action("feed")
            self.pet.add_memory("You opened the care menu together.", "🍓")

        if keys[pygame.K_p]:
            # Go to mini game and log a memory
            self.state_machine.handle_action("play")
            self.pet.add_memory("You went to play a game!", "✨")

        if keys[pygame.K_m]:
            # View memory book
            self.state_machine.handle_action("view_memory")

        if keys[pygame.K_s]:
            # Toggle sleep and return home
            self.state_machine.handle_action("sleep_toggle")

        if keys[pygame.K_ESCAPE]:
            # Return home from any menu
            self.state_machine.handle_action("home")

        # Accessories 1–5
        if keys[pygame.K_1]:
            self.pet.set_accessory_index(1)
        if keys[pygame.K_2]:
            self.pet.set_accessory_index(2)
        if keys[pygame.K_3]:
            self.pet.set_accessory_index(3)
        if keys[pygame.K_4]:
            self.pet.set_accessory_index(4)
        if keys[pygame.K_5]:
            self.pet.set_accessory_index(5)

        # Memory book paging (only when that screen is active)
        if self.state_machine.current_state == PetOSState.MEMORY_BOOK:
            if keys[pygame.K_LEFT]:
                self.pet.memory_book.prev_page()
            if keys[pygame.K_RIGHT]:
                self.pet.memory_book.next_page()
