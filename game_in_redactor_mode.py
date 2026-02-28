import pygame
import copy

import ui_elements
from tile import Tile
from config import user_config
from ui_elements import ImagedButton
from start_empty_map import Camera
from start_empty_map import World
from start_empty_map import UI


class GameInRedactorMode:
    def __init__(self, world_width: int, world_height: int, start_biome: str) -> None:
        self.SCREEN_WIDTH: int = user_config.screen_width
        self.SCREEN_HEIGHT: int = user_config.screen_height
        self.TILE_SIZE: int = 64
        self.FPS: int = 60

        self.world_width: int = world_width
        self.world_height: int = world_height
        self.start_biome: str = start_biome

        self.world: World = World(self.world_width, self.world_height, self.start_biome)
        self.camera: Camera = Camera()
        self.ui: UI = UI()

        self.actions = []

        self.is_running: bool = True

    @staticmethod
    def _mark_only_button(button: ui_elements.ImagedButton, buttons: tuple) -> None:
        for buttn in buttons:
            buttn.border_color = ui_elements.Colors.black
        button.border_color = ui_elements.Colors.dark_red

    @staticmethod
    def _clear_tile(tile: Tile, world: World, screen: pygame.Surface, camera: Camera) -> None:
        tile.stored_resource = None
        if world.flags_tiles.get(tile.stored_flag) == tile:
            world.flags_tiles[tile.stored_flag] = None
        tile.stored_flag = None
        tile.draw(screen, camera)

    @staticmethod
    def _is_tiles_same(tile1: Tile, tile2: Tile) -> bool:
        return tile1.type == tile2.type and tile1.stored_resource == tile2.stored_resource and tile1.stored_flag == tile2.stored_flag

    def on_select_select_tool(self, select_tool_button: ImagedButton, all_buttons: tuple, ui: UI) -> None:
        self._mark_only_button(select_tool_button, all_buttons)
        ui.selected_item = "select_tool"
        ui.current_tool = "tool"

    def _on_select_remove_tool(self, remove_tool_button: ui_elements.ImagedButton, all_buttons: tuple, ui: UI) -> None:
        self._mark_only_button(remove_tool_button, all_buttons)
        ui.selected_item = "remove_tool"
        ui.current_tool = "tool"

    def _on_select_back_tool(self, screen: pygame.Surface) -> None:
        if len(self.actions) > 0:
            tile_before_act = self.actions[-1]["before"]
            tile = self.actions[-1]["after"]
            tile.type = tile_before_act.type
            tile.stored_resource = tile_before_act.stored_resource
            tile.stored_flag = tile_before_act.stored_flag
            self.actions.pop(-1)
            tile.draw(screen, self.camera)

    def _on_f1(self):
        self.ui.do_show_grid = not self.ui.do_show_grid

    def _on_f2(self):
        self.ui.do_show_minimap = not self.ui.do_show_minimap

    def _on_f4(self):
        self.camera.toggle_edge_scrolling()

    def _on_space(self):
        if self.ui.selected_tile:
            self.camera.center_on_tile(self.ui.selected_tile.x, self.ui.selected_tile.y)

    def _on_1(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Biomes":
            self._mark_only_button(biomes_buttons[0],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "grass"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[0],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "food"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[0],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "aqua_flag"
            self.ui.current_tool = "flag"

    def _on_2(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Biomes":
            self._mark_only_button(biomes_buttons[1],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "mountain"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[1],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "wood"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[1],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "black_flag"
            self.ui.current_tool = "flag"

    def _on_3(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Biomes":
            self._mark_only_button(biomes_buttons[2],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "water"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[2],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "stone"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[2],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "blue_flag"
            self.ui.current_tool = "flag"

    def _on_4(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Biomes":
            self._mark_only_button(biomes_buttons[3],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "sand"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[3],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "copper"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[3],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "green_flag"
            self.ui.current_tool = "flag"

    def _on_5(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Biomes":
            self._mark_only_button(biomes_buttons[4],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "snow"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[4],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "iron"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[4],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "orange_flag"
            self.ui.current_tool = "flag"

    def _on_6(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Biomes":
            self._mark_only_button(biomes_buttons[5],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "swamp"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[5],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "silver"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[5],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "red_flag"
            self.ui.current_tool = "flag"

    def _on_7(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Resources":
            self._mark_only_button(resources_buttons[6],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "gold"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[6],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "white_flag"
            self.ui.current_tool = "flag"

    def _on_8(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple):
        if self.ui.current_section == "Start positions":
            self._mark_only_button(flags_buttons[7],
                                   (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons))
            self.ui.selected_item = "yellow_flag"
            self.ui.current_tool = "flag"

    def _on_z(self, select_tool_button: ui_elements.ImagedButton, all_buttons: tuple):
        self.on_select_select_tool(select_tool_button, all_buttons, self.ui)

    def _on_x(self, remove_tool_button: ui_elements.ImagedButton, all_buttons: tuple):
        self._on_select_remove_tool(remove_tool_button, all_buttons, self.ui)

    def _on_c(self, screen: pygame.Surface):
        self._on_select_back_tool(screen)

    def _on_tab(self, redactor_type_dropdown: ui_elements.Dropdown, dropdown_options: list[str]):
        current_option_index = dropdown_options.index(self.ui.current_section)
        new_index = {0: 1, 1: 0, 2: 0, 3: 0}
        self.ui.current_section = dropdown_options[new_index[current_option_index]]
        redactor_type_dropdown.selected_index = new_index[current_option_index]

    def on_escape(self):
        self.is_running = False
    
    def _on_use_remove_tool(self, tile: Tile, screen: pygame.Surface) -> None:
        if self.ui.selected_item == "remove_tool":
            tile_before_act = copy.deepcopy(tile)
            self._clear_tile(tile, self.world, screen, self.camera)
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})

    def _on_use_biome_tool(self, tile: Tile, screen: pygame.Surface) -> None:
        biome = self.ui.selected_item
        if biome != "water" or tile.stored_flag is None:
            tile_before_act = copy.deepcopy(tile)
            tile.type = biome
            if tile.type == "water":
                tile.stored_resource = None
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
            tile.draw(screen, self.camera)

    def _on_use_resource_tool(self, tile: Tile, screen: pygame.Surface) -> None:
        resource = self.ui.selected_item
        if not tile.stored_flag:
            tile_before_act = copy.deepcopy(tile)
            tile.stored_resource = resource
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
            tile.draw(screen, self.camera)

    def _on_use_flag_tool(self, tile: Tile, screen: pygame.Surface) -> None:
        flag = self.ui.selected_item
        if not tile.stored_resource:
            tile_before_act = copy.deepcopy(tile)
            if self.world.flags_tiles[flag] is not None:
                self.world.flags_tiles[flag].stored_flag = None
            self.world.flags_tiles[flag] = tile
            tile.stored_flag = flag
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
            tile.draw(screen, self.camera)

    def _on_mousewheel(self, event: pygame.event) -> None:
        self.camera.handle_event(event)

    def _on_tile_click(self, tile: Tile, screen: pygame.Surface) -> None:
        tile.selected = True
        self.ui.update_selected_tile(tile)
        print(f"Tile: ({tile.x}, {tile.y}) - {tile.type}")

        if self.ui.current_tool == "tool" and self.ui.selected_item:
            self._on_use_remove_tool(tile, screen)

        if (self.ui.current_section == "Biomes") and self.ui.selected_item and self.ui.current_tool == "biome":
            self._on_use_biome_tool(tile, screen)

        elif (self.ui.current_section == "Resources") and self.ui.selected_item and self.ui.current_tool == "resource":
            self._on_use_resource_tool(tile, screen)

        elif (self.ui.current_section == "Start positions") and self.ui.selected_item and self.ui.current_tool == "flag":
            self._on_use_flag_tool(tile, screen)

    def _update_camera(self, map_name_input_box: ui_elements.InputBox, keys, mouse_pos: tuple[int, int]) -> None:
        mouse_x, mouse_y = mouse_pos
        if not map_name_input_box.active:
            self.camera.update_with_mouse(mouse_x, mouse_y)
            self.camera.update_with_keyboard(keys)
        self.camera.update()

    @staticmethod
    def _draw_buttons(buttons_to_draw: tuple, screen: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        for button in buttons_to_draw:
            button.check_hover(mouse_pos)
            button.draw(screen)

    @staticmethod
    def _draw_save_map_interface(map_name_input_box: ui_elements.InputBox, save_map_button: ui_elements.Button, screen: pygame.Surface) -> None:
        map_name_input_box.active = True
        save_map_button.draw(screen)
        map_name_input_box.draw(screen)

    def _draw_interface(self, biomes_buttons: tuple, resources_buttons: tuple, flags_buttons: tuple, tools_buttons: tuple, map_name_input_box: ui_elements.InputBox, save_map_button: ui_elements.Button, clock: pygame.Clock, screen: pygame.Surface, mouse_pos: tuple[int, int]) -> None:
        if self.ui.current_section == "Biomes":
            self._draw_buttons((*biomes_buttons, *tools_buttons), screen, mouse_pos)

        elif self.ui.current_section == "Resources":
            self._draw_buttons((*resources_buttons, *tools_buttons), screen, mouse_pos)

        elif self.ui.current_section == "Start positions":
            self._draw_buttons((*flags_buttons, *tools_buttons), screen, mouse_pos)

        elif self.ui.current_section == "Save map":
            self._draw_save_map_interface(map_name_input_box, save_map_button, screen)

        fps_text = self.ui.small_font.render(f"FPS: {int(clock.get_fps())}", True, ui_elements.Colors.green)
        screen.blit(fps_text, (self.SCREEN_WIDTH - 80, self.SCREEN_HEIGHT - 25))

    def start_game(self) -> None:
        screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("DespEco")
        import redactor_ui_elements

        clock = pygame.time.Clock()
        self.ui.current_section = "Biomes"

        dropdown_options = ["Biomes", "Resources", "Start positions", "Save map"]

        redactor_type_dropdown = redactor_ui_elements.redactor_type_dropdown
        save_map_button = redactor_ui_elements.save_map_button

        map_name_input_box = redactor_ui_elements.map_name_input_box
        grass_button = redactor_ui_elements.grass_button
        mountain_button = redactor_ui_elements.mountain_button
        water_button = redactor_ui_elements.water_button
        sand_button = redactor_ui_elements.sand_button
        snow_button = redactor_ui_elements.snow_button
        swamp_button = redactor_ui_elements.swamp_button

        aqua_flag_button = redactor_ui_elements.aqua_flag_button
        black_flag_button = redactor_ui_elements.black_flag_button
        blue_flag_button = redactor_ui_elements.blue_flag_button
        green_flag_button = redactor_ui_elements.green_flag_button
        orange_flag_button = redactor_ui_elements.orange_flag_button
        red_flag_button = redactor_ui_elements.red_flag_button
        white_flag_button = redactor_ui_elements.white_flag_button
        yellow_flag_button = redactor_ui_elements.yellow_flag_button

        food_resource_button = redactor_ui_elements.food_resource_button
        wood_resource_button = redactor_ui_elements.wood_resource_button
        stone_resource_button = redactor_ui_elements.stone_resource_button
        copper_resource_button = redactor_ui_elements.copper_resource_button
        iron_resource_button = redactor_ui_elements.iron_resource_button
        silver_resource_button = redactor_ui_elements.silver_resource_button
        gold_resource_button = redactor_ui_elements.gold_resource_button

        select_tool_button = redactor_ui_elements.select_tool_button
        remove_tool_button = redactor_ui_elements.remove_tool_button
        back_tool_button = redactor_ui_elements.back_tool_button

        biomes_buttons = (grass_button, mountain_button, water_button, sand_button, snow_button, swamp_button)
        resources_buttons = (food_resource_button, wood_resource_button, stone_resource_button, copper_resource_button, iron_resource_button,silver_resource_button, gold_resource_button)
        flags_buttons = (aqua_flag_button, black_flag_button, blue_flag_button, green_flag_button, orange_flag_button, red_flag_button,white_flag_button, yellow_flag_button)
        tools_buttons = (select_tool_button, remove_tool_button, back_tool_button)
        all_buttons = (*biomes_buttons, *resources_buttons, *flags_buttons, *tools_buttons)
        scenes_objects = (*all_buttons, redactor_type_dropdown, save_map_button, map_name_input_box)

        minimap_score = 0
        print("Game started")

        while self.is_running:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_pos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                redactor_type_dropdown.handle_event(event)

                if event.type == pygame.QUIT:
                    self.is_running = False

                elif event.type == pygame.KEYDOWN:
                    map_name_input_box.handle_event(event)

                    keys_to_acts = {
                        pygame.K_ESCAPE: self.on_escape,
                        pygame.K_F1: lambda: self._on_f1(),
                        pygame.K_F2: lambda: self._on_f2(),
                        pygame.K_F4: lambda: self._on_f4(),
                        pygame.K_SPACE: lambda: self._on_space(),
                        pygame.K_z: lambda: self._on_z(select_tool_button, all_buttons),
                        pygame.K_x: lambda: self._on_x(remove_tool_button, all_buttons),
                        pygame.K_c: lambda: self._on_select_back_tool(screen),
                        pygame.K_TAB: lambda: self._on_tab(redactor_type_dropdown, dropdown_options),
                        pygame.K_1: lambda: self._on_1(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_2: lambda: self._on_2(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_3: lambda: self._on_3(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_4: lambda: self._on_4(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_5: lambda: self._on_5(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_6: lambda: self._on_6(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_7: lambda: self._on_7(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                        pygame.K_8: lambda: self._on_8(biomes_buttons, resources_buttons, flags_buttons, tools_buttons),
                    }

                    if keys_to_acts.get(event.key) is not None:
                        keys_to_acts.get(event.key)()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True

                        if select_tool_button.is_clicked(mouse_pos, mouse_click):
                            self.on_select_select_tool(select_tool_button, all_buttons, self.ui)
                        if remove_tool_button.is_clicked(mouse_pos, mouse_click):
                            self._on_select_remove_tool(remove_tool_button, all_buttons, self.ui)
                        if back_tool_button.is_clicked(mouse_pos, mouse_click) and len(self.actions) > 0:
                            self._on_select_back_tool(screen)

                        if self.ui.current_section == "Biomes":
                            for buttn in biomes_buttons:
                                if buttn.is_clicked(mouse_pos, mouse_click):
                                    self._mark_only_button(buttn, all_buttons)
                                    buttons2items = {grass_button: "grass",
                                                     mountain_button: "mountain",
                                                     water_button: "water",
                                                     sand_button: "sand",
                                                     snow_button: "snow",
                                                     swamp_button: "swamp"}
                                    self.ui.selected_item = buttons2items[buttn]
                                    self.ui.current_tool = "biome"

                        elif self.ui.current_section == "Resources":
                            for buttn in resources_buttons:
                                if buttn.is_clicked(mouse_pos, mouse_click):
                                    self._mark_only_button(buttn, all_buttons)
                                    buttons2items = {food_resource_button: "food",
                                                     wood_resource_button: "wood",
                                                     stone_resource_button: "stone",
                                                     copper_resource_button: "copper",
                                                     iron_resource_button: "iron",
                                                     silver_resource_button: "silver",
                                                     gold_resource_button: "gold"}
                                    self.ui.selected_item = buttons2items[buttn]
                                    self.ui.current_tool = "resource"

                        elif self.ui.current_section == "Start positions":
                            for buttn in flags_buttons:
                                if buttn.is_clicked(mouse_pos, mouse_click):
                                    self._mark_only_button(buttn, all_buttons)
                                    buttons2items = {aqua_flag_button: "aqua_flag",
                                                     black_flag_button: "black_flag",
                                                     blue_flag_button: "blue_flag",
                                                     green_flag_button: "green_flag",
                                                     orange_flag_button: "orange_flag",
                                                     red_flag_button: "red_flag",
                                                     white_flag_button: "white_flag",
                                                     yellow_flag_button: "yellow_flag", }
                                    self.ui.selected_item = buttons2items[buttn]
                                    self.ui.current_tool = "flag"

                        if not (any(obj.rect.collidepoint(mouse_pos) for obj in scenes_objects)) and not (redactor_type_dropdown.item_rect.collidepoint(mouse_pos)):
                            tile_x, tile_y = self.camera.screen_to_world(mouse_x, mouse_y)
                            self.world.deselect_all_tiles()
                            tile = self.world.get_tile_by_cords(tile_x, tile_y)
                            if tile:
                                self._on_tile_click(tile, screen)

                elif event.type == pygame.MOUSEWHEEL:
                    self._on_mousewheel(event)

            self._update_camera(map_name_input_box, keys, mouse_pos)

            screen.fill(ui_elements.Colors.black)
            self.world.draw(screen, self.camera)

            minimap_score += 1
            if minimap_score == 60:
                minimap_score = 0
                terrain_map = self.ui.map_saver.code_maps(self.world.tiles)["terrain_map"]
                self.ui.minimap_former.do_pipeline(terrain_map)

            self.ui.draw(screen, self.camera)
            redactor_type_dropdown.draw(screen)
            self.ui.current_section = redactor_type_dropdown.get_selected_option()
            map_name_input_box.active = False
            self._draw_interface(biomes_buttons, resources_buttons, flags_buttons, tools_buttons, map_name_input_box, save_map_button, clock, screen, mouse_pos)

            pygame.display.flip()
            clock.tick(self.FPS)

        pygame.quit()
        print("\nGame over")