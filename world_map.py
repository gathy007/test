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
            ["ruins","ruins","ruins","ruins","village","village","graveyard","graveyard","graveyard","graveyard","village","village","forest","forest","forest","forest","forest","ruins","ruins","ruins","ruins"],
            ["ruins","ruins","ruins","ruins", "village", "graveyard", "graveyard", "graveyard",  "graveyard", "graveyard",  "village",  "village","forest","forest", "village", "village", "forest", "ruins", "ruins", "ruins", "ruins"],
            ["ruins","ruins","ruins","ruins","graveyard","graveyard","graveyard","graveyard","graveyard","graveyard","graveyard","graveyard","forest","forest", "village", "village", "village", "ruins", "ruins", "ruins", "ruins"],
            ["ruins","ruins","ruins","ruins","graveyard","graveyard","graveyard","graveyard","graveyard","graveyard","graveyard","village","forest","forest", "village","village","village", "village", "village", "ruins", "forest"],
            ["village","village","village","village","graveyard", "graveyard", "graveyard", "graveyard", "graveyard", "graveyard","village","village","forest","forest","village","village","village","village","forest","forest","forest"],
            ["village","village","village","village","village","graveyard","graveyard","graveyard","village","village","village",  "forest","forest","forest", "village", "village", "village", "village", "village", "forest", "forest"],
            ["village","forest","forest","village","village","village","village","village","village","forest","village","grassland","forest","forest","forest","forest", "village", "village", "village", "forest", "forest"],
            ["village","forest","village","village","forest","forest","village","grassland","grassland","forest","grassland","grassland","forest","forest", "forest", "forest", "forest", "forest", "forest", "forest", "forest"],
            ["forest","forest","forest","village", "village", "forest", "village", "forest", "grassland", "grassland","grassland","grassland","grassland","forest", "forest", "forest", "forest", "forest", "grassland", "forest", "grassland"],
            ["forest","forest","forest","forest","forest","forest","forest","forest","grassland","grassland","grassland","grassland","grassland","grassland", "forest", "forest", "grassland", "forest", "grassland", "grassland", "grassland"],
            ["forest","graveyard","graveyard","forest","forest","forest","grassland","grassland","grassland","grassland","grassland","grassland","grassland","grassland", "grassland", "grassland", "grassland", "grassland", "grassland", "grassland", "grassland"],
            ["graveyard","forest","graveyard","forest","graveyard","graveyard","forest","grassland","grassland","grassland","grassland","grassland","grassland","grassland", "grassland", "grassland", "grassland", "village", "grassland", "village", "grassland"],
            ["forest",  "forest","ruins","ruins", "ruins", "graveyard", "forest", "forest", "grassland", "grassland","grassland","grassland","grassland","forest", "forest", "forest", "village", "village", "grassland", "village", "grassland"],
            ["forest","ruins","ruins","ruins","ruins","ruins","ruins","forest","forest","grassland","grassland","grassland","forest","village", "village", "village", "village", "village", "village", "village", "village"],
            ["ruins","ruins","ruins","ruins","ruins","ruins","ruins","forest","forest","forest","grassland","forest","forest","forest", "castle", "castle", "castle", "village", "volcano", "volcano", "volcano"],
            ["ruins","ruins","ruins","ruins","ruins","graveyard","forest","forest","castle","forest","forest","forest","forest","volcano", "castle","castle", "castle", "volcano", "volcano", "volcano", "volcano"],
            ["graveyard","graveyard","graveyard","graveyard", "graveyard", "graveyard", "graveyard", "castle", "castle", "castle","graveyard","forest","village","volcano", "castle", "castle", "castle", "volcano", "volcano", "volcano", "volcano"],
            ["graveyard","graveyard","graveyard","graveyard","graveyard","graveyard","castle","castle","castle","castle","castle","village","village","volcano", "volcano", "volcano", "volcano", "volcano", "volcano", "volcano", "volcano"],
            ["graveyard","graveyard","graveyard","graveyard","graveyard","castle","castle","castle","castle","castle","castle","village","village","village","volcano", "volcano", "volcano", "volcano", "volcano", "volcano", "volcano"],
            ["graveyard","graveyard","graveyard","graveyard","castle","castle","castle","castle","castle","castle","castle","graveyard","graveyard","village","volcano", "volcano", "volcano", "volcano", "volcano", "volcano", "volcano"],
            ["graveyard","graveyard","graveyard","graveyard","graveyard","castle","castle","castle","castle","castle","castle","castle","castle","village", "village", "volcano", "volcano", "volcano", "volcano", "volcano", "volcano"],
       
        ]

        self.areas = {}
        for y, row in enumerate(map_layout):
            for x, name in enumerate(row):
                if name:
                    self.areas[(x, y)] = name
        self.map_objects = {
            (10, 10): "inn0",
            (19, 11): "inn1",
            (17, 3): "inn2",
            (1, 1): "inn3",
            (0, 16): "inn4",
            (7, 19): "inn5",
            (19, 18): "inn6",
            (13, 11): "dungeon0",
            (13, 4): "dungeon1",
            (16, 2): "dungeon2",
            (6, 3): "dungeon3",
            (0, 2): "dungeon4",
            (10, 20): "dungeon5",
            (20, 20): "dungeon6",
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
