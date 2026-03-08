import random
from dataclasses import dataclass
from pathlib import Path

import pygame


@dataclass
class Sounds:
    button_click: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Effects/button_click.mp3"))

    theme1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme1.mp3"))


class SoundsManager:
    def __init__(self) -> None:
        self.channel: pygame.Channel | None = None

    def randomly_play_random_theme(self) -> None:
        if (self.channel is None) or (not self.channel.get_busy()):
            a = random.randint(0, 1000)
            if a == 52:
                self.channel = Sounds.theme1.play()