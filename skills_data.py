skills_data = {
    "fireball": {
        "name": "ファイアボール",
        "damage": 2,
        "mp_cost": 2,
        "cooldown": 3000,
        "last_used": 0,
        "type": "throw",
        "se": "fireball",
        "animation": {
            "folder": "assets/effects/fireball/",
            "frame_count": 10,
            "interval": 50,
        }
    },
    "ice": {
        "name": "アイス",
        "damage": 20,
        "mp_cost": 5,
        "cooldown": 5000,
        "last_used": 0,
        "type": "put",
        "se": "ice",
        "animation": {
            "folder": "assets/effects/ice/",
            "frame_count": 3,
            "interval": 500,
        }
    },
}

def get_skill_by_key(key):
    skill = skills_data.get(key)
    if skill:
        skill_with_key = skill.copy()
        skill_with_key["key"] = key
        return skill_with_key
    return None
