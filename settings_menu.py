import sys

import pygame

import ui_elements
from settings_controller import SettingsController
from sounds_manager import Sounds
from config import user_config


class SettingsMenu:
    def __init__(self) -> None:
        self.button_width: int = 260
        self.button_height: int = 70

        self.button_for_section_width: int = 120
        self.button_for_section_height: int = 40

        self.screen_resolution_options: list[str] = ["1920 x 1080", "2560 x 1440", "3840 x 2160", "1366 x 768", "1280 x 720"]

        self.is_screen_changed: bool = False

        self.settings_controller: SettingsController = SettingsController()

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.background = ui_elements.MenuBackground.load_background_image()

        self.title = ui_elements.Fonts.title_font.render("Settings", True, ui_elements.Colors.dark_golden)
        self.title_rect = self.title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))

        self.screen_section_button = ui_elements.Button(
            user_config.screen_width * 0.309,
            user_config.screen_height * 0.3,
            self.button_for_section_width,
            self.button_for_section_height,
            "Screen",
            (176, 171, 171),
            (166, 151, 151),
            font = ui_elements.Fonts.font_for_labels2,
            border_radius=0
        )

        self.audio_section_button = ui_elements.Button(
            user_config.screen_width * 0.389,
            user_config.screen_height * 0.3,
            self.button_for_section_width,
            self.button_for_section_height,
            "Audio",
            (176, 171, 171),
            (166, 151, 151),
            font=ui_elements.Fonts.font_for_labels2,
            border_radius=0
        )

        self.mouse_section_button = ui_elements.Button(
            user_config.screen_width * 0.469,
            user_config.screen_height * 0.3,
            self.button_for_section_width,
            self.button_for_section_height,
            "Mouse",
            (176, 171, 171),
            (166, 151, 151),
            font=ui_elements.Fonts.font_for_labels2,
            border_radius=0
        )

        self.keyboard_section_button = ui_elements.Button(
            user_config.screen_width * 0.549,
            user_config.screen_height * 0.3,
            self.button_for_section_width,
            self.button_for_section_height,
            "Keyboard",
            (176, 171, 171),
            (166, 151, 151),
            font=ui_elements.Fonts.font_for_labels2,
            border_radius=0
        )

        self.parameters_section_button = ui_elements.Button(
            user_config.screen_width * 0.629,
            user_config.screen_height * 0.3,
            self.button_for_section_width,
            self.button_for_section_height,
            "Parameters",
            (176, 171, 171),
            (166, 151, 151),
            font=ui_elements.Fonts.font_for_labels2,
            border_radius=0
        )

        self.confirm_button = ui_elements.Button(
            user_config.screen_width * 0.425,
            user_config.screen_height * 0.7,
            self.button_width,
            self.button_height,
            "Save Changes",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.back_button = ui_elements.Button(
            user_config.screen_width * 0.425,
            user_config.screen_height * 0.79,
            self.button_width,
            self.button_height,
            "Back",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

        self.screen_resolution_dropdown = ui_elements.Dropdown(
            user_config.screen_width * 0.425,
            user_config.screen_height * 0.482,
            260,
            40,
            options=self.screen_resolution_options,
            default_index=0,
            bg_color=(255, 255, 255),
            border_color=(135, 129, 126),
            active_border_color=(135, 129, 126)
        )

        self.screen_resolution_label = ui_elements.Fonts.font2.render("Resolution", True, ui_elements.Colors.black)
        self.screen_resolution_label_rect = self.screen_resolution_label.get_rect(center=(user_config.screen_width * 0.38, user_config.screen_height * 0.5,))

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))

        screen.blit(self.title, self.title_rect)

        screen.blit(self.screen_resolution_label, self.screen_resolution_label_rect)

        self.screen_section_button.check_hover(mouse_pos)
        self.screen_section_button.draw(screen)

        self.audio_section_button.check_hover(mouse_pos)
        self.audio_section_button.draw(screen)

        self.mouse_section_button.check_hover(mouse_pos)
        self.mouse_section_button.draw(screen)

        self.keyboard_section_button.check_hover(mouse_pos)
        self.keyboard_section_button.draw(screen)

        self.screen_section_button.check_hover(mouse_pos)
        self.screen_section_button.draw(screen)

        self.parameters_section_button.check_hover(mouse_pos)
        self.parameters_section_button.draw(screen)

        self.confirm_button.check_hover(mouse_pos)
        self.confirm_button.draw(screen)

        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(screen)

        self.screen_resolution_dropdown.draw(screen)

    def open_settings_menu(self, screen: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            mouse_pos = pygame.mouse.get_pos()
            self._draw_ui(mouse_pos, screen)

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

                        self.screen_resolution_dropdown.handle_event(event)

                        if self.confirm_button.is_clicked(mouse_pos, mouse_click):
                            new_options = tuple(map(int, self.screen_resolution_dropdown.get_selected_option().split("x")))
                            if (user_config.screen_width, user_config.screen_height) != new_options:
                                self.settings_controller.change_resolution(new_options)

                        if self.back_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            is_running = False

                pygame.display.flip()
                clock.tick(60)
