from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt

class WorldMapWindow(QMainWindow):
    def __init__(self, world_map, parent=None):
        super().__init__(parent)
        self.setWindowTitle("World Map")
        self.world_map = world_map
        self.tile_size = 24
        self.setFixedSize(self.tile_size * world_map.map_width, self.tile_size * world_map.map_height)
        self.setWindowFlags(Qt.Tool | Qt.WindowStaysOnTopHint)

        self.object_icons = {
            "inn0": QPixmap("assets/shop/INN0.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "inn1": QPixmap("assets/shop/INN1.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "inn2": QPixmap("assets/shop/INN2.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "inn3": QPixmap("assets/shop/INN3.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "inn4": QPixmap("assets/shop/INN4.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "inn5": QPixmap("assets/shop/INN5.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "inn6": QPixmap("assets/shop/INN6.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),            
            "dungeon0": QPixmap("assets/dungeon/dungeon0.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "dungeon1": QPixmap("assets/dungeon/dungeon1.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "dungeon2": QPixmap("assets/dungeon/dungeon2.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "dungeon3": QPixmap("assets/dungeon/dungeon3.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "dungeon4": QPixmap("assets/dungeon/dungeon4.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "dungeon5": QPixmap("assets/dungeon/dungeon5.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
            "dungeon6": QPixmap("assets/dungeon/dungeon6.png").scaled(18, 18, Qt.KeepAspectRatio, Qt.SmoothTransformation),
        }

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        #マップの初期位置
        screen_geometry = self.screen().geometry()
        x = screen_geometry.width() - self.width() - 50
        y = 50
        self.move(x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)

        area_colors = {
            "town": QColor(203, 133, 27),
            "grassland": QColor(144, 238, 144),
            "forest": QColor(34, 139, 34),
            "village": QColor(224, 129, 104),
            "graveyard": QColor(105, 105, 105),
            "ruins": QColor(169, 169, 169),
            "castle": QColor(249, 204, 68),
            "volcano": QColor(255, 69, 0),
        }

        for y in range(self.world_map.map_height):
            for x in range(self.world_map.map_width):
                rect_x = x * self.tile_size
                rect_y = y * self.tile_size

                #現在位置をハイライト
                if (x, y) == (self.world_map.current_x, self.world_map.current_y):
                    rect_color = QColor(100, 200, 255)
                else:
                    area_name = self.world_map.areas.get((x, y), "")
                    rect_color = area_colors.get(area_name, QColor(200, 200, 200)) 

                painter.fillRect(rect_x, rect_y, self.tile_size, self.tile_size, rect_color)
                painter.drawRect(rect_x, rect_y, self.tile_size, self.tile_size)

                obj_name = self.world_map.map_objects.get((x, y), "")
                #オブジェクトのアイコン表示
                icon = self.object_icons.get(obj_name)
                if icon:
                    icon_x = rect_x + (self.tile_size - icon.width()) // 2
                    icon_y = rect_y + (self.tile_size - icon.height()) // 2
                    painter.drawPixmap(icon_x, icon_y, icon)
                #ダンジョンやオブジェクトのネーム表示
                #label = obj_name or area_name
                #if label:
                #     painter.drawText(rect_x + 4, rect_y + 16, label)

    def closeEvent(self, event):
        event.ignore()
        self.hide()  