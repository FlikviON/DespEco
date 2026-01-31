import pygame
import sys

from config import UserConfig
import ui_elements


def open_redactor_menu(screen):
    background = ui_elements.MenuBackground.load_background_image()
    screen.blit(background, (0, 0))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False