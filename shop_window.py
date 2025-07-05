from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from items import ITEMS
from sound import play_se

class ShopWindow(QWidget):
    def __init__(self, character, inventory_window, main_window=None):
        super().__init__(None)
        self.main_window = main_window
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.character = character
        self.inventory_window = inventory_window
        self.setWindowTitle("ショップ")
        self.setFixedSize(320, 400)
        main_layout = QVBoxLayout()

        main_layout.addWidget(QLabel("いらっしゃい！ポーションはいかが？"))
        # スクロール領域を作成
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # 内容のサイズに合わせてスクロール可能に

        # スクロールの中に置くウィジェット（アイテム一覧コンテナ）
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        for item_key, item in ITEMS.items():
            # アイテム毎の縦レイアウトを作成
            item_layout = QVBoxLayout()

            # 画像ラベル
            image_label = QLabel()
            pixmap = QPixmap(item.image_path).scaled(32, 32, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            item_layout.addWidget(image_label)

            # 名前ラベル
            name_label = QLabel(item.name)
            name_label.setAlignment(Qt.AlignCenter)
            item_layout.addWidget(name_label)

            # 説明ラベル
            desc_label = QLabel(item.description)
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignCenter)
            item_layout.addWidget(desc_label)

            # 「購入」ボタン
            buy_button = QPushButton(f"買う ({item.price} G)")
            buy_button.clicked.connect(lambda _, key=item_key: self.buy_item(key))
            item_layout.addWidget(buy_button)

            # メインレイアウトに追加
            scroll_layout.addLayout(item_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def buy_item(self, item_key):
        item = ITEMS[item_key]
        if self.character.coins >= item.price:
            self.character.coins -= item.price
            self.character.inventory.append(item)
            self.inventory_window.update_inventory(self.character.inventory)
            if self.main_window and hasattr(self.main_window, "hp_window"):
                self.main_window.hp_window.update_coin(self.character.coins)
                play_se("buy")
        else:
            if self.main_window and hasattr(self.main_window, "hp_window"):
                self.main_window.hp_window.show_message("コインが足りません！")
            play_se("nouse")
    def closeEvent(self, event):
        self.hide()  #閉じるのではなく隠す
        event.ignore() 
