import pygame

from config import user_config
from start_empty_map import Camera
from tile import Tile


class MinimapManager:
    def __init__(self, tile_map: list[list[Tile]], width: int = 320, height: int = 220, margin: int = 12, inner_padding: int = 4) -> None:
        self.tile_map: list[list[Tile]] = tile_map
        self.width: int = width
        self.height: int = height
        self.margin: int = margin
        self.inner_padding: int = inner_padding
        self.screen_width: int = user_config.screen_width
        self.screen_height: int = user_config.screen_height
        self.tile_size: int = 64
        self.view_rect_color: tuple[int, int, int] = (220, 220, 255)
        self.view_rect_fill: tuple[int, int, int, int] = (180, 180, 255, 60)
        self.colors: dict = {
            "grass": (34, 139, 34),
            "forest": (0, 100, 0),
            "mountain": (139, 137, 137),
            "water": (30, 144, 255),
            "sand": (238, 214, 175),
            "snow": (245, 245, 245),
            "swamp": (0, 60, 30),
        }
        self.map_area_width: int = width - inner_padding * 2
        self.map_area_height: int = height - inner_padding * 2
        self.surface: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.background_color: tuple[int, int, int, int] = (16, 16, 24, 190)
        self.dirty: bool = True

        self.map_width_tiles: int = 0
        self.map_height_tiles: int = 0
        self.scale: float = 1.0
        self.minimap_map_w: float = 0.0
        self.minimap_map_h: float = 0.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0

        self._update_map_size()

    def _update_map_size(self) -> None:
        if not self.tile_map or not self.tile_map[0]:
            self.map_width_tiles = 0
            self.map_height_tiles = 0
            self.scale = 1.0
            return

        self.map_width_tiles = len(self.tile_map[0])
        self.map_height_tiles = len(self.tile_map)

        world_w = self.map_width_tiles * self.tile_size
        world_h = self.map_height_tiles * self.tile_size

        if world_w <= 0 or world_h <= 0:
            self.scale = 1.0
            return

        self.scale = min(
            self.map_area_width / world_w,
            self.map_area_height / world_h
        )

        self.minimap_map_w = world_w * self.scale
        self.minimap_map_h = world_h * self.scale

        self.offset_x = self.inner_padding + (self.map_area_width - self.minimap_map_w) / 2
        self.offset_y = self.inner_padding + (self.map_area_height - self.minimap_map_h) / 2

    def world_to_minimap(self, world_x: float, world_y: float) -> tuple[float, float]:
        mx = self.offset_x + world_x * self.scale
        my = self.offset_y + world_y * self.scale
        return mx, my

    def minimap_to_world(self, mx: float, my: float) -> tuple[float, float]:
        if self.scale <= 0:
            return 0.0, 0.0
        wx = (mx - self.offset_x) / self.scale
        wy = (my - self.offset_y) / self.scale
        return wx, wy

    def update(self, tiles_to_update: list[Tile]) -> None:
        if len(tiles_to_update) > 0:
            for tile in tiles_to_update:
                self.tile_map[tile.y][tile.x] = tile
            self._update_map_size()
            self.dirty = True
        else:
            self.dirty = False

    def redraw(self) -> None:
        self.surface.fill(self.background_color)
        if not self.tile_map:
            self.dirty = False
            return
        tile_size_minimap = max(1, int(self.tile_size * self.scale))
        for row in self.tile_map:
            for tile in row:
                wx = tile.x * self.tile_size
                wy = tile.y * self.tile_size
                mx, my = self.world_to_minimap(wx, wy)
                rect = pygame.Rect(
                    int(mx),
                    int(my),
                    tile_size_minimap,
                    tile_size_minimap
                )
                color = self.colors.get(tile.type, (200, 100, 200))
                pygame.draw.rect(self.surface, color, rect)
        self.dirty = False

    def draw(self, screen: pygame.Surface, camera: Camera) -> None:
        if self.dirty:
            self.redraw()

        pos_x = (self.screen_width - self.width) // 2
        pos_y = (self.screen_height - self.height) // 2

        screen.blit(self.surface, (pos_x, pos_y))

        cam_wx = camera.x
        cam_wy = camera.y
        cam_ww = self.screen_width / camera.zoom
        cam_wh = self.screen_height / camera.zoom

        lt_x, lt_y = self.world_to_minimap(cam_wx, cam_wy)
        rb_x, rb_y = self.world_to_minimap(cam_wx + cam_ww, cam_wy + cam_wh)

        view_rect = pygame.Rect(
            pos_x + lt_x,
            pos_y + lt_y,
            rb_x - lt_x,
            rb_y - lt_y
        )

        if view_rect.width > 2 and view_rect.height > 2:
            fill_surf = pygame.Surface((view_rect.width, view_rect.height), pygame.SRCALPHA)
            fill_surf.fill(self.view_rect_fill)
            screen.blit(fill_surf, (view_rect.x, view_rect.y))

        pygame.draw.rect(screen, self.view_rect_color, view_rect, width=2)

    def handle_click(self, mouse_pos: tuple[int, int], camera: Camera) -> bool:
        pos_x = (self.screen_width - self.width) // 2
        pos_y = (self.screen_height - self.height) // 2

        mx = mouse_pos[0] - pos_x
        my = mouse_pos[1] - pos_y

        if not (0 <= mx <= self.width and 0 <= my <= self.height):
            return False

        mx = max(self.offset_x, min(mx, int(self.offset_x + self.minimap_map_w)))
        my = max(self.offset_y, min(my, int(self.offset_y + self.minimap_map_h)))

        world_x, world_y = self.minimap_to_world(mx, my)

        vis_w = self.screen_width / camera.zoom
        vis_h = self.screen_height / camera.zoom
        camera.x = world_x - vis_w / 2
        camera.y = world_y - vis_h / 2

        return True