import pygame
import sys

import ui_elements
from config import UserConfig
from create_map_menu import open_create_map_menu


def open_redactor_menu(screen: pygame.Surface) -> None:
    button_width, button_height = 260, 70

    create_map_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 2 - 40,
        button_width,
        button_height,
        "Create Map",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    load_map_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 2 + 60,
        button_width,
        button_height,
        "Load Map",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    back_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 2 + 160,
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

        title = ui_elements.Fonts.title_font.render("Map Redactor", True, ui_elements.Colors.dark_golden)
        title_rect = title.get_rect(center=(UserConfig.screen_width // 2, UserConfig.screen_height // 6))
        screen.blit(title, title_rect)

        create_map_button.check_hover(mouse_pos)
        load_map_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        create_map_button.draw(screen)
        load_map_button.draw(screen)
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

                    if create_map_button.is_clicked(mouse_pos, mouse_click):
                        open_create_map_menu(screen)

                    if load_map_button.is_clicked(mouse_pos, mouse_click):
                        ...

                    if back_button.is_clicked(mouse_pos, mouse_click):
                        is_running = False

            pygame.display.flip()
            clock.tick(60)
