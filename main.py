import pygame
import time

from pet import Pet
from scheduler import Scheduler
from storage import Storage
from power import PowerManager
from display import Display
from state_machine import PetOSStateMachine, PetOSState
from gpio import GPIO
from watchdog import Watchdog  # remove if you don't actually have this


def create_pet(storage: Storage) -> Pet:
    data = storage.load()
    if data:
        return Pet.from_dict(data)
    pet = Pet("Mochi")
    return pet


def main():
    pygame.init()

    WIDTH, HEIGHT = 320, 180
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pixel Pet")

    clock = pygame.time.Clock()

    storage = Storage()
    scheduler = Scheduler()
    power = PowerManager()
    display = Display(screen)

    pet = create_pet(storage)
    display.attach_pet(pet)

    state_machine = PetOSStateMachine(
        pet=pet,
        scheduler=scheduler,
        storage=storage,
        power=power,
        display=display,
    )

    gpio = GPIO(state_machine)
    watchdog = Watchdog() if "Watchdog" in globals() else None

    running = True
    state_machine.set_state(PetOSState.BOOT)

    print("🌼 PetOS v1.0")
    print("Initializing GPIO... ✓")
    print("Initializing Display... ✓")
    print("Loading Save Data... ✓")
    print("Starting Scheduler... ✓")
    print("PetOS is waking up your lil buddy...")
    print("♡")

    boot_start = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # After a short boot, go to HOME
        if state_machine.current_state == PetOSState.BOOT:
            if time.time() - boot_start > 1.5:
                state_machine.set_state(PetOSState.HOME)

        gpio.poll_input()
        scheduler.update()
        state_machine.update()

        display.render(state_machine)
        pygame.display.flip()

        clock.tick(30)

    storage.save(pet.to_dict())
    pygame.quit()


if __name__ == "__main__":
    main()
