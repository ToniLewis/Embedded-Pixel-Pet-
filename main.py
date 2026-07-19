import asyncio
import pygame

from pet import Pet
from display import Display
from state_machine import PetOSStateMachine, PetOSState
from gpio import GPIOController


async def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((640, 360))  # comfy for 128x128 pet
    pygame.display.set_caption("Pixel PetOS")
    clock = pygame.time.Clock()

    pet = Pet("Pixel")
    display = Display(screen, pet)
    state_machine = PetOSStateMachine(pet, display)
    gpio = GPIOController(pet, state_machine)

    running = True
    state_machine.set_state(PetOSState.BOOT)
    boot_start_ms = pygame.time.get_ticks()

    while running:
        dt = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if state_machine.current_state == PetOSState.BOOT:
            if pygame.time.get_ticks() - boot_start_ms > 1500:
                state_machine.set_state(PetOSState.HOME)

        gpio.poll_input()
        state_machine.update()
        display.update_notification(dt)
        display.render(state_machine)
        pygame.display.flip()

        await asyncio.sleep(0)

    pygame.quit()
    print("🌼 PetOS shutting down. See you next time!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🌼 PetOS interrupted. See you next time!")
