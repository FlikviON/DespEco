import pygame

import ui_elements
from config import user_config


button_width, button_height = 100, 100
dropdown_width, dropdown_height = 200, 32
dropdown_options = ["Biomes", "Resources", "Start positions", "Save map"]

pygame.init()

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
    button_height * 0.8,
    "Save Map",
    (255, 127, 80),
(233, 105, 58)
)

map_name_input_box = ui_elements.InputBox(
    10,
    user_config.screen_height // 2 - 200,
    dropdown_width * 1.5,
    dropdown_height,
    "Map name: ",
    max_length=15
)

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

brush_tool_button = ui_elements.ImagedButton(
    user_config.screen_width // 2 - button_width // 2 - 768,
    user_config.screen_height // 2 + 290,
    button_width,
    button_height,
    image_path="Assets/ToolsButtons/Light/brush_tool.png",
    hover_image_path="Assets/ToolsButtons/Dark/brush_tool.png"
)

brush_size_slider = ui_elements.VerticalSlider(
    user_config.screen_width * 0.14,
    user_config.screen_height * 0.03,
    width=20,
    height=1000,
    min_val=0,
    max_val=50,
    start_val=1,
    step=2,
    track_color=(200, 191, 231),
    thumb_color=ui_elements.Colors.blue
)
