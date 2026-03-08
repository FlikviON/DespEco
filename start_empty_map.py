import copy

import pygame

import ui_elements
from tile import Tile
from config import user_config
from ui_elements import ImagedButton
from map_manager import MapManager
from minimap_former import MinimapFormer


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
RED = (255, 0, 0)       #
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)      #
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)    #
GRAY = (100, 100, 100)      #

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

        self._set_correct_min_zoom_values()

    def _set_correct_min_zoom_values(self):
        min_zoom_values = {96: 0.275, 80: 0.33, 64: 0.42, 48: 0.56, 32: 0.82, 16: 1.68}
        if WORLD_WIDTH in min_zoom_values:
            self.min_zoom = min_zoom_values.get(WORLD_WIDTH)
            if self.min_zoom > 1:
                self.zoom = self.min_zoom

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
            print(self.zoom)

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


CHUNK_SIZE = 16

class Chunk:
    def __init__(self, tiles, x, y):
        self.tiles = tiles
        self.x = x * CHUNK_SIZE * TILE_SIZE
        self.y = y * CHUNK_SIZE * TILE_SIZE
        self.surface = None
        self.dirty = True

    def rebuild_surface(self):
        if self.surface is None:
            self.surface = pygame.Surface((CHUNK_SIZE * TILE_SIZE, CHUNK_SIZE * TILE_SIZE))
        self.surface.fill((0,0,0,0))
        for tile in self.tiles:
            tile.draw_on_surface(self.surface, tile.x - self.x, tile.y - self.y)
        self.dirty = False

    def draw(self, screen, camera):
        if self.dirty:
            self.rebuild_surface()
        screen.blit(self.surface, camera.world_to_screen(self.x, self.y))


class World:
    def __init__(self, width: int, height: int, start_biome: str = "Meadows", tile_map: list[list[Tile]] = None) -> None:
        global WORLD_WIDTH, WORLD_HEIGHT
        WORLD_WIDTH, WORLD_HEIGHT = width, height
        self.width: int = width
        self.height: int = height
        self.start_biome = {"Meadows": "grass", "Mountains": "mountain", "Water": "water", "Desert": "sand", "Tundra": "snow", "Swamp": "swamp"}[start_biome]
        self.tiles: list[list[Tile]] = tile_map
        self.flags_tiles = {"aqua_flag": None,
                            "black_flag": None,
                            "blue_flag": None,
                            "green_flag": None,
                            "orange_flag": None,
                            "red_flag": None,
                            "white_flag": None,
                            "yellow_flag": None}
        if tile_map is None:
            self.generate_world()

    def generate_world(self) -> None:
        self.tiles = [[Tile(x, y, self.start_biome) for x in range(self.width)] for y in range(self.height)]

    def get_tile_by_cords(self, x: int, y: int) -> Tile | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def deselect_all_tiles(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.tiles[y][x].selected = False

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        start_x, start_y, end_x, end_y = camera.get_visible_tiles()

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile_by_cords(x, y)
                if tile:
                    tile.draw(surface, camera)


class UI:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)

        self.do_show_hud: bool = True
        self.do_show_grid: bool = True
        self.do_show_minimap: bool = False
        self.do_show_brush_size_slider: bool = False

        self.map_saver: MapManager = MapManager()
        self.minimap_former: MinimapFormer = MinimapFormer()

        self.selected_tile: Tile | None = None
        self.selected_item: str = "select_tool"
        self.current_tool: str = "tool"
        self.current_section: str = "Biomes"

        self.current_label = None

    @staticmethod
    def draw_grid(surface: pygame.Surface, camera: Camera, start_x: int, start_y: int, end_x: int, end_y: int) -> None:
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

    def draw(self, surface: pygame.Surface, camera: Camera) -> None:
        info_panel = pygame.Surface((200, 140), pygame.SRCALPHA)
        info_panel.fill((0, 0, 0, 100))
        font = pygame.font.SysFont('tahoma', 22)
        y_offset = 15

        if self.do_show_grid:
            start_x = 0
            start_y = 0
            end_x = WORLD_WIDTH
            end_y = WORLD_HEIGHT
            self.draw_grid(surface, camera, start_x, start_y, end_x, end_y)
        '''
        if self.do_show_minimap:
            mini_map = ui_elements.ImagedButton(
                user_config.screen_width - 400,
                user_config.screen_height - 200,
                400,
                200,
                image_path="Assets/Images/Minimap/current_minimap.png",
                hover_image_path="Assets/Images/Minimap/current_minimap.png"
            )
            mini_map.draw(surface)
        '''

        if self.selected_tile:
            tile = self.selected_tile
            biomes = {"grass": "Meadows", "mountain": "Mountains", "water": "Water", "sand": "Desert", "snow": "Tundra", "swamp": "Swamp"}
            tile_info = [
                f"({tile.x}, {tile.y})",
                f"Biome: {biomes[tile.type]}",
                f"Resource: {tile.stored_resource.capitalize() if tile.stored_resource else '-'}",
                f"Flag: {tile.stored_flag.capitalize()[:tile.stored_flag.capitalize().find('_')] if tile.stored_flag else '-'}",
            ]

            for info in tile_info:
                text_surface = font.render(info, True, YELLOW)
                info_panel.blit(text_surface, (10, y_offset))
                y_offset += 25

            surface.blit(info_panel, (10, 10))

    def update_selected_tile(self, tile: Tile) -> None:
        self.selected_tile = tile



def mark_only_button(button: ui_elements.ImagedButton, buttons: tuple) -> None:
    for buttn in buttons:
        buttn.border_color = ui_elements.Colors.black
    button.border_color = ui_elements.Colors.dark_red

def clear_tile(tile: Tile, world: World, screen: pygame.Surface, camera: Camera) -> None:
    tile.stored_resource = None
    if world.flags_tiles.get(tile.stored_flag) == tile:
        world.flags_tiles[tile.stored_flag] = None
    tile.stored_flag = None
    tile.draw(screen, camera)

def is_tiles_same(tile1: Tile, tile2: Tile) -> bool:
    return tile1.type == tile2.type and tile1.stored_resource == tile2.stored_resource and tile1.stored_flag == tile2.stored_flag

def on_select_select_tool(select_tool_button: ImagedButton, all_buttons: tuple, ui: UI) -> None:
    mark_only_button(select_tool_button, all_buttons)
    ui.selected_item = "select_tool"
    ui.current_tool = "tool"

def on_select_remove_tool(remove_tool_button: ui_elements.ImagedButton, all_buttons: tuple, ui: UI) -> None:
    mark_only_button(remove_tool_button, all_buttons)
    ui.selected_item = "remove_tool"
    ui.current_tool = "tool"

def on_select_back_tool(actions: list, screen: pygame.Surface, camera: Camera) -> None:
    if len(actions) > 0:
        tile_before_act = actions[-1]["before"]
        tile = actions[-1]["after"]
        tile.type = tile_before_act.type
        tile.stored_resource = tile_before_act.stored_resource
        tile.stored_flag = tile_before_act.stored_flag
        actions.pop(-1)
        tile.draw(screen, camera)