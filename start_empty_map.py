import pygame
import copy

import ui_elements
from tile import Tile
from config import user_config
from ui_elements import ImagedButton
from map_saver import MapSaver
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


class World:
    def __init__(self, width: int, height: int, start_biome: str = "Meadows") -> None:
        global WORLD_WIDTH, WORLD_HEIGHT
        WORLD_WIDTH, WORLD_HEIGHT = width, height
        self.width: int = width
        self.height: int = height
        self.start_biome = {"Meadows": "grass", "Mountains": "mountain", "Water": "water", "Desert": "sand", "Tundra": "snow", "Swamp": "swamp"}[start_biome]
        self.tiles: list[list[Tile]] = []
        self.flags_tiles = {"aqua_flag": None,
                            "black_flag": None,
                            "blue_flag": None,
                            "green_flag": None,
                            "orange_flag": None,
                            "red_flag": None,
                            "white_flag": None,
                            "yellow_flag": None}
        self.generate_world()

    def generate_world(self) -> None:
        print(f"Generation world {self.width}x{self.height}...")
        self.tiles = [[Tile(x, y, self.start_biome) for x in range(self.width)] for y in range(self.height)]
        print("Done")

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

        self.do_show_grid: bool = True
        self.do_show_minimap: bool = True

        self.map_saver: MapSaver = MapSaver()
        self.minimap_former: MinimapFormer = MinimapFormer()

        self.selected_tile: Tile | None = None
        self.selected_item: str | None = None
        self.current_tool: str | None = None
        self.current_section: str | None = None

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

        mini_map = ui_elements.ImagedButton(
            user_config.screen_width - 400,
            user_config.screen_height - 200,
            400,
            200,
            image_path="Assets/Images/Minimap/current_minimap.png",
            hover_image_path="Assets/Images/Minimap/current_minimap.png"
        )

        if self.do_show_grid:
            start_x = 0
            start_y = 0
            end_x = WORLD_WIDTH
            end_y = WORLD_HEIGHT
            self.draw_grid(surface, camera, start_x, start_y, end_x, end_y)

        if self.do_show_minimap:
            mini_map.draw(surface)

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


