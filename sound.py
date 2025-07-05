import pygame
import os
import time  
from settings_manager import load_settings,save_settings

pygame.mixer.init()


# サウンドパスの定義
SOUND_PATH = "assets/sounds"
settings = load_settings()

#SEファイルの読み込みと音量調整（0.0 ～ 1.0）
SE_BASE_VOLUMES = {
    "coin": 0.8,
    "attack_c": 1.0,
    "check_sound1": 1.0,
    "death_c": 1.0,
    "death_m": 1.0,
    "leverup1": 1.0,
    "walk": 1.0,
    "window_close": 1.0,
    "window_open": 1.0,
    "save": 1.0,
    "exp": 1.0,
    "heal": 0.7,
    "INN": 1.0,
    "dungeon": 1.0,
    "buy": 1.0,
    "use": 1.0,
    "nouse": 1.0,
}

SE_SOUNDS = {}
for name in SE_BASE_VOLUMES.keys():
    path = os.path.join(SOUND_PATH, f"{name}.wav")
    SE_SOUNDS[name] = pygame.mixer.Sound(path)

#ボリュームを反映
def apply_se_volume():
    se_volume = settings.get("se_volume", 1.0)
    for name, sound in SE_SOUNDS.items():
        base = SE_BASE_VOLUMES.get(name, 1.0)
        sound.set_volume(base * se_volume)

apply_se_volume()

#BGMファイル定義（ファイル名のみで管理）
BGM_TRACKS = {
    "BGM": "BGM.mp3",
}

#現在のBGM名を記録（停止時などに利用）
current_bgm = None

#クールダウン管理辞書
SE_COOLDOWN = {}
SE_COOLDOWN_TIME = {
    "walk": 0.3,       # 秒単位
}

def set_bgm_volume(volume: float):
    pygame.mixer.music.set_volume(volume)
    settings["bgm_volume"] = volume
    save_settings(settings)
    
def set_se_volume(volume: float):
    settings["se_volume"] = volume
    save_settings(settings)
    apply_se_volume()

def play_bgm(name, volume=1, loop=-1):
    global current_bgm
    if name not in BGM_TRACKS:
        print(f"BGM '{name}' は存在しません")
        return
    stop_bgm()
    path = os.path.join(SOUND_PATH, BGM_TRACKS[name])
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(settings.get("bgm_volume", 1.0))
    pygame.mixer.music.play(loop)
    current_bgm = name

def stop_bgm():
    pygame.mixer.music.stop()

def play_se(name):
    now = time.time()
    cooldown = SE_COOLDOWN_TIME.get(name, 0)
    last_play = SE_COOLDOWN.get(name, 0)

    if now - last_play >= cooldown:
        if name in SE_SOUNDS:
            SE_SOUNDS[name].play()
            SE_COOLDOWN[name] = now
        else:
            print(f"SE '{name}' は存在しません")
