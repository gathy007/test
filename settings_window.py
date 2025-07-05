from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt
from sound import set_bgm_volume, set_se_volume
from settings_manager import load_settings, save_settings

class SettingsWindow(QWidget):
    def __init__(self, parent=None): 
        super().__init__(parent)
        self.setWindowFlags(Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.settings = load_settings()
        self.setWindowTitle("設定")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # BGM 音量スライダー
        self.bgm_label = QLabel(f"BGM 音量: {int(self.settings.get('bgm_volume', 1.0) * 100)}")
        self.bgm_slider = QSlider(Qt.Horizontal)
        self.bgm_slider.setMinimum(0)
        self.bgm_slider.setMaximum(100)
        self.bgm_slider.setValue(int(self.settings.get("bgm_volume", 1.0) * 100))
        self.bgm_slider.valueChanged.connect(self.bgm_volume_changed)

        layout.addWidget(self.bgm_label)
        layout.addWidget(self.bgm_slider)

        # SE 音量スライダー
        self.se_label = QLabel(f"SE 音量: {int(self.settings.get('se_volume', 1.0) * 100)}")
        self.se_slider = QSlider(Qt.Horizontal)
        self.se_slider.setMinimum(0)
        self.se_slider.setMaximum(100)
        self.se_slider.setValue(int(self.settings.get("se_volume", 1.0) * 100)) 
        self.se_slider.valueChanged.connect(self.se_volume_changed)

        layout.addWidget(self.se_label)
        layout.addWidget(self.se_slider)

        # 閉じるボタン
        self.close_button = QPushButton("閉じる")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def bgm_volume_changed(self, value):
        self.bgm_label.setText(f"BGM 音量: {value}")
        volume = value / 100
        set_bgm_volume(volume)
        self.settings["bgm_volume"] = volume
        save_settings(self.settings) 

    def se_volume_changed(self, value):
        self.se_label.setText(f"SE 音量: {value}")
        volume = value / 100
        set_se_volume(volume)
        self.settings["se_volume"] = volume
        save_settings(self.settings) 

