import pygame


pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 1000
TILE_SIZE = 64

WORLD_WIDTH = 400
WORLD_HEIGHT = 400

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


class Tile:
    def __init__(self, x: int, y: int, tile_type: str = "grass") -> None:
        self.x: int = x
        self.y: int = y

        self.type: str = tile_type

        self.passable: bool = True
        self.buildable: bool = True
        self.resources: dict = {}
        self.defense_bonus: int = 0

        self.selected: bool = False
        self.highlighted: bool = False
        self.visible: bool = True

        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        self._set_properties()

    def _set_properties(self) -> None:
        """Sets tile's properties by its type"""
        properties = {
                      "grass": {"passable": True, "buildable": True, "defense_bonus": 0},
                      "forest": {"passable": True, "buildable": True, "defense_bonus": 1},
                      "mountain": {"passable": False, "buildable": False, "defense_bonus": 3},
                      "water": {"passable": False, "buildable": False, "defense_bonus": 0},
                      "sand": {"passable": True, "buildable": True, "defense_bonus": -1},
                      "snow": {"passable": True, "buildable": False, "defense_bonus": 1},
                      "swamp": {"passable": True, "buildable": False, "defense_bonus": -2},
                      "rock": {"passable": False, "buildable": False, "defense_bonus": 2}
                      }

        self.passable = properties[self.type]["passable"]
        self.buildable = properties[self.type]["buildable"]
        self.defense_bonus = properties[self.type]["defense_bonus"]

    def get_color(self) -> tuple[int, int, int]:
        base_color = COLORS.get(self.type, WHITE)

        if self.selected:
            r = min(255, base_color[0] + 60)
            g = min(255, base_color[1] + 60)
            b = min(255, base_color[2] + 60)
            return r, g, b

        elif self.highlighted:
            r = int(base_color[0] * 0.6 + 255 * 0.4)
            g = int(base_color[1] * 0.6 + 255 * 0.4)
            b = int(base_color[2] * 0.6)
            return r, g, b

        elif not self.visible:
            return DARK_GRAY

        else:
            return base_color

    def draw(self, surface: pygame.Surface, camera: 'Camera', is_show_grid: bool = True) -> None:
        """Draws tile on map"""
        screen_x = int((self.x * TILE_SIZE - camera.x) * camera.zoom)
        screen_y = int((self.y * TILE_SIZE - camera.y) * camera.zoom)
        screen_size = int(TILE_SIZE * camera.zoom)

        if (screen_x + screen_size < 0 or screen_x > SCREEN_WIDTH or
                screen_y + screen_size < 0 or screen_y > SCREEN_HEIGHT):
            return

        color = self.get_color()
        tile_rect = pygame.Rect(screen_x, screen_y, screen_size, screen_size)
        pygame.draw.rect(surface, color, tile_rect)

        if is_show_grid:
            grid_color = GRAY if self.visible else DARK_GRAY
            pygame.draw.rect(surface, grid_color, tile_rect, 1)

        if self.resources and self.visible:
            resources_colors = {"wood": (139, 69, 19), "stone": (128, 128, 128), "gold": (255, 215, 0), "food": (255, 100, 100)}
            for i, resource in enumerate(self.resources.keys()):
                resource_color = resources_colors.get(resource)
                if resource_color:
                    center_x = screen_x + screen_size // 4 + (i * screen_size // 3)
                    center_y = screen_y + screen_size - screen_size // 4
                    radius = max(2, screen_size // 10)

                    pygame.draw.circle(surface, resource_color,
                                       (center_x, center_y),
                                       radius)

    def __str__(self) -> str:
        return f"Tile({self.x}, {self.y}, {self.type})"


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
    def __init__(self) -> None:
        self.width: int = WORLD_WIDTH
        self.height: int = WORLD_HEIGHT
        self.tiles: list[list[Tile]] = []
        self.generate_world()

    def generate_world(self) -> None:
        print(f"Generation world {self.width}x{self.height}...")
        self.tiles = [Tile(x, y) for x in range(self.width) for y in range(self.height)]
        print("Done")

    def get_tile_by_cords(self, x: int, y: int) -> Tile | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def draw(self, surface: pygame.Surface, camera: Camera, show_grid: bool = True) -> None:
        start_x, start_y, end_x, end_y = camera.get_visible_tiles()
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.get_tile_by_cords(x, y)
                if tile:
                    tile.draw(surface, camera, show_grid)


class UI:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont('Arial', 20)
        self.small_font = pygame.font.SysFont('Arial', 16)
        self.selected_tile: Tile | None = None

    def draw(self, surface: pygame.Surface, camera: Camera, world: World) -> None:
        info_panel = pygame.Surface((320, 170), pygame.SRCALPHA)
        info_panel.fill((0, 0, 0, 200))

        cam_text = f"Камера: ({int(camera.x)}:{int(camera.y)})"
        zoom_text = f"Зум: {camera.zoom:.2f}x"
        world_text = f"Мир: {world.width}x{world.height} тайлов"
        scroll_text = f"Автоскролл: {'ВКЛ' if camera.is_edge_scrolling else 'ВЫКЛ'}"

        texts = [cam_text, zoom_text, world_text, scroll_text]
        y_offset = 10

        for text in texts:
            text_surface = self.font.render(text, True, WHITE)
            info_panel.blit(text_surface, (10, y_offset))
            y_offset += 25

        if self.selected_tile:
            tile = self.selected_tile
            y_offset += 5

            tile_info = [
                f"Tile: ({tile.x}, {tile.y})",
                f"Type: {tile.type}",
                f": {'yes' if tile.passable else 'no'}",
                f"Buildable: {'yes' if tile.buildable else 'no'}",
                f"Resources: {', '.join(tile.resources.keys()) if tile.resources else 'no'}"
            ]

            for info in tile_info:
                text_surface = self.small_font.render(info, True, YELLOW)
                info_panel.blit(text_surface, (10, y_offset))
                y_offset += 20

        if camera.is_edge_scrolling:
            self._draw_scroll_indicator(surface)


    def _draw_scroll_indicator(self, surface: pygame.Surface) -> None:
        margin = SCROLL_MARGIN

        indicator = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        top_rect = pygame.Rect(0, 0, SCREEN_WIDTH, margin)
        pygame.draw.rect(indicator, (255, 255, 0, 30), top_rect)

        bottom_rect = pygame.Rect(0, SCREEN_HEIGHT - margin, SCREEN_WIDTH, margin)
        pygame.draw.rect(indicator, (255, 255, 0, 30), bottom_rect)

        left_rect = pygame.Rect(0, 0, margin, SCREEN_HEIGHT)
        pygame.draw.rect(indicator, (255, 255, 0, 30), left_rect)

        right_rect = pygame.Rect(SCREEN_WIDTH - margin, 0, margin, SCREEN_HEIGHT)
        pygame.draw.rect(indicator, (255, 255, 0, 30), right_rect)

        surface.blit(indicator, (0, 0))

    def update_selected_tile(self, tile: Tile) -> None:
        self.selected_tile = tile


def start_game() -> None:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("DespEco")

    world = World()
    camera = Camera()
    ui = UI()

    clock = pygame.time.Clock()
    show_grid = True
    running = True

    print("Game started")

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F1:
                    show_grid = not show_grid
                    print(f"Сетка: {'ВКЛ' if show_grid else 'ВЫКЛ'}")
                elif event.key == pygame.K_F2:
                    camera.toggle_edge_scrolling()
                    status = "ВКЛЮЧЕН" if camera.is_edge_scrolling else "ВЫКЛЮЧЕН"
                    print(f"Автоматический скролл: {status}")
                elif event.key == pygame.K_SPACE:
                    # Центрировать камеру на выбранном тайле или в центре мира
                    if ui.selected_tile:
                        camera.center_on_tile(ui.selected_tile.x, ui.selected_tile.y)
                        print(f"Камера центрирована на тайле ({ui.selected_tile.x}, {ui.selected_tile.y})")
                    else:
                        camera.x = (WORLD_WIDTH * TILE_SIZE) / 2 - (SCREEN_WIDTH / camera.zoom) / 2
                        camera.y = (WORLD_HEIGHT * TILE_SIZE) / 2 - (SCREEN_HEIGHT / camera.zoom) / 2
                        print("Камера центрирована в центре мира")
                elif event.key == pygame.K_c:
                    # Показать координаты камеры
                    print(f"Камера: x={camera.x:.1f}, y={camera.y:.1f}, zoom={camera.zoom:.2f}")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ - выбор тайла
                    # Получаем координаты тайла
                    tile_x, tile_y = camera.screen_to_world(mouse_x, mouse_y)

                    # Снимаем выделение со всех тайлов
                    for y in range(world.height):
                        for x in range(world.width):
                            world.tiles[y][x].selected = False

                    # Выбираем новый тайл
                    tile = world.get_tile_by_cords(tile_x, tile_y)
                    if tile:
                        tile.selected = True
                        ui.update_selected_tile(tile)
                        print(f"Выбран тайл: ({tile.x}, {tile.y}) - {tile.type}")

            elif event.type == pygame.MOUSEWHEEL:
                # Передаем событие зума камере
                camera.handle_event(event)

        # Обновление камеры на основе положения мыши
        camera.update_with_mouse(mouse_x, mouse_y)

        # Обновление камеры на основе клавиатуры
        camera.update_with_keyboard(keys)

        # Ограничение границ камеры
        camera.update()

        # Отрисовка
        screen.fill(BLACK)

        # Отрисовка мира
        world.draw(screen, camera, show_grid)

        # Отрисовка UI
        ui.draw(screen, camera, world)

        # Отображение FPS
        fps_text = ui.small_font.render(f"FPS: {int(clock.get_fps())}", True, GREEN)
        screen.blit(fps_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 25))

        # Отображение количества видимых тайлов
        start_x, start_y, end_x, end_y = camera.get_visible_tiles()
        visible_tiles = (end_x - start_x) * (end_y - start_y)
        total_tiles = world.width * world.height
        tiles_text = ui.small_font.render(f"Тайлы: {visible_tiles}/{total_tiles}", True, BLUE)
        screen.blit(tiles_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 25))

        tile_x, tile_y = camera.screen_to_world(mouse_x, mouse_y)
        mouse_text = ui.small_font.render(f"Мышь: ({tile_x}, {tile_y})", True, YELLOW)
        screen.blit(mouse_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))

        control_text = ui.small_font.render("WASD + Автоскролл курсором", True, (255, 200, 100))
        screen.blit(control_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    print("\nИгра завершена")