def start_game(world_width: int, world_height: int, start_biome: str) -> None:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DespEco")

    world = World(world_width, world_height, start_biome)
    camera = Camera()
    ui = UI()

    clock = pygame.time.Clock()
    ui.current_section = "Biomes"

    button_width, button_height = 100, 100
    dropdown_width, dropdown_height = 200, 32

    dropdown_options = ["Biomes", "Resources", "Start positions", "Save map"]

    redactor_type_dropdown = ui_elements.Dropdown(
        10,
        user_config.screen_height // 2 - 330,
        dropdown_width,
        dropdown_height,
        dropdown_options,
        default_index=0,
        visible_items=4
    )

    save_map_button = ui_elements.Button(
        10,
        user_config.screen_height // 2 - 100,
        button_width + 100,
        button_height - 10,
        "Save Map",
        (255, 127, 80),
        ui_elements.Colors.grass_darker_color,
    )

    map_name_input_box = ui_elements.InputBox(10,
                                              user_config.screen_height // 2 - 200,
                                              dropdown_width * 1.5,
                                              dropdown_height,
                                              "Map name: ",
                                              max_length=15)

    grass_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 340,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Tiles/Light/grass.png",
        hover_image_path="Assets/Tiles/Dark/grass.png"
    )

    mountain_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 210,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Tiles/Light/mountain.png",
        hover_image_path="Assets/Tiles/Dark/mountain.png"
    )

    water_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 80,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Tiles/Light/water.png",
        hover_image_path="Assets/Tiles/Dark/water.png"
    )

    sand_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 50,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Tiles/Light/sand.png",
        hover_image_path="Assets/Tiles/Dark/sand.png"
    )

    snow_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 180,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Tiles/Light/snow.png",
        hover_image_path="Assets/Tiles/Dark/snow.png"
    )

    swamp_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 310,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Tiles/Light/swamp.png",
        hover_image_path="Assets/Tiles/Dark/swamp.png"
    )

    aqua_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 470,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/aqua_flag.png",
        hover_image_path="Assets/Flags/Dark/aqua_flag.png"
    )

    black_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 340,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/black_flag.png",
        hover_image_path="Assets/Flags/Dark/black_flag.png"
    )

    blue_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 210,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/blue_flag.png",
        hover_image_path="Assets/Flags/Dark/blue_flag.png"
    )

    green_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 80,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/green_flag.png",
        hover_image_path="Assets/Flags/Dark/green_flag.png"
    )

    orange_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 50,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/orange_flag.png",
        hover_image_path="Assets/Flags/Dark/orange_flag.png"
    )

    red_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 180,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/red_flag.png",
        hover_image_path="Assets/Flags/Dark/red_flag.png"
    )

    white_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 310,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/white_flag.png",
        hover_image_path="Assets/Flags/Dark/white_flag.png"
    )

    yellow_flag_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 440,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Flags/Light/yellow_flag.png",
        hover_image_path="Assets/Flags/Dark/yellow_flag.png"
    )

    food_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 400,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/wheat.png",
        hover_image_path="Assets/Resources/Dark/wheat.png"
    )

    wood_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 270,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/tree.png",
        hover_image_path="Assets/Resources/Dark/tree.png"
    )

    stone_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 140,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/stone.png",
        hover_image_path="Assets/Resources/Dark/stone.png"
    )

    copper_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 10,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/copper.png",
        hover_image_path="Assets/Resources/Dark/copper.png"
    )

    iron_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 120,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/iron.png",
        hover_image_path="Assets/Resources/Dark/iron.png"
    )

    silver_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 250,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/silver.png",
        hover_image_path="Assets/Resources/Dark/silver.png"
    )

    gold_resource_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 + 380,
        user_config.screen_height // 2 + 380,
        button_width,
        button_height,
        image_path="Assets/Resources/Light/gold.png",
        hover_image_path="Assets/Resources/Dark/gold.png"
    )

    select_tool_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 768,
        user_config.screen_height // 2 - 100,
        button_width,
        button_height,
        image_path="Assets/ToolsButtons/Light/select_tool.png",
        hover_image_path="Assets/ToolsButtons/Dark/select_tool.png"
    )

    remove_tool_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 768,
        user_config.screen_height // 2 + 30,
        button_width,
        button_height,
        image_path="Assets/ToolsButtons/Light/remove_tool.png",
        hover_image_path="Assets/ToolsButtons/Dark/remove_tool.png"
    )

    back_tool_button = ui_elements.ImagedButton(
        user_config.screen_width // 2 - button_width // 2 - 768,
        user_config.screen_height // 2 + 160,
        button_width,
        button_height,
        image_path="Assets/ToolsButtons/Light/back_tool.png",
        hover_image_path="Assets/ToolsButtons/Dark/back_tool.png"
    )

    biomes_buttons = (grass_button, mountain_button, water_button, sand_button, snow_button, swamp_button)
    resources_buttons = (food_resource_button, wood_resource_button, stone_resource_button, copper_resource_button, iron_resource_button, silver_resource_button, gold_resource_button)
    flags_buttons = (aqua_flag_button, black_flag_button, blue_flag_button, green_flag_button, orange_flag_button, red_flag_button,white_flag_button, yellow_flag_button)
    tools_buttons = (select_tool_button, remove_tool_button, back_tool_button)
    all_buttons = (*biomes_buttons, *flags_buttons, *resources_buttons, *tools_buttons)
    scenes_objects = (*all_buttons, redactor_type_dropdown, save_map_button, map_name_input_box)

    actions = []

    is_running = True
    minimap_score = 0
    print("Game started")

    while is_running:

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            redactor_type_dropdown.handle_event(event)

            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.KEYDOWN:
                map_name_input_box.handle_event(event)
                if event.key == pygame.K_ESCAPE:
                    is_running = False
                elif event.key == pygame.K_F1:
                    ui.do_show_grid = not ui.do_show_grid
                elif event.key == pygame.K_F2:
                    ui.do_show_minimap = not ui.do_show_minimap
                elif event.key == pygame.K_F4:
                    camera.toggle_edge_scrolling()

                elif event.key == pygame.K_SPACE:
                    if ui.selected_tile:
                        camera.center_on_tile(ui.selected_tile.x, ui.selected_tile.y)

                elif event.key == pygame.K_z:
                    on_select_select_tool(select_tool_button, all_buttons, ui)
                elif event.key == pygame.K_x:
                    on_select_remove_tool(remove_tool_button, all_buttons, ui)
                elif event.key == pygame.K_c:
                    on_select_back_tool(actions, screen, camera)

                elif event.key == pygame.K_TAB:
                    current_option_index = dropdown_options.index(ui.current_section)
                    new_index = {0: 1, 1: 0, 2: 0, 3: 0}
                    ui.current_section = dropdown_options[new_index[current_option_index]]
                    redactor_type_dropdown.selected_index = new_index[current_option_index]

                elif event.key == pygame.K_1:
                    if ui.current_section == "Biomes":
                        mark_only_button(biomes_buttons[0],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "grass"
                        ui.current_tool = "biome"
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[0],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "food"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[0],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "aqua_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_2:
                    if ui.current_section == "Biomes":
                        mark_only_button(biomes_buttons[1],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "mountain"
                        ui.current_tool = "biome"
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[1],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "wood"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[1],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "black_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_3:
                    if ui.current_section == "Biomes":
                        mark_only_button(biomes_buttons[2],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "water"
                        ui.current_tool = "biome"
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[2],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "stone"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[2],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "blue_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_4:
                    if ui.current_section == "Biomes":
                        mark_only_button(biomes_buttons[3],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "sand"
                        ui.current_tool = "biome"
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[3],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "copper"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[3],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "green_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_5:
                    if ui.current_section == "Biomes":
                        mark_only_button(biomes_buttons[4],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "snow"
                        ui.current_tool = "biome"
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[4],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "iron"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[4],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "orange_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_6:
                    if ui.current_section == "Biomes":
                        mark_only_button(biomes_buttons[5],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "swamp"
                        ui.current_tool = "biome"
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[5],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "silver"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[5],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "red_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_7:
                    if ui.current_section == "Resources":
                        mark_only_button(resources_buttons[6],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "gold"
                        ui.current_tool = "resource"
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[6],(*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "white_flag"
                        ui.current_tool = "flag"

                elif event.key == pygame.K_8:
                    if ui.current_section == "Start positions":
                        mark_only_button(flags_buttons[7],
                                         (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                        ui.selected_item = "yellow_flag"
                        ui.current_tool = "flag"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

                    if select_tool_button.is_clicked(mouse_pos, mouse_click):
                        on_select_select_tool(select_tool_button, all_buttons, ui)
                    if remove_tool_button.is_clicked(mouse_pos, mouse_click):
                        on_select_remove_tool(remove_tool_button, all_buttons, ui)
                    if back_tool_button.is_clicked(mouse_pos, mouse_click) and len(actions) > 0:
                        on_select_back_tool(actions, screen, camera)

                    if ui.current_section == "Biomes":
                        for buttn in biomes_buttons:
                            if buttn.is_clicked(mouse_pos, mouse_click):
                                mark_only_button(buttn, (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                                buttons2items = {grass_button: "grass",
                                                 mountain_button: "mountain",
                                                 water_button: "water",
                                                 sand_button: "sand",
                                                 snow_button: "snow",
                                                 swamp_button: "swamp"}
                                ui.selected_item = buttons2items[buttn]
                                ui.current_tool = "biome"

                    elif ui.current_section == "Resources":
                        for buttn in resources_buttons:
                            if buttn.is_clicked(mouse_pos, mouse_click):
                                mark_only_button(buttn, (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                                buttons2items = {food_resource_button: "food",
                                                 wood_resource_button: "wood",
                                                 stone_resource_button: "stone",
                                                 copper_resource_button: "copper",
                                                 iron_resource_button: "iron",
                                                 silver_resource_button: "silver",
                                                 gold_resource_button: "gold"}
                                ui.selected_item = buttons2items[buttn]
                                ui.current_tool = "resource"

                    elif ui.current_section == "Start positions":
                        for buttn in flags_buttons:
                            if buttn.is_clicked(mouse_pos, mouse_click):
                                mark_only_button(buttn, (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
                                buttons2items = {aqua_flag_button: "aqua_flag",
                                                 black_flag_button: "black_flag",
                                                 blue_flag_button: "blue_flag",
                                                 green_flag_button: "green_flag",
                                                 orange_flag_button: "orange_flag",
                                                 red_flag_button: "red_flag",
                                                 white_flag_button: "white_flag",
                                                 yellow_flag_button: "yellow_flag",}
                                ui.selected_item = buttons2items[buttn]
                                ui.current_tool = "flag"

                    if not(any(obj.rect.collidepoint(mouse_pos) for obj in scenes_objects)) and not(redactor_type_dropdown.item_rect.collidepoint(mouse_pos)):
                        tile_x, tile_y = camera.screen_to_world(mouse_x, mouse_y)

                        for y in range(world.height):
                            for x in range(world.width):
                                world.tiles[y][x].selected = False

                        tile = world.get_tile_by_cords(tile_x, tile_y)
                        if tile:
                            tile.selected = True
                            ui.update_selected_tile(tile)
                            print(f"Tile: ({tile.x}, {tile.y}) - {tile.type}")

                            if ui.current_tool == "tool" and ui.selected_item:
                                if ui.selected_item == "remove_tool":
                                    tile_before_act = copy.deepcopy(tile)
                                    clear_tile(tile, world, screen, camera)
                                    if not is_tiles_same(tile_before_act, tile):
                                        actions.append({"before": tile_before_act, "after": tile})


                            if (ui.current_section == "Biomes") and ui.selected_item and ui.current_tool == "biome":
                                biome = ui.selected_item
                                if biome != "water" or tile.stored_flag is None:
                                    tile_before_act = copy.deepcopy(tile)
                                    tile.type = biome
                                    if tile.type == "water":
                                        tile.stored_resource = None
                                    if not is_tiles_same(tile_before_act, tile):
                                        actions.append({"before": tile_before_act, "after": tile})
                                    tile.draw(screen, camera)

                            elif (ui.current_section == "Resources") and ui.selected_item and ui.current_tool == "resource":
                                resource = ui.selected_item
                                if not tile.stored_flag:
                                    tile_before_act = copy.deepcopy(tile)
                                    tile.stored_resource = resource
                                    if not is_tiles_same(tile_before_act, tile):
                                        actions.append({"before": tile_before_act, "after": tile})
                                    tile.draw(screen, camera)

                            elif (ui.current_section == "Start positions") and ui.selected_item and ui.current_tool == "flag":
                                flag = ui.selected_item
                                if not tile.stored_resource:
                                    tile_before_act = copy.deepcopy(tile)
                                    if world.flags_tiles[flag] is not None:
                                        world.flags_tiles[flag].stored_flag = None
                                    world.flags_tiles[flag] = tile
                                    tile.stored_flag = flag
                                    if not is_tiles_same(tile_before_act, tile):
                                        actions.append({"before": tile_before_act, "after": tile})
                                    tile.draw(screen, camera)

                elif event.button == 4 or event.button == 5:
                    redactor_type_dropdown.handle_event(event)
            elif event.type == pygame.MOUSEWHEEL:
                camera.handle_event(event)

        if not map_name_input_box.active:
            camera.update_with_mouse(mouse_x, mouse_y)
            camera.update_with_keyboard(keys)
        camera.update()

        screen.fill(BLACK)
        world.draw(screen, camera)

        minimap_score += 1
        if minimap_score == 60:
            minimap_score = 0
            terrain_map = ui.map_saver.code_maps(world.tiles)["terrain_map"]
            ui.minimap_former.do_pipeline(terrain_map)
        ui.draw(screen, camera)

        redactor_type_dropdown.draw(screen)

        ui.current_section = redactor_type_dropdown.get_selected_option()
        map_name_input_box.active = False

        if ui.current_section == "Biomes":
            for button in (*biomes_buttons, *tools_buttons):
                button.check_hover(mouse_pos)
                button.draw(screen)

        elif ui.current_section == "Resources":
            for button in (*resources_buttons, *tools_buttons):
                button.check_hover(mouse_pos)
                button.draw(screen)

        elif ui.current_section == "Start positions":
            for button in (*flags_buttons, *tools_buttons):
                button.check_hover(mouse_pos)
                button.draw(screen)

        elif ui.current_section == "Save map":
            map_name_input_box.active = True
            save_map_button.draw(screen)
            map_name_input_box.draw(screen)


        fps_text = ui.small_font.render(f"FPS: {int(clock.get_fps())}", True, GREEN)
        screen.blit(fps_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print("\nGame over")