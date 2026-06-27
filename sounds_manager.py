import random
import time
from dataclasses import dataclass
from pathlib import Path

import pygame


@dataclass
class Sounds:
    button_click: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Effects/button_click.mp3"))

    theme1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme1.mp3"))
    theme2: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme2.mp3"))
    theme3: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme3.mp3"))
    theme4: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme4.mp3"))
    theme5: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme5.mp3"))
    theme6: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme6.mp3"))
    theme7: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/Music/theme7.mp3"))
    theme8: pygame.Sound = ...

    theme1_lasting: int = 60
    theme2_lasting: int = 44
    theme3_lasting: int = 40
    theme4_lasting: int = 272
    theme5_lasting: int = 120
    theme6_lasting: int = 120
    theme7_lasting: int = 120
    theme8_lasting: int = ...

    sound_meadows1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/meadow1.mp3"))
    sound_mountains1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/mountains1.mp3"))
    sound_water1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/water1.mp3"))
    sound_desert1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/desert1.mp3"))
    sound_tundra1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/tundra1.mp3"))
    sound_swamp1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/swamp1.mp3"))
    sound_forest1: pygame.Sound = pygame.mixer.Sound(Path("Assets/Sounds/AmbientSounds/forest1.mp3"))


class SoundsManager:
    def __init__(self) -> None:
        self.theme_playing_probability: float = 0.001
        self.min_theme_playing_interval: int = 240

        self.ambient_playing_probability: float = 0.0015
        self.min_ambient_playing_interval: int = 100

        self.last_theme_played: pygame.Sound | None = None
        self.last_time_theme_played: int = int(time.time())
        self.last_time_ambient_played: int = int(time.time())

        self.themes: tuple[pygame.Sound, ...] = (Sounds.theme1, Sounds.theme2, Sounds.theme3, Sounds.theme4, Sounds.theme5, Sounds.theme6, Sounds.theme7, Sounds.theme8)
        self.themes_lastings: dict = {Sounds.theme1: 60, Sounds.theme2: 44, Sounds.theme3: 40, Sounds.theme4: 272}

        self.ambients: dict = {"grass": (Sounds.sound_meadows1,), "mountain": (Sounds.sound_mountains1,), "water": (Sounds.sound_water1,), "sand": (Sounds.sound_desert1,), "snow": (Sounds.sound_tundra1,), "swamp": (Sounds.sound_swamp1,), "forest": (Sounds.sound_forest1,)}
        self.ambients_lastings: dict = {}

        self.channel: pygame.Channel | None = None

        self.master_volume: float = 0.5  # 0.0 to 1.0
        self.music_volume: float = 0.5
        self.sfx_volume: float = 0.5

        self.set_master_volume(self.master_volume)

    def randomly_play_random_theme(self) -> None:
        if ((self.channel is None) or (not self.channel.get_busy())) and (int(time.time()) - self.last_time_theme_played >= self.min_theme_playing_interval):
            a = random.randint(0, int(1 / self.theme_playing_probability))
            theme = random.choice(self.themes)
            while theme == self.last_theme_played:
                theme = random.choice(self.themes)
            if a == 1:
                self.last_theme_played = theme
                self.last_time_theme_played = int(time.time()) + self.themes_lastings[theme]
                self.channel = theme.play()

    def randomly_play_ambient_sound(self, ambient_type: str) -> None:
        if ((self.channel is None) or (not self.channel.get_busy())) and (int(time.time()) - self.last_time_ambient_played >= self.min_ambient_playing_interval):
            a = random.randint(0, int(1 / self.ambient_playing_probability))
            if a == 1:
                ambient = random.choice(self.ambients[ambient_type])
                self.last_time_ambient_played = int(time.time())
                self.channel = ambient.play()

    def set_master_volume(self, volume: float) -> None:
        """Установить общую громкость (0.0 - 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))
        self.set_music_volume(self.music_volume)
        self.set_sfx_volume(self.sfx_volume)

    def set_music_volume(self, volume: float) -> None:
        """Установить громкость музыки (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        final_volume = self.music_volume * self.master_volume

        # Применить ко всем музыкальным темам
        for theme in self.themes:
            if theme != ...:  # Пропустить пустые значения
                theme.set_volume(final_volume)

    def set_sfx_volume(self, volume: float) -> None:
        """Установить громкость звуковых эффектов (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        final_volume = self.sfx_volume * self.master_volume

        # Применить ко всем звукам окружения
        for ambient_group in self.ambients.values():
            for sound in ambient_group:
                if sound != ...:
                    sound.set_volume(final_volume)

        # Применить к звуку кнопки
        Sounds.button_click.set_volume(final_volume)

    def change_master_volume(self, delta: float) -> None:
        """Изменить общую громкость на delta"""
        new_volume = self.master_volume + delta
        self.set_master_volume(new_volume)

    def change_music_volume(self, delta: float) -> None:
        """Изменить громкость музыки на delta"""
        new_volume = self.music_volume + delta
        self.set_music_volume(new_volume)

    def change_sfx_volume(self, delta: float) -> None:
        """Изменить громкость SFX на delta"""
        new_volume = self.sfx_volume + delta
        self.set_sfx_volume(new_volume)