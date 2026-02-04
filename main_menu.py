import pygame
import sys

import config
import ui_elements
from redactor_menu import open_redactor_menu
from config import UserConfig


config.initialize_config()

pygame.init()
screen = pygame.display.set_mode((UserConfig.screen_width, UserConfig.screen_height))
pygame.display.set_caption("Game menu")


def open_main_menu() -> None:
    button_width, button_height = 260, 70

    singleplayer_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 3 - 40,
        button_width,
        button_height,
        "Singleplayer",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    multiplayer_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 3 + 50,
        button_width,
        button_height,
        "Multiplayer",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    redactor_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 3 + 140,
        button_width,
        button_height,
        "Map Redactor",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    settings_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 3 + 230,
        button_width,
        button_height,
        "Settings",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    exit_button = ui_elements.Button(
        UserConfig.screen_width // 2 - button_width // 2,
        UserConfig.screen_height // 3 + 320,
        button_width,
        button_height,
        "Quit game",
        ui_elements.Colors.red,
        ui_elements.Colors.hover_red
    )

    clock = pygame.time.Clock()

    is_running = True
    while is_running:
        background = ui_elements.MenuBackground.load_background_image()
        screen.blit(background, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        title = ui_elements.Fonts.title_font.render("DespEco", True, ui_elements.Colors.dark_golden)
        title_rect = title.get_rect(center=(UserConfig.screen_width // 2, UserConfig.screen_height // 6))
        screen.blit(title, title_rect)

        singleplayer_button.check_hover(mouse_pos)
        multiplayer_button.check_hover(mouse_pos)
        redactor_button.check_hover(mouse_pos)
        settings_button.check_hover(mouse_pos)
        exit_button.check_hover(mouse_pos)

        singleplayer_button.draw(screen)
        multiplayer_button.draw(screen)
        redactor_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

                    if singleplayer_button.is_clicked(mouse_pos, mouse_click):
                        return

                    if multiplayer_button.is_clicked(mouse_pos, mouse_click):
                        ...

                    if redactor_button.is_clicked(mouse_pos, mouse_click):
                        open_redactor_menu(screen)

                    if settings_button.is_clicked(mouse_pos, mouse_click):
                        ...

                    if exit_button.is_clicked(mouse_pos, mouse_click):
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(60)
