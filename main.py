import pygame

from pet import Pet
from display import Display
from state_machine import PetOSStateMachine, PetOSState


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((320, 180))
    pygame.display.set_caption("Pixel PetOS")
    clock = pygame.time.Clock()

    pet = Pet("Pixel")
    display = Display(screen, pet)
    state_machine = PetOSStateMachine(pet, display)

    running = True
    state_machine.set_state(PetOSState.BOOT)
    boot_start_ms = pygame.time.get_ticks()

    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Input for memory book paging
            if event.type == pygame.KEYDOWN:
                if state_machine.current_state == PetOSState.MEMORY_BOOK:
                    if event.key == pygame.K_LEFT:
                        pet.memory_book.prev_page()
                    elif event.key == pygame.K_RIGHT:
                        pet.memory_book.next_page()

                # Global controls
                if event.key == pygame.K_f:
                    state_machine.handle_action("feed")
                    pet.add_memory("You shared a snack together.", "🍓")
                elif event.key == pygame.K_p:
                    state_machine.handle_action("play")
                    pet.add_memory("You played and had fun!", "✨")
                elif event.key == pygame.K_m:
                    state_machine.handle_action("view_memory")
                elif event.key == pygame.K_s:
                    state_machine.handle_action("sleep_toggle")
                elif event.key == pygame.K_ESCAPE:
                    state_machine.handle_action("home")
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    index = int(event.unicode)
                    pet.set_accessory_index(index)

        # Boot to home after 1.5s
        if state_machine.current_state == PetOSState.BOOT:
            if pygame.time.get_ticks() - boot_start_ms > 1500:
                state_machine.set_state(PetOSState.HOME)

        state_machine.update()
        display.update_notification(dt)
        display.render(state_machine)
        pygame.display.flip()

    pygame.quit()
    print("🌼 PetOS shutting down. See you next time!")


if __name__ == "__main__":
    main()
