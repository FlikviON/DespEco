import sys

import pygame

import ui_elements
from config import user_config
from sounds_manager import Sounds


class RenameMapMenu:
    def __init__(self) -> None:
        self.button_width: int = 260
        self.button_height: int = 70

        self.is_running: bool = False

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.background = ui_elements.MenuBackground.load_background_image()



        self.new_map_name_inputbox = ui_elements.InputBox(
            x=user_config.screen_width * 0.405,
            y=user_config.screen_height * 0.4,
            width=300,
            height=32,
            max_length=15
        )

        self.submit_button = ui_elements.Button(
            user_config.screen_width * 0.42,
            user_config.screen_height * 0.6,
            self.button_width,
            self.button_height,
            "Submit",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.cancel_button = ui_elements.Button(
            user_config.screen_width * 0.42,
            user_config.screen_height * 0.69,
            self.button_width,
            self.button_height,
            "Cancel",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))

        self.new_map_name_inputbox.draw(screen)
        self.new_map_name_inputbox.active = True

        self.submit_button.draw(screen)
        self.submit_button.check_hover(mouse_pos)

        self.cancel_button.draw(screen)
        self.cancel_button.check_hover(mouse_pos)

    def open_rename_map_menu(self, map_name: str, screen: pygame.Surface) -> str:
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            mouse_pos = pygame.mouse.get_pos()

            self.new_map_name_inputbox.update()
            self._draw_ui(mouse_pos, screen)

            title = ui_elements.Fonts.font_for_maps_delete.render(f"Enter a new name for «{map_name}»", True,
                                                                  (111, 11, 179))
            title_rect = title.get_rect(center=(user_config.screen_width * 0.5, user_config.screen_height * 0.3))
            screen.blit(title, title_rect)

            for event in pygame.event.get():
                self.new_map_name_inputbox.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                        return ""

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True

                        if self.cancel_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.is_running = False
                            return ""

                        elif self.submit_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            return self.new_map_name_inputbox.text

            pygame.display.flip()
            clock.tick(60)