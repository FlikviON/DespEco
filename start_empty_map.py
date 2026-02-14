import pygame

import ui_elements
from tile import Tile
from config import user_config


pygame.init()

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


class World:
    def __init__(self, width: int, height: int) -> None:
        global WORLD_WIDTH, WORLD_HEIGHT
        WORLD_WIDTH, WORLD_HEIGHT = width, height
        self.width: int = width
        self.height: int = height
        self.tiles: list[list[Tile]] = []
        self.generate_world()

    def generate_world(self) -> None:
        print(f"Generation world {self.width}x{self.height}...")
        self.tiles = [[Tile(x, y) for x in range(self.width)] for y in range(self.height)]
        print("Done")

    def get_tile_by_cords(self, x: int, y: int) -> Tile | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    @staticmethod
    def draw_grid(surface: pygame.Surface, camera: Camera,
                  start_x: int, start_y: int, end_x: int, end_y: int) -> None:
        grid_color = (0, 0, 0)
        thickness = 1

        for x in range(start_x, end_x + 1):
            world_x = x * TILE_SIZE
            screen_x = int(round((world_x - camera.x) * camera.zoom))
            pygame.draw.line(surface, grid_color, (screen_x, 0), (screen_x, SCREEN_HEIGHT), thickness)

        for y in range(start_y, end_y + 1):
            world_y = y * TILE_SIZE
            screen_y = int(round((world_y - camera.y) * camera.zoom))
            pygame.draw.line(surface, grid_color, (0, screen_y), (SCREEN_WIDTH, screen_y), thickness)

    def draw(self, surface: pygame.Surface, camera: Camera, show_grid: bool = False) -> None:
        start_x, start_y, end_x, end_y = camera.get_visible_tiles()

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile_by_cords(x, y)
                if tile:
                    tile.draw(surface, camera)

        if show_grid:
            self.draw_grid(surface, camera, start_x, start_y, end_x, end_y)


class UI:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        self.selected_tile: Tile | None = None
        self.selected_item: str | None = None

    def draw(self, surface: pygame.Surface) -> None:
        info_panel = pygame.Surface((320, 170), pygame.SRCALPHA)
        info_panel.fill((0, 0, 0, 200))
        y_offset = 15

        if self.selected_tile:
            tile = self.selected_tile
            tile_info = [
                f"Tile: ({tile.x}, {tile.y})",
                f"Type: {tile.type[0].upper()}{tile.type[1:]}",
                f"Passable: {'Yes' if tile.passable else 'No'}",
                f"Buildable: {'Yes' if tile.buildable else 'No'}",
                f"Resources: {', '.join(tile.resources.keys()) if tile.resources else 'No'}"
            ]

            for info in tile_info:
                text_surface = self.small_font.render(info, True, YELLOW)
                info_panel.blit(text_surface, (10, y_offset))
                y_offset += 20

            surface.blit(info_panel, (10, 10))

    def update_selected_tile(self, tile: Tile) -> None:
        self.selected_tile = tile


