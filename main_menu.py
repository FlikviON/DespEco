import sys

import pygame

import ui_elements
from redactor_menu import RedactorMenu
from config import user_config
from sounds_manager import Sounds


class MainMenu:
    def __init__(self) -> None:
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((user_config.screen_width, user_config.screen_height))
        pygame.display.set_caption("Game menu")

        self.button_width: int = 260
        self.button_height: int = 70

        self.redactor_menu: RedactorMenu = RedactorMenu()

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.background = ui_elements.MenuBackground.load_background_image()

        self.title = ui_elements.Fonts.title_font.render("DespEco", True, ui_elements.Colors.dark_golden)
        self.title_rect = self.title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))

        self.singleplayer_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 3 - 40,
            self.button_width,
            self.button_height,
            "Singleplayer",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.multiplayer_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 3 + 50,
            self.button_width,
            self.button_height,
            "Multiplayer",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.redactor_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 3 + 140,
            self.button_width,
            self.button_height,
            "Map Redactor",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.settings_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 3 + 230,
            self.button_width,
            self.button_height,
            "Settings",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.exit_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 3 + 320,
            self.button_width,
            self.button_height,
            "Quit game",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        self.screen.blit(self.background, (0, 0))

        self.screen.blit(self.title, self.title_rect)

        self.singleplayer_button.check_hover(mouse_pos)
        self.singleplayer_button.draw(screen)

        self.multiplayer_button.check_hover(mouse_pos)
        self.multiplayer_button.draw(screen)

        self.redactor_button.check_hover(mouse_pos)
        self.redactor_button.draw(screen)

        self.settings_button.check_hover(mouse_pos)
        self.settings_button.draw(screen)

        self.exit_button.check_hover(mouse_pos)
        self.exit_button.draw(screen)

    def open_main_menu(self) -> None:
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            mouse_pos = pygame.mouse.get_pos()
            self._draw_ui(mouse_pos, self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        is_running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True

                        if self.singleplayer_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            ...

                        if self.multiplayer_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            ...

                        if self.redactor_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.redactor_menu.open_redactor_menu(self.screen)

                        if self.settings_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            ...

                        if self.exit_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(60)
