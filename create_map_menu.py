import pygame
import sys

import ui_elements
from config import UserConfig



def open_create_map_menu(screen):
    button_width, button_height = 260, 70
    input_width, input_height = 200, 50

    background = ui_elements.MenuBackground.load_background_image()
    screen.blit(background, (0, 0))

    # Создаем поля ввода
    center_x = UserConfig.screen_width // 2
    input_y = UserConfig.screen_height // 2 - 50

    # Поле для длины карты
    length_input = InputBox(
        center_x - input_width - 20,
        input_y,
        input_width,
        input_height,
        "Длина карты:",
        max_length=3
    )

    # Поле для ширины карты
    width_input = InputBox(
        center_x + 20,
        input_y,
        input_width,
        input_height,
        "Ширина карты:",
        max_length=3
    )

    # Список полей ввода для удобного переключения
    input_fields = [length_input, width_input]
    current_input_index = 0
    input_fields[current_input_index].active = True

    # Кнопка создания
    create_button = ui_elements.Button(
        center_x - button_width // 2,
        UserConfig.screen_height // 2 + 40,
        button_width,
        button_height,
        "Создать карту",
        ui_elements.Colors.blue,
        ui_elements.Colors.hover_blue
    )

    # Кнопка назад
    back_button = ui_elements.Button(
        center_x - button_width // 2,
        UserConfig.screen_height // 2 + 120,
        button_width,
        button_height,
        "Назад",
        ui_elements.Colors.red,
        ui_elements.Colors.hover_red
    )

    # Сообщение об ошибке/подсказка
    error_message = ""
    error_timer = 0

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        # Обновляем фон
        screen.blit(background, (0, 0))

        # Заголовок
        title = ui_elements.Fonts.title_font.render("Создание новой карты", True, ui_elements.Colors.dark_golden)
        title_rect = title.get_rect(center=(UserConfig.screen_width // 2, UserConfig.screen_height // 6))
        screen.blit(title, title_rect)

        # Подсказка
        hint_font = pygame.font.Font(None, 24)
        hint = hint_font.render("Введите размеры карты (только цифры)", True, ui_elements.Colors.light_gray)
        hint_rect = hint.get_rect(center=(UserConfig.screen_width // 2, input_y - 70))
        screen.blit(hint, hint_rect)

        # Обновляем и рисуем поля ввода
        for field in input_fields:
            field.update()
            field.draw(screen)

        # Отображаем текущие значения
        values_font = pygame.font.Font(None, 28)
        if not length_input.is_empty() and not width_input.is_empty():
            length = length_input.get_value()
            width = width_input.get_value()
            values_text = f"Размер карты: {length} × {width}"
            values_surface = values_font.render(values_text, True, ui_elements.Colors.light_green)
            values_rect = values_surface.get_rect(center=(UserConfig.screen_width // 2, input_y + 80))
            screen.blit(values_surface, values_rect)

        # Отображаем сообщение об ошибке
        if error_message:
            error_font = pygame.font.Font(None, 26)
            error_surface = error_font.render(error_message, True, ui_elements.Colors.red)
            error_rect = error_surface.get_rect(center=(UserConfig.screen_width // 2, input_y + 110))
            screen.blit(error_surface, error_rect)

            # Автоматическое скрытие сообщения об ошибке через 3 секунды
            current_time = pygame.time.get_ticks()
            if current_time - error_timer > 3000:
                error_message = ""

        # Обновляем кнопки
        create_button.check_hover(mouse_pos)
        back_button.check_hover(mouse_pos)

        # Рисуем кнопки
        create_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False

                # Обработка Tab для переключения между полями
                if event.key == pygame.K_TAB:
                    input_fields[current_input_index].active = False
                    current_input_index = (current_input_index + 1) % len(input_fields)
                    input_fields[current_input_index].active = True
                    input_fields[current_input_index].cursor_visible = True
                    input_fields[current_input_index].cursor_timer = pygame.time.get_ticks()

                # Передаем события активному полю ввода
                result = input_fields[current_input_index].handle_event(event)
                if result == "TAB":
                    input_fields[current_input_index].active = False
                    current_input_index = (current_input_index + 1) % len(input_fields)
                    input_fields[current_input_index].active = True
                    input_fields[current_input_index].cursor_visible = True
                    input_fields[current_input_index].cursor_timer = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

                    # Проверяем клик по полям ввода
                    for i, field in enumerate(input_fields):
                        if field.rect.collidepoint(event.pos):
                            # Деактивируем все поля
                            for f in input_fields:
                                f.active = False
                            # Активируем выбранное поле
                            field.active = True
                            field.cursor_visible = True
                            field.cursor_timer = pygame.time.get_ticks()
                            current_input_index = i

                    # Проверяем клик по кнопкам
                    if create_button.is_clicked(mouse_pos, mouse_click):
                        length = length_input.get_value()
                        width = width_input.get_value()

                        # Проверка валидности ввода
                        if length <= 0 or width <= 0:
                            error_message = "Размеры должны быть больше 0!"
                            error_timer = pygame.time.get_ticks()
                        elif length > 999 or width > 999:
                            error_message = "Размеры не могут превышать 999!"
                            error_timer = pygame.time.get_ticks()
                        else:
                            # Здесь можно добавить создание карты с указанными размерами
                            print(f"Создание карты: длина={length}, ширина={width}")
                            # Возвращаем значения размеров карты
                            return {"length": length, "width": width}

                    elif back_button.is_clicked(mouse_pos, mouse_click):
                        is_running = False

        pygame.display.flip()
        clock.tick(60)

    return None