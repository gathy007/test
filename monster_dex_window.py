from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QGridLayout, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MonsterDexWindow(QMainWindow):
    def __init__(self, defeated_monsters, monster_data, monster_folder, main_window=None):
        super().__init__(main_window)
        self.setWindowTitle("モンスター図鑑")
        self.setFixedSize(600, 600)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        self.defeated_monsters = defeated_monsters
        self.monster_data = monster_data
        self.monster_folder = monster_folder

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.scroll = QScrollArea()
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout()
        self.grid_widget.setLayout(self.grid_layout)
        self.scroll.setWidget(self.grid_widget)
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        # 最初の描画をメソッド化して呼ぶ
        self.refresh_grid()

    def refresh_grid(self):
        # 既存のレイアウトをクリアする
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        sorted_monsters = sorted(
            self.monster_data.items(),
            key=lambda item: item[1].get("dex_number", 999)
        )

        for i, (filename, data) in enumerate(sorted_monsters):
            row = i // 4
            col = i % 4

            image_label = QLabel()
            name = data.get("display_name", "？？？")

            if filename in self.defeated_monsters:
                pixmap = QPixmap(f"{self.monster_folder}/{filename}").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                hp = data.get("hp", "?")
                exp = data.get("exp", "?")
                coin = data.get("coin", "?")
                attack_power = data.get("attack_power", "?")           
            else:
                pixmap = QPixmap(64, 64)
                pixmap.fill(Qt.black)
                hp = exp = coin = attack_power = "？"

            #画像ラベル
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            #名前ラベル
            name_label = QLabel(name if filename in self.defeated_monsters else "？？？")
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setStyleSheet("font-size: 12px;")
            name_label.setFixedSize(100 , 10)
            #ステータスラベルを作成（HP, EXP, Coin, Attack）
            status_text = f"HP：{hp}\nEXP：{exp}\nコイン：{coin}\n攻撃力：{attack_power}"
            status_label = QLabel(status_text)
            status_label.setAlignment(Qt.AlignCenter)
            status_label.setStyleSheet("font-size: 12px;")
            status_label.setFixedSize(100 , 48)
            #画像・名前・ステータスをまとめるレイアウト
            box = QVBoxLayout()
            box_widget = QWidget()
            box.addWidget(image_label)
            box.addWidget(name_label)
            box.addWidget(status_label)
            box_widget.setLayout(box)
            box_widget.setFixedSize(120, 160)

            self.grid_layout.addWidget(box_widget, row, col)

    def update_dex(self, defeated_monsters):
        self.defeated_monsters = defeated_monsters
        self.refresh_grid()

    def closeEvent(self, event):
        event.ignore()
        self.hide()  