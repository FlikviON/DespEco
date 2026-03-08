import math

from PIL import Image


class MinimapFormer:
    def __init__(self) -> None:
        self.game_map: list[list[int]] | None = None
        self.types2colors: dict = {10: (112, 134, 50), 11: (75, 90, 112), 12: (40, 148, 170), 13: (240, 200, 135), 14: (200, 200, 200), 15: (92, 86, 60)}

    def draw_minimap(self, game_map: list[list[int]]) -> Image:
        self.game_map = game_map
        width = height = len(self.game_map)

        receptive_field_x = math.floor(width / 200) if width > 200 else 1
        receptive_field_y = math.floor(height / 80) if height > 200 else 1

        image = Image.new("RGB", (width // receptive_field_x + 1, height // receptive_field_y + 1), color = "black")
        pixels = image.load()

        for x in range(0, width, receptive_field_x):
            for y in range(0, height, receptive_field_y):
                pixels[x // receptive_field_x, y // receptive_field_y] = self.types2colors[int(str(self.game_map[y][x])[:2])]
        return image

    @staticmethod
    def resize_minimap(minimap: Image) -> Image:
        return minimap.resize((400, 200), resample=0)

    @staticmethod
    def save_minimap(minimap: Image, path: str="Assets/Images/Minimap/current_minimap.png") -> None:
        minimap.save(path)

    def do_pipeline(self, game_map: list[list[int]]) -> None:
        img = self.draw_minimap(game_map)
        img = self.resize_minimap(img)
        self.save_minimap(img)