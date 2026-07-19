import pygame

from state_machine import PetOSStateMachine, PetOSState
from pet import Pet


class GPIOController:
    """
    Simulated GPIO/input layer for PetOS using keyboard.
    """

    def __init__(self, pet: Pet, state_machine: PetOSStateMachine) -> None:
        self.pet = pet
        self.state_machine = state_machine

    def poll_input(self) -> None:
        keys = pygame.key.get_pressed()

        # Feed
        if keys[pygame.K_f]:
            self.pet.feed()
            self.pet.add_memory("You fed your pet a tasty snack.", "🍓")
            self.state_machine.handle_action("feed")

        # Play
        if keys[pygame.K_p]:
            self.pet.play()
            self.pet.add_memory("You played together and had fun!", "✨")
            self.state_machine.handle_action("play")

        # Memory book
        if keys[pygame.K_m]:
            self.state_machine.handle_action("view_memory")

        # Sleep / wake
        if keys[pygame.K_s]:
            self.state_machine.handle_action("sleep_toggle")

        # Back home
        if keys[pygame.K_ESCAPE]:
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

        # Memory book paging
        if self.state_machine.current_state == PetOSState.MEMORY_BOOK:
            if keys[pygame.K_LEFT]:
                self.pet.memory_book.prev_page()
            if keys[pygame.K_RIGHT]:
                self.pet.memory_book.next_page()
