from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from sound import play_se
from dungeons import DUNGEONS
from shop_window import ShopWindow
from save_manager import save_game

class InnWindow(QWidget):
    def __init__(self, parent=None, on_dungeon_selected=None, on_return_home=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.setFixedSize(300, 300)
        self.setWindowTitle("INN")
        self.setStyleSheet("background-color: #f0e4d7;")
        self.on_dungeon_selected = on_dungeon_selected
        self.on_return_home = on_return_home
        self.setFocusPolicy(Qt.StrongFocus)
        self.buttons = []

        layout = QVBoxLayout()

        self.label = QLabel("ようこそ！宿屋へ！\n休むとHPが全回復します。")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        for dungeon_name, dungeon_data in DUNGEONS.items():
            dungeon_key = dungeon_data.get("dungeon_key", dungeon_name)
            if dungeon_key in self.parent().unlocked_dungeons:
                button = QPushButton(dungeon_data["display_name"])
                button.clicked.connect(lambda _, key=dungeon_key: self.select_dungeon(key))
                layout.addWidget(button)
                self.buttons.append(button)
        
        self.shop_button = QPushButton("ショップに入る")
        self.shop_button.clicked.connect(self.open_shop)
        layout.addWidget(self.shop_button)
        self.buttons.append(self.shop_button)

        self.rest_button = QPushButton("休む")
        self.rest_button.clicked.connect(self.rest)
        layout.addWidget(self.rest_button)
        self.buttons.append(self.rest_button)

        self.home_button = QPushButton("ホームに戻る")  
        self.home_button.clicked.connect(self.return_home)
        layout.addWidget(self.home_button)
        self.buttons.append(self.home_button)

        self.close_button = QPushButton("閉じる")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)
        self.buttons.append(self.close_button)

        self.setLayout(layout)
        if hasattr(self.parent(), "character") and hasattr(self.parent(), "inventory_window"):
            self.shop_window = ShopWindow(self.parent().character, self.parent().inventory_window, main_window=self.parent())
            self.shop_window.hide()
        self.current_index = 0
        self.update_button_focus()

    def showEvent(self, event):
        super().showEvent(event)
        self.setFocus()  # ウィンドウ全体にフォーカスを強制的にあてる
        self.update_button_focus()
    #フォーカスしたボタンの色変える
    def update_button_focus(self):
        for i, btn in enumerate(self.buttons):
            if i == self.current_index:
                btn.setStyleSheet("background-color: #a0c0ff;")
            else:
                btn.setStyleSheet("")
    #ボタンの移動処理
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_W:
            self.current_index = (self.current_index - 1) % len(self.buttons)
            self.update_button_focus()
            event.accept()
        elif event.key() == Qt.Key_Down or event.key() == Qt.Key_S:
            self.current_index = (self.current_index + 1) % len(self.buttons)
            self.update_button_focus()
            event.accept()
        elif event.key() == Qt.Key_Space:
            self.buttons[self.current_index].click()
            event.accept()
        elif event.key() == Qt.Key_Escape:
            self.close()
            event.accept()
        else:
            super().keyPressEvent(event)
    #休む処理
    def rest(self):
        if hasattr(self.parent(), 'character'):
            character = self.parent().character
            character.hp = character.max_hp
            character.mp = character.max_mp
            if hasattr(self.parent(), 'hp_window'):
                self.parent().hp_window.update_hp(character.hp, character.max_hp)
                self.parent().hp_window.update_mp(character.mp, character.max_mp)
                self.parent().hp_window.show_message("HPとMPが全回復した！")
            if hasattr(self.parent(), 'monsters'):
                self.parent().monsters.clear()
            #セーブ処理追加
            defeated_bosses = getattr(self.parent(), 'defeated_bosses', [])
            defeated_monsters = getattr(self.parent(), 'defeated_monsters', set())
            monster_kill_count = getattr(self.parent(), 'monster_kill_count', {})
            unlocked_dungeons = getattr(self.parent(), 'unlocked_dungeons', set())
            inventory = getattr(character, 'inventory', [])
            current_area_level = getattr(self.parent(), "current_area_level", 1)
            world_map = getattr(self.parent(), 'world_map', None)
            if world_map:
                world_map_x = world_map.current_x
                world_map_y = world_map.current_y
            else:
                world_map_x = 0
                world_map_y = 0

            save_game(
                character,
                world_map_x,
                world_map_y,
                current_area_level,
                defeated_bosses,
                defeated_monsters,
                monster_kill_count,
                unlocked_dungeons,
                inventory,
            )
            if hasattr(self.parent(), 'hp_window'):
                self.parent().hp_window.show_message("ゲームをセーブしました")
        play_se("heal")
        self.close()
    #ホームに戻る処理
    def return_home(self):
        play_se("dungeon")
        if self.on_return_home:
            self.on_return_home()
        self.close()
    #ダンジョンに入る処理
    def select_dungeon(self, dungeon_key):
        play_se("dungeon")
        if self.on_dungeon_selected:
            self.on_dungeon_selected(dungeon_key)
        self.close()
    #ショップを開く処理
    def open_shop(self):
        play_se("window_open")
        if hasattr(self.parent(), "character") and hasattr(self.parent(), "inventory_window"):
            if self.shop_window.isVisible():
                self.shop_window.hide()
            else:
                self.shop_window = ShopWindow(self.parent().character, self.parent().inventory_window, main_window=self.parent())
                self.shop_window.show()
                self.shop_window.raise_()
                self.shop_window.activateWindow()
    def closeEvent(self, event):
        if hasattr(self, "shop_window") and self.shop_window.isVisible():
            self.shop_window.hide()
        super().closeEvent(event)
