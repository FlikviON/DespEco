import os
import pygame
import math
from config import user_config


SCREEN_WIDTH = user_config.screen_width
SCREEN_HEIGHT = user_config.screen_height
TILE_SIZE = 64

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DARK_GRAY = (50, 50, 50)

COLORS = {
    "grass": (34, 139, 34),
    "forest": (0, 100, 0),
    "mountain": (139, 137, 137),
    "water": (30, 144, 255),
    "sand": (238, 214, 175),
    "snow": (255, 250, 250),
    "swamp": (0, 60, 30),
}

TEXTURES = {
    "grass": "Assets/Tiles/Light/grass.png",
    "mountain": "Assets/Tiles/Light/mountain.png",
    "water": "Assets/Tiles/Light/water.png",
    "sand": "Assets/Tiles/Light/sand.png",
    "snow": "Assets/Tiles/Light/snow.png",
    "swamp": "Assets/Tiles/Light/swamp.png",
}


_BASE_TEXTURES: dict[str, pygame.Surface] = {}
_SCALED_TEXTURES: dict[tuple[str, int], pygame.Surface] = {}


def _load_texture(path: str) -> pygame.Surface:
    if path in _BASE_TEXTURES:
        return _BASE_TEXTURES[path]

    if not os.path.exists(path):
        raise Exception(f"Texture not found: {path}")

    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

    _BASE_TEXTURES[path] = img
    return img


def _get_scaled_texture(path: str, size: int) -> pygame.Surface:
    size = max(1, int(size))
    key = (path, size)

    if key in _SCALED_TEXTURES:
        return _SCALED_TEXTURES[key]

    base = _load_texture(path)
    scaled = pygame.transform.scale(base, (size, size))

    _SCALED_TEXTURES[key] = scaled
    return scaled


class Tile:
    def __init__(self, x: int, y: int,
                 tile_type: str = "grass",
                 stored_resource: str | None = None,
                 stored_flag: str | None = None) -> None:
        self.x: int = x
        self.y: int = y
        self.type: str = tile_type
        self.stored_resource: str | None = stored_resource
        self.stored_flag: str | None = stored_flag

        self.passable: bool = True
        self.buildable: bool = True

        self.selected: bool = False
        self.highlighted: bool = False
        self.visible: bool = True

        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        self._set_properties()

    def _set_properties(self) -> None:
        properties = {
            "grass": {"passable": True, "buildable": True},
            "mountain": {"passable": True, "buildable": True},
            "water": {"passable": False, "buildable": False},
            "sand": {"passable": True, "buildable": True},
            "snow": {"passable": True, "buildable": True},
            "swamp": {"passable": True, "buildable": True},
        }

        if self.type not in properties:
            self.type = "grass"

        self.passable = properties[self.type]["passable"]
        self.buildable = properties[self.type]["buildable"]

    def get_color(self) -> tuple[int, int, int]:
        base_color = COLORS.get(self.type, WHITE)

        if self.selected:
            return (
                min(255, base_color[0] + 60),
                min(255, base_color[1] + 60),
                min(255, base_color[2] + 60),
            )

        if self.highlighted:
            return (
                int(base_color[0] * 0.6 + 255 * 0.4),
                int(base_color[1] * 0.6 + 255 * 0.4),
                int(base_color[2] * 0.6),
            )

        if not self.visible:
            return DARK_GRAY

        return base_color

    def draw(self, surface: pygame.Surface, camera: "Camera") -> None:
        world_left = self.x * TILE_SIZE
        world_top = self.y * TILE_SIZE
        world_right = world_left + TILE_SIZE
        world_bottom = world_top + TILE_SIZE

        screen_left = int(math.floor((world_left - camera.x) * camera.zoom))
        screen_top = int(math.floor((world_top - camera.y) * camera.zoom))
        screen_right = int(math.ceil((world_right - camera.x) * camera.zoom))
        screen_bottom = int(math.ceil((world_bottom - camera.y) * camera.zoom))

        screen_w = screen_right - screen_left
        screen_h = screen_bottom - screen_top

        if screen_w <= 0 or screen_h <= 0:
            return

        if (screen_right < 0 or screen_left > SCREEN_WIDTH or
                screen_bottom < 0 or screen_top > SCREEN_HEIGHT):
            return

        tile_rect = pygame.Rect(screen_left, screen_top, screen_w, screen_h)
        if self.stored_flag and self.type != "water":
            row_texture = f"Assets/TilesWithFlags/{self.type}_with_{self.stored_flag}.png"
        elif self.stored_resource:
            tile_type2resource = {"food": {"grass": "wheat", "mountain": "deer", "sand": "сactus", "snow": "wheat", "swamp": "berries", "water": None},
                 "wood": {"grass": "tree", "mountain": "tree", "sand": "tree", "snow": "tree", "swamp": "tree", "water": None},
                 "stone": {"grass": "stone", "mountain": "stone", "sand": "stone", "snow": "stone", "swamp": "stone", "water": None},
                 "copper": {"grass": "copper", "mountain": "copper", "sand": "copper", "snow": "copper", "swamp": "copper", "water": None},
                 "iron": {"grass": "iron", "mountain": "iron", "sand": "iron", "snow": "iron", "swamp": "iron", "water": None},
                 "silver": {"grass": "silver", "mountain": None, "sand": "silver", "snow": "silver", "swamp": "silver", "water": None},
                 "gold": {"grass": "gold", "mountain": "gold", "sand": "gold", "snow": "gold", "swamp": "gold", "water": None}}
            view = tile_type2resource[self.stored_resource][self.type]
            if view is None:
                row_texture = TEXTURES[self.type]
            else:
                row_texture = f"Assets/TilesWithResources/{self.type}_with_{view}.png"
        else:
            row_texture = TEXTURES[self.type]

        texture = _get_scaled_texture(row_texture, screen_w)
        surface.blit(texture, (screen_left, screen_top))

        if self.selected:
            pygame.draw.rect(surface, YELLOW, tile_rect, max(1, int(3 * camera.zoom)))

    def __str__(self) -> str:
        return f"Tile({self.x}, {self.y}, {self.type})"
