from enum import Enum, auto
import time

from pet import Pet, Mood
from scheduler import Scheduler
from storage import Storage
from power import PowerManager
from display import Display


class PetOSState(Enum):
    BOOT = auto()
    HOME = auto()
    CARE_MENU = auto()
    SLEEP = auto()
    MINI_GAME = auto()
    MEMORY_BOOK = auto()
    SETTINGS = auto()
    ERROR = auto()


class PetOSStateMachine:
    def __init__(
        self,
        pet: Pet,
        scheduler: Scheduler,
        storage: Storage,
        power: PowerManager,
        display: Display,
    ):
        self.pet = pet
        self.scheduler = scheduler
        self.storage = storage
        self.power = power
        self.display = display
        self.current_state = PetOSState.BOOT
        self.last_update_time = time.time()
        self.weather = "Sunny"
        self.season = "Spring"

        self._register_tasks()

    def _register_tasks(self):
        # Idle pet personality
        self.scheduler.add_task(self._idle_tick, interval_seconds=2.0)
        # Random dialogue
        self.scheduler.add_task(self._random_dialogue, interval_seconds=180.0)
        # Daily gift
        self.scheduler.add_task(self._daily_gift, interval_seconds=3600.0)
        # Weather effects
        self.scheduler.add_task(self._update_weather, interval_seconds=600.0)
        # Sleep mode check
        self.scheduler.add_task(self._check_sleep_mode, interval_seconds=60.0)

    def set_state(self, new_state: PetOSState):
        self.current_state = new_state
        self.display.on_state_change(new_state)

    def update(self):
        now = time.time()
        dt = now - self.last_update_time
        self.last_update_time = now

        if self.current_state == PetOSState.HOME:
            self.pet.tick_idle(dt)
        elif self.current_state == PetOSState.SLEEP:
            self.power.enter_low_power()
        # other states can have their own logic

    def handle_action(self, action: str):
        # Called by GPIO / input layer with high-level actions
        if action == "feed":
            self.set_state(PetOSState.CARE_MENU)
        elif action == "play":
            self.set_state(PetOSState.MINI_GAME)
        elif action == "view_memory":
            self.set_state(PetOSState.MEMORY_BOOK)
        elif action == "wake":
            if self.current_state == PetOSState.SLEEP:
                self.power.exit_low_power()
                self.set_state(PetOSState.HOME)
        elif action.startswith("feed_snack:"):
            snack_name = action.split(":", 1)[1]
            self.pet.feed(snack_name)
            self.display.show_notification(
                f"{self.pet.name} happily eats the {snack_name.lower()} 🍓"
            )
            self.set_state(PetOSState.HOME)
        elif action == "play_simple":
            self.pet.play()
            self.display.show_notification(f"{self.pet.name} had fun playing! ✨")
            self.set_state(PetOSState.HOME)

    def _idle_tick(self):
        # Trigger cute idle animations depending on mood
        if self.current_state != PetOSState.HOME:
            return

        mood = self.pet.mood
        if mood == Mood.HAPPY:
            self.display.queue_idle_animation("wiggle")
        elif mood == Mood.SLEEPY:
            self.display.queue_idle_animation("yawn")
        elif mood == Mood.HUNGRY:
            self.display.queue_idle_animation("bounce_for_food")
        elif mood == Mood.LONELY:
            self.display.queue_idle_animation("look_up")
        elif mood == Mood.SICK:
            self.display.queue_idle_animation("tiny_tears")
        elif mood == Mood.EXCITED:
            self.display.queue_idle_animation("sparkle_bounce")
        elif mood == Mood.GRUMPY:
            self.display.queue_idle_animation("pout")
        elif mood == Mood.LOVED:
            self.display.queue_idle_animation("heart_pulse")

    def _random_dialogue(self):
        if self.current_state != PetOSState.HOME:
            return

        mood = self.pet.mood
        if mood == Mood.HAPPY:
            text = "Let's play!"
        elif mood == Mood.LONELY:
            text = "I missed you! ♡"
        elif mood == Mood.EXCITED:
            text = "Today feels lucky!"
        elif mood == Mood.SLEEPY:
            text = "I'm feeling cozy... 🌙"
        elif mood == Mood.LOVED:
            text = "You're doing great today!"
        else:
            text = "I'm happy you're here."

        self.display.show_dialogue(self.pet.name, text)

    def _daily_gift(self):
        # Simple version: every call, give a flower (you can refine with real day tracking)
        self.pet.add_memory("You found me a tiny flower!", "🌸")
        self.display.show_notification(
            f"{self.pet.name} found you a tiny flower! 🌸"
        )

    def _update_weather(self):
        # Dummy random cycle for now
        cycle = ["Sunny", "Rain", "Snow", "Cherry Blossoms"]
        idx = cycle.index(self.weather) if self.weather in cycle else 0
        self.weather = cycle[(idx + 1) % len(cycle)]
        self.display.set_weather(self.weather)

    def _check_sleep_mode(self):
        # If too long since interaction, enter sleep
        idle_threshold = 300  # seconds
        if time.time() - self.pet.last_interaction_time > idle_threshold:
            self.set_state(PetOSState.SLEEP)