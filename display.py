import os
from typing import Optional

import pygame

from memory_book import MemoryBook, MemoryEntry
from pet import Pet, PetMood, PetAccessory
from state_machine import PetOSState

ASSET_DIR = os.path.join(os.path.dirname(__file__), "assets")


def load_image(name: str) -> pygame.Surface:
    path = os.path.join(ASSET_DIR, name)
    image = pygame.image.load(path).convert_alpha()
    return image


class Display:
    """
    Handles drawing for PetOS using:
    - base_pet_<mood>.png
    - accessory_<accessory>_<mood>.png
    - base_pet_feed.png, base_pet_play.png
    """

    def __init__(self, screen: pygame.Surface, pet: Optional[Pet] = None) -> None:
        self.screen = screen
        self.pet: Optional[Pet] = pet

        pygame.font.init()
        self.font = pygame.font.SysFont("PixelOperator", 14)
        self.big_font = pygame.font.SysFont("PixelOperator", 20, bold=True)

        self.sprite_cache: dict[str, pygame.Surface] = {}
        self.notification_text: Optional[str] = None
        self.notification_timer: float = 0.0

    def set_pet(self, pet: Pet) -> None:
        self.pet = pet

    def show_notification(self, text: str, duration: float = 2.0) -> None:
        self.notification_text = text
        self.notification_timer = duration

    def update_notification(self, dt: float) -> None:
        if self.notification_timer > 0:
            self.notification_timer -= dt
            if self.notification_timer <= 0:
                self.notification_text = None

    def render(self, state_machine) -> None:
        state = state_machine.current_state

        if state == PetOSState.BOOT:
            self._render_boot()
        elif state == PetOSState.HOME:
            self._render_home()
        elif state == PetOSState.CARE_MENU:
            self._render_care_menu()
        elif state == PetOSState.MINI_GAME:
            self._render_minigame()
        elif state == PetOSState.MEMORY_BOOK:
            self._render_memory_book()
        else:
            self._render_home()

        if self.notification_text:
            self._render_notification()

    # -------- screens --------

    def _render_boot(self) -> None:
        self.screen.fill((10, 10, 20))
        title = self.big_font.render("🌼 PetOS v1.0", True, (240, 240, 240))
        msg = self.font.render("Waking up your lil buddy...", True, (200, 200, 200))
        self.screen.blit(title, (20, 40))
        self.screen.blit(msg, (20, 70))

    def _render_home(self) -> None:
        WIDTH, HEIGHT = self.screen.get_size()
        self.screen.fill((230, 250, 255))

        if not self.pet:
            return

        pet_sprite = self._get_pet_sprite()
        sprite_rect = pet_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(pet_sprite, sprite_rect)

        status_lines = [
            f"Name: {self.pet.name}",
            f"Mood: {self.pet.mood.value.capitalize()}",
            f"Accessory: {self.pet.accessory.value.replace('_', ' ').capitalize()}",
            f"Days together: {self.pet.days_together}",
            f"Hunger: {self.pet.hunger}",
            f"Fun: {self.pet.fun}",
        ]
        y = 10
        for line in status_lines:
            surf = self.font.render(line, True, (40, 40, 80))
            self.screen.blit(surf, (10, y))
            y += 16

        hints = [
            "[F] Feed / Care menu",
            "[P] Play",
            "[M] Memory book",
            "[S] Sleep / Wake",
            "[1-5] Accessories",
        ]
        y = HEIGHT - 80
        for line in hints:
            surf = self.font.render(line, True, (60, 60, 100))
            self.screen.blit(surf, (10, y))
            y += 14

    def _render_care_menu(self) -> None:
        WIDTH, HEIGHT = self.screen.get_size()
        self.screen.fill((255, 245, 230))

        title = self.big_font.render("Care Menu", True, (120, 70, 20))
        self.screen.blit(title, (20, 15))

        options = [
            "Feeding your pet...",
            "Press ESC or S to go home",
        ]
        y = 50
        for opt in options:
            surf = self.font.render(opt, True, (100, 60, 20))
            self.screen.blit(surf, (30, y))
            y += 20

        # Show explicit feed sprite if available
        try:
            feed_sprite = load_image("base_pet_feed.png")
            rect = feed_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            self.screen.blit(feed_sprite, rect)
        except Exception:
            pass

    def _render_minigame(self) -> None:
        WIDTH, HEIGHT = self.screen.get_size()
        self.screen.fill((220, 240, 220))

        title = self.big_font.render("Play Time", True, (20, 90, 40))
        self.screen.blit(title, (20, 15))

        msg = self.font.render("Playing with your pet...", True, (30, 80, 40))
        self.screen.blit(msg, (20, 50))

        hint = self.font.render("Press S or ESC to return home", True, (30, 80, 40))
        self.screen.blit(hint, (20, HEIGHT - 30))

        # Show explicit play sprite if available
        try:
            play_sprite = load_image("base_pet_play.png")
            rect = play_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            self.screen.blit(play_sprite, rect)
        except Exception:
            pass

    def _render_memory_book(self) -> None:
        WIDTH, HEIGHT = self.screen.get_size()
        self.screen.fill((240, 230, 255))

        title = self.big_font.render("Memory Book ♡", True, (80, 40, 120))
        self.screen.blit(title, (20, 10))

        if not self.pet or not self.pet.memory_book.entries:
            msg = self.font.render("No memories yet... make some!", True, (80, 40, 120))
            self.screen.blit(msg, (20, 50))
        else:
            book: MemoryBook = self.pet.memory_book
            entries = book.get_page(book.current_page)

            y = 50
            for entry in entries:
                text = self.font.render(
                    f"Day {entry.day}: {entry.text} {entry.emoji}",
                    True,
                    (80, 40, 120),
                )
                self.screen.blit(text, (20, y))
                y += 22

            page_info = self.font.render(
                f"Page {book.current_page + 1}/{book.page_count()}",
                True,
                (120, 80, 160),
            )
            self.screen.blit(page_info, (20, HEIGHT - 50))

        hint1 = self.font.render("← / → to change page", True, (120, 80, 160))
        hint2 = self.font.render("Press M or S to go home", True, (120, 80, 160))
        self.screen.blit(hint1, (20, HEIGHT - 32))
        self.screen.blit(hint2, (20, HEIGHT - 18))

    # -------- helpers --------

    def _get_pet_sprite(self) -> pygame.Surface:
        """
        Use your filenames:

        - base_pet_<mood>.png
        - accessory_<accessory>_<mood>.png when accessory != none
        """

        if not self.pet:
            surf = pygame.Surface((32, 32))
            surf.fill((255, 0, 255))
            return surf

        mood_name = self.pet.mood.value           # happy, lonely, etc.
        accessory_name = self.pet.accessory.value # none, bow, sun_hat, ...

        cache_key = f"{accessory_name}_{mood_name}"
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]

        # 1) If accessory, try accessory_<accessory>_<mood>.png
        if accessory_name != "none":
            acc_filename = f"accessory_{accessory_name}_{mood_name}.png"
            acc_path = os.path.join(ASSET_DIR, acc_filename)
            if os.path.exists(acc_path):
                sprite = load_image(acc_filename)
                self.sprite_cache[cache_key] = sprite
                return sprite

        # 2) Base pet_<mood>.png
        base_filename = f"base_pet_{mood_name}.png"
        base_path = os.path.join(ASSET_DIR, base_filename)
        if os.path.exists(base_path):
            sprite = load_image(base_filename)
        else:
            # 3) Fallback: base_pet_happy or colored box
            fallback_filename = "base_pet_happy.png"
            fallback_path = os.path.join(ASSET_DIR, fallback_filename)
            if os.path.exists(fallback_path):
                sprite = load_image(fallback_filename)
            else:
                sprite = pygame.Surface((32, 32))
                sprite.fill((200, 0, 200))

        self.sprite_cache[cache_key] = sprite
        return sprite

    def _render_notification(self) -> None:
        WIDTH, HEIGHT = self.screen.get_size()
        bar_height = 24
        rect = pygame.Rect(0, HEIGHT - bar_height, WIDTH, bar_height)
        pygame.draw.rect(self.screen, (0, 0, 0), rect)

        if self.notification_text:
            surf = self.font.render(self.notification_text, True, (255, 255, 255))
            self.screen.blit(surf, (6, HEIGHT - bar_height + 4))
