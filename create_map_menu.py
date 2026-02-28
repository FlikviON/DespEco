import pygame
import sys

import ui_elements
import start_empty_map
from game_in_redactor_mode import GameInRedactorMode
from config import user_config


def open_create_map_menu(screen: pygame.Surface) -> None:
    button_width, button_height = 260, 70
    dropdown_width, dropdown_height = 200, 32
    map_size_dropdown_options = [f"{16 * i}x{16 * i}" for i in range(1, 65)]
    biome_dropdown_options = ["Meadows", "Mountains", "Water", "Desert", "Tundra", "Swamp"]

    map_size_dropdown = ui_elements.Dropdown(
        user_config.screen_width // 2 - dropdown_width // 2,
        user_config.screen_height // 3,
        dropdown_width,
        dropdown_height,
        map_size_dropdown_options,
        default_index=3,
        visible_items=5
    )

    biome_dropdown = ui_elements.Dropdown(
        user_config.screen_width // 2 - dropdown_width // 2,
        user_config.screen_height // 2.6,
        dropdown_width,
        dropdown_height,
        biome_dropdown_options,
        default_index=0,
        visible_items=5
    )

    create_button = ui_elements.Button(
        user_config.screen_width // 2 - button_width // 2,
        user_config.screen_height // 2 + 100,
        button_width,
        button_height,
        "Create Map",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    back_button = ui_elements.Button(
        user_config.screen_width // 2 - button_width // 2,
        user_config.screen_height // 2 + 200,
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

        title = ui_elements.Fonts.title_font.render("Create New Map", True, ui_elements.Colors.dark_golden)
        title_rect = title.get_rect(center=(user_config.screen_width // 2, user_config.screen_height // 6))
        screen.blit(title, title_rect)

        map_size_label = ui_elements.Fonts.font2.render("Map size", True, ui_elements.Colors.dark_green)
        map_size_label_rect = map_size_label.get_rect(center=(user_config.screen_width // 2 - dropdown_width * 0.8, user_config.screen_height * 0.345,))
        screen.blit(map_size_label, map_size_label_rect)

        biome_label = ui_elements.Fonts.font2.render("Biome", True, ui_elements.Colors.dark_green)
        biome_label_rect = map_size_label.get_rect(center=(user_config.screen_width // 2 - dropdown_width * 0.8, user_config.screen_height * 0.398,))
        screen.blit(biome_label, biome_label_rect)

        create_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        map_size_dropdown.draw(screen)
        if not map_size_dropdown.is_open:
            biome_dropdown.draw(screen)

        create_button.draw(screen)
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
                    mouse_pos = pygame.mouse.get_pos()

                    map_size_dropdown_state = map_size_dropdown.is_open

                    map_size_dropdown.handle_event(event)
                    if not map_size_dropdown_state:
                        biome_dropdown.handle_event(event)

                    if create_button.is_clicked(mouse_pos, mouse_click):
                        width = height = map_size_dropdown.get_selected_value()
                        start_biome = biome_dropdown.get_selected_option()
                        GameInRedactorMode(width, height, start_biome).start_game()

                    elif back_button.is_clicked(mouse_pos, mouse_click):
                        is_running = False

                elif event.button == 4 or event.button == 5:
                    map_size_dropdown.handle_event(event)
                    biome_dropdown.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

    return None
