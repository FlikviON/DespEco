import sys

import pygame

import ui_elements
from config import user_config
from game_in_redactor_mode import GameInRedactorMode
from sounds_manager import Sounds


class CreateMapMenu:
    def __init__(self) -> None:
        self.button_width: int = 260
        self.button_height: int = 70
        self.dropdown_width: int = 200
        self.dropdown_height: int = 32
        self.map_size_dropdown_options: list[str] = [f"{16 * i}x{16 * i}" for i in range(1, 65)]
        self.biome_dropdown_options: list[str] = ["Meadows", "Mountains", "Water", "Desert", "Tundra", "Swamp"]

        self._initialize_ui()
        self._initialize_updating_ui()

    def _initialize_ui(self) -> None:
        self.background = ui_elements.MenuBackground.load_background_image()

        self.map_size_dropdown = ui_elements.Dropdown(
            user_config.screen_width // 2 - self.dropdown_width // 2,
            user_config.screen_height // 3,
            self.dropdown_width,
            self.dropdown_height,
            self.map_size_dropdown_options,
            default_index=3,
            visible_items=5
        )

        self.biome_dropdown = ui_elements.Dropdown(
            user_config.screen_width // 2 - self.dropdown_width // 2,
            user_config.screen_height // 2.6,
            self.dropdown_width,
            self.dropdown_height,
            self.biome_dropdown_options,
            default_index=0,
            visible_items=5
        )

        self.create_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 2 + 100,
            self.button_width,
            self.button_height,
            "Create Map",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.back_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height // 2 + 200,
            self.button_width,
            self.button_height,
            "Back",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

        self.title = ui_elements.Fonts.title_font.render("Create New Map", True, ui_elements.Colors.dark_golden)
        self.title_rect = self.title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))

        self.map_size_label = ui_elements.Fonts.font2.render("Map size", True, ui_elements.Colors.dark_green)
        self.map_size_label_rect = self.map_size_label.get_rect(center=(user_config.screen_width // 2 - self.dropdown_width * 0.8, user_config.screen_height * 0.345,))

        self.biome_label = ui_elements.Fonts.font2.render("Biome", True, ui_elements.Colors.dark_green)
        self.biome_label_rect = self.map_size_label.get_rect(center=(user_config.screen_width // 2 - self.dropdown_width * 0.8, user_config.screen_height * 0.398,))


    def _initialize_updating_ui(self):
        self.preview_image = f"Assets/MapPreviews/{self.biome_dropdown.get_selected_option()}_map.png"
        width = height = self.map_size_dropdown.get_selected_value()

        self.preview_button = ui_elements.ImagedButton(
            user_config.screen_width * 0.656,
            user_config.screen_height // 3,
            350,
            350,
            self.preview_image,
            self.preview_image,
            do_draw_wrapper=False
        )

        self.width_label = ui_elements.Fonts.font2.render(f"{width}", True, ui_elements.Colors.black)
        self.width_label_rect = self.width_label.get_rect(
            center=(user_config.screen_width * 0.76, user_config.screen_height * 0.68,))

        self.height_label = ui_elements.Fonts.font2.render(f"{height}", True, ui_elements.Colors.black)
        self.height_label_rect = self.height_label.get_rect(
            center=(user_config.screen_width * 0.879, user_config.screen_height * 0.5,))

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))

        screen.blit(self.title, self.title_rect)

        screen.blit(self.map_size_label, self.map_size_label_rect)

        screen.blit(self.biome_label, self.biome_label_rect)

        screen.blit(self.height_label, self.height_label_rect)

        screen.blit(self.width_label, self.width_label_rect)

        self.create_button.check_hover(mouse_pos)
        self.create_button.draw(screen)

        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(screen)

        self.preview_button.draw(screen)

        self.map_size_dropdown.draw(screen)

        if not self.map_size_dropdown.is_open:
            self.biome_dropdown.draw(screen)

    def _on_mouse_click(self, event: pygame.Event, mouse_pos: tuple[int, int]) -> None:
        mouse_click = True

        map_size_dropdown_state = self.map_size_dropdown.is_open
        self.map_size_dropdown.handle_event(event)

        if not map_size_dropdown_state:
            self.biome_dropdown.handle_event(event)

        if self.create_button.is_clicked(mouse_pos, mouse_click):
            Sounds.button_click.play()
            width = height = self.map_size_dropdown.get_selected_value()
            start_biome = self.biome_dropdown.get_selected_option()
            GameInRedactorMode(width, height, start_biome).start_game()

    def open_create_map_menu(self, screen: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        is_running = True
        while is_running:
            mouse_pos = pygame.mouse.get_pos()
            self._initialize_updating_ui()
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
                        self._on_mouse_click(event, mouse_pos)
                        if self.back_button.is_clicked(mouse_pos, True):
                            Sounds.button_click.play()
                            is_running = False

                    elif event.button == 4 or event.button == 5:
                        self.map_size_dropdown.handle_event(event)
                        self.biome_dropdown.handle_event(event)

            pygame.display.flip()
            clock.tick(60)