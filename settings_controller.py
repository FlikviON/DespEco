from config import user_config


class SettingsController:
    def __init__(self) -> None:
        ...

    @staticmethod
    def change_resolution(new_screen_resolution: tuple[int, int]) -> None:
        print(new_screen_resolution)
        user_config.screen_width = new_screen_resolution[0]
        user_config.screen_height = new_screen_resolution[1]
