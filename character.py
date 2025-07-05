from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from sound import play_bgm, stop_bgm, play_se
import math

class Character:
    character_data = {
        #各キャラのステータス
        "swordman": {
            "hp": 10,             #体力 → HPに反映　
            "power": 1,           #力 → 物理攻撃力に反映
            "defense": 1,         #守備力 → 被ダメージ軽減に反映予定
            "magic": 1,           #魔法力 → 魔法攻撃に使用予定
            "speed": 30,          #移動力 → 移動速度に反映 
            "attack_speed": 50,   #攻撃モーション1フレームごとの表示時間(ms)
            #静止時に画像
            "static_image": "assets/character/Sowrdman/swordman.png",
            #移動時の画像
            "walk_frames": [
                "assets/character/Sowrdman/sm_walk0.png",
                "assets/character/Sowrdman/sm_walk1.png",
                "assets/character/Sowrdman/sm_walk2.png",
                "assets/character/Sowrdman/sm_walk3.png",
            ],
            #攻撃時の画像
            "attack_frames": [
                "assets/character/Sowrdman/sm_attack0.png",
                "assets/character/Sowrdman/sm_attack1.png",
                "assets/character/Sowrdman/sm_attack2.png",
                "assets/character/Sowrdman/sm_attack3.png",
            ],
        },
        "knight": {
            "hp": 20,             #体力 → HPに反映　
            "power": 0.5,           #力 → 物理攻撃力に反映
            "defense": 5,         #守備力 → 被ダメージ軽減に反映予定
            "magic": 0,           #魔法力 → 魔法攻撃に使用予定
            "speed": 15,          #移動力 → 移動速度に反映 
            "attack_speed": 70,   #攻撃モーション1フレームごとの表示時間(ms)
            #静止時に画像
            "static_image": "assets/character/Knight/knight.png",
            #移動時の画像
            "walk_frames": [
                "assets/character/Knight/kt_walk0.png",
                "assets/character/Knight/kt_walk1.png",
                "assets/character/Knight/kt_walk2.png",
                "assets/character/Knight/kt_walk3.png",
            ],
            #攻撃時の画像
            "attack_frames": [
                "assets/character/Knight/kt_attack0.png",
                "assets/character/Knight/kt_attack1.png", 
                "assets/character/Knight/kt_attack2.png",
                "assets/character/Knight/kt_attack3.png",
            ],
        },

    }

    def __init__(self, name="swordman"):
        self.name = name
        data = self.character_data.get(name)
        #それぞれのステータスの定義
        self.power_base = data["power"]
        self.defense_base = data["defense"]
        self.magic_base = data["magic"]
        self.speed_base = data["speed"]
        self.attack_speed_base = data["attack_speed"]
        self.power = self.power_base      
        self.defense = self.defense_base   
        self.magic = self.magic_base     
        self.speed = self.speed_base
        self.attack_speed = self.attack_speed_base      
        self.attack_power = self.calculate_attack_power()
        #ボスモンスターを倒したフラグ
        self.boss_level_base = 1
        self.boss_level = self.boss_level_base

        self.hp_base = data["hp"]
        self.max_hp_original = self.hp_base
        self.max_hp = self.hp_base
        self.hp = self.max_hp 
        #生存フラグ
        self.character_alive = True

        self.inventory = [] 

        self.static_pixmap = QPixmap(data["static_image"]).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.frames = [QPixmap(path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation) for path in data["walk_frames"]]
        self.attack_frames = [QPixmap(path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation) for path in data["attack_frames"]]

        #レベルと経験値とコイン
        self.level_base = 1
        self.exp_base = 0
        self.coins_base = 0
        self.exp_to_next_base = 5 #初期レベルアップ必要EXP       
        self.level = self.level_base
        self.exp = self.exp_base
        self.coins = self.coins_base
        self.exp_to_next = self.exp_to_next_base
    #攻撃力の計算式
    def calculate_attack_power(self):
        return math.floor(self.power * 1.5 + 0.5)
    def calculate_max_hp(self):
        return math.floor(self.max_hp_original * 2)

    #レベルアップシステム
    def add_exp(self, amount, hp_window=None):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            play_se("leverup1")
            self.exp -= self.exp_to_next
            self.level += 1
            self.max_hp_original = math.floor(self.max_hp_original * 1.15 + 0.5)
            self.max_hp = self.calculate_max_hp()
            self.power += 1
            self.attack_power = self.calculate_attack_power()
            self.hp = self.max_hp
            self.exp_to_next = math.floor(self.exp_to_next * 1.25 + 0.5)  #必要EXP増加
            if hp_window:
                hp_window.show_message(f"レベルアップ！ Lv.{self.level}")
        if hp_window:
            hp_window.update_exp(self.level, self.exp, self.exp_to_next)
            hp_window.update_status(self)
            hp_window.update_hp(self.hp, self.max_hp)