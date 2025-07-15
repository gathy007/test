from PyQt5.QtCore import QRect

class WorldMap:
    def __init__(self, map_width, map_height, tile_size=64):
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
        self.current_x = 0
        self.current_y = 0

        #エリアマップの定義（2Dで設定できる、エリアの広さはmain.pyのself.world_mapで設定）
        map_layout = [
            [     "town",  "grassland",    "forest",   "grassland", "grassland", "grassland", "grassland", "grassland", "grassland", "grassland"],
            ["grassland",  "grassland",    "forest",       "ruins",          "",          "",          "",          "",          "",          ""],
            [   "forest",     "forest",    "forest",       "ruins",          "",          "",          "",          "",          "",          ""],
            ["graveyard",  "graveyard",     "ruins",       "ruins",   "volcano",          "",          "",          "",          "",          ""],
        ]

        self.areas = {}
        for y, row in enumerate(map_layout):
            for x, name in enumerate(row):
                if name:
                    self.areas[(x, y)] = name
        self.map_objects = {
            (4, 3): "inn",
            (2, 1): "dungeon1",
            (4, 2): "dungeon2",
        }
    def get_map_object(self, x, y):
        return self.map_objects.get((x, y), None)

    def get_current_area(self):
        return self.areas.get((self.current_x, self.current_y), "unknown")

    def move_if_needed(self, player_x, player_y, screen_width, screen_height):
        # 画面端に到達したかを判定し、エリアを変更する
        moved = False
        new_player_x = player_x
        new_player_y = player_y
        edge_margin = 1  
        if hasattr(self, "world_map_window") and self.world_map_window.isVisible():
            self.world_map_window.update()

        if player_x <= 0 and self.current_x > 0:
            self.current_x -= 1
            new_player_x = screen_width - self.tile_size- edge_margin
            moved = True
        elif player_x + self.tile_size >= screen_width and self.current_x < self.map_width - 1:
            self.current_x += 1
            new_player_x = edge_margin
            moved = True
        if player_y <= 0 and self.current_y > 0:
            self.current_y -= 1
            new_player_y = screen_height - self.tile_size - edge_margin
            moved = True
        elif player_y + self.tile_size >= screen_height and self.current_y < self.map_height - 1:
            self.current_y += 1
            new_player_y = edge_margin
            moved = True

        return moved, new_player_x, new_player_y
