import sys
from pathlib import Path

import pygame

import ui_elements
from game_in_redactor_mode import GameInRedactorMode
from config import user_config
from map_manager import MapManager
from Menues.rename_map_menu import RenameMapMenu
from Menues.submit_delete_map_menu import SubmitDeleteMapMenu
from sounds_manager import Sounds


class SavedMapsMenu:
    def __init__(self) -> None:
        self.button_width: int = 260
        self.button_height: int = 70

        self.is_running: bool = False

        self.maps_directory: Path = Path("Saves")
        self.maps_names: list[str] = self._get_saved_maps_names()

        self.submit_delete_map_menu: SubmitDeleteMapMenu = SubmitDeleteMapMenu()
        self.rename_map_menu: RenameMapMenu = RenameMapMenu()
        self.map_manager: MapManager = MapManager()

        self._initialize_ui()

    def _initialize_ui(self) -> None:
        self.background = ui_elements.MenuBackground.load_background_image()

        self.title = ui_elements.Fonts.title_font.render("Saved Maps", True, ui_elements.Colors.dark_golden)
        self.title_rect = self.title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))

        self.maps_optionbox = ui_elements.OptionBox(user_config.screen_width * 0.376,
                                                                           user_config.screen_height * 0.26,
                                                                           400,
                                                                           260,
                                                                           self.maps_names,
                                                                           visible_items=8,
                                                                           default_index=0)

        self.launch_map_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.55,
            self.button_width,
            self.button_height,
            "Launch Map",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.rename_map_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.64,
            self.button_width,
            self.button_height,
            "Rename Map",
            ui_elements.Colors.blue,
            ui_elements.Colors.hover_blue
        )

        self.delete_map_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.73,
            self.button_width,
            self.button_height,
            "Delete Map",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

        self.back_button = ui_elements.Button(
            user_config.screen_width // 2 - self.button_width // 2,
            user_config.screen_height * 0.82,
            self.button_width,
            self.button_height,
            "Back",
            ui_elements.Colors.red,
            ui_elements.Colors.hover_red
        )

    def _draw_ui(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))
        screen.blit(self.title, self.title_rect)

        self.maps_optionbox.draw(screen)

        self.launch_map_button.check_hover(mouse_pos)
        self.launch_map_button.draw(screen)

        self.rename_map_button.check_hover(mouse_pos)
        self.rename_map_button.draw(screen)

        self.delete_map_button.check_hover(mouse_pos)
        self.delete_map_button.draw(screen)

        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(screen)

    def _get_saved_maps_names(self) -> list[str]:
        directory = self.maps_directory
        all_maps_names = list(filter(lambda q: q[-5:] == ".json", [item.name for item in directory.iterdir() if item.is_file()]))
        all_maps_names = list(map(lambda q: q[:-5], all_maps_names))
        return all_maps_names

    def _on_launch_map_button_click(self, selected_map: str) -> None:
        Sounds.button_click.play()
        if selected_map is not None:
            game_map = self.map_manager.load_map(selected_map)
            tile_map = self.map_manager.decode_map(game_map)
            width = len(tile_map[0])
            height = len(tile_map)
            GameInRedactorMode(width, height, tile_map=tile_map).start_game()

    def _on_rename_map_button(self, selected_map: str, screen: pygame.Surface) -> None:
        Sounds.button_click.play()
        new_map_name = self.rename_map_menu.open_rename_map_menu(selected_map, screen)
        if new_map_name:
            current_map_path = Path(f"Saves/{selected_map}.json")
            new_path = Path(f"Saves/{new_map_name}.json")
            current_map_path.rename(new_path)
            self.maps_names = self._get_saved_maps_names()
            self._initialize_ui()

    def _on_delete_map_button(self, map_name: str, screen: pygame.Surface) -> None:
        Sounds.button_click.play()
        if self.submit_delete_map_menu.open_submit_delete_map_menu(map_name, screen):
            if map_name in self.maps_names:
                self.maps_names.remove(map_name)
                map_path = Path(f"Saves/{map_name}.json")
                if map_path.exists():
                    map_path.unlink()
                self.maps_names = self._get_saved_maps_names()
                self._initialize_ui()

    def open_saved_maps_menu(self, screen: pygame.Surface) -> None:
        clock = pygame.time.Clock()
        self.is_running = True
        while self.is_running:
            mouse_pos = pygame.mouse.get_pos()
            self._draw_ui(mouse_pos, screen)

            for event in pygame.event.get():
                self.maps_optionbox.handle_event(event)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True
                        selected_map = self.maps_optionbox.get_selected_option()

                        if self.launch_map_button.is_clicked(mouse_pos, mouse_click):
                            self._on_launch_map_button_click(selected_map)

                        elif self.rename_map_button.is_clicked(mouse_pos, mouse_click):
                            self._on_rename_map_button(selected_map, screen)

                        elif self.delete_map_button.is_clicked(mouse_pos, mouse_click):
                            self._on_delete_map_button(selected_map, screen)

                        elif self.back_button.is_clicked(mouse_pos, mouse_click):
                            Sounds.button_click.play()
                            self.is_running = False

            pygame.display.flip()
            clock.tick(60)