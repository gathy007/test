from PyQt5.QtCore import QRect

class WorldMap:
    def __init__(self, width, height, tile_size=64):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.current_x = 0
        self.current_y = 0

        # エリアマップの定義（エリアID or 地名）
        self.areas = {
            (0, 0): "grassland",
            (1, 0): "desert",
            (0, 1): "forest",
            (1, 1): "volcano",
        }

    def get_current_area(self):
        return self.areas.get((self.current_x, self.current_y), "unknown")

    def move_if_needed(self, player_x, player_y, screen_width, screen_height):
        # 画面端に到達したかを判定し、エリアを変更する
        moved = False
        new_player_x = player_x
        new_player_y = player_y
        if player_x <= 0 and self.current_x > 0:
            self.current_x -= 1
            new_player_x = screen_width - self.tile_size
            moved = True
        elif player_x + self.tile_size >= screen_width and self.current_x < self.width - 1:
            self.current_x += 1
            new_player_x = 0
            moved = True
        if player_y <= 0 and self.current_y > 0:
            self.current_y -= 1
            new_player_y = screen_height - self.tile_size
            moved = True
        elif player_y + self.tile_size >= screen_height and self.current_y < self.height - 1:
            self.current_y += 1
            new_player_y = 0
            moved = True

        return moved, new_player_x, new_player_y
