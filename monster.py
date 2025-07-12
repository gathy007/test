from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Monster:
    #モンスターごとの個別設定
    monster_data = {
        "Slime.png":       {"dex_number": 1,  "hp": 1,    "exp": 1,    "coin":2,    "map_level": 1,   "attack_power": 1, "width": 64, "height": 64, "display_name": "スライム", "area_level": 1},
        
        "YellowSlime.png": {"dex_number": 2,  "hp": 3,    "exp": 2,    "coin":3,    "map_level": 1,   "attack_power": 2, "width": 64, "height": 64, "display_name": "イエロースライム", "area_level": 2},
        "RedSlime.png":    {"dex_number": 3,  "hp": 5,    "exp": 4,    "coin":5,    "map_level": 1,   "attack_power": 2, "width": 64, "height": 64, "display_name": "レッドスライム", "area_level": 2},
        "BlueSlime.png":   {"dex_number": 4,  "hp": 12,   "exp": 7,    "coin":6,    "map_level": 1,   "attack_power": 5, "width": 64, "height": 64, "display_name": "ブルースライム", "area_level": 2},
        "BigSlime.png":    {"dex_number": 5,  "hp": 60,   "exp": 15,   "coin":8,    "map_level": 1,   "attack_power": 10, "width": 128, "height": 128, "display_name": "ビッグスライム", "type": "boss", "area_level": 2},
        
        "Dog.png":         {"dex_number": 6,  "hp": 30,   "exp": 10,   "coin":7,    "map_level": 3,   "attack_power": 8, "width": 64, "height": 64, "display_name": "ドッグ", "area_level": 3},       
        "Goblin.png":      {"dex_number": 7,  "hp": 38,   "exp": 17,   "coin":11,   "map_level": 5,   "attack_power": 17, "width": 64, "height": 64, "display_name": "ゴブリン", "area_level": 3},        
        "Ogre.png":        {"dex_number": 8,  "hp": 52,   "exp": 25,   "coin":15,   "map_level": 9,   "attack_power": 26, "width": 64, "height": 64, "display_name": "オーガ", "area_level": 3},       
        "Treant.png":      {"dex_number": 9,  "hp": 200,  "exp": 124,  "coin":37,   "map_level": 10,  "attack_power": 37, "width": 128, "height": 128, "display_name": "トレント", "type": "boss", "area_level": 3},  
        
        "Ghost.png":       {"dex_number": 10, "hp": 60,   "exp": 43,   "coin":23,   "map_level": 2,   "attack_power": 33, "width": 64, "height": 64, "display_name": "ゴースト", "area_level": 4},       
        "Zombie.png":      {"dex_number": 11, "hp": 74,   "exp": 54,   "coin":26,   "map_level": 4,   "attack_power": 49, "width": 64, "height": 64, "display_name": "ゾンビ", "area_level": 4},        
        "Skeleton.png":    {"dex_number": 12, "hp": 40,   "exp": 81,   "coin":12,   "map_level": 6,   "attack_power": 81, "width": 64, "height": 64, "display_name": "スケルトン", "area_level": 4},       
        "Mummy.png":       {"dex_number": 13, "hp": 420,  "exp": 242,  "coin":55,   "map_level": 8,   "attack_power": 25, "width": 128, "height": 128, "display_name": "マミー",  "type": "boss", "area_level": 4},
        
        "Harpy.png":       {"dex_number": 14, "hp": 91,   "exp": 129,  "coin":41,   "map_level": 12,  "attack_power": 72, "width": 64, "height": 64, "display_name": "ハーピー", "area_level": 5},
        "Mimic.png":       {"dex_number": 15, "hp": 153,  "exp": 277,  "coin":135,  "map_level": 14,  "attack_power": 136, "width": 64, "height": 64, "display_name": "ミミック", "area_level": 5},       
        "Lizardman.png":   {"dex_number": 16, "hp": 118,  "exp": 179,  "coin":67,   "map_level": 16,  "attack_power": 187, "width": 64, "height": 64, "display_name": "リザードマン", "area_level": 5},
        "Minotaur.png":    {"dex_number": 17, "hp": 1000, "exp": 598,  "coin":156,  "map_level": 20,  "attack_power": 200, "width": 128, "height": 128, "display_name": "ミノタウロス", "type": "boss", "area_level": 5}, 
        
        "Kobold.png":      {"dex_number": 18, "hp": 60,   "exp": 132,  "coin":28,   "map_level": 7,   "attack_power": 121, "width": 64, "height": 64, "display_name": "コボルト", "area_level": 6},
        "Troll.png":       {"dex_number": 19, "hp": 191,  "exp": 287,  "coin":81,   "map_level": 18,  "attack_power": 185, "width": 64, "height": 64, "display_name": "トロール", "area_level": 6},
        "Gargoyle.png":    {"dex_number": 20, "hp": 387,  "exp": 703,  "coin":47,   "map_level": 22,  "attack_power": 87,  "width": 64, "height": 64, "display_name": "ガーゴイル", "area_level": 6},
        "Golem.png":       {"dex_number": 21, "hp": 1500, "exp": 1877, "coin":215,  "map_level": 24,  "attack_power": 148, "width": 128, "height": 128, "display_name": "ゴーレム", "type": "boss", "area_level": 6},
        
        "Cerberus.png":    {"dex_number": 22, "hp": 430,  "exp": 1264, "coin":131,  "map_level": 26,  "attack_power": 230, "width": 64, "height": 64, "display_name": "ケルベロス", "area_level": 7},
        "Gazer.png":       {"dex_number": 23, "hp": 444,  "exp": 2222, "coin":222,  "map_level": 28,  "attack_power": 333, "width": 64, "height": 64, "display_name": "ゲイザー", "area_level": 7},
        "Efreet.png":      {"dex_number": 24, "hp": 670,  "exp": 3287, "coin":401,  "map_level": 30,  "attack_power": 543, "width": 128, "height": 128, "display_name": "イフリート", "area_level": 7},
        "Dragon.png":      {"dex_number": 25, "hp": 5000, "exp": 100000, "coin":100000, "map_level": 35,  "attack_power": 1000, "width": 256, "height": 256, "display_name": "ドラゴン", "type": "boss", "area_level": 7},

        "Alraune.png":     {"dex_number": 26, "hp": 60,   "exp": 132,  "coin":28,   "map_level": 7,   "attack_power": 121, "width": 64, "height": 64, "display_name": "アルウラネ", "area_level": 8},
        "Maneater.png":    {"dex_number": 27, "hp": 191,  "exp": 287,  "coin":81,   "map_level": 18,  "attack_power": 185, "width": 64, "height": 64, "display_name": "マンイーター", "area_level": 8},
        "Hellhound.png":   {"dex_number": 28, "hp": 387,  "exp": 703,  "coin":47,   "map_level": 22,  "attack_power": 87,  "width": 64, "height": 64, "display_name": "ヘルハウンド", "area_level": 8},
        "Cyclops.png":     {"dex_number": 28, "hp": 387,  "exp": 703,  "coin":47,   "map_level": 22,  "attack_power": 87,  "width": 64, "height": 64, "display_name": "サイクロプス", "area_level": 8},
        "Cockatrice.png":  {"dex_number": 28, "hp": 387,  "exp": 703,  "coin":47,   "map_level": 22,  "attack_power": 87,  "width": 64, "height": 64, "display_name": "コカトリス", "area_level": 8},
   
    }

    def __init__(self, folder, filename):
        data = self.monster_data.get(filename, {"hp": 100, "attack_power": 1, "width": 256, "height": 256})
        self.dex_number = data.get("dex_number", 999)
        self.max_hp = data["hp"]
        self.hp = self.max_hp
        self.exp = data.get("exp", 1)
        self.coin = data.get("coin", 1)
        self.attack_power = data.get("attack_power", 1)
        self.display_name = data.get("display_name", filename.replace(".png", ""))
        self.type = data.get("type", "normal")
        self.pixmap = QPixmap(f"{folder}/{filename}").scaled(data["width"], data["height"], Qt.KeepAspectRatio, Qt.SmoothTransformation)
