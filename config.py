import json
from dataclasses import dataclass


@dataclass
class UserConfig:
    screen_width: int = 1600
    screen_height: int = 1000

    max_last_actions_len: int = 64


def initialize_config() -> None:
    with open("user_config.json") as file:
        user_config_file = json.load(file)

        user_config.screen_width = user_config_file["screen"]["width"]
        user_config.screen_height = user_config_file["screen"]["height"]

        user_config.max_last_actions_len = user_config_file["redactor"]["max_last_actions_len"]


user_config = UserConfig()
initialize_config()

