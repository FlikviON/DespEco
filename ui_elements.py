import pygame
from dataclasses import dataclass
from pathlib import Path

from config import user_config


if not pygame.get_init():
    pygame.init()


@dataclass
class Colors:
    white: tuple[int, int, int] = (255, 255, 255)
    black: tuple[int, int, int] = (0, 0, 0)

    gray: tuple[int, int, int] = (200, 200, 200)
    gray1: tuple[int, int, int] = (100, 100, 100)
    light_gray: tuple[int, int, int] = (220, 220, 220)
    lighter_gray: tuple[int, int, int] = (211, 211, 211)
    dark_gray: tuple[int, int, int] = (169, 169, 169)
    dark_gray1: tuple[int, int, int] = (50, 50, 50)

    green: tuple[int, int, int] = (0, 255, 0)
    light_green: tuple[int, int, int] = (100, 255, 100)
    light_green1: tuple[int, int, int] = (152, 251, 152)
    light_green2: tuple[int, int, int] = (118, 212, 118)
    dark_green: tuple[int, int, int] = (0, 100, 0)

    dark_golden: tuple[int, int, int] = (184, 134, 11)

    blue: tuple[int, int, int] = (100, 150, 255)
    blue1: tuple[int, int, int] = (0, 0, 255)
    hover_blue: tuple[int, int, int] = (80, 130, 235)

    red: tuple[int, int, int] = (255, 100, 100)
    red1: tuple[int, int, int] = (255, 0, 0)
    hover_red: tuple[int, int, int] = (235, 80, 80)
    dark_red: tuple[int, int, int] = (255, 0, 0)

    yellow: tuple[int, int, int] = (255, 255, 0)

    grass_color: tuple[int, int, int] = (34, 139, 34)
    grass_darker_color: tuple[int, int, int] = (14, 119, 14)
    forest_color: tuple[int, int, int] = (0, 100, 0)
    forest_darker_color: tuple[int, int, int] = (0, 80, 0)
    mountain_color: tuple[int, int, int] = (139, 137, 137)
    mountain_darker_color: tuple[int, int, int] = (119, 117, 117)
    water_color: tuple[int, int, int] = (30, 144, 255)
    water_darker_color: tuple[int, int, int] = (10, 124, 235)
    sand_color: tuple[int, int, int] = (238, 214, 175)
    sand_darker_color: tuple[int, int, int] = (218, 194, 155)
    snow_color: tuple[int, int, int] = (255, 250, 250)
    snow_darker_color: tuple[int, int, int] = (235, 230, 230)
    swamp_color: tuple[int, int, int] = (0, 60, 30)
    swamp_darker_color: tuple[int, int, int] = (0, 40, 30)


@dataclass
class Fonts:
    font1 = pygame.font.SysFont('tahoma', 32, bold = True)
    font2 = pygame.font.SysFont('tahoma', 22, bold = True)
    title_font = pygame.font.SysFont('tahoma', 90, bold=True)


class Button:
    def __init__(self, x: float, y: float, width: float, height: float, text: str,
                 color: tuple[int, int, int], hover_color: tuple[int, int, int]) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.text: str = text
        self.color: tuple[int, int, int] = color
        self.hover_color: tuple[int, int, int] = hover_color
        self.is_hovered: bool = False

    def draw(self, screen: pygame.Surface) -> None:
        color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, Colors.black, self.rect, 2, border_radius=12)

        text_surface = Fonts.font1.render(self.text, True, Colors.black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos: tuple[int, int]) -> bool:
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos: tuple[int, int], click: bool) -> bool:
        return self.rect.collidepoint(pos) and click


class ImagedButton:
    def __init__(self, x: float, y: float, width: float, height: float,
                 image_path: str = None,
                 hover_image_path: str = None) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.is_hovered: bool = False
        self.border_color: tuple[int, int, int] = Colors.black

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width - 10, height - 10))
        self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
        self.hover_image = pygame.transform.scale(self.hover_image, (width - 10, height - 10))
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.border_color, self.rect)
        screen.blit(self.image if not self.is_hovered else self.hover_image, self.image_rect)

    def check_hover(self, pos: tuple[int, int]) -> bool:
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos: tuple[int, int], click: bool) -> bool:
        return self.rect.collidepoint(pos) and click


class MenuBackground:
    @staticmethod
    def load_background_image() -> pygame.Surface:
        background_image_path = Path("Assets/Images/background_image.png")
        background = pygame.image.load(background_image_path).convert()
        background = pygame.transform.scale(background, (user_config.screen_width, user_config.screen_height))
        return background

    @staticmethod
    def create_dark_overlay(screen: pygame.Surface, alpha: int=128):
        overlay = pygame.Surface((user_config.screen_width, user_config.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))
        return screen


