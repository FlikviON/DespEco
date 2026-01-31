import json
from dataclasses import dataclass


@dataclass
class UserConfig:
    screen_width: int = 800
    screen_height: int = 600


def initialize_config():
    with open("user_config.json") as file:
        user_config = json.load(file)
        UserConfig.screen_width = user_config["screen"]["width"]
        UserConfig.screen_height = user_config["screen"]["height"]