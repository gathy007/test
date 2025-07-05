from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout,QSpacerItem, QSizePolicy, QToolTip
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QRect
from sound import play_se 
import os

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # カーソルを合わせると枠線を表示
        self.setStyleSheet("""
            QLabel {
                border: 2px solid transparent;
                border-radius: 5px;
            }
            QLabel:hover {
                border: 2px solid #0078D7;
                background-color: #eef;
            }
        """)

    def mousePressEvent(self, event):
        self.clicked.emit()
    def setToolTip(self, text):
        super().setToolTip(text)
        self._tooltip_text = text

    def enterEvent(self, event):
        # マウスが入ったら即座にツールチップを表示
        QToolTip.showText(self.mapToGlobal(self.rect().bottomRight()), self._tooltip_text, self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        # マウスが出たらツールチップを消す
        QToolTip.hideText()
        super().leaveEvent(event)

class InventoryWindow(QWidget):
    def __init__(self, parent=None, character=None, inventory=None, on_inventory_updated=None):
        super().__init__(parent)
        self.setFixedSize(500, 150)
        self.setWindowTitle("所持アイテム")
        self.setStyleSheet("background-color: #ddd;")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.character = character  # キャラクターへの参照（useで必要）
        self.inventory = inventory or []  # インベントリの実体
        self.on_inventory_updated = on_inventory_updated   
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def update_inventory(self, inventory):
        self.inventory = inventory
        self.clear_layout(self.layout)

        self.inventory.sort(key=lambda item: item.no)

        counts = {}
        for item in self.inventory:
            counts[item.name] = counts.get(item.name, 0) + 1

        displayed = set()
        for item in self.inventory:
            if item.name in displayed:
                continue
            displayed.add(item.name)

            if os.path.exists(item.image_path):
                pixmap = QPixmap(item.image_path)
            else:
                pixmap = QPixmap()

            #画像クリックで使用できるようにする（画像設定）
            icon_label = ClickableLabel()     #↓画像自体の大きさ
            icon_label.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            icon_label.setAlignment(Qt.AlignCenter)
            #画像を表示する箱の大きさ
            icon_label.setFixedSize(64, 64)

            # item をスコープに閉じ込めておく（lambda late-binding 問題回避）
            def on_click(item=item, widget=icon_label):
                healed = item.use(self.character)
                if healed > 0:
                    play_se("use")
                    self.parent().hp_window.update_hp(self.character.hp, self.character.max_hp)
                    self.parent().show_message(f"{item.name} を使用して HP を {healed} 回復しました。")
                    
                    # インベントリから1個削除
                    for i, inv_item in enumerate(self.inventory):
                        if inv_item.name == item.name:
                            del self.inventory[i]
                            break
                    self.update_inventory(self.inventory)  # 表示更新
                    if self.on_inventory_updated:
                        self.on_inventory_updated()
                else:
                    play_se("nouse")
                    self.parent().show_message("HPが全快なので使用できません")

            icon_label.clicked.connect(on_click)
            #カーソルを合わせると表示される説明
            icon_label.setToolTip(f"{item.name}\n効果: HPを{item.heal_amount}回復")

            #個数ラベルの設定
            count_label = QLabel(str(counts[item.name]))
            count_label.setStyleSheet("""
                QLabel {
                    background-color: transparent;
                }
            """)
            count_label.setFont(QFont("Arial", 13, QFont.Bold))
            count_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

            #コンテナに画像とラベルを重ねる
            container = QWidget()
            container.setFixedSize(64, 64) 
            grid = QGridLayout(container)
            grid.setContentsMargins(0, 0, 0, 0)
            grid.addWidget(icon_label, 0, 0)

            #個数ラベルの位置調整
            count_label.setContentsMargins(5, 5, 5, 5)
            grid.addWidget(count_label, 0, 0, alignment=Qt.AlignRight | Qt.AlignTop)

            self.layout.addWidget(container)