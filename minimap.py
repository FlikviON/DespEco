from typing import List, Tuple

import pygame

from config import user_config
from tile import Tile

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

import pygame
from typing import List, Tuple

class Minimap:
    """
    Класс для отображения миникарты игрового мира.
    Миникарта рисуется в правом нижнем углу экрана.
    """

    def __init__(self, tile_map: List[List[Tile]], width: int = 300, height: int = 200):
        """
        :param tile_map: двумерный список объектов Tile
        :param width: ширина миникарты в пикселях (по умолчанию 300)
        :param height: высота миникарты в пикселях (по умолчанию 200)
        """
        self.tile_map = tile_map
        self.width = width
        self.height = height

        # Размеры карты в тайлах
        self.map_width_tiles = len(tile_map[0]) if tile_map else 0
        self.map_height_tiles = len(tile_map) if tile_map else 0

        # Размеры карты в мировых координатах (пикселях)
        self.map_world_width = self.map_width_tiles * TILE_SIZE
        self.map_world_height = self.map_height_tiles * TILE_SIZE

        # Масштаб: во сколько раз уменьшаем карту, чтобы она поместилась в область миникарты
        self.scale = min(width / self.map_world_width, height / self.map_world_height)

        # Реальные размеры карты на миникарте (после масштабирования)
        self.minimap_map_width = self.map_world_width * self.scale
        self.minimap_map_height = self.map_world_height * self.scale

        # Смещение внутри поверхности миникарты, чтобы карта была по центру
        # (если пропорции не совпадают, остаются поля)
        self.offset_x = (width - self.minimap_map_width) / 2
        self.offset_y = (height - self.minimap_map_height) / 2

        # Поверхность, на которой рисуется миникарта
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)

        self.background_color = (0, 0, 0, 180)  # ярко-красный

        self.dirty = True

    def world_to_minimap(self, world_x: float, world_y: float) -> Tuple[float, float]:
        """
        Преобразует мировые координаты (в пикселях) в координаты на поверхности миникарты.
        """
        minimap_x = self.offset_x + world_x * self.scale
        minimap_y = self.offset_y + world_y * self.scale
        return minimap_x, minimap_y

    def minimap_to_world(self, minimap_x: float, minimap_y: float) -> Tuple[float, float]:
        """
        Преобразует координаты на миникарте в мировые координаты (пиксели).
        Может использоваться для обработки кликов по миникарте.
        """
        world_x = (minimap_x - self.offset_x) / self.scale
        world_y = (minimap_y - self.offset_y) / self.scale
        return world_x, world_y

    def update(self, tile_map: List[List[Tile]] = None):
        if tile_map is not None:
            self.tile_map = tile_map
            self.map_width_tiles = len(tile_map[0]) if tile_map else 0
            self.map_height_tiles = len(tile_map) if tile_map else 0
            self.map_world_width = self.map_width_tiles * TILE_SIZE
            self.map_world_height = self.map_height_tiles * TILE_SIZE
            self.scale = min(self.width / self.map_world_width, self.height / self.map_world_height)
            self.minimap_map_width = self.map_world_width * self.scale
            self.minimap_map_height = self.map_world_height * self.scale
            self.offset_x = (self.width - self.minimap_map_width) / 2
            self.offset_y = (self.height - self.minimap_map_height) / 2
        self.dirty = True

    def _draw_map(self):
        self.surface.fill(self.background_color)

        for row in self.tile_map:
            for tile in row:
                world_x = tile.x * TILE_SIZE
                world_y = tile.y * TILE_SIZE

                minimap_x, minimap_y = self.world_to_minimap(world_x, world_y)

                tile_size_minimap = TILE_SIZE * self.scale

                color = COLORS.get(tile.type, WHITE)

                rect = pygame.Rect(
                    int(minimap_x),
                    int(minimap_y),
                    max(1, int(tile_size_minimap)),
                    max(1, int(tile_size_minimap))
                )
                pygame.draw.rect(self.surface, color, rect)

        self.dirty = False

    def draw(self, screen: pygame.Surface, camera):
        if self.dirty:
            self._draw_map()

        margin = 10
        pos_x = SCREEN_WIDTH - self.width - margin
        pos_y = SCREEN_HEIGHT - self.height - margin
        screen.blit(self.surface, (pos_x, pos_y))

        cam_world_x = camera.x
        cam_world_y = camera.y
        cam_world_width = SCREEN_WIDTH / camera.zoom
        cam_world_height = SCREEN_HEIGHT / camera.zoom

        left_top = self.world_to_minimap(cam_world_x, cam_world_y)
        right_bottom = self.world_to_minimap(
            cam_world_x + cam_world_width,
            cam_world_y + cam_world_height
        )

        view_rect = pygame.Rect(
            left_top[0],
            left_top[1],
            right_bottom[0] - left_top[0],
            right_bottom[1] - left_top[1]
        )

        pygame.draw.rect(screen, (255, 255, 255), view_rect, 2)