class InputBox:
    def __init__(self, x: float, y: float, width: float, height: float, label: str="", font_size: int=28, max_length: int=10) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.label: str = label
        self.text: str = ""
        self.font: pygame.Font = pygame.font.Font(None, font_size)
        self.label_font: pygame.Font = pygame.font.Font(None, font_size - 4)
        self.active: bool = False
        self.max_length: int = max_length

        self.color: tuple[int, int, int] = Colors.light_gray
        self.active_color: tuple[int, int, int] = Colors.blue
        self.text_color: tuple[int, int, int] = Colors.black

        self.cursor_visible: bool = True
        self.cursor_timer: float = 0

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()
            else:
                self.active = False

            self.color = self.active_color if self.active else Colors.light_gray

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_TAB:
                pass
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def update(self) -> None:
        current_time = pygame.time.get_ticks()
        if self.active and current_time - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time

    def draw(self, screen: pygame.Surface) -> None:
        label_surface = self.label_font.render(self.label, True, Colors.white)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 30))

        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        pygame.draw.rect(screen, Colors.white,
                         (self.rect.x + 2, self.rect.y + 2,
                          self.rect.width - 4, self.rect.height - 4),
                         border_radius=3)

        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + text_surface.get_width()
            cursor_y1 = self.rect.y + 10
            cursor_y2 = self.rect.y + self.rect.height - 10
            pygame.draw.line(screen, Colors.black,
                             (cursor_x, cursor_y1),
                             (cursor_x, cursor_y2), 2)

    def get_value(self) -> int:
        """Get the number from Input Box"""
        if self.text:
            try:
                return int(self.text)
            except ValueError:
                return 0
        return 0

    def is_empty(self) -> bool:
        return len(self.text) == 0


