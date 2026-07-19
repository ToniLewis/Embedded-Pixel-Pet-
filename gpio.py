import pygame

from state_machine import PetOSStateMachine, PetOSState
from pet import Pet, PetMood


class GPIOController:
    """
    Simulated GPIO/input layer for PetOS.
    Uses keyboard keys to drive actions.
    """

    def __init__(self, pet: Pet, state_machine: PetOSStateMachine) -> None:
        self.pet = pet
        self.state_machine = state_machine

    def poll_input(self) -> None:
        keys = pygame.key.get_pressed()  # continuous key state[web:159][web:153]

        # Global actions
        if keys[pygame.K_f]:
            self.state_machine.handle_action("feed")
            self.pet.add_memory("You opened the care menu together.", "🍓")

        if keys[pygame.K_p]:
            self.state_machine.handle_action("play")
            self.pet.add_memory("You went to play a game!", "✨")

        if keys[pygame.K_m]:
            self.state_machine.handle_action("view_memory")

        if keys[pygame.K_s]:
            self.state_machine.handle_action("sleep_toggle")

        if keys[pygame.K_ESCAPE]:
            self.state_machine.handle_action("home")

        # Mood test keys (optional: cycle moods directly)
        if keys[pygame.K_h]:
            self.pet.set_mood(PetMood.HAPPY)
        if keys[pygame.K_g]:
            self.pet.set_mood(PetMood.GRUMPY)
        if keys[pygame.K_e]:
            self.pet.set_mood(PetMood.EXCITED)
        if keys[pygame.K_u]:  # hungry
            self.pet.set_mood(PetMood.HUNGRY)
        if keys[pygame.K_l]:
            self.pet.set_mood(PetMood.LONELY)
        if keys[pygame.K_v]:  # love
            self.pet.set_mood(PetMood.LOVE)
        if keys[pygame.K_k]:  # sick
            self.pet.set_mood(PetMood.SICK)
        if keys[pygame.K_y]:  # sleepy
            self.pet.set_mood(PetMood.SLEEPY)

        # Memory book paging
        if self.state_machine.current_state == PetOSState.MEMORY_BOOK:
            if keys[pygame.K_LEFT]:
                self.pet.memory_book.prev_page()
            if keys[pygame.K_RIGHT]:
                self.pet.memory_book.next_page()
