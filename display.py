import os
import pygame
from typing import Optional

from pet import Pet, Mood


ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets", "sprites")


class Display:
    """
    Handles all rendering for the Pixel Pet device:
    - Mood-based pet sprite.
    - Accessory overlay sprites.
    - Home screen stats, care menu, sleep, memory book.
    - Notifications and dialogue overlays.
    """

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.big_font = pygame.font.SysFont("Arial", 24)

        self.notification: Optional[str] = None
        self.dialogue: Optional[str] = None
        self.dialogue_speaker: Optional[str] = None
        self.weather: str = "Sunny"
        self.idle_animation: Optional[str] = None
        self.current_state = None
        self.pet: Optional[Pet] = None

    def _load_sprite(self, filename: str) -> Optional[pygame.Surface]:
        path = os.path.join(ASSETS_DIR, filename)
        if not os.path.exists(path):
            return None
        image = pygame.image.load(path).convert_alpha()
        return image

    def attach_pet(self, pet: Pet):
        self.pet = pet

    def on_state_change(self, new_state):
        self.current_state = new_state
        self.notification = None
        self.dialogue = None
        self.idle_animation = None

    def show_notification(self, text: str):
        self.notification = text

    def show_dialogue(self, speaker: str, text: str):
        self.dialogue_speaker = speaker
        self.dialogue = text

    def set_weather(self, weather: str):
        self.weather = weather

    def queue_idle_animation(self, name: str):
        self.idle_animation = name

    def render(self, state_machine):
        self.screen.fill((240, 230, 255))

        if self.pet is None:
            self.pet = state_machine.pet

        state_name = getattr(self.current_state, "name", None)

        if state_name == "BOOT":
            self._render_boot()
        elif state_name == "HOME":
            self._render_home()
        elif state_name == "CARE_MENU":
            self._render_care_menu()
        elif state_name == "SLEEP":
            self._render_sleep()
        elif state_name == "MEMORY_BOOK":
            self._render_memory_book()
        else:
            self._render_home()

        self._render_notification()
        self._render_dialogue()

    def _render_boot(self):
        text = self.big_font.render("🌼 PetOS v1.0", True, (80, 40, 120))
        self.screen.blit(text, (40, 40))
        sub = self.font.render("Waking up your lil buddy...", True, (80, 40, 120))
        self.screen.blit(sub, (40, 80))

    def _render_home(self):
        WIDTH, HEIGHT = 320, 180
        center_x, center_y = WIDTH // 2, HEIGHT // 2  # 160, 90

        # Mood-based base pet sprite
        if self.pet:
            mood_name = self.pet.mood.name.lower()
        else:
            mood_name = "happy"

        base_filename = f"base_pet_{mood_name}.png"
        base_sprite = self._load_sprite(base_filename)

        if base_sprite:
            rect = base_sprite.get_rect(center=(center_x, center_y))
            self.screen.blit(base_sprite, rect.topleft)
        else:
            # Fallback circle if sprite missing
            pygame.draw.circle(self.screen, (255, 255, 255), (center_x, center_y), 32)
            pygame.draw.circle(self.screen, (150, 120, 200), (center_x, center_y), 32, 2)

        # Accessory sprite that matches accessory + mood
        if self.pet and self.pet.equipped_accessory:
            accessory_name = self.pet.equipped_accessory  # "Bow", "Sun Hat", etc.
            accessory_key = accessory_name.lower().replace(" ", "_")
            accessory_filename = f"accessory_{accessory_key}_{mood_name}.png"
            accessory_sprite = self._load_sprite(accessory_filename)

            if accessory_sprite:
                # Center accessory on pet; sprite art decides what part sits high/low
                acc_rect = accessory_sprite.get_rect(center=(center_x, center_y))
                self.screen.blit(accessory_sprite, acc_rect.topleft)

        # Text UI around the pet
        if self.pet:
            name_text = self.big_font.render(self.pet.name, True, (80, 40, 120))
            self.screen.blit(name_text, (10, 10))

            mood_text = self.font.render(
                f"Mood: {self.pet.mood.name.title()}", True, (80, 40, 120)
            )
            self.screen.blit(mood_text, (10, 30))

            hunger_text = self.font.render(
                f"Hunger: {int(self.pet.hunger)}", True, (80, 40, 120)
            )
            self.screen.blit(hunger_text, (10, 50))

            energy_text = self.font.render(
                f"Energy: {int(self.pet.energy)}", True, (80, 40, 120)
            )
            self.screen.blit(energy_text, (10, 70))

            coins_text = self.font.render(
                f"Coins: {int(self.pet.coins)}", True, (80, 40, 120)
            )
            self.screen.blit(coins_text, (10, 90))

        weather_text = self.font.render(f"Weather: {self.weather}", True, (80, 40, 120))
        self.screen.blit(weather_text, (10, 110))

        if self.idle_animation:
            anim_text = self.font.render(f"* {self.idle_animation} *", True, (150, 120, 200))
            self.screen.blit(anim_text, (10, 130))

    def _render_care_menu(self):
        title = self.big_font.render("Care Menu", True, (80, 40, 120))
        self.screen.blit(title, (20, 10))

        options = [
            "F: Feed (1–6 to choose snack)",
            "P: Play",
            "M: Memory Book",
            "S: Sleep/Wake",
        ]
        y = 50
        for opt in options:
            text = self.font.render(opt, True, (80, 40, 120))
            self.screen.blit(text, (20, y))
            y += 30

    def _render_sleep(self):
        self.screen.fill((30, 10, 60))
        moon = self.big_font.render("🌙", True, (255, 255, 255))
        self.screen.blit(moon, (140, 70))
        zzz = self.font.render("Zzz...", True, (200, 180, 255))
        self.screen.blit(zzz, (140, 100))

    def _render_memory_book(self):
        title = self.big_font.render("Memory Book", True, (80, 40, 120))
        self.screen.blit(title, (20, 10))
        y = 40
        if self.pet:
            for entry in self.pet.memories[-5:]:
                text = self.font.render(
                    f"Day {entry.day}: {entry.text} {entry.emoji}", True, (80, 40, 120)
                )
                self.screen.blit(text, (20, y))
                y += 25

    def _render_notification(self):
        if not self.notification:
            return
        # Adjusted for 180px height
        box_rect = pygame.Rect(10, 140, 300, 30)
        pygame.draw.rect(self.screen, (255, 245, 255), box_rect)
        pygame.draw.rect(self.screen, (150, 120, 200), box_rect, 2)
        text = self.font.render(self.notification, True, (80, 40, 120))
        self.screen.blit(text, (15, 145))

    def _render_dialogue(self):
        if not self.dialogue:
            return
        box_rect = pygame.Rect(10, 110, 300, 25)
        pygame.draw.rect(self.screen, (255, 250, 255), box_rect)
        pygame.draw.rect(self.screen, (150, 120, 200), box_rect, 2)
        speaker = self.dialogue_speaker or (self.pet.name if self.pet else "")
        text = self.font.render(f"{speaker}: {self.dialogue}", True, (80, 40, 120))
        self.screen.blit(text, (15, 115))
