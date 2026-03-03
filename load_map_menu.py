import sys
from pathlib import Path

import pygame

import ui_elements
from game_in_redactor_mode import GameInRedactorMode
from config import user_config
from map_manager import MapManager


def get_saved_maps_names() -> list[str]:
    directory = Path("Saves")
    all_maps_names = list(filter(lambda q: q[-5:] == ".json", [item.name for item in directory.iterdir() if item.is_file()]))
    all_maps_names = list(map(lambda q: q[:-5], all_maps_names))
    return all_maps_names

def open_load_map_menu(screen: pygame.Surface) -> None:
    button_width, button_height = 260, 70
    view_map_button_start = 0
    view_map_button_end = 10

    back_button = ui_elements.Button(
        user_config.screen_width // 2 - button_width // 2,
        user_config.screen_height * 0.78,
        button_width,
        button_height,
        "Back",
        ui_elements.Colors.red,
        ui_elements.Colors.hover_red
    )

    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        background = ui_elements.MenuBackground.load_background_image()
        screen.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        title = ui_elements.Fonts.title_font.render("Load Map", True, ui_elements.Colors.dark_golden)
        title_rect = title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))
        screen.blit(title, title_rect)

        maps_names = get_saved_maps_names()
        maps_names_buttons = []
        for i, map_name in enumerate(maps_names):
            maps_names_buttons.append(
                ui_elements.Button(
                user_config.screen_width * 0.378,
                user_config.screen_height * (0.32 + 0.04 * i),
                400,
                32,
                map_name,
                (222, 235, 176),
                (200, 213, 174),
                font = ui_elements.Fonts.font_for_maps_names)
            )

        for map_name_button in maps_names_buttons[view_map_button_start: view_map_button_end]:
            map_name_button.check_hover(mouse_pos)
            map_name_button.draw(screen)

        back_button.check_hover(mouse_pos)
        back_button.draw(screen)

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

                    if any(map_button.is_clicked(mouse_pos) for map_button in maps_names_buttons[view_map_button_start: view_map_button_end]):
                        for button in maps_names_buttons:
                            if button.is_clicked(mouse_pos):
                                map_manager = MapManager()
                                game_map = map_manager.load_map(button.text)
                                tile_map = map_manager.decode_map(game_map)
                                width = len(tile_map[0])
                                height = len(tile_map)
                                GameInRedactorMode(width, height, tile_map=tile_map).start_game()

                    if back_button.is_clicked(mouse_pos, mouse_click):
                        is_running = False

            elif event.type == pygame.MOUSEWHEEL:
                if event.y < 0:
                    view_map_button_start += 1
                    view_map_button_end += 1
                elif event.y > 0:
                    view_map_button_start -= 1
                    view_map_button_end -= 1

            pygame.display.flip()
            clock.tick(60)
