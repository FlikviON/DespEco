import json
from dataclasses import dataclass


@dataclass
class UserConfig:
    screen_width: int = 1600
    screen_height: int = 1000


def initialize_config() -> None:
    with open("user_config.json") as file:
        user_config_file = json.load(file)
        user_config.screen_width = user_config_file["screen"]["width"]
        user_config.screen_height = user_config_file["screen"]["height"]


user_config = UserConfig()
initialize_config()

