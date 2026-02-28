from PIL import Image


class MinimapFormer:
    def __init__(self) -> None:
        self.game_map: list[list[int]] | None = None
        self.types2colors: dict = {0: (112, 134, 50), 1: (75, 90, 112), 2: (40, 148, 170), 3: (240, 200, 135), 4: (200, 200, 200), 5: (92, 86, 60)}

    def draw_minimap(self, game_map: list[list[int]]) -> Image:
        self.game_map = game_map
        width = height = len(self.game_map)
        image = Image.new("RGB", (width, height), color = "black")
        pixels = image.load()
        for x in range(width):
            for y in range(height):
                pixels[x, y] = self.types2colors[self.game_map[y][x]]
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

'''
minmap = [[1, 1, 1], [2, 2, 1], [3, 5, 5]]
mapa = MinimapFormer(minmap)
mapula = mapa.draw_minimap()
mapula = mapa.resize_minimap(mapula)
mapa.save_minimap(mapula)
'''