def start_game(world_width: int, world_height: int) -> None:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DespEco")

    world = World(world_width, world_height)
    camera = Camera()
    ui = UI()

    clock = pygame.time.Clock()
    show_grid = True

    button_width, button_height = 100, 100
    dropdown_width, dropdown_height = 200, 32

    dropdown_options = ["Biomes", "Resources", "Start positions"]

    redactor_type_dropdown = ui_elements.Dropdown(
        user_config.screen_width // 2 - dropdown_width // 2 - 700,
        user_config.screen_height // 2 + 350,
        dropdown_width,
        dropdown_height,
        dropdown_options,
        default_index=0,
        visible_items=3
    )

    grass_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 400,
        user_config.screen_height // 2 + 350,
        button_width,
        button_height,
        ui_elements.Colors.grass_darker_color,
        image_path="Assets/Tiles/grass.png"
    )

    mountain_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 270,
        user_config.screen_height // 2 + 350,
        button_width,
        button_height,
        ui_elements.Colors.mountain_color,
        image_path="Assets/Tiles/mountain.png"
    )

    water_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 140,
        user_config.screen_height // 2 + 350,
        button_width,
        button_height,
        ui_elements.Colors.water_color,
        image_path="Assets/Tiles/water.png"
    )

    sand_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 10,
        user_config.screen_height // 2 + 350,
        button_width,
        button_height,
        ui_elements.Colors.sand_color,
        image_path="Assets/Tiles/sand.png"
    )

    snow_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 120,
        user_config.screen_height // 2 + 350,
        button_width,
        button_height,
        ui_elements.Colors.snow_color,
        image_path="Assets/Tiles/snow.png"
    )

    swamp_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 250,
        user_config.screen_height // 2 + 350,
        button_width,
        button_height,
        ui_elements.Colors.swamp_color,
        image_path="Assets/Tiles/swamp.png"
    )

    is_running = True
    print("Game started")

    while is_running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                elif event.key == pygame.K_F1:
                    show_grid = not show_grid
                elif event.key == pygame.K_F2:
                    camera.toggle_edge_scrolling()
                elif event.key == pygame.K_SPACE:
                    if ui.selected_tile:
                        camera.center_on_tile(ui.selected_tile.x, ui.selected_tile.y)
                    else:
                        camera.x = (WORLD_WIDTH * TILE_SIZE) / 2 - (SCREEN_WIDTH / camera.zoom) / 2
                        camera.y = (WORLD_HEIGHT * TILE_SIZE) / 2 - (SCREEN_HEIGHT / camera.zoom) / 2

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
                    redactor_type_dropdown.handle_event(event)

                    if grass_button.is_clicked(mouse_pos, mouse_click):
                        ui.selected_item = "grass"
                    elif mountain_button.is_clicked(mouse_pos, mouse_click):
                        ui.selected_item = "mountain"
                    elif water_button.is_clicked(mouse_pos, mouse_click):
                        ui.selected_item = "water"
                    elif sand_button.is_clicked(mouse_pos, mouse_click):
                        ui.selected_item = "sand"
                    elif snow_button.is_clicked(mouse_pos, mouse_click):
                        ui.selected_item = "snow"
                    elif swamp_button.is_clicked(mouse_pos, mouse_click):
                        ui.selected_item = "swamp"
                    elif redactor_type_dropdown.rect.collidepoint(mouse_pos):
                        print("Redactor")
                    elif redactor_type_dropdown.item_rect.collidepoint(mouse_pos):
                        print("Redactor chose")

                    else:
                        tile_x, tile_y = camera.screen_to_world(mouse_x, mouse_y)

                        for y in range(world.height):
                            for x in range(world.width):
                                world.tiles[y][x].selected = False

                        tile = world.get_tile_by_cords(tile_x, tile_y)
                        if tile:
                            tile.selected = True
                            ui.update_selected_tile(tile)
                            print(f"Tile: ({tile.x}, {tile.y}) - {tile.type}")

                            if ui.selected_item:
                                tile.type = ui.selected_item
                                tile.draw(screen, camera)

                elif event.button == 4 or event.button == 5:
                    redactor_type_dropdown.handle_event(event)
            elif event.type == pygame.MOUSEWHEEL:
                camera.handle_event(event)

        camera.update_with_mouse(mouse_x, mouse_y)
        camera.update_with_keyboard(keys)
        camera.update()

        screen.fill(BLACK)
        world.draw(screen, camera, show_grid)
        ui.draw(screen)
        redactor_type_dropdown.draw(screen)

        current_section = redactor_type_dropdown.get_selected_option()
        if current_section == "Biomes":
            biomes_buttons = (grass_button, mountain_button, water_button, sand_button, snow_button, swamp_button)
            for button in biomes_buttons:
                button.draw(screen)
                button.check_hover(mouse_pos)

        fps_text = ui.small_font.render(f"FPS: {int(clock.get_fps())}", True, GREEN)
        screen.blit(fps_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print("\nGame over")
