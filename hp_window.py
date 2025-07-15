from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QMessageBox,QMainWindow, QToolBar, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from sound import play_se, stop_bgm
from settings_window import SettingsWindow

class HPWindow(QMainWindow):
    def __init__(self, parent=None, save_callback=None, character=None, defeated_bosses=None, defeated_monsters=None, monster_kill_count=None, return_to_menu_callback=None, unlocked_dungeons=None, inventory=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.save_callback = save_callback
        self.return_to_menu_callback = return_to_menu_callback
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.character = character
        self.defeated_bosses = defeated_bosses
        self.defeated_monsters = defeated_monsters
        self.monster_kill_count = monster_kill_count
        self.unlocked_dungeons = unlocked_dungeons if unlocked_dungeons is not None else []
        self.inventory = inventory
        
        self.setWindowTitle("ステータス")
        self.setGeometry(100, 100, 300, 300)

        self.title_label = QLabel("ステータス", self)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.hp_label = QLabel("現在のHP", self)
        self.mp_label = QLabel("現在のMP", self)
        self.exp_label = QLabel("現在のレベルと経験値", self)
        self.coin_label = QLabel("現在のコイン", self)
        self.status_label = QLabel("ステータス", self)

        self.msg_log = QTextEdit(self)
        self.msg_log.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.hp_label)
        layout.addWidget(self.mp_label)
        layout.addWidget(self.exp_label)
        layout.addWidget(self.coin_label) 
        layout.addWidget(self.status_label)
        layout.addWidget(self.msg_log)

        central_widget.setLayout(layout)

        #ツールバー作成
        toolbar = QToolBar("メインツールバー")
        self.addToolBar(toolbar)
        #終了ボタン
        exit_action = QAction(QIcon(), "終了", self)
        exit_action.triggered.connect(self.handle_exit)
        toolbar.addAction(exit_action)

        #セーブボタン
        save_action = QAction(QIcon(), "セーブ", self)
        save_action.triggered.connect(self.handle_save)
        toolbar.addAction(save_action)

        #設定（音量）ボタン
        settings_action = QAction(QIcon(), "音量", self)
        settings_action.triggered.connect(self.open_settings)
        toolbar.addAction(settings_action)

        # ヘルプボタン
        help_action = QAction(QIcon(), "ヘルプ", self)
        help_action.triggered.connect(self.show_help)
        toolbar.addAction(help_action)     

        # 設定ウィンドウのインスタンス（まだ開かない）
        self.settings_window = None       

        self.show()
    #ステータスウィンドウ上でのゲーム終了
    def handle_exit(self):
        play_se("window_open")
        reply = QMessageBox.question(
            self,
            "ゲーム終了の確認",
            "スタート画面に戻りますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            stop_bgm()
            self.hide()
            parent = self.parent()
            if parent and hasattr(parent, "settings_window"):
                parent.settings_window.close()
            if hasattr(parent, "inn_window"):
                parent.inn_window.close()
            if hasattr(parent, "shop_window"):
                parent.shop_window.close()
            if hasattr(parent, "monster_dex_window"):
                parent.monster_dex_window.close()
            if hasattr(parent, "world_map_window"):
                parent.world_map_window.close()
            parent.close()  # TransparentWindow を閉じる
            if self.return_to_menu_callback:
                self.return_to_menu_callback()
    #ステータスウィンドウ上でのセーブ
    def handle_save(self):
        play_se("save")  # セーブ音を鳴らす（適宜修正）
        if self.save_callback and self.character:
            parent = self.parent()
            current_area_level = getattr(parent, "current_area_level", 1)
            world_map = getattr(parent, "world_map", None)
            if world_map:
                world_map_x = world_map.current_x
                world_map_y = world_map.current_y
            else:
                world_map_x = 0
                world_map_y = 0
            parent_kill_count = getattr(parent, "monster_kill_count", self.monster_kill_count)
            parent_unlocked = getattr(self.parent(), "unlocked_dungeons", self.unlocked_dungeons)
            parent_inventory = getattr(parent, "inventory", self.inventory)
            self.save_callback(
                self.character, 
                world_map_x,
                world_map_y,
                current_area_level,
                defeated_bosses=self.defeated_bosses, 
                defeated_monsters=self.defeated_monsters,
                monster_kill_count=parent_kill_count or {},
                unlocked_dungeons=parent_unlocked or [],
                inventory=parent_inventory or [],
            )  # 既存のセーブ関数を呼び出し
            self.show_message("セーブしました")
    #ステータスウィンドウ上での音量設定
    def open_settings(self):
        if hasattr(self.parent(), "settings_window"):
            settings_window = self.parent().settings_window
            settings_window.show()
            settings_window.raise_()
            settings_window.activateWindow()
        else:
            # 念のため fallback（必要なら）
            self.settings_window = SettingsWindow(parent=self)
            self.settings_window.show()

    def update_hp(self, current, maximum):
        self.hp_label.setText(f"HP：{current} / {maximum}")
    def update_mp(self, current, maximum):
        self.mp_label.setText(f"MP：{current} / {maximum}")

    def update_status(self, character):
        self.status_label.setText(
            f"力：{character.power} 守：{character.defense} 魔：{character.magic} 速：{character.speed} 攻：{character.attack_power}"
        )

    def update_exp(self, level, exp, next_exp):
        self.exp_label.setText(f"Lv.{level} EXP：{exp} / {next_exp}")

    def update_coin(self, amount):
        self.coin_label.setText(f"コイン：{amount}")

    def show_message(self, text):
        self.msg_log.append(text)

    def closeEvent(self, event):
        #ウィンドウを閉じてもアプリ終了しないようにする
        self.hide()  #閉じるのではなく隠す
        event.ignore()  #閉じるイベントを無視する

    def show_help(self):
        try:
            with open("README.txt", "r", encoding="utf-8") as file:
                help_text = file.read()
        except Exception as e:
            help_text = f"ヘルプを読み込めませんでした: {e}"

        QMessageBox.information(self, "ヘルプ", help_text)