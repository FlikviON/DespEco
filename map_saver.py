from tile import Tile


class MapSaver:
    def __init__(self) -> None:
        self.tiles2digits: dict = {"grass": 0, "mountain": 1, "water": 2, "sand": 3, "snow": 4, "swamp": 5}
        self.resources2digits: dict = {None: 0, "food": 1, "wood": 2, "stone": 3, "copper": 4, "iron": 5, "silver": 6, "gold": 7}

    def code_maps(self, tiles_map: list[list[Tile]]) -> dict:
        width = len(tiles_map)
        height = len(tiles_map[0])
        terrain_map = [[0 for _ in range(width)] for _ in range(height)]
        resources_map = [[0 for _ in range(width)] for _ in range(height)]
        for x in range(width):
            for y in range(height):
                current_tile = tiles_map[y][x]
                terrain_map[y][x] = self.tiles2digits[current_tile.type]
                resources_map[y][x] = self.resources2digits[current_tile.stored_resource]
        maps = {"terrain_map": terrain_map, "resources_map": resources_map}
        return maps

