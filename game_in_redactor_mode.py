import copy

import pygame

import ui_elements
from tile import Tile
from config import user_config
from start_empty_map import Camera
from start_empty_map import World
from start_empty_map import UI
from map_manager import MapManager
from sounds_manager import SoundsManager
from minimap_manager import MinimapManager


class GameInRedactorMode:
    def __init__(self, world_width: int, world_height: int, start_biome: str = "Meadows", tile_map: list[list[Tile]] = None) -> None:
        self.screen_WIDTH: int = user_config.screen_width
        self.screen_HEIGHT: int = user_config.screen_height
        self.TILE_SIZE: int = 64
        self.FPS: int = 60

        self.world_width: int = world_width
        self.world_height: int = world_height
        self.start_biome: str = start_biome

        self.world: World = World(self.world_width, self.world_height, self.start_biome, tile_map)
        self.camera: Camera = Camera()
        self.ui: UI = UI()
        self.screen: pygame.Surface | None = None
        self.map_manager = MapManager()
        self.sounds_manager: SoundsManager = SoundsManager()

        self.changed_tile_in_tick: Tile | None = None
        self.actions: list = []
        self.game_map: list[list[int]] | None = None
        self.brush_size: int = 2

        self.tick: int = 0
        self.back_button_tick: int = -10
        self.brush_button_tick: int = -10

        self.minimap_manager = MinimapManager(self.world.tiles, width=self.screen_WIDTH, height=self.screen_HEIGHT)
        self.changed_tiles_in_cycle: list = []
        self.dirty = True

        self.map_name_for_repeated_saving: str = ""

        self.is_running: bool = True

    @staticmethod
    def _mark_button(button: ui_elements.ImagedButton) -> None:
        if button is not None:
            button.border_color = ui_elements.Colors.dark_red

    @staticmethod
    def _unmark_button(button: ui_elements.ImagedButton) -> None:
        if button is not None:
            button.border_color = ui_elements.Colors.black

    @staticmethod
    def _mark_only_button(button: ui_elements.ImagedButton, buttons: tuple) -> None:
        for buttn in buttons:
            buttn.border_color = ui_elements.Colors.black
        if button is not None:
            button.border_color = ui_elements.Colors.dark_red

    def _clear_tile(self, tile: Tile, world: World, camera: Camera) -> None:
        tile.stored_resource = None
        if world.flags_tiles.get(tile.stored_flag) == tile:
            world.flags_tiles[tile.stored_flag] = None
        tile.stored_flag = None
        tile.draw(self.screen, camera)

    @staticmethod
    def _is_tiles_same(tile1: Tile, tile2: Tile) -> bool:
        return tile1.type == tile2.type and tile1.stored_resource == tile2.stored_resource and tile1.stored_flag == tile2.stored_flag
    
    def _create_objects(self):
        import redactor_ui_elements

        self.dropdown_options = ["Biomes", "Resources", "Start positions", "Save map"]

        self.redactor_type_dropdown = redactor_ui_elements.redactor_type_dropdown
        self.save_map_button = redactor_ui_elements.save_map_button

        self.map_name_input_box = redactor_ui_elements.map_name_input_box
        self.grass_button = redactor_ui_elements.grass_button
        self.mountain_button = redactor_ui_elements.mountain_button
        self.water_button = redactor_ui_elements.water_button
        self.sand_button = redactor_ui_elements.sand_button
        self.snow_button = redactor_ui_elements.snow_button
        self.swamp_button = redactor_ui_elements.swamp_button

        self.food_resource_button = redactor_ui_elements.food_resource_button
        self.wood_resource_button = redactor_ui_elements.wood_resource_button
        self.stone_resource_button = redactor_ui_elements.stone_resource_button
        self.copper_resource_button = redactor_ui_elements.copper_resource_button
        self.iron_resource_button = redactor_ui_elements.iron_resource_button
        self.silver_resource_button = redactor_ui_elements.silver_resource_button
        self.gold_resource_button = redactor_ui_elements.gold_resource_button
        
        self.aqua_flag_button = redactor_ui_elements.aqua_flag_button
        self.black_flag_button = redactor_ui_elements.black_flag_button
        self.blue_flag_button = redactor_ui_elements.blue_flag_button
        self.green_flag_button = redactor_ui_elements.green_flag_button
        self.orange_flag_button = redactor_ui_elements.orange_flag_button
        self.red_flag_button = redactor_ui_elements.red_flag_button
        self.white_flag_button = redactor_ui_elements.white_flag_button
        self.yellow_flag_button = redactor_ui_elements.yellow_flag_button

        self.select_tool_button = redactor_ui_elements.select_tool_button
        self.remove_tool_button = redactor_ui_elements.remove_tool_button
        self.back_tool_button = redactor_ui_elements.back_tool_button
        self.brush_tool_button = redactor_ui_elements.brush_tool_button

        self.brush_size_slider = redactor_ui_elements.brush_size_slider

        self.biomes_buttons = (self.grass_button, self.mountain_button, self.water_button, self.sand_button, self.snow_button, self.swamp_button)
        self.resources_buttons = (self.food_resource_button, self.wood_resource_button, self.stone_resource_button, self.copper_resource_button, self.iron_resource_button,self.silver_resource_button, self.gold_resource_button)
        self.flags_buttons = (self.aqua_flag_button, self.black_flag_button, self.blue_flag_button, self.green_flag_button, self.orange_flag_button, self.red_flag_button,self.white_flag_button, self.yellow_flag_button)
        self.tools_buttons = (self.select_tool_button, self.remove_tool_button, self.back_tool_button, self.brush_tool_button)
        self.all_buttons = (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons)
        self.scenes_objects = (*self.all_buttons, self.redactor_type_dropdown, self.save_map_button, self.map_name_input_box, self.brush_size_slider)
    
    def on_select_select_tool(self) -> None:
        self._mark_only_button(self.select_tool_button, self.all_buttons)
        self.ui.selected_item = "select_tool"
        self.ui.current_tool = "tool"

    def _on_select_remove_tool(self) -> None:
        self._mark_only_button(self.remove_tool_button, self.all_buttons)
        self.ui.selected_item = "remove_tool"
        self.ui.current_tool = "tool"

    def _on_select_back_tool(self) -> None:
        self._mark_button(self.back_tool_button)
        self.back_button_tick = self.tick
        if len(self.actions) == 0:
            return None
        self.back_button_tick = self.tick
        if len(self.actions) > 0:
            tile_before_act = self.actions[-1]["before"]
            tile = self.actions[-1]["after"]
            tile.type = tile_before_act.type
            tile.stored_resource = tile_before_act.stored_resource
            if tile.stored_flag != tile_before_act.stored_flag:
                self.world.flags_tiles[tile.stored_flag] = None
                self.world.flags_tiles[tile_before_act.stored_flag] = tile
            tile.stored_flag = tile_before_act.stored_flag
            self.actions.pop(-1)
            self.changed_tile_in_tick = tile
            tile.draw(self.screen, self.camera)

    def _on_select_brush_tool(self) -> None:
        self._mark_button(self.brush_tool_button)
        self.brush_button_tick = self.tick
        self.ui.do_show_brush_size_slider = not self.ui.do_show_brush_size_slider

    def _on_f1(self) -> None:
        self.ui.do_show_hud = not self.ui.do_show_hud

    def _on_f2(self) -> None:
        self.ui.do_show_grid = not self.ui.do_show_grid

    def _on_f3(self) -> None:
        self.camera.toggle_edge_scrolling()

    def _on_f4(self) -> None:
        ...

    def _on_space(self) -> None:
        if self.ui.selected_tile:
            self.camera.center_on_tile(self.ui.selected_tile.x, self.ui.selected_tile.y)

    def _on_1(self) -> None:
        if self.ui.current_section == "Biomes":
            self._mark_only_button(self.biomes_buttons[0],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "grass"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[0],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "food"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[0],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "aqua_flag"
            self.ui.current_tool = "flag"

    def _on_2(self) -> None:
        if self.ui.current_section == "Biomes":
            self._mark_only_button(self.biomes_buttons[1],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "mountain"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[1],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "wood"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[1],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "black_flag"
            self.ui.current_tool = "flag"

    def _on_3(self) -> None:
        if self.ui.current_section == "Biomes":
            self._mark_only_button(self.biomes_buttons[2],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "water"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[2],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "stone"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[2],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "blue_flag"
            self.ui.current_tool = "flag"

    def _on_4(self) -> None:
        if self.ui.current_section == "Biomes":
            self._mark_only_button(self.biomes_buttons[3],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "sand"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[3],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "copper"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[3],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "green_flag"
            self.ui.current_tool = "flag"

    def _on_5(self) -> None:
        if self.ui.current_section == "Biomes":
            self._mark_only_button(self.biomes_buttons[4],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "snow"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[4],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "iron"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[4],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "orange_flag"
            self.ui.current_tool = "flag"

    def _on_6(self) -> None:
        if self.ui.current_section == "Biomes":
            self._mark_only_button(self.biomes_buttons[5],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "swamp"
            self.ui.current_tool = "biome"
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[5],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "silver"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[5],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "red_flag"
            self.ui.current_tool = "flag"

    def _on_7(self) -> None:
        if self.ui.current_section == "Resources":
            self._mark_only_button(self.resources_buttons[6],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "gold"
            self.ui.current_tool = "resource"
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[6],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "white_flag"
            self.ui.current_tool = "flag"

    def _on_8(self) -> None:
        if self.ui.current_section == "Start positions":
            self._mark_only_button(self.flags_buttons[7],
                                   (*self.biomes_buttons, *self.resources_buttons, *self.flags_buttons, *self.tools_buttons))
            self.ui.selected_item = "yellow_flag"
            self.ui.current_tool = "flag"

    def _on_z(self) -> None:
        self.on_select_select_tool()

    def _on_x(self) -> None:
        self._on_select_remove_tool()

    def _on_c(self) -> None:
        self._on_select_back_tool()

    def _on_q(self) -> None:
        current_option_index = self.dropdown_options.index(self.ui.current_section)
        new_index = {0: 1, 1: 0, 2: 0, 3: 0}
        self.ui.current_section = self.dropdown_options[new_index[current_option_index]]
        self.redactor_type_dropdown.selected_index = new_index[current_option_index]

    def _on_tab(self) -> None:
        self.minimap_manager.update(self.changed_tiles_in_cycle)
        self.changed_tiles_in_cycle.clear()
        self.ui.do_show_minimap = not self.ui.do_show_minimap

    def on_escape(self) -> None:
        self.is_running = False
    
    def _on_use_remove_tool(self, tile: Tile) -> None:
        if self.ui.selected_item == "remove_tool":
            tile_before_act = copy.deepcopy(tile)
            self._clear_tile(tile, self.world, self.camera)
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
                if len(self.actions) > user_config.max_last_actions_len:
                    self.actions.pop(0)
                self.changed_tile_in_tick = tile

    def _on_use_biome_tool(self, tile: Tile) -> None:
        biome = self.ui.selected_item
        if biome != "water" or tile.stored_flag is None:
            tile_before_act = copy.deepcopy(tile)
            tile.type = biome
            if tile.type == "water":
                tile.stored_resource = None
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
                if len(self.actions) > user_config.max_last_actions_len:
                    self.actions.pop(0)
                self.changed_tile_in_tick = tile
            tile.draw(self.screen, self.camera)

    def _on_use_resource_tool(self, tile: Tile) -> None:
        resource = self.ui.selected_item
        if not tile.stored_flag:
            tile_before_act = copy.deepcopy(tile)
            tile.stored_resource = resource
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
                if len(self.actions) > user_config.max_last_actions_len:
                    self.actions.pop(0)
                self.changed_tile_in_tick = tile
            tile.draw(self.screen, self.camera)

    def _on_use_flag_tool(self, tile: Tile) -> None:
        flag = self.ui.selected_item
        if not tile.stored_resource:
            tile_before_act = copy.deepcopy(tile)
            if self.world.flags_tiles[flag] is not None:
                self.world.flags_tiles[flag].stored_flag = None
            self.world.flags_tiles[flag] = tile
            tile.stored_flag = flag
            if not self._is_tiles_same(tile_before_act, tile):
                self.actions.append({"before": tile_before_act, "after": tile})
                if len(self.actions) > user_config.max_last_actions_len:
                    self.actions.pop(0)
                self.changed_tile_in_tick = tile
            tile.draw(self.screen, self.camera)

    def _on_mousewheel(self, event: pygame.event) -> None:
        self.camera.handle_event(event)

    def _on_tile_click(self, tile: Tile) -> None:
        tile.selected = True
        self.world.selected_tiles.append((tile.x, tile.y))
        self.ui.update_selected_tile(tile)
        print(f"Tile: ({tile.x}, {tile.y}) - {tile.type}")

        if self.ui.current_tool == "tool" and self.ui.selected_item:
            self._on_use_remove_tool(tile)

        if (self.ui.current_section == "Biomes") and self.ui.selected_item and self.ui.current_tool == "biome":
            self._on_use_biome_tool(tile)

        elif (self.ui.current_section == "Resources") and self.ui.selected_item and self.ui.current_tool == "resource":
            self._on_use_resource_tool(tile)

        elif (self.ui.current_section == "Start positions") and self.ui.selected_item and self.ui.current_tool == "flag":
            self._on_use_flag_tool(tile)
        self.changed_tiles_in_cycle.append(tile)

    def _update_camera(self, keys, mouse_pos: tuple[int, int]) -> None:
        mouse_x, mouse_y = mouse_pos
        if not self.map_name_input_box.active:
            self.camera.update_with_mouse(mouse_x, mouse_y)
            self.camera.update_with_keyboard(keys)
        self.camera.update()

    def _draw_buttons(self, buttons_to_draw: tuple, mouse_pos: tuple[int, int]) -> None:
        for button in buttons_to_draw:
            button.check_hover(mouse_pos)
            button.draw(self.screen)

    def _draw_save_map_interface(self, mouse_pos: tuple[int, int]) -> None:
        self.map_name_input_box.active = True
        self.save_map_button.check_hover(mouse_pos)
        self.save_map_button.draw(self.screen)
        self.map_name_input_box.draw(self.screen)

    def _draw_interface(self, clock: pygame.Clock, mouse_pos: tuple[int, int]) -> None:
        if self.ui.do_show_grid:
            start_x = 0
            start_y = 0
            end_x = self.world_height
            end_y = self.world_width
            self.ui.draw_grid(self.screen, self.camera, start_x, start_y, end_x, end_y)
        if not self.ui.do_show_hud:
            return
        self.ui.draw(self.screen, self.camera)
        self.redactor_type_dropdown.draw(self.screen)
        if self.ui.do_show_brush_size_slider:
            self.brush_size_slider.draw(self.screen)
        if self.ui.current_label:
            self.screen.blit(self.ui.current_label, (self.screen_WIDTH * 0.01, self.screen_HEIGHT * 0.35))

        if self.ui.current_section == "Biomes":
            self._draw_buttons((*self.biomes_buttons, *self.tools_buttons), mouse_pos)

        elif self.ui.current_section == "Resources":
            self._draw_buttons((*self.resources_buttons, *self.tools_buttons), mouse_pos)

        elif self.ui.current_section == "Start positions":
            self._draw_buttons((*self.flags_buttons, *self.tools_buttons), mouse_pos)

        elif self.ui.current_section == "Save map":
            self._draw_save_map_interface(mouse_pos)

        fps_text = self.ui.small_font.render(f"FPS: {int(clock.get_fps())}", True, ui_elements.Colors.green)
        self.screen.blit(fps_text, (self.screen_WIDTH - 80, self.screen_HEIGHT - 25))

    def _handle_tools_buttons(self, mouse_pos: tuple[int, int]) -> None:
        if self.select_tool_button.is_clicked(mouse_pos):
            self.on_select_select_tool()
        if self.remove_tool_button.is_clicked(mouse_pos):
            self._on_select_remove_tool()
        if self.back_tool_button.is_clicked(mouse_pos):
            self._on_select_back_tool()
        if self.brush_tool_button.is_clicked(mouse_pos):
            self._on_select_brush_tool()

    def _handle_biomes_buttons(self, mouse_pos: tuple[int, int]) -> None:
        for buttn in self.biomes_buttons:
            if buttn.is_clicked(mouse_pos):
                self._mark_only_button(buttn, self.all_buttons)
                buttons2items = {self.grass_button: "grass",
                                 self.mountain_button: "mountain",
                                 self.water_button: "water",
                                 self.sand_button: "sand",
                                 self.snow_button: "snow",
                                 self.swamp_button: "swamp"}
                self.ui.selected_item = buttons2items[buttn]
                self.ui.current_tool = "biome"

    def _handle_resources_buttons(self, mouse_pos: tuple[int, int]) -> None:
        for buttn in self.resources_buttons:
            if buttn.is_clicked(mouse_pos):
                self._mark_only_button(buttn, self.all_buttons)
                buttons2items = {self.food_resource_button: "food",
                                 self.wood_resource_button: "wood",
                                 self.stone_resource_button: "stone",
                                 self.copper_resource_button: "copper",
                                 self.iron_resource_button: "iron",
                                 self.silver_resource_button: "silver",
                                 self.gold_resource_button: "gold"}
                self.ui.selected_item = buttons2items[buttn]
                self.ui.current_tool = "resource"

    def _handle_flags_buttons(self, mouse_pos: tuple[int, int]) -> None:
        for buttn in self.flags_buttons:
            if buttn.is_clicked(mouse_pos):
                self._mark_only_button(buttn, self.all_buttons)
                buttons2items = {self.aqua_flag_button: "aqua_flag",
                                 self.black_flag_button: "black_flag",
                                 self.blue_flag_button: "blue_flag",
                                 self.green_flag_button: "green_flag",
                                 self.orange_flag_button: "orange_flag",
                                 self.red_flag_button: "red_flag",
                                 self.white_flag_button: "white_flag",
                                 self.yellow_flag_button: "yellow_flag", }
                self.ui.selected_item = buttons2items[buttn]
                self.ui.current_tool = "flag"

    def _handle_hood_buttons(self, mouse_pos: tuple[int, int]) -> None:
        sections2interfaces = {"Biomes": self._handle_biomes_buttons,
                               "Resources": self._handle_resources_buttons,
                               "Start positions": self._handle_flags_buttons}
        if self.ui.current_section in sections2interfaces:
            sections2interfaces[self.ui.current_section](mouse_pos)

    def _handle_save_map_button(self, mouse_pos: tuple[int, int]) -> None:
        self.ui.current_label = None
        exists_error_label = ui_elements.Fonts.font_for_labels.render(
            "The map hasn't saved: Map with this name already exists\nPress Save button one more time to rewrite existing map",
            True, ui_elements.Colors.crimson)
        small_error_label = ui_elements.Fonts.font_for_labels.render("The map hasn't saved: Map name is too small", True,
                                                               ui_elements.Colors.crimson)
        success_label = ui_elements.Fonts.font_for_labels.render("The map was successfully saved", True,
                                                                 ui_elements.Colors.green)

        if self.save_map_button.is_clicked(mouse_pos):
            if len(self.map_name_input_box.text) == 0:
                self.ui.current_label = small_error_label
            else:
                map_name = self.map_name_input_box.text
                path_to_save = f"Saves/{map_name}.json"
                game_map = self.map_manager.encode_map(self.world.tiles)
                if self.map_manager.save_map(game_map, path_to_save) == "Map already exists":
                    if self.map_name_for_repeated_saving != map_name:
                        self.ui.current_label = exists_error_label
                        self.map_name_for_repeated_saving = map_name
                    else:
                        self.map_manager.save_map(game_map, path_to_save, is_forcedly=True)
                        self.ui.current_label = success_label
                        self.map_name_for_repeated_saving = ""
                else:
                    self.ui.current_label = success_label

    def _on_keyboard_event(self, event: pygame.Event) -> None:
        if not self.ui.do_show_minimap:
            self.map_name_input_box.handle_event(event)

            keys2acts = {
                pygame.K_ESCAPE: self.on_escape,
                pygame.K_F1: lambda: self._on_f1(),
                pygame.K_F2: lambda: self._on_f2(),
                pygame.K_F3: lambda: self._on_f3(),
                pygame.K_F4: lambda: self._on_f4(),
                pygame.K_SPACE: lambda: self._on_space(),
                pygame.K_z: lambda: self._on_z(),
                pygame.K_x: lambda: self._on_x(),
                pygame.K_c: lambda: self._on_select_back_tool(),
                pygame.K_v: lambda: self._on_select_brush_tool(),
                pygame.K_q: lambda: self._on_q(),
                pygame.K_TAB: lambda: self._on_tab(),
                pygame.K_1: lambda: self._on_1(),
                pygame.K_2: lambda: self._on_2(),
                pygame.K_3: lambda: self._on_3(),
                pygame.K_4: lambda: self._on_4(),
                pygame.K_5: lambda: self._on_5(),
                pygame.K_6: lambda: self._on_6(),
                pygame.K_7: lambda: self._on_7(),
                pygame.K_8: lambda: self._on_8(),
            }

            if event.key in keys2acts:
                keys2acts.get(event.key)()
        else:
            if event.key == pygame.K_TAB:
                self.ui.do_show_minimap = False

    def _on_mouse_click(self, mouse_pos: tuple[int, int]) -> None:
        mouse_x, mouse_y = mouse_pos

        if not self.ui.do_show_minimap:
            self._handle_tools_buttons(mouse_pos)
            self._handle_hood_buttons(mouse_pos)
            if self.ui.current_section == "Save map":
                self._handle_save_map_button(mouse_pos)

            if not(any(obj.rect.collidepoint(mouse_pos) for obj in self.scenes_objects)) and not(self.redactor_type_dropdown.item_rect.collidepoint(mouse_pos)):
                tile_x, tile_y = self.camera.screen_to_world(mouse_x, mouse_y)
                self.world.deselect_all_tiles()
                tile = self.world.get_tile_by_cords(tile_x, tile_y)
                if tile:
                    if self.brush_size > 1:
                        self._draw_with_brush(tile)
                    self._on_tile_click(tile)
        else:
            self.minimap_manager.handle_click(mouse_pos, self.camera)

    def _on_lkm_pressed(self, mouse_pos: tuple[int, int]) -> None:
        if not (any(obj.rect.collidepoint(mouse_pos) for obj in self.scenes_objects)) and not (self.redactor_type_dropdown.item_rect.collidepoint(mouse_pos)):
            tile_x, tile_y = self.camera.screen_to_world(mouse_pos[0], mouse_pos[1])
            self.world.deselect_all_tiles()
            tile = self.world.get_tile_by_cords(tile_x, tile_y)
            if tile:
                if self.brush_size > 1:
                    self._draw_with_brush(tile)
                self._on_tile_click(tile)

    def _choose_select_button(self):
        if self.ui.selected_item in ("select_tool", None) and self.ui.current_tool in ("tool", None):
            self._mark_only_button(self.select_tool_button, self.all_buttons)

    def _draw_with_brush(self, start_tile: Tile) -> None:
        self.world.deselect_all_tiles()
        start_x = max(0, start_tile.x - self.brush_size // 2)
        end_x = min(self.world_width - 1, start_tile.x + self.brush_size // 2)
        start_y = max(0, start_tile.y - self.brush_size // 2)
        end_y = min(self.world_height - 1, start_tile.y + self.brush_size // 2)
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                current_tile = self.world.get_tile_by_cords(x, y)
                self._on_tile_click(current_tile)

    def _highlight_tiles(self, mouse_pos: tuple[int, int]) -> None:
        self.world.deselect_all_tiles()
        tile_x, tile_y = self.camera.screen_to_world(mouse_pos[0], mouse_pos[1])
        tile = self.world.get_tile_by_cords(tile_x, tile_y)
        if tile:
            tile.selected = True
            self.world.selected_tiles.append((tile.x, tile.y))
        if self.brush_size > 1:
            self.world.deselect_all_tiles()
            for x in range(max(0, tile.x - self.brush_size // 2), min(self.world_width, tile.x + self.brush_size // 2 + 1)):
                for y in range(max(0, tile.y - self.brush_size // 2), min(self.world_width, tile.y + self.brush_size // 2 + 1)):
                    tile_new = self.world.get_tile_by_cords(x, y)
                    if tile_new:
                        tile_new.selected = True
                        self.world.selected_tiles.append((tile_new.x, tile_new.y))

    def _on_ticks(self) -> None:
        self.tick += 1
        if self.back_button_tick >= 0:
            if self.tick == self.back_button_tick + 12:
                self._unmark_button(self.back_tool_button)
                self.back_button_tick = -10
        if self.brush_button_tick >= 0:
            if self.tick == self.brush_button_tick + 12:
                self._unmark_button(self.brush_tool_button)
                self.brush_button_tick = -10

    def _determine_biome_for_ambient(self, mouse_x: int, mouse_y: int) -> str:
        tile_x, tile_y = self.camera.screen_to_world(mouse_x, mouse_y)
        tile = self.world.get_tile_by_cords(tile_x, tile_y)
        if tile.stored_resource == "wood":
            return "forest"
        return tile.type

    def start_game(self) -> None:
            self.screen = pygame.display.set_mode((self.screen_WIDTH, self.screen_HEIGHT))
            pygame.display.set_caption("DespEco")
            clock = pygame.time.Clock()
            self.minimap_manager.tile_map = self.world.tiles
            self.minimap_manager.redraw()
            self.ui.current_section = "Biomes"
            self._create_objects()
            self._choose_select_button()

            is_lkm_pressed = False

            while self.is_running:
                self._on_ticks()
                self.changed_tile_in_tick = None
                self.brush_size = self.brush_size_slider.current_val

                mouse_pos = pygame.mouse.get_pos()
                keys = pygame.key.get_pressed()

                self._highlight_tiles(mouse_pos)

                self.sounds_manager.randomly_play_random_theme()
                biome_for_ambient = self._determine_biome_for_ambient(mouse_pos[0], mouse_pos[1])
                self.sounds_manager.randomly_play_ambient_sound(biome_for_ambient)

                for event in pygame.event.get():
                    self.redactor_type_dropdown.handle_event(event)
                    if self.ui.do_show_brush_size_slider:
                        self.brush_size_slider.handle_event(event)

                    if event.type == pygame.QUIT:
                        self.is_running = False

                    elif event.type == pygame.KEYDOWN:
                        self._on_keyboard_event(event)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self._on_mouse_click(mouse_pos)
                            if not self.ui.do_show_minimap:
                                is_lkm_pressed = True

                    elif event.type == pygame.MOUSEBUTTONUP:
                        if not self.ui.do_show_minimap:
                            if event.button == 1:
                                is_lkm_pressed = False

                    elif event.type == pygame.MOUSEWHEEL:
                        self._on_mousewheel(event)

                if is_lkm_pressed:
                    self._on_lkm_pressed(mouse_pos)

                self._update_camera(keys, mouse_pos)
                self.world.draw(self.screen, self.camera)

                self.ui.current_section = self.redactor_type_dropdown.get_selected_option()
                self.map_name_input_box.active = False
                if not self.ui.do_show_minimap:
                    self._draw_interface(clock, mouse_pos)
                else:
                    is_lkm_pressed = False
                    self.minimap_manager.draw(self.screen, self.camera)

                pygame.display.flip()
                clock.tick(self.FPS)

            pygame.quit()
            print("\nGame over")