import os
from PyQt5.QtGui import QPixmap

def load_animation_frames(folder_path):
    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frames.append(QPixmap(os.path.join(folder_path, filename)))
    return frames

def get_drop_item_types():
    return {
        "coin_1": {
            "type": "coin",
            "amount": 1,
            "frames": load_animation_frames("assets/items/Coin1"),
            "size": (16, 16),
        },
        "coin_5": {
            "type": "coin",
            "amount": 5,
            "frames": load_animation_frames("assets/items/Coin5"),
            "size": (16, 16),
        },
        "coin_10": {
            "type": "coin",
            "amount": 10,
            "frames": load_animation_frames("assets/items/Coin10"),
            "size": (16, 16),
        },


        "exp_1": {
            "type": "exp",
            "amount": 1,
            "frames": load_animation_frames("assets/items/exp1"),
            "size": (16, 16),
        },
        "exp_5": {
            "type": "exp",
            "amount": 5,
            "frames": load_animation_frames("assets/items/exp5"),
            "size": (16, 16),
        },
        "exp_10": {
            "type": "exp",
            "amount": 10,
            "frames": load_animation_frames("assets/items/exp10"),
            "size": (16, 16),
        },

    }