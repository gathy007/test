import sys
from PyQt5.QtWidgets import QApplication
from start_window import StartMenu
from character_selection import CharacterSelectWindow
from main import TransparentWindow
from save_manager import load_game

class GameController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.start_menu = StartMenu()
        self.character_select = None
        self.game_window = None

        # スタートメニューのシグナル等はないので代わりにポーリング的に状態監視もありですが、理想はシグナル実装
        result = self.start_menu.exec_() 
        self.handle_start_menu_closed() 

    def handle_start_menu_closed(self):
        option = self.start_menu.selected_option
        if option == "quit":
            sys.exit(0)
        elif option == "new":
            self.character_select = CharacterSelectWindow()
            result = self.character_select.exec_()

            if self.character_select.return_to_menu:
                self.start_menu = StartMenu()
                self.start_menu.exec_()
                self.handle_start_menu_closed()
            elif self.character_select.character_selected:
                self.start_game_with_character(self.character_select.character_selected)
        elif option == "load":
            # セーブデータロード処理などここに実装
            # 成功すればゲーム起動
            self.start_game_with_load()

    def handle_character_select_closed(self):
        if self.character_select.return_to_menu:
            self.start_menu.show()
        elif self.character_select.character_selected:
            self.start_game_with_character(self.character_select.character_selected)

    def start_game_with_character(self, character_name):
        self.game_window = TransparentWindow(selected_character=character_name, use_save_data=False, return_to_menu_callback=self.back_to_start_menu)
        self.game_window.show()

    def back_to_start_menu(self):
        self.start_menu = StartMenu()
        result = self.start_menu.exec_()
        self.handle_start_menu_closed()

    def start_game_with_load(self):
        # load_game関数を呼んでセーブデータ取得
        save_data = load_game()
        if save_data and "character_name" in save_data:
            self.game_window = TransparentWindow(selected_character=save_data["character_name"], use_save_data=True, return_to_menu_callback=self.back_to_start_menu)
            self.game_window.show()
        else:
            # セーブデータなしはスタートメニューへ戻るなど
            self.start_menu = StartMenu()
            result = self.start_menu.exec_()
            self.handle_start_menu_closed()

    def run(self):
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    controller = GameController()
    controller.run()
