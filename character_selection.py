from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QPushButton, QLabel
from sound import play_bgm, stop_bgm, play_se

class CharacterSelectWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("キャラクター選択")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()
        label = QLabel("キャラクターを選択してください")
        layout.addWidget(label)

        self.character_selected = None
        self.return_to_menu = False

        # キャラクターの選択肢
        characters = ["swordman", "knight"]
        for name in characters:
            button = QPushButton(name)
            button.clicked.connect(lambda checked, n=name: self.select_character(n))
            layout.addWidget(button)
        
        #戻るボタン
        back_button = QPushButton("戻る")
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button)

        self.setLayout(layout)

    def select_character(self, name):
        play_se("check_sound1")
        self.character_selected = name
        self.accept()

    def go_back(self):
        play_se("window_close")
        self.return_to_menu = True  # ← フラグを設定
        self.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    selector = CharacterSelectWindow()
    selector.show()

    if selector.exec_() == QDialog.Accepted and selector.character_selected:
        print("選択されたキャラクター:", selector.character_selected)
    elif selector.return_to_menu:
        print("メニューに戻る")
