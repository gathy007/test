from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QApplication, QMessageBox
from sound import play_se
from save_manager import load_game

class StartMenu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("スタートメニュー")
        self.setGeometry(300, 300, 300, 150)

        self.selected_option = None

        layout = QVBoxLayout()
        label = QLabel("ゲームを始めますか？")
        layout.addWidget(label)

        load_button = QPushButton("セーブデータから再開")
        load_button.clicked.connect(self.load_game)
        layout.addWidget(load_button)

        new_game_button = QPushButton("最初から始める")
        new_game_button.clicked.connect(self.new_game)
        layout.addWidget(new_game_button)

        exit_button = QPushButton("ゲームを終了する")
        exit_button.clicked.connect(self.quit_game)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def load_game(self):
        play_se("check_sound1")
        save_data = load_game()  
        if save_data is None:   
            QMessageBox.information(self, "エラー", "セーブデータがありません。")
            return 
        self.selected_option = "load"
        self.accept()

    def new_game(self):
        play_se("check_sound1")
        self.selected_option = "new"
        self.accept()

    def quit_game(self):
        play_se("check_sound1")
        reply = QMessageBox.question(
            self,
            "終了確認",
            "本当にゲームを終了しますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.selected_option = "quit" 
            self.accept()
