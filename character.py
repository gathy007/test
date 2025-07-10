from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDateTime
from sound import play_bgm, stop_bgm, play_se
from skills_data import skills_data
import math

class Character:
    character_data = {
        #各キャラのステータス
        "swordman": {
            "hp": 10,             #体力 → HPに反映
            "mp": 5,              #MP
            "power": 1,           #力 → 物理攻撃力に反映
            "defense": 1,         #守備力 → 被ダメージ軽減に反映予定
            "magic": 1,           #魔法力 → 魔法攻撃に反映
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
            "level_up_bonus": {
               "bonus_hp": 1.15, #HP増加の倍率
               "bonus_mp": 1.15,
               "bonus_power": 1, #増加する力の量
               "bonus_defense": 0.5,
               "bonus_magic": 0.2,
               "bonus_speed": 0,
           }
        },
        "knight": {
            "hp": 20, 
            "mp": 1,
            "power": 0.5, 
            "defense": 5, 
            "magic": 0, 
            "speed": 15, 
            "attack_speed": 70,
            "static_image": "assets/character/Knight/knight.png",
            "walk_frames": [
                "assets/character/Knight/kt_walk0.png",
                "assets/character/Knight/kt_walk1.png",
                "assets/character/Knight/kt_walk2.png",
                "assets/character/Knight/kt_walk3.png",
            ],
            "attack_frames": [
                "assets/character/Knight/kt_attack0.png",
                "assets/character/Knight/kt_attack1.png", 
                "assets/character/Knight/kt_attack2.png",
                "assets/character/Knight/kt_attack3.png",
            ],
            "level_up_bonus": {
               "bonus_hp": 1.8,
               "bonus_mp": 1.1,
               "bonus_power": 0.5,
               "bonus_defense": 2,
               "bonus_magic": 0.1,
               "bonus_speed": 0,
           }            
        },

    }

    def __init__(self, name="swordman"):
        #キャラクターごとに覚えるスキル一覧
        self.skills = {}
        self.learned_skill_keys = []
        self.name = name
        if self.name == "swordman":
            self.learnable_skills = [
                {"key": "fireball", "level": 3, "data": skills_data["fireball"]},
                {"key": "ice", "level": 6, "data": skills_data["ice"]},
            ]
        elif self.name == "knight":
            self.learnable_skills = [
                {"key": "ice", "level": 2, "data": skills_data["ice"]},
            ]
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
        #HPの定義
        self.hp_base = data["hp"]
        self.max_hp_original = self.hp_base
        self.max_hp = self.hp_base
        self.hp = self.max_hp 
        #MPの定義
        self.mp_base = data["mp"]
        self.max_mp_original = self.mp_base
        self.max_mp = self.mp_base
        self.mp = self.max_mp
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

    #スキルの使用システム
    def use_skill(self, skill_key, show_message=None, hp_window=None):
        skill = self.skills.get(skill_key)
        if not skill:
            if show_message:
                show_message("そのスキルは存在しません")
            return False

        now = QDateTime.currentMSecsSinceEpoch()
        if now - skill["last_used"] < skill["cooldown"]:
            if show_message:
                show_message(f"{skill['name']} はクールダウン中です")
            return False

        if self.mp < skill.get("mp_cost", 0):
            if show_message:
                show_message("MPが足りません")
            return False
        self.mp -= skill.get("mp_cost", 0)
        if hp_window:
            hp_window.update_mp(self.mp, self.max_mp)

        skill["last_used"] = now
        if show_message:
            show_message(f"{skill['name']} を使用！")
        if "se" in skill:
            play_se(skill["se"])
        return True


    #攻撃力の計算式
    def calculate_attack_power(self):
        return math.floor(self.power * 1.75 + 0.5)
    #HPの計算式
    def calculate_max_hp(self):
        return math.floor(self.max_hp_original * 2)
    #MPの計算式
    def calculate_max_mp(self):
        return math.floor(self.max_mp_original * 1.5)

    #レベルアップシステム
    def add_exp(self, amount, hp_window=None):
        self.exp += amount
        while self.exp >= self.exp_to_next:
            play_se("leverup1")
            self.exp -= self.exp_to_next
            self.level += 1
            bonus = self.character_data[self.name].get("level_up_bonus", {})
            self.max_hp_original = math.floor(self.max_hp_original * bonus.get("bonus_hp", 1.1) + 0.5)
            self.max_hp = self.calculate_max_hp()
            self.max_mp_original = math.floor(self.max_mp_original * bonus.get("bonus_mp", 1.1) + 0.5)
            self.max_mp = self.calculate_max_mp()
            self.power = round(self.power + bonus.get("bonus_power", 0), 1)
            self.defense = round(self.defense + bonus.get("bonus_defense", 0), 1)
            self.magic = round(self.magic + bonus.get("bonus_magic", 0), 1)
            self.speed = round(self.speed + bonus.get("bonus_speed", 0), 1)
            self.attack_power = self.calculate_attack_power()
            self.hp = self.max_hp
            self.mp = self.max_mp
            self.exp_to_next = math.floor(self.exp_to_next * 1.25 + 0.5)  #必要EXP増加

            new_skills = []
            for skill in self.learnable_skills:
                if skill["level"] <= self.level and skill["key"] not in self.skills:
                    self.skills[skill["key"]] = skill["data"]
                    self.learned_skill_keys.append(skill["key"])
                    new_skills.append(skill["data"]["name"])

            if hp_window:
                hp_window.show_message(f"レベルアップ！ Lv.{self.level}")
                for skill_name in new_skills:
                    hp_window.show_message(f"スキル「{skill_name}」を習得！")

        if hp_window:
            hp_window.update_exp(self.level, self.exp, self.exp_to_next)
            hp_window.update_status(self)
            hp_window.update_hp(self.hp, self.max_hp)
            hp_window.update_mp(self.mp, self.max_mp)