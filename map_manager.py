import json
from pathlib import Path

from tile import Tile


class MapManager:
    def __init__(self) -> None:
        self.terrain2digits: dict = {"grass": 10, "mountain": 11, "water": 12, "sand": 13, "snow": 14, "swamp": 15}
        self.resources2digits: dict = {None: 10, "food": 11, "wood": 12, "stone": 13, "copper": 14, "iron": 15, "silver": 16, "gold": 17}

        self.digits2terrain: dict = {self.terrain2digits[item]: item for item in self.terrain2digits}
        self.digits2resources: dict = {self.resources2digits[item]: item for item in self.resources2digits}

    def encode_map(self, tiles_map: list[list[Tile]]) -> list[list[int]]:
        width = len(tiles_map[0])
        height = len(tiles_map)
        game_map = [[0 for _ in range(width)] for _ in range(height)]
        for x in range(width):
            for y in range(height):
                current_tile = tiles_map[y][x]
                current_string = f"{self.terrain2digits[current_tile.type]}{self.resources2digits[current_tile.stored_resource]}"
                game_map[y][x] = int(current_string)
        return game_map

    def update_map(self, game_map: list[list[int]], tile: Tile) -> list[list[int]]:
        x, y = tile.x, tile.y
        current_string = f"{self.terrain2digits[tile.type]}{self.resources2digits[tile.stored_resource]}"
        game_map[y][x] = int(current_string)
        return game_map

    @staticmethod
    def save_map(game_map: list[list[int]], path_to_save: str = "Saves/map.txt") -> None:
        with open(path_to_save, "w") as file:
            json.dump(game_map, file, indent=4)

    @staticmethod
    def load_map(map_name: str):
        path_to_map = Path(f"Saves/{map_name}.json")
        with open(path_to_map, "r") as file:
            game_map = json.load(file)
        return game_map

    def decode_map(self, game_map: list[list[int]]) -> list[list[Tile]]:
        width = len(game_map[0])
        height = len(game_map)
        tile_map = [[None for _ in range(width)] for _ in range(height)]
        for x in range(width):
            for y in range(height):
                current_string = str(game_map[y][x])

                terrain_suffix = int(current_string[0:2])
                resource_suffix = int(current_string[2:4])
                current_terrain = self.digits2terrain[terrain_suffix]
                current_resource = self.digits2resources[resource_suffix]

                current_tile = Tile(x, y, tile_type = current_terrain, stored_resource=current_resource)
                tile_map[y][x] = current_tile
        return tile_map
