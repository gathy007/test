import os

class Item:
    def __init__(self, no, name, description, heal_amount, image_filename, price):
        self.no = no  
        self.name = name                      # アイテム名（表示名）
        self.description = description        # アイテム説明
        self.heal_amount = heal_amount        # 回復量（0なら装備やその他に転用可能）
        self.price = price                    # 購入価格
        self.image_path = self.get_image_path(image_filename)  # 画像のパス

    def get_image_path(self, filename):
        """画像ファイルのフルパスを返す（PyInstaller対応を意識）"""
        base_path = os.path.join("assets", "items", "Potion")
        return os.path.join(base_path, filename)

    def use(self, character):
        """キャラクターに使用した時の効果（回復）"""
        if self.heal_amount > 0:
            healed = min(self.heal_amount, character.max_hp - character.hp)
            character.hp += healed
            return healed
        return 0


# アイテム一覧定義
ITEMS = {
    "small_potion": Item(
        no=1,
        name="スモールポーション",
        description="HPを10回復する",
        heal_amount=10,
        image_filename="small_potion.png",
        #price=1,
        price=50
    ),
    "small_high_potion": Item(
        no=2,
        name="スモールハイポーション",
        description="HPを50回復する",
        heal_amount=50,
        image_filename="small_high_potion.png",
        #price=1,
        price=200
    ),
    "medium_potion": Item(
        no=3,
        name="ミディアムポーション",
        description="HPを100回復する",
        heal_amount=100,
        image_filename="medium_potion.png",
        #price=1,
        price=300
    ),
    "medium_high_potion": Item(
        no=4,
        name="ミディアムハイポーション",
        description="HPを500回復する",
        heal_amount=500,
        image_filename="medium_high_potion.png",
        #price=1,
        price=500
    ),
    "large_potion": Item(
        no=5,
        name="ラージポーション",
        description="HPを1000回復する",
        heal_amount=1000,
        image_filename="large_potion.png",
        #price=1,
        price=700
    ),
    "large_high_potion": Item(
        no=6,
        name="ラージハイポーション",
        description="HPを2500回復する",
        heal_amount=2500,
        image_filename="large_high_potion.png",
        #price=1,
        price=1000
    ),
}
