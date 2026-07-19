import time
import pygame

from gpio import GPIO
from scheduler import Scheduler
from state_machine import PetOSStateMachine, PetOSState
from display import Display
from pet import Pet
from storage import Storage
from power import PowerManager
from watchdog import Watchdog


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
FPS = 60


def boot_pet_os():
    print("🌼 PetOS v1.0")
    time.sleep(0.3)

    print("Initializing GPIO... ✓")
    time.sleep(0.3)

    print("Initializing Display... ✓")
    time.sleep(0.3)

    print("Loading Save Data... ✓")
    time.sleep(0.3)

    print("Starting Scheduler... ✓")
    time.sleep(0.3)

    print("PetOS is waking up your lil buddy...")
    print("♡")
    time.sleep(0.3)


def create_pet(storage: Storage) -> Pet:
    # Try to load an existing pet from storage
    saved_data = storage.load_pet_data()
    if saved_data:
        pet = Pet.from_dict(saved_data)
        return pet

    # No save: ask for a name in a simple text prompt first
    name = input("What would you like to name your pet? (press Enter for Mochi) ")
    name = name.strip()
    if not name:
        name = "Mochi"
    pet = Pet(name)
    storage.save_pet_data(pet.to_dict())
    return pet


def main():
    boot_pet_os()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Pet - PetOS")
    clock = pygame.time.Clock()

    gpio = GPIO()
    storage = Storage()
    power = PowerManager()
    scheduler = Scheduler()
    display = Display(screen)
    watchdog = Watchdog()

    pet = create_pet(storage)
    state_machine = PetOSStateMachine(pet, scheduler, storage, power, display)

    running = True
    state_machine.set_state(PetOSState.HOME)

    while running:
        clock.tick(FPS)
        watchdog.tick()

        # Handle events (buttons, quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            gpio.handle_event(event, state_machine)

        # Update power and scheduler
        power.update()
        scheduler.run_pending()

        # Update state machine (pet moods, animations, etc.)
        state_machine.update()

        # Draw current screen
        display.render(state_machine)

        pygame.display.flip()

    # Graceful shutdown
    storage.save_pet_data(pet.to_dict())
    pygame.quit()
    print("🌼 PetOS shutting down. See you next time!")


if __name__ == "__main__":
    main()