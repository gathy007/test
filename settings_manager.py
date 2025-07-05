import json
import os

SETTINGS_FILE = "config/settings.json"

# 初期値
DEFAULT_SETTINGS = {
    "bgm_volume": 1.0,
    "se_volume": 1.0
}

def load_settings():
    """設定ファイルから読み込む。なければ初期値を返す。"""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """設定をファイルに保存する"""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)
