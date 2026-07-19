import pygame

from state_machine import PetOSStateMachine


class GPIO:
    """
    Abstracts button inputs into high-level actions that the
    PetOS state machine can understand.
    """

    def handle_event(self, event: pygame.event.Event, state_machine: PetOSStateMachine):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Open care menu (feed)
                state_machine.handle_action("feed")
            elif event.key == pygame.K_p:
                # Simple play action
                state_machine.handle_action("play_simple")
            elif event.key == pygame.K_m:
                # Memory book
                state_machine.handle_action("view_memory")
            elif event.key == pygame.K_s:
                # Sleep/wake toggle (for testing)
                state_machine.handle_action("wake")
            elif event.key == pygame.K_1:
                state_machine.handle_action("feed_snack:Strawberry")
            elif event.key == pygame.K_2:
                state_machine.handle_action("feed_snack:Cupcake")
            elif event.key == pygame.K_3:
                state_machine.handle_action("feed_snack:Carrot")
            elif event.key == pygame.K_4:
                state_machine.handle_action("feed_snack:Cookie")
            elif event.key == pygame.K_5:
                state_machine.handle_action("feed_snack:Rice Ball")
            elif event.key == pygame.K_6:
                state_machine.handle_action("feed_snack:Tea")