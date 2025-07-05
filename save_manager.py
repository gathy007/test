import json
import os
from items import ITEMS

SAVE_FILE = "config/save_data.json"
#セーブデータの保存
def save_game(character, defeated_bosses=None, defeated_monsters=None, monster_kill_count=None, unlocked_dungeons=None, inventory=None):
    #保存するもの
    item_obj_to_key = {v: k for k, v in ITEMS.items()}
    data = {
        "level": character.level,
        "exp": character.exp,
        "exp_to_next": character.exp_to_next,
        "hp": character.hp,
        "max_hp": character.max_hp,
        "max_hp_original": character.max_hp_original,
        "coins": character.coins,
        "power": character.power,
        "defense": character.defense,
        "magic": character.magic,
        "speed": character.speed,
        "attack_power":character.attack_power,
        "character_name": character.name,
        "boss_level": character.boss_level,
        "defeated_bosses": defeated_bosses if defeated_bosses is not None else [],
        "defeated_monsters": list(defeated_monsters) if defeated_monsters is not None else [], 
        "monster_kill_count": monster_kill_count or {},
        "unlocked_dungeons": list(unlocked_dungeons),
        "inventory": [item_obj_to_key[item] for item in inventory if item in item_obj_to_key] if inventory else [],
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_game():
    if not os.path.exists(SAVE_FILE):
        return None  # セーブがなければ None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data
