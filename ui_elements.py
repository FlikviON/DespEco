import pygame

from dataclasses import dataclass
from pathlib import Path

from config import UserConfig


@dataclass
class Colors:
    if not pygame.get_init():
        pygame.init()
    white: tuple[int, int, int] = (255, 255, 255)
    black: tuple[int, int, int] = (0, 0, 0)
    gray: tuple[int, int, int] = (200, 200, 200)
    light_gray: tuple[int, int, int] = (220, 220, 220)
    light_green: tuple[int, int, int] = (100, 255, 100)
    dark_golden = (184, 134, 11)

    blue: tuple[int, int, int] = (100, 150, 255)
    hover_blue: tuple[int, int, int] = (80, 130, 235)

    red: tuple[int, int, int] = (255, 100, 100)
    hover_red: tuple[int, int, int] = (235, 80, 80)


@dataclass
class Fonts:
    font1 = pygame.font.SysFont('tahoma', 32, bold = True)
    title_font = pygame.font.SysFont('tahoma', 90, bold=True)


class Button:
    def __init__(self, x: float, y: float, width: float, height: float, text: str, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(surface, color, self.rect, border_radius = 12)
        pygame.draw.rect(surface, Colors.black, self.rect, 2, border_radius = 12)

        text_surface = Fonts.font1.render(self.text, True, Colors.black)
        text_rect = text_surface.get_rect(center = self.rect.center)

        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click


class MenuBackground:
    @staticmethod
    def load_background_image():
        background_image_path = Path("assets/images/background_image.png")
        background = pygame.image.load(background_image_path).convert()
        background = pygame.transform.scale(background, (UserConfig.screen_width, UserConfig.screen_height))
        return background

    @staticmethod
    def create_dark_overlay(surface, alpha=128):
        overlay = pygame.Surface((UserConfig.screen_width, UserConfig.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        surface.blit(overlay, (0, 0))
        return surface