import sys

import pygame

import ui_elements
from config import user_config
from Menues.create_map_menu import CreateMapMenu
from Menues.saved_maps_menu import SavedMapsMenu
from sounds_manager import Sounds


class RedactorMenu:
    def __init__(self) -> None:
        self.button_width: int = 260
        self.button_height: int = 70

        self.is_running: bool = False

        self.saved_maps_menu: SavedMapsMenu = SavedMapsMenu()
        self.create_map_menu: CreateMapMenu = CreateMapMenu()

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.background = ui_elements.MenuBackground.load_background_image()

        self.title = ui_elements.Fonts.title_font.render("Map Redactor", True, ui_elements.Colors.dark_golden)
        self.title_rect = self.title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))

        self.create_map_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.46,
            self.button_width,
            self.button_height,
            "Create Map",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.saved_maps_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.55,
            self.button_width,
            self.button_height,
            "Saved Maps",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.back_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.64,
            self.button_width,
            self.button_height,
            "Back",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, self.title_rect)

        self.create_map_button.check_hover(mouse_pos)
        self.create_map_button.draw(screen)

        self.saved_maps_button.check_hover(mouse_pos)
        self.saved_maps_button.draw(screen)

        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(screen)

    def open_redactor_menu(self, screen: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            mouse_pos = pygame.mouse.get_pos()
            self._draw_ui(mouse_pos, screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True

                        if self.create_map_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.create_map_menu.open_create_map_menu(screen)

                        if self.saved_maps_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.saved_maps_menu.open_saved_maps_menu(screen)

                        if self.back_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.is_running = False

                pygame.display.flip()
                clock.tick(60)
