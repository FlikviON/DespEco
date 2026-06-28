import sys

import pygame

import ui_elements
from config import user_config
from sounds_manager import Sounds


class SubmitDeleteMapMenu:
    def __init__(self) -> None:
        self.button_width: int = 260
        self.button_height: int = 70

        self.is_running: bool = True

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.submit_button = ui_elements.Button(
            user_config.screen_width * 0.3,
            user_config.screen_height * 0.5,
            self.button_width,
            self.button_height,
            "Delete Map",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

        self.cancel_button = ui_elements.Button(
            user_config.screen_width * 0.56,
            user_config.screen_height * 0.5,
            self.button_width,
            self.button_height,
            "Cancel",
            ui_elements.Colors.darker_green,
            ui_elements.Colors.hover_darker_green
        )

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        self.submit_button.draw(screen)
        self.submit_button.check_hover(mouse_pos)

        self.cancel_button.draw(screen)
        self.cancel_button.check_hover(mouse_pos)

    def open_submit_delete_map_menu(self, map_name: str, screen: pygame.Surface) -> bool:
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            background = ui_elements.MenuBackground.load_background_image()
            screen.blit(background, (0, 0))

            mouse_pos = pygame.mouse.get_pos()

            title = ui_elements.Fonts.font_for_maps_delete.render(f"Are you sure you want to delete «{map_name}»?", True, (111, 11, 179))
            title_rect = title.get_rect(center=(user_config.screen_width * 0.5, user_config.screen_height * 0.3))
            screen.blit(title, title_rect)

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

                        if self.cancel_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.is_running = False
                            return False

                        elif self.submit_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            return True

            pygame.display.flip()
            clock.tick(60)