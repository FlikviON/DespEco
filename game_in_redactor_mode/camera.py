import pygame
from config import user_config


SCREEN_WIDTH = user_config.screen_width
SCREEN_HEIGHT = user_config.screen_height
TILE_SIZE = 64

WORLD_WIDTH = 64
WORLD_HEIGHT = 64

FPS = 60
SCROLL_MARGIN = 50
SCROLL_SPEED = 25
KEYBOARD_SCROLL_SPEED = 25

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)
GRAY = (100, 100, 100)

COLORS = {
    "grass": (34, 139, 34),
    "water": (30, 144, 255),
    "mountain": (139, 137, 137),
    "forest": (0, 100, 0),
    "sand": (238, 214, 175),
    "snow": (255, 250, 250),
    "swamp": (0, 60, 30),
    "rock": (90, 90, 90)
}


class Camera:
    def __init__(self) -> None:
        self.x: float = 0.0
        self.y: float = 0.0
        self.zoom: float = 1.0
        self.min_zoom: float = 0.25
        self.max_zoom: float = 3.0
        self.scroll_speed: float = SCROLL_SPEED
        self.keyboard_speed: float = KEYBOARD_SCROLL_SPEED
        self.scroll_margin: int = SCROLL_MARGIN
        self.is_edge_scrolling: bool = True

    def update_with_mouse(self, mouse_x: int, mouse_y: int) -> None:
        if not self.is_edge_scrolling:
            return

        scroll_up = 0
        scroll_down = 0
        scroll_left = 0
        scroll_right = 0

        if mouse_y < self.scroll_margin:
            distance = self.scroll_margin - mouse_y
            scroll_up = (self.scroll_speed * (distance / self.scroll_margin)) / self.zoom
        elif mouse_y > SCREEN_HEIGHT - self.scroll_margin:
            distance = mouse_y - (SCREEN_HEIGHT - self.scroll_margin)
            scroll_down = (self.scroll_speed * (distance / self.scroll_margin)) / self.zoom

        if mouse_x < self.scroll_margin:
            distance = self.scroll_margin - mouse_x
            scroll_left = (self.scroll_speed * (distance / self.scroll_margin)) / self.zoom
        elif mouse_x > SCREEN_WIDTH - self.scroll_margin:
            distance = mouse_x - (SCREEN_WIDTH - self.scroll_margin)
            scroll_right = (self.scroll_speed * (distance / self.scroll_margin)) / self.zoom

        self.x += scroll_right - scroll_left
        self.y += scroll_down - scroll_up

    def update_with_keyboard(self, keys) -> None:
        move_speed = self.keyboard_speed / self.zoom

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += move_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= move_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += move_speed

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_x_before = mouse_x / self.zoom + self.x
            world_y_before = mouse_y / self.zoom + self.y

            if event.y > 0:
                self.zoom = min(self.max_zoom, self.zoom * 1.1)
            else:
                self.zoom = max(self.min_zoom, self.zoom / 1.1)

            world_x_after = mouse_x / self.zoom + self.x
            world_y_after = mouse_y / self.zoom + self.y

            self.x += world_x_before - world_x_after
            self.y += world_y_before - world_y_after

    def update(self) -> None:
        max_x = max(0.0, WORLD_WIDTH * TILE_SIZE - SCREEN_WIDTH / self.zoom)
        max_y = max(0.0, WORLD_HEIGHT * TILE_SIZE - SCREEN_HEIGHT / self.zoom)

        self.x = max(0.0, min(self.x, max_x))
        self.y = max(0.0, min(self.y, max_y))

    def screen_to_world(self, screen_x: int, screen_y: int) -> tuple[int, int]:
        world_x = (screen_x / self.zoom) + self.x
        world_y = (screen_y / self.zoom) + self.y
        tile_x = int(world_x // TILE_SIZE)
        tile_y = int(world_y // TILE_SIZE)
        return tile_x, tile_y

    def world_to_screen(self, world_x: float, world_y: float) -> tuple[int, int]:
        screen_x = int((world_x - self.x) * self.zoom)
        screen_y = int((world_y - self.y) * self.zoom)
        return screen_x, screen_y

    def get_visible_tiles(self) -> tuple[int, int, int, int]:
        start_x = int(self.x // TILE_SIZE) - 1
        start_y = int(self.y // TILE_SIZE) - 1
        end_x = int((self.x + SCREEN_WIDTH / self.zoom) // TILE_SIZE) + 2
        end_y = int((self.y + SCREEN_HEIGHT / self.zoom) // TILE_SIZE) + 2

        start_x = max(0, start_x)
        start_y = max(0, start_y)
        end_x = min(WORLD_WIDTH, end_x)
        end_y = min(WORLD_HEIGHT, end_y)

        return start_x, start_y, end_x, end_y

    def center_on_tile(self, tile_x: int, tile_y: int) -> None:
        self.x = tile_x * TILE_SIZE + TILE_SIZE / 2 - (SCREEN_WIDTH / self.zoom) / 2
        self.y = tile_y * TILE_SIZE + TILE_SIZE / 2 - (SCREEN_HEIGHT / self.zoom) / 2

    def toggle_edge_scrolling(self) -> None:
        self.is_edge_scrolling = not self.is_edge_scrolling