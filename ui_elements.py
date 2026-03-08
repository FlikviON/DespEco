from dataclasses import dataclass
from pathlib import Path

import pygame
import pyperclip

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
    darker_green: tuple[int, int, int] = (0, 200, 0)
    hover_darker_green: tuple[int, int, int] = (0, 180, 0)
    light_green: tuple[int, int, int] = (100, 255, 100)
    light_green1: tuple[int, int, int] = (152, 251, 152)
    light_green2: tuple[int, int, int] = (118, 212, 118)
    dark_green: tuple[int, int, int] = (0, 100, 0)

    dark_golden: tuple[int, int, int] = (184, 134, 11)

    blue: tuple[int, int, int] = (100, 150, 255)
    blue1: tuple[int, int, int] = (0, 0, 255)
    hover_blue: tuple[int, int, int] = (80, 130, 235)
    sky_blue: tuple[int, int, int] = (154, 197, 219)

    red: tuple[int, int, int] = (255, 100, 100)
    red1: tuple[int, int, int] = (255, 0, 0)
    hover_red: tuple[int, int, int] = (235, 80, 80)
    dark_red: tuple[int, int, int] = (255, 0, 0)
    crimson: tuple[int, int, int] = (143, 0, 0)

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
    font1: pygame.font = pygame.font.SysFont('tahoma', 32, bold = True)
    font2: pygame.font = pygame.font.SysFont('tahoma', 22, bold = True)
    font_for_maps_names: pygame.font = pygame.font.SysFont('tahoma', 19, bold = False)
    font_for_maps_delete: pygame.font = pygame.font.SysFont('tahoma', 60, bold=True)
    font_for_labels: pygame.font = pygame.font.SysFont('tahoma', 16, bold=True)
    title_font: pygame.font = pygame.font.SysFont('tahoma', 90, bold=True)


class Button:
    def __init__(self, x: float, y: float, width: float, height: float, text: str,
                 color: tuple[int, int, int], hover_color: tuple[int, int, int],
                 font: pygame.Font = Fonts.font1) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.text: str = text
        self.color: tuple[int, int, int] = color
        self.hover_color: tuple[int, int, int] = hover_color
        self.is_hovered: bool = False
        self.font: pygame.Font = font

    def draw(self, screen: pygame.Surface) -> None:
        color = self.hover_color if self.is_hovered else self.color

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, Colors.black, self.rect, 2, border_radius=12)

        text_surface = self.font.render(self.text, True, Colors.black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, pos: tuple[int, int]) -> bool:
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos: tuple[int, int], click: bool = True) -> bool:
        return self.rect.collidepoint(pos) and click


class ImagedButton:
    def __init__(self, x: float, y: float, width: float, height: float,
                 image_path: str = None,
                 hover_image_path: str = None,
                 do_draw_wrapper: bool = True) -> None:
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.is_hovered: bool = False
        self.do_draw_wrapper = do_draw_wrapper
        self.border_color: tuple[int, int, int] = Colors.black

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width - 10, height - 10))
        self.hover_image = pygame.image.load(hover_image_path).convert_alpha()
        self.hover_image = pygame.transform.scale(self.hover_image, (width - 10, height - 10))
        self.image_rect = self.image.get_rect(center=self.rect.center)

    def draw(self, screen: pygame.Surface) -> None:
        if self.do_draw_wrapper:
            pygame.draw.rect(screen, self.border_color, self.rect)
        screen.blit(self.image if not self.is_hovered else self.hover_image, self.image_rect)

    def check_hover(self, pos: tuple[int, int]) -> bool:
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)


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
    def __init__(self, x: float, y: float, width: float, height: float,
                 label: str = "", font_size: int = 28, max_length: int = 10) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.text = ""
        self.font = pygame.font.Font(None, font_size)
        self.label_font = pygame.font.Font(None, font_size - 4)
        self.active = False
        self.max_length = max_length

        self.color = Colors.light_gray
        self.active_color = Colors.blue
        self.text_color = Colors.black

        self.cursor_visible = True
        self.cursor_timer = 0

        # Для повторения Backspace при зажатии
        self.backspace_pressed = False
        self.backspace_repeat_delay = 400  # мс — первая задержка
        self.backspace_repeat_rate = 35  # мс — интервал между удалениями
        self.last_backspace_time = 0

    def handle_event(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.cursor_visible = True
                self.cursor_timer = pygame.time.get_ticks()
            else:
                self.active = False
            self.color = self.active_color if self.active else Colors.light_gray

        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.backspace_pressed = True
                self.last_backspace_time = pygame.time.get_ticks()
                self._handle_backspace()  # сразу удаляем один символ
            elif event.key == pygame.K_TAB:
                pass
            else:
                if len(self.text) < self.max_length:
                    if event.unicode and (event.unicode.isalnum() or event.unicode in " -_.,@"):
                        self.text += event.unicode

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
            if keys[pygame.K_c]:
                pyperclip.copy(self.text)
            if keys[pygame.K_v]:
                paste = pyperclip.paste()
                for char in paste:
                    if len(self.text) < self.max_length:
                        if char.isalnum() or char in " -_.,@":
                            self.text += char
                    else:
                        break
            if keys[pygame.K_a]:
                self.text = ""  # или можно выделение, но это сложнее

    def _handle_backspace(self):
        """Удаление одного символа или слова при Ctrl"""
        keys = pygame.key.get_pressed()
        ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

        if ctrl:
            # Ctrl + Backspace → удаляем до ближайшего пробела слева
            if self.text:
                i = len(self.text) - 1
                while i >= 0 and self.text[i].isspace():
                    i -= 1
                while i >= 0 and not self.text[i].isspace():
                    i -= 1
                self.text = self.text[:i + 1].rstrip()
        else:
            # Обычный Backspace
            if self.text:
                self.text = self.text[:-1]

    def update(self) -> None:
        current_time = pygame.time.get_ticks()

        # Мигание курсора
        if self.active and current_time - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time

        # Повтор Backspace при удержании
        keys = pygame.key.get_pressed()
        if self.active and self.backspace_pressed and keys[pygame.K_BACKSPACE]:
            if current_time - self.last_backspace_time > self.backspace_repeat_delay:
                interval = self.backspace_repeat_rate
                if current_time - self.last_backspace_time >= interval:
                    self._handle_backspace()
                    self.last_backspace_time = current_time
        else:
            self.backspace_pressed = False

    def draw(self, screen: pygame.Surface) -> None:
        # Метка
        if self.label:
            label_surface = self.label_font.render(self.label, True, Colors.white)
            screen.blit(label_surface, (self.rect.x, self.rect.y - 30))

        # Рамка
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        pygame.draw.rect(screen, Colors.white,
                         (self.rect.x + 2, self.rect.y + 2,
                          self.rect.width - 4, self.rect.height - 4),
                         border_radius=3)

        # Текст
        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(text_surface, (self.rect.x + 10,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

        # Курсор
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 10 + text_surface.get_width() + 2
            cursor_y1 = self.rect.y + 6
            cursor_y2 = self.rect.y + self.rect.height - 6
            pygame.draw.line(screen, Colors.black,
                             (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

    def get_text(self) -> str:
        return self.text

    def is_empty(self) -> bool:
        return len(self.text) == 0

    def clear(self):
        self.text = ""


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


class OptionBox:
    def __init__(self, x, y, width, height, options, visible_items=5, default_index=0, font_size=32):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.visible_items = visible_items
        self.selected_index = default_index if 0 <= default_index < len(options) else 0
        self.font = pygame.font.Font(None, font_size)

        self.scroll_offset = 0
        self.max_scroll = max(0, len(options) - visible_items)

        self.scrollbar_width = 12
        self.scrollbar_rect = None
        self.is_dragging_scrollbar = False
        self.drag_start_y = 0
        self.drag_start_scroll = 0

        self.item_height = height // visible_items

        self.bg_color = (200, 220, 200)           # светлый зелёный
        self.hover_color = (180, 210, 180)        # для подсветки при наведении
        self.border_color = (80, 80, 80)          # тёмно-серый
        self.text_color = (0, 0, 0)                # чёрный
        self.active_border_color = (122, 0, 156)     # тёмно-зелёный для выделенного элемента
        self.scrollbar_color = (80, 80, 80)        # цвет ползунка
        self.scrollbar_hover_color = (120, 120, 120) # при наведении или перетаскивании

        self.hovered_index = None       # индекс опции под курсором
        self._just_selected = None       # опция, выбранная последним кликом (для однократного возврата)

    def handle_event(self, event):
        """Обрабатывает события мыши: движение, колёсико, клики, перетаскивание ползунка."""
        mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(mouse_pos):
                if event.y > 0:  # вверх
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.y < 0:  # вниз
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + 1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Левая кнопка мыши
            if self.rect.collidepoint(mouse_pos):
                # Проверяем клик по элементам списка
                visible_options = self.get_visible_options()
                for i, option in enumerate(visible_options):
                    global_index = i + self.scroll_offset
                    item_rect = pygame.Rect(
                        self.rect.x,
                        self.rect.y + i * self.item_height,
                        self.rect.width - (self.scrollbar_width if len(self.options) > self.visible_items else 0),
                        self.item_height
                    )
                    if item_rect.collidepoint(mouse_pos):
                        self.selected_index = global_index
                        self._just_selected = self.options[global_index]
                        return True

                # Проверяем клик по скроллбару
                if self.scrollbar_rect and self.scrollbar_rect.collidepoint(mouse_pos):
                    self.is_dragging_scrollbar = True
                    self.drag_start_y = mouse_pos[1]
                    self.drag_start_scroll = self.scroll_offset
                    return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging_scrollbar = False

        elif event.type == pygame.MOUSEMOTION:
            # Обновляем подсветку опции под курсором
            if self.rect.collidepoint(mouse_pos):
                relative_y = mouse_pos[1] - self.rect.y
                line = relative_y // self.item_height
                if 0 <= line < self.visible_items:
                    global_index = self.scroll_offset + line
                    if global_index < len(self.options):
                        self.hovered_index = global_index
                    else:
                        self.hovered_index = None
                else:
                    self.hovered_index = None
            else:
                self.hovered_index = None

            # Перетаскивание скроллбара
            if self.is_dragging_scrollbar:
                delta_y = mouse_pos[1] - self.drag_start_y
                total_height = self.rect.height
                if total_height > 0 and self.max_scroll > 0:
                    scroll_ratio = delta_y / total_height
                    new_offset = self.drag_start_scroll + int(scroll_ratio * self.max_scroll)
                    self.scroll_offset = max(0, min(self.max_scroll, new_offset))

        return False

    def get_visible_options(self):
        """Возвращает список опций, видимых в данный момент."""
        end_index = min(self.scroll_offset + self.visible_items, len(self.options))
        return self.options[self.scroll_offset:end_index]

    def update_scrollbar(self):
        """Обновляет положение и размер ползунка на основе scroll_offset."""
        if len(self.options) <= self.visible_items:
            self.scrollbar_rect = None
            return

        visible_ratio = self.visible_items / len(self.options)
        scrollbar_height = max(20, int(self.rect.height * visible_ratio))

        if self.max_scroll > 0:
            scroll_ratio = self.scroll_offset / self.max_scroll
        else:
            scroll_ratio = 0

        scrollable_height = self.rect.height - scrollbar_height
        scrollbar_y = self.rect.y + (scroll_ratio * scrollable_height)

        self.scrollbar_rect = pygame.Rect(
            self.rect.right - self.scrollbar_width - 2,
            scrollbar_y,
            self.scrollbar_width,
            scrollbar_height
        )

    def draw(self, screen):
        """Отрисовывает виджет на экране."""
        # Фон и рамка всего виджета
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)

        # Ограничиваем отрисовку внутренней областью
        old_clip = screen.get_clip()
        screen.set_clip(self.rect)

        visible_options = self.get_visible_options()
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(visible_options):
            global_index = i + self.scroll_offset
            item_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + i * self.item_height,
                self.rect.width - (self.scrollbar_width if len(self.options) > self.visible_items else 0),
                self.item_height
            )

            # Цвет фона для текущего элемента
            bg_color = self.hover_color if global_index == self.hovered_index else self.bg_color
            pygame.draw.rect(screen, bg_color, item_rect, border_radius=5)
            pygame.draw.rect(screen, self.border_color, item_rect, 1, border_radius=5)

            # Рамка для выбранного элемента
            if global_index == self.selected_index:
                pygame.draw.rect(screen, self.active_border_color, item_rect, 2, border_radius=5)

            # Текст
            text_surf = self.font.render(str(option), True, self.text_color)
            text_rect = text_surf.get_rect(center=item_rect.center)
            screen.blit(text_surf, text_rect)

        # Восстанавливаем область отсечения
        screen.set_clip(old_clip)

        # Скроллбар (рисуется поверх, но внутри общей рамки)
        self.update_scrollbar()
        if self.scrollbar_rect:
            is_hovering = self.scrollbar_rect.collidepoint(mouse_pos)
            scrollbar_color = self.scrollbar_hover_color if (is_hovering or self.is_dragging_scrollbar) else self.scrollbar_color
            pygame.draw.rect(screen, scrollbar_color, self.scrollbar_rect, border_radius=6)
            pygame.draw.rect(screen, self.border_color, self.scrollbar_rect, 1, border_radius=6)

    def get_selected(self):
        """Возвращает опцию, выбранную последним кликом (однократно), и сбрасывает флаг."""
        value = self._just_selected
        self._just_selected = None
        return value

    def get_selected_option(self):
        """Возвращает текущую выбранную опцию (без сброса)."""
        return self.options[self.selected_index]

    def get_selected_index(self):
        """Возвращает индекс текущей выбранной опции."""
        return self.selected_index

class VerticalSlider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val,
                 track_color, thumb_color, callback=None, step=1):
        self.min_val = int(min_val)
        self.max_val = int(max_val)
        self.step = int(step)
        self.callback = callback

        # Трек (вертикальная полоса)
        self.rect = pygame.Rect(x, y, width, height)

        # Ползунок: ширина равна ширине трека, высота фиксированная (минимум 20)
        self.thumb_width = width
        self.thumb_height = min(20, height)

        self.current_val = self._clamp_value(start_val)
        self.thumb_rect = pygame.Rect(
            x,
            y + self._val_to_pos(self.current_val),
            self.thumb_width,
            self.thumb_height
        )

        self.track_color = track_color
        self.thumb_color = thumb_color

        self.dragging = False
        self.drag_offset_y = 0  # смещение от верхнего края ползунка до точки захвата

        # Шрифт для подписей
        self.font = pygame.font.Font(None, 20)

    def _clamp_value(self, val):
        """Округление до ближайшего целого, кратного step, и ограничение диапазоном."""
        val = int(round(val / self.step) * self.step)
        return max(self.min_val, min(self.max_val, val))

    def _val_to_pos(self, val):
        """
        Возвращает смещение верхнего края ползунка относительно верха трека.
        """
        if self.max_val == self.min_val:
            return 0
        track_range = self.rect.height - self.thumb_height
        val_range = self.max_val - self.min_val
        proportion = (val - self.min_val) / val_range
        return proportion * track_range

    def _pos_to_val(self, thumb_top):
        """
        Преобразует позицию верхнего края ползунка в значение (float).
        """
        if self.max_val == self.min_val:
            return self.min_val
        track_range = self.rect.height - self.thumb_height
        val_range = self.max_val - self.min_val
        proportion = (thumb_top - self.rect.top) / track_range
        return self.min_val + proportion * val_range

    def set_value(self, new_val):
        """Установить новое значение (округляется до step)."""
        new_val = self._clamp_value(new_val)
        if new_val != self.current_val:
            self.current_val = new_val
            self.thumb_rect.y = self.rect.top + self._val_to_pos(new_val)
            if self.callback:
                self.callback(new_val)

    def handle_event(self, event):
        """Обработка событий мыши."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.thumb_rect.collidepoint(event.pos):
                self.dragging = True
                self.drag_offset_y = event.pos[1] - self.thumb_rect.y
            elif self.rect.collidepoint(event.pos):
                # Клик по треку — переместить ползунок так, чтобы его центр был в месте клика
                new_top = event.pos[1] - self.thumb_height // 2
                new_top = max(self.rect.top,
                              min(new_top, self.rect.bottom - self.thumb_height))
                new_val = self._pos_to_val(new_top)
                self.set_value(new_val)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging and event.buttons[0]:
                new_top = event.pos[1] - self.drag_offset_y
                new_top = max(self.rect.top,
                              min(new_top, self.rect.bottom - self.thumb_height))
                new_val = self._pos_to_val(new_top)
                self.set_value(new_val)

    def draw_labels(self, surface):
        """Рисует подписи целых значений справа от трека."""
        num_vals = (self.max_val - self.min_val) // self.step + 1
        label_x = self.rect.left + 2  # небольшой отступ справа

        if num_vals > 30:  # если слишком много — только минимум, максимум и текущее
            # Минимум (внизу)
            y_min = self.rect.bottom - self.thumb_height // 2
            self._draw_label(surface, self.min_val, label_x, y_min, align='center')
            # Максимум (вверху)
            y_max = self.rect.top + self.thumb_height // 2
            self._draw_label(surface, self.max_val, label_x, y_max, align='center')
            # Текущее значение (рядом с ползунком)
            y_cur = self.thumb_rect.centery
            self._draw_label(surface, self.current_val, label_x, y_cur, align='center')
        else:
            # Подпись для каждого значения
            for val in range(self.min_val, self.max_val + 1, self.step):
                y_center = self.rect.top + self._val_to_pos(val) + self.thumb_height // 2
                self._draw_label(surface, val, label_x, y_center, align='center')

    def _draw_label(self, surface, val, x, y_center, align='center'):
        """Рисует одну подпись числа с выравниванием по центру по вертикали."""
        text = self.font.render(str(val), True, (0, 0, 0))
        text_rect = text.get_rect()
        if align == 'center':
            text_rect.centery = y_center
        text_rect.left = x
        surface.blit(text, text_rect)

    def draw(self, surface):
        """Отрисовка трека, ползунка и подписей."""
        pygame.draw.rect(surface, self.track_color, self.rect)
        pygame.draw.rect(surface, self.thumb_color, self.thumb_rect)
        self.draw_labels(surface)