class Dropdown:
    def __init__(self, x: float, y: float, width: float, height: float, options: list, default_index: int=3, font_size: int=32, visible_items: int=5) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.item_rect: pygame.Rect = pygame.Rect(x, y + height * 4, width, height)
        self.options: list = options
        self.selected_index: int = default_index
        self.is_open: bool = False
        self.font: pygame.Font = pygame.font.Font(None, font_size)

        self.visible_items: int = visible_items
        self.scroll_offset: int = 0
        self.max_scroll: int = max(0, len(options) - visible_items)

        self.scrollbar_width: int = 12
        self.scrollbar_rect: pygame.Rect | None = None
        self.is_dragging_scrollbar: bool = False
        self.drag_start_y: float = 0
        self.drag_start_scroll: float = 0

        self.item_height: float = height
        self.bg_color: tuple[int, int, int] = Colors.light_green1
        self.hover_color: tuple[int, int, int] = Colors.light_green2
        self.border_color: tuple[int, int, int] = Colors.dark_gray
        self.text_color: tuple[int, int, int] = Colors.black
        self.active_border_color: tuple[int, int, int] = Colors.dark_green
        self.scrollbar_color: tuple[int, int, int] = Colors.dark_gray
        self.scrollbar_hover_color: tuple[int, int, int] = Colors.gray

    def handle_event(self, event: pygame.Event) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(mouse_pos):
                    self.is_open = not self.is_open
                    return True

                elif self.is_open:
                    visible_options = self.get_visible_options()
                    for i, option in enumerate(visible_options):
                        global_index = i + self.scroll_offset
                        item_rect = pygame.Rect(
                            self.rect.x,
                            self.rect.y + self.rect.height * (i + 1),
                            self.rect.width - (self.scrollbar_width if len(self.options) > self.visible_items else 0),
                            self.rect.height
                        )
                        self.item_rect = item_rect
                        if item_rect.collidepoint(mouse_pos):
                            self.selected_index = global_index
                            self.is_open = False
                            self.scroll_offset = 0
                            return True

                    if self.scrollbar_rect and self.scrollbar_rect.collidepoint(mouse_pos):
                        self.is_dragging_scrollbar = True
                        self.drag_start_y = mouse_pos[1]
                        self.drag_start_scroll = self.scroll_offset
                        return True

                    dropdown_area = pygame.Rect(
                        self.rect.x,
                        self.rect.y + self.rect.height,
                        self.rect.width,
                        self.rect.height * self.visible_items
                    )
                    if dropdown_area.collidepoint(mouse_pos):
                        return True

                    self.is_open = False
                    return False

            elif event.button == 4:
                if self.is_open and len(self.options) > self.visible_items:
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    return True

            elif event.button == 5:
                if self.is_open and len(self.options) > self.visible_items:
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + 1)
                    return True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging_scrollbar:
                delta_y = mouse_pos[1] - self.drag_start_y
                total_dropdown_height = self.rect.height * self.visible_items

                if total_dropdown_height > 0 and self.max_scroll > 0:
                    scroll_ratio = delta_y / total_dropdown_height
                    new_offset = self.drag_start_scroll + int(scroll_ratio * self.max_scroll)
                    self.scroll_offset = max(0, min(self.max_scroll, new_offset))

        return False

    def get_visible_options(self) -> list :
        """Returns only currently visible options"""
        end_index = min(self.scroll_offset + self.visible_items, len(self.options))
        return self.options[self.scroll_offset:end_index]

    def update_scrollbar(self, dropdown_height: float) -> None:
        """Updates scrollbar's position and size"""
        if len(self.options) <= self.visible_items:
            self.scrollbar_rect = None
            return

        visible_ratio = self.visible_items / len(self.options)
        scrollbar_height = max(20, int(dropdown_height * visible_ratio))

        if self.max_scroll > 0:
            scroll_ratio = self.scroll_offset / self.max_scroll
        else:
            scroll_ratio = 0

        scrollable_height = dropdown_height - scrollbar_height
        scrollbar_y = self.rect.y + self.rect.height + (scroll_ratio * scrollable_height)

        self.scrollbar_rect = pygame.Rect(
            self.rect.right - self.scrollbar_width - 2,
            scrollbar_y,
            self.scrollbar_width,
            scrollbar_height
        )

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)

        if self.is_open:
            pygame.draw.rect(screen, self.active_border_color, self.rect, 2, border_radius=5)

        selected_text = self.font.render(
            self.options[self.selected_index],
            True,
            self.text_color
        )
        text_rect = selected_text.get_rect(center=self.rect.center)
        screen.blit(selected_text, text_rect)

        arrow_size = 10
        arrow_x = self.rect.right - 20
        arrow_y = self.rect.centery

        if self.is_open:
            points = [
                (arrow_x, arrow_y - arrow_size // 2),
                (arrow_x - arrow_size, arrow_y + arrow_size // 2),
                (arrow_x + arrow_size, arrow_y + arrow_size // 2)
            ]
        else:
            points = [
                (arrow_x, arrow_y + arrow_size // 2),
                (arrow_x - arrow_size, arrow_y - arrow_size // 2),
                (arrow_x + arrow_size, arrow_y - arrow_size // 2)
            ]

        pygame.draw.polygon(screen, self.text_color, points)

        if self.is_open:
            dropdown_height = self.rect.height * self.visible_items

            dropdown_container = pygame.Rect(
                self.rect.x,
                self.rect.y + self.rect.height + 2,
                self.rect.width,
                dropdown_height
            )
            pygame.draw.rect(screen, Colors.white, dropdown_container)
            pygame.draw.rect(screen, self.border_color, dropdown_container, 2, border_radius=5)

            self.update_scrollbar(dropdown_height)

            visible_options = self.get_visible_options()
            mouse_pos = pygame.mouse.get_pos()

            for i, option in enumerate(visible_options):
                global_index = i + self.scroll_offset

                item_width = self.rect.width
                if len(self.options) > self.visible_items:
                    item_width -= self.scrollbar_width

                item_rect = pygame.Rect(
                    self.rect.x,
                    self.rect.y + self.rect.height * (i + 1),
                    item_width,
                    self.rect.height
                )

                bg_color = self.hover_color if item_rect.collidepoint(mouse_pos) else self.bg_color

                pygame.draw.rect(screen, bg_color, item_rect, border_radius=5)
                pygame.draw.rect(screen, self.border_color, item_rect, 1, border_radius=5)

                if global_index == self.selected_index:
                    pygame.draw.rect(screen, Colors.dark_green, item_rect, 2, border_radius=5)

                text = self.font.render(option, True, self.text_color)
                text_rect = text.get_rect(center=item_rect.center)
                screen.blit(text, text_rect)

            if self.scrollbar_rect:
                is_hovering = self.scrollbar_rect.collidepoint(mouse_pos)
                scrollbar_color = self.scrollbar_hover_color if (
                            is_hovering or self.is_dragging_scrollbar) else self.scrollbar_color

                pygame.draw.rect(screen, scrollbar_color, self.scrollbar_rect, border_radius=6)
                pygame.draw.rect(screen, self.border_color, self.scrollbar_rect, 1, border_radius=6)

    def get_selected_option(self) -> str:
        return self.options[self.selected_index]

    def get_selected_index(self) -> int:
        return self.selected_index

    def get_selected_value(self) -> int:
        selected_option = self.get_selected_option()
        try:
            return int(selected_option.split("x")[0])
        except ValueError:
            return 64
