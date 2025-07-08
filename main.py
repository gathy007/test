import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLabel
from PyQt5.QtGui import QPainter, QTransform,QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

#他のpyからクラスをインポートする関数
from character import Character  # キャラクター定義読み込み
from monster import Monster      # モンスター定義読み込み
from hp_window import HPWindow   #　ステータスウィンドウ定義読み込み
from drop_item import get_drop_item_types  #ドロップアイテム定義読み込み
from sound import play_bgm, stop_bgm, play_se #サウンド定義読み込み
from settings_window import SettingsWindow
from save_manager import load_game,save_game
from inn_window import InnWindow
from dungeons import DUNGEONS
from shop_window import ShopWindow  
from inventory_window import InventoryWindow 
from items import ITEMS
from monster_dex_window import MonsterDexWindow  

class TransparentWindow(QWidget):
    def __init__(self, selected_character="swordman", use_save_data=True, return_to_menu_callback=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen.width(), screen.height())
        self.return_to_menu_callback = return_to_menu_callback

        self.setFocusPolicy(Qt.StrongFocus)

        #キャラクターとモンスターの読み込み
        char_folder = "assets/character"
        monster_folder = "assets/monster"
        self.defeated_bosses = [] 
        self.defeated_monsters = set()
        self.unlocked_dungeons = set()
        self.monster_kill_count = {}
        self.selected_skill_key = "fireball"
        self.character = Character(selected_character)
        if use_save_data:
            save_data = load_game()
            if save_data:
                self.character.level = save_data["level"]
                self.character.exp = save_data["exp"]
                self.character.exp_to_next = save_data["exp_to_next"]
                self.character.hp = save_data["hp"]
                self.character.max_hp = save_data["max_hp"]
                self.character.max_hp_original = save_data["max_hp_original"]
                self.character.coins = save_data["coins"]
                self.character.power = save_data["power"]
                self.character.defense = save_data["defense"]
                self.character.magic = save_data["magic"]
                self.character.speed = save_data["speed"]
                self.character.attack_power = self.character.calculate_attack_power()
                self.character.name  = save_data["character_name"]
                self.character.boss_level = save_data["boss_level"]
                self.defeated_bosses = save_data.get("defeated_bosses", [])
                self.defeated_monsters = set(save_data.get("defeated_monsters", []))
                self.monster_kill_count = save_data.get("monster_kill_count", {})
                self.unlocked_dungeons = set(save_data.get("unlocked_dungeons", ["grassland"]))
                self.character.inventory = []
                for item_key in save_data.get("inventory", []):
                    if item_key in ITEMS:
                        self.character.inventory.append(ITEMS[item_key])
            else:
                self.defeated_monsters = set()
                self.unlocked_dungeons = {"grassland"}
        else:
            self.unlocked_dungeons = {"grassland"}
        #INNの描写設定
        self.inn_pixmap = QPixmap("assets/shop/INN.png").scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.inn_x = self.width() // 2 - self.inn_pixmap.width() // 2
        self.inn_y = self.height() // 2 - self.inn_pixmap.height() // 2
        self.show_inn_dialog = False
        self.inn_window = InnWindow(on_dungeon_selected=self.enter_dungeon, on_return_home=self.return_to_home, parent=self)

        self.monster_folder = monster_folder
        self.monsters = []
        self.dropped_coins = [] 
        self.drop_item_types = get_drop_item_types()

        # インベントリウィンドウの初期化と表示
        self.inventory_window = InventoryWindow(
            parent=self,
            character=self.character,
            inventory=self.character.inventory,
            on_inventory_updated=None,
        )
        x = (self.width() - self.inventory_window.width()) // 2
        y = self.height() - self.inventory_window.height() - 40
        self.inventory_window.move(x, y)
        self.inventory_window.show()
        self.inventory_window.update_inventory(self.character.inventory)

        #モンスターの移動速度
        self.monster_move_timer = QTimer()
        self.monster_move_timer.timeout.connect(self.move_monsters)
        self.monster_move_timer.start(1000)  # 500ミリ秒 = 0.5秒ごとに動作
        #モンスターのリスポーン間隔
        self.spawn_monster_timer = QTimer()
        self.spawn_monster_timer.timeout.connect(self.spawn_monster)
        self.spawn_monster_timer.start(1000)  # 5000ミリ秒 → 5秒ごとに呼び出し

        #ウィンドウの表示
        self.hp_window = HPWindow(
            parent=self, 
            save_callback=save_game, 
            character=self.character, 
            defeated_bosses=self.defeated_bosses, 
            defeated_monsters=self.defeated_monsters,
            return_to_menu_callback=self.return_to_menu_callback,
            monster_kill_count=self.monster_kill_count,
            inventory=self.character.inventory,
            unlocked_dungeons=self.unlocked_dungeons,
        )
        self.hp_window.update_hp(self.character.hp, self.character.max_hp)
        self.hp_window.update_exp(self.character.level, self.character.exp, self.character.exp_to_next)
        self.hp_window.update_coin(self.character.coins)
        self.hp_window.update_status(self.character)

        self.settings_window = SettingsWindow(parent=self)

        self.current_frame_index = 0
        self.attack_frame_index = 0
        self.current_pixmap = self.character.static_pixmap

        self.x = screen.width() // 2
        self.y = screen.height() // 2

        #攻撃モーションタイマー
        self.attack_timer = QTimer()
        self.attack_timer.timeout.connect(self.update_attack_frame)
        #コインのモーションタイマー
        self.coin_animation_timer = QTimer()
        self.coin_animation_timer.timeout.connect(self.update_coin_animation)
        self.coin_animation_timer.start(100)
        #ゲーム全体の更新速度（アニメーションの速度など）
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)
        self.keys_pressed = set()
        #キャラクターの移動速度
        self.move_speed = self.character.speed

        self.attacking = False
        self.attack_animation_playing = False

        self.facing_right = False
        self.facing_down = False

        self.show() 
        #ウィンドウを強制的にアクティブにしてキーボードを受け付けるようにする
        self.activateWindow()  
        self.setFocus()       
        play_bgm("BGM") 
    #ダンジョンを選択した処理
    def enter_dungeon(self, dungeon_name):
        play_se("dungeon")
        dungeon = DUNGEONS[dungeon_name]
        self.selected_dungeon = dungeon_name
        self.current_area_level = dungeon["area_level"]
        if hasattr(self, "inn_window"):
            self.inn_window.close()
        self.hp_window.show_message(f"{dungeon['display_name']} に入った！")   
        self.monsters.clear()
    #ダンジョンから離れた時
    def return_to_home(self): 
        self.monsters.clear()
        if hasattr(self, "current_area_level"):
            del self.current_area_level
        self.hp_window.show_message("ホームに戻りました")

    #モンスター生成
    def spawn_monster(self):
        #マップレベル
        map_level = self.character.level
        boss_level = self.character.boss_level
        #出現可能モンスター一覧を取得
        #ダンジョン選択時はarea_level参照
        if hasattr(self, "current_area_level"):
            dungeon_name = getattr(self, "selected_dungeon", None)
            available_monsters = []
            for name, data in Monster.monster_data.items():
                if data.get("area_level", 1) == self.current_area_level:
                    # ボスモンスターは条件がそろうまで出さない
                    if data.get("type") == "boss":
                        kill_count = self.monster_kill_count.get(dungeon_name, 0)
                        if kill_count >= 10:
                            available_monsters.append(name)
                    else:
                        available_monsters.append(name)
        #ホーム画面：area_level 1 または 倒したことのあるモンスター（ボスも含む）        
        else:
            available_monsters = [
                name for name, data in Monster.monster_data.items()
                if (data.get("area_level", 1) == 1 or name in self.defeated_monsters)
                 #and (data.get("type") != "boss" or name not in self.defeated_bosses)
            ]

        if not available_monsters:
            return

        filename = random.choice(available_monsters)
        #既に出現しているボスを除外
        if Monster.monster_data[filename].get("type") == "boss":
            for m in self.monsters:
                if m["alive"] and m["name"] == filename:
                    return

        # スポーン禁止範囲設定（INNとキャラクターの周辺）
        forbidden_areas = []

        inn_rect = QRect(self.inn_x - 5, self.inn_y - 5,
                         self.inn_pixmap.width() + 10, self.inn_pixmap.height() + 10)
        forbidden_areas.append(inn_rect)

        char_pixmap = self.current_pixmap
        char_rect = QRect(self.x - 5, self.y - 5,
                          char_pixmap.width() + 10, char_pixmap.height() + 10)
        forbidden_areas.append(char_rect)

        max_attempts = 30
        for attempt in range(max_attempts):
            x = random.randint(0, self.width() - 64)
            y = random.randint(0, self.height() - 64)

            candidate_rect = QRect(x, y, 64, 64)
            #禁止範囲と重ならなければ決定
            if not any(candidate_rect.intersects(area) for area in forbidden_areas):
                break
        else:
            #max_attempts超えたらそのまま出す
            x = random.randint(0, self.width() - 64)
            y = random.randint(0, self.height() - 64)        

        #スポーンするモンスターの初期定義
        monster_obj = Monster(self.monster_folder, filename)
        monster = {
            "pixmap": monster_obj.pixmap,
            "x": x,
            "y": y,
            "origin_x": None,
            "origin_y": None,
            "alive": True,
            "hp": monster_obj.hp,
            "max_hp": monster_obj.max_hp,
            "exp": monster_obj.exp,
            "coin": monster_obj.coin,
            "attack_power": monster_obj.attack_power,
            "name": filename,
            "dx": random.choice([-1, 0, 1]),
            "dy": random.choice([-1, 0, 1]),
            "display_name": monster_obj.display_name,
            "type": monster_obj.type,
        }
        self.monsters.append(monster)

    #モンスターの移動
    def move_monsters(self):
        for m in self.monsters:
            if m["alive"]:
                m["dx"] = random.choice([-1, 0, 1])
                m["dy"] = random.choice([-1, 0, 1])
                m["x"] = max(0, min(self.width() - m["pixmap"].width(), m["x"] + m["dx"] * 10))
                m["y"] = max(0, min(self.height() - m["pixmap"].height(), m["y"] + m["dy"] * 10))
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.inn_x, self.inn_y, self.inn_pixmap)
        for m in self.monsters:
            if m["alive"]:
                painter.drawPixmap(m["x"], m["y"], m["pixmap"])
                if m["hp"] < m["max_hp"]:
                    #モンスターHPバー
                    bar_width = m["pixmap"].width()
                    bar_height = 5
                    hp_ratio = m["hp"] / m["max_hp"]
                    current_bar_width = int(bar_width * hp_ratio)
                    #背景バー（灰色）
                    painter.setBrush(Qt.gray)
                    painter.drawRect(m["x"], m["y"] - 10, bar_width, bar_height)
                    #HPバー（緑→黄色→赤の順）
                    if hp_ratio <= 0.25:
                        painter.setBrush(Qt.red)
                    elif hp_ratio <= 0.5:
                        painter.setBrush(Qt.yellow)
                    else:
                        painter.setBrush(Qt.green)
                    painter.drawRect(m["x"], m["y"] - 10, current_bar_width, bar_height)   

        if self.character.character_alive:
            #キャラクターのHPバー
            char_pixmap_width = self.current_pixmap.width()
            bar_width = char_pixmap_width
            bar_height = 5
            hp_ratio = self.character.hp / self.character.max_hp
            current_bar_width = int(bar_width * hp_ratio)
            #HPバーの背景（灰色）
            painter.setBrush(Qt.gray)
            painter.drawRect(self.x, self.y - 10, bar_width, bar_height)
            #HPバー（緑→黄色→赤の順）
            if hp_ratio <= 0.25:
                painter.setBrush(Qt.red)
            elif hp_ratio <= 0.5:
                painter.setBrush(Qt.yellow)
            else:
                painter.setBrush(Qt.green)
            painter.drawRect(self.x, self.y - 10, current_bar_width, bar_height)

            painter.drawPixmap(self.x, self.y, self.current_pixmap)
            from PyQt5.QtGui import QPixmap
            for coin in self.dropped_coins:
                frames = coin["frames"]
                frame = frames[coin["frame_index"]]
                width, height = coin.get("size", (32, 32))  #←ここでコインのサイズ取得
                painter.drawPixmap(coin["x"], coin["y"], width, height, frame)

    def get_oriented_pixmap(self, pixmap):
        if self.facing_right:
            return pixmap.transformed(QTransform().scale(-1, 1))
        else:
            return pixmap

    def start_attack_animation(self):
        if self.attack_animation_playing:  #既に攻撃中なら新しい攻撃はしない
            return
        self.attacking = True
        self.attack_frame_index = 0
        self.attack_animation_playing = True
        self.attack_timer.start(self.character.attack_speed)
    #スキルアニメーションの表示処理
    def show_skill_animation(self, skill_info, position, skill_type="throw", facing_right=True, facing_down = True):
        anim_info = skill_info.get("animation")
        if not anim_info:
            return 

        folder = anim_info["folder"]
        frame_count = anim_info["frame_count"]
        interval = anim_info["interval"]
        damage = skill_info.get("damage", 0)

        frames = [
            QPixmap(f"{folder}{i}.png").scaled(32, 632, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            for i in range(frame_count)
        ]

        SkillAnimation(
            parent=self,
            frames=frames,
            pos=position,
            interval=interval,
            damage=damage,
            skill_type=skill_type,
            facing_right=self.facing_right,
            facing_down = self.facing_down,
        )

    def apply_knockback(self, m):
        dx = m["x"] - self.x
        dy = m["y"] - self.y
        knockback_strength = 2

        m["origin_x"] = m["x"]
        m["origin_y"] = m["y"]

        if dx > 0:
            m["x"] = min(m["x"] + knockback_strength, self.width() - 64)
        elif dx < 0:
            m["x"] = max(m["x"] - knockback_strength, 0)

        if dy > 0:
            m["y"] = min(m["y"] + knockback_strength, self.height() - 64)
        elif dy < 0:
            m["y"] = max(m["y"] - knockback_strength, 0)
    #戻す用タイマー起動
        QTimer.singleShot(300, lambda: self.reset_monster_position(m))
    
    def reset_monster_position(self, m):
        if m["origin_x"] is not None and m["origin_y"] is not None:
            m["x"] = m["origin_x"]
            m["y"] = m["origin_y"]

    def update_coin_animation(self):
        for coin in self.dropped_coins:
            coin["frame_index"] = (coin["frame_index"] + 1) % len(coin["frames"])
        self.update() 

    def update_attack_frame(self):
        if self.attack_frame_index < len(self.character.attack_frames):
            base_frame = self.character.attack_frames[self.attack_frame_index]
            self.current_pixmap = self.get_oriented_pixmap(base_frame)
            self.attack_frame_index += 1
        else:
            self.attack_animation_playing = False
            self.attacking = False
            self.attack_frame_index = 0
            self.attack_timer.stop()
            self.current_pixmap = self.get_oriented_pixmap(self.character.static_pixmap)
        self.update()
    #モンスター撃破の処理（撃破記録やアイテムドロップへの移行）
    def handle_monster_death(self, m):
        m["alive"] = False

        #撃破記録
        if m["name"] not in self.defeated_monsters:
            self.defeated_monsters.add(m["name"])
        if hasattr(self, "monster_dex_window") and self.monster_dex_window and self.monster_dex_window.isVisible():
            self.monster_dex_window.update_dex(self.defeated_monsters)

        #ダンジョン内撃破カウント
        if hasattr(self, "selected_dungeon"):
            dungeon_name = self.selected_dungeon
            self.monster_kill_count[dungeon_name] = self.monster_kill_count.get(dungeon_name, 0) + 1
            if self.monster_kill_count[dungeon_name] == 10:
                display_name = DUNGEONS.get(dungeon_name, {}).get("display_name", dungeon_name)
                self.hp_window.show_message(f"{display_name} のモンスターを10体倒した！ボスが出現するようになった！")

        #ボス処理（ダンジョンキー取得）
        if m.get("type") == "boss":
            if m["name"] not in self.defeated_bosses:
                self.defeated_bosses.append(m["name"])
                dungeon_key = getattr(self, "selected_dungeon", None)
                if dungeon_key:
                    next_key = DUNGEONS.get(dungeon_key, {}).get("next_dungeon_key")
                    if next_key:
                        self.unlocked_dungeons.add(next_key)
                        self.hp_window.show_message(f"{DUNGEONS[next_key]['display_name']} の鍵を手に入れた！")

        self.hp_window.update_hp(self.character.hp, self.character.max_hp)
        self.hp_window.update_exp(self.character.level, self.character.exp, self.character.exp_to_next)
        self.hp_window.update_status(self.character)

        play_se("death_m")

        #ドロップ処理へ移行
        self.drop_items_from_monster(m)
    #アイテムのドロップ処理
    def drop_items_from_monster(self, m):
        coin_total = m.get("coin", 1)
        exp_total = m.get("exp", 0)

        coin_keys = []
        while coin_total > 0:
            if coin_total >= 10 and "coin_10" in self.drop_item_types:
                coin_keys.append("coin_10")
                coin_total -= 10
            elif coin_total >= 5 and "coin_5" in self.drop_item_types:
                coin_keys.append("coin_5")
                coin_total -= 5
            elif "coin_1" in self.drop_item_types:
                coin_keys.append("coin_1")
                coin_total -= 1
            else:
                break

        for coin_key in coin_keys:
            coin_data = self.drop_item_types[coin_key]
            self.dropped_coins.append({
                "x": m["x"] + random.randint(-10, 10),
                "y": m["y"] + random.randint(-10, 10),
                "type": coin_data["type"],
                "amount": coin_data["amount"],
                "frames": coin_data["frames"],
                "frame_index": 0,
            })
    
        exp_keys = []
        while exp_total > 0:
            if exp_total >= 10 and "exp_10" in self.drop_item_types:
                exp_keys.append("exp_10")
                exp_total -= 10
            elif exp_total >= 5 and "exp_5" in self.drop_item_types:
                exp_keys.append("exp_5")
                exp_total -= 5
            elif "exp_1" in self.drop_item_types:
                exp_keys.append("exp_1")
                exp_total -= 1
            else:
                break
    
        for exp_key in exp_keys:
            exp_data = self.drop_item_types[exp_key]
            self.dropped_coins.append({
                "x": m["x"] + random.randint(-10, 10),
                "y": m["y"] + random.randint(-10, 10),
                "type": exp_data["type"],
                "amount": exp_data["amount"],
                "frames": exp_data["frames"],
                "frame_index": 0,
            })


    def update_frame(self):
        if not self.character.character_alive:
            self.update()
            return
        #攻撃アニメーション中は通常アニメーション処理をしない
        if self.attack_animation_playing:
            self.update()
            return
        if self.keys_pressed:
            dx, dy = 0, 0
            if Qt.Key_Left in self.keys_pressed or Qt.Key_A in self.keys_pressed:
                play_se("walk")
                dx -= self.move_speed
                self.facing_right = False
            if Qt.Key_Right in self.keys_pressed or Qt.Key_D in self.keys_pressed:
                play_se("walk")
                dx += self.move_speed
                self.facing_right = True

            if Qt.Key_Up in self.keys_pressed or Qt.Key_W in self.keys_pressed:
                play_se("walk")
                dy -= self.move_speed
                self.facing_down = False
            if Qt.Key_Down in self.keys_pressed or Qt.Key_S in self.keys_pressed:
                play_se("walk")
                dy += self.move_speed
                self.facing_down = True
            new_x = min(max(self.x + dx, 0), self.width() - self.current_pixmap.width())
            new_y = min(max(self.y + dy, 0), self.height() - self.current_pixmap.height())
            
            if dx != 0 or dy != 0:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.character.frames)
                base_frame = self.character.frames[self.current_frame_index]
                self.current_pixmap = self.get_oriented_pixmap(base_frame)
            else:
                # 動いていないときは静止画像
                self.current_pixmap = self.get_oriented_pixmap(self.character.static_pixmap)

            player_rect = QRect(new_x, new_y, self.current_pixmap.width(), self.current_pixmap.height())
            for m in self.monsters:
                if m["alive"]:
                    m_rect = QRect(m["x"], m["y"], m["pixmap"].width(), m["pixmap"].height())
                    if player_rect.intersects(m_rect) and not self.attack_animation_playing:
                     play_se("attack_c")
                     m["hp"] -= self.character.attack_power #キャラからモンスターへのダメージ
                     self.character.hp -= m["attack_power"]  #モンスターからキャラへのダメージ（個別攻撃力）
                     self.hp_window.update_hp(self.character.hp, self.character.max_hp)
                     self.hp_window.show_message(f"{m['display_name']} の攻撃！ {m['attack_power']} ダメージ！")
                     self.hp_window.show_message(f"{m['display_name']} のHP: {m['hp']}/{m['max_hp']}")
                     self.start_attack_animation()
                     self.apply_knockback(m)  # ノックバック処理追加
                if m["hp"] <= 0 and m["alive"]:
                    self.handle_monster_death(m)
                if self.character.hp <= 0:
                    play_se("death_c")
                    self.character.character_alive = False
                    self.hp_window.show_message("ゲームオーバー") 
                        #ゲームオーバーの通知とスタート画面への遷移
                    QMessageBox.information(
                        self,
                        "ゲームオーバー",
                        "あなたは倒れました...\nスタート画面に戻ります。",
                        QMessageBox.Ok
                    )

                    stop_bgm()
                    if self.hp_window and self.hp_window.isVisible():
                        self.hp_window.close()
                    if self.settings_window and self.settings_window.isVisible():
                        self.settings_window.close()
                    if hasattr(self, "inn_window") and self.inn_window and self.inn_window.isVisible():
                        self.inn_window.close()
                    if hasattr(self, "shop_window") and self.shop_window and self.shop_window.isVisible():
                        self.shop_window.close()
                    if hasattr(self, "monster_dex_window") and self.monster_dex_window and self.monster_dex_window.isVisible():
                        self.monster_dex_window.close()
                    self.close()
                    if self.return_to_menu_callback:
                        self.return_to_menu_callback()
                    return 
            if not self.attack_animation_playing:
                self.x, self.y = new_x, new_y
        else:
            self.current_pixmap = self.get_oriented_pixmap(self.character.static_pixmap)
        
        #ドロップアイテムの取得
        picked_up_coin = False
        picked_up_exp = False
        player_rect = QRect(self.x, self.y, self.current_pixmap.width(), self.current_pixmap.height())
        new_coin_list = []
        for item in self.dropped_coins:
            width, height = item.get("size", (32, 32))
            item_rect = QRect(item["x"], item["y"], width, height)
            if player_rect.intersects(item_rect):
                if item["type"] == "coin":
                    self.character.coins += item["amount"]
                    self.hp_window.update_coin(self.character.coins)
                    self.hp_window.show_message(f"{item['amount']}コインを拾った！")
                    picked_up_coin = True
                elif item["type"] == "exp":
                    self.character.add_exp(item["amount"], hp_window=self.hp_window)
                    self.hp_window.update_exp(self.character.level, self.character.exp, self.character.exp_to_next)
                    self.hp_window.show_message(f"{item['amount']} 経験値を獲得！")
                    picked_up_exp = True
            else:
                new_coin_list.append(item)
        if picked_up_coin == True:
            play_se("coin") 
        if picked_up_exp == True:
            play_se("exp")   
        self.dropped_coins = new_coin_list

        self.update()

    def keyPressEvent(self, event):

        #escで終了
        if event.key() == Qt.Key_Escape:
            play_se("window_open")
            reply = QMessageBox.question(
                self,
                "ゲーム終了の確認",
                "スタート画面に戻りますか？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                stop_bgm()
                if self.hp_window.isVisible():
                    self.hp_window.close()      # もしくは self.hp_window.hide()
                if self.settings_window.isVisible():
                    self.settings_window.close()
                if hasattr(self, "inn_window") and self.inn_window.isVisible():
                    self.inn_window.close()
                if hasattr(self, "shop_window") and self.shop_window.isVisible():
                    self.shop_window.close()
                if hasattr(self, "monster_dex_window") and self.monster_dex_window and self.monster_dex_window.isVisible():
                    self.monster_dex_window.close()
                self.close()
                if self.return_to_menu_callback:
                    self.return_to_menu_callback() 
            return

        #ctrl+Cでリセット
        #elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            #self.reset_positions()  
        #1と2でスキル選択（後でスキルボタン作成）
        elif event.key() == Qt.Key_1:
            self.selected_skill_key = "fireball"
            self.show_message("スキルをファイアボールに切り替えました")
        elif event.key() == Qt.Key_2:
            self.selected_skill_key = "ice"
            self.show_message("スキルをアイスブラストに切り替えました")
        #Fでスキル発動
        elif event.key() == Qt.Key_F:
            skill_key = self.selected_skill_key
            if self.character.use_skill(skill_key, show_message=self.hp_window.show_message):
                skill_info = self.character.skills[skill_key]
                skill_type = skill_info.get("type", "throw")
                #スキルの位置を決定（キャラの左上が基準、＋が右と下）
                if skill_type == "throw":
                    offset_x = 64 if self.facing_right else -500 #右向いてたら64PXの位置にスキル出現(画像の左上を基準)
                    skill_pos = QPoint(self.x + offset_x, self.y)
                elif skill_type == "put":
                    offset_y = 64 if self.facing_down else -500 #下を向いてたら64pxの位置
                    skill_pos = QPoint(self.x, self.y + offset_y)
                else:
                    skill_pos = QPoint(self.x, self.y) 
                self.show_skill_animation(skill_info, position=skill_pos, skill_type=skill_type, facing_right=self.facing_right, facing_down = self.facing_down)

        #Sでステータス画面表示
        elif event.key() == Qt.Key_C:
            if self.hp_window.isVisible():
                play_se("window_close")
                self.hp_window.hide()
            else:
                play_se("window_open")
                self.hp_window.show()
                self.activateWindow()
                self.setFocus()

        #Qで設定画面表示
        elif event.key() == Qt.Key_Q:
            if self.settings_window.isVisible():
                play_se("window_close")
                self.settings_window.hide()
            else:
                play_se("window_open")
                self.settings_window.show()
                self.activateWindow()
                self.setFocus()

        #Pでセーブ
        elif event.key() == Qt.Key_P:
            play_se("save")
            save_game(
                self.character, 
                self.defeated_bosses, 
                self.defeated_monsters,
                self.monster_kill_count,
                self.unlocked_dungeons,
                self.character.inventory,
            )
            self.hp_window.show_message("セーブしました")

        elif not self.character.character_alive:
            return

        #Mでモンスター図鑑
        elif event.key() == Qt.Key_M:
            if hasattr(self, "monster_dex_window") and self.monster_dex_window.isVisible():
                play_se("window_close")
                self.monster_dex_window.hide()
            else:
                play_se("window_open")
                self.monster_dex_window = MonsterDexWindow(self.defeated_monsters, Monster.monster_data, self.monster_folder, main_window=self)
                self.monster_dex_window.show()
                self.activateWindow()
                self.setFocus()

        #spaceでINNに入る
        elif event.key() == Qt.Key_Space:
            if hasattr(self, "inn_window") and self.inn_window is not None and self.inn_window.isVisible():
                self.inn_window.close()
                self.inn_window = None
                return 
            player_rect = QRect(self.x, self.y, self.current_pixmap.width(), self.current_pixmap.height())
            inn_rect = QRect(self.inn_x, self.inn_y, self.inn_pixmap.width(), self.inn_pixmap.height())
            if player_rect.intersects(inn_rect):
                play_se("INN")
                self.keys_pressed.clear() 
                self.inn_window = InnWindow(on_dungeon_selected=self.enter_dungeon, on_return_home=self.return_to_home, parent=self)
                self.inn_window.show()  
                self.inn_window.activateWindow()
                self.inn_window.setFocus()

        else:
            self.keys_pressed.add(event.key())
        
    def keyReleaseEvent(self, event):
        if event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())
        if not self.character.character_alive:
            return
    #リセット機能
    def reset_positions(self):
        screen = QApplication.primaryScreen().geometry()

        self.x = screen.width() // 2
        self.y = screen.height() // 2

        self.character.max_hp = self.character.hp_base
        self.character.hp = self.character.hp_base
        self.character.power = self.character.power_base
        self.character.defense = self.character.defense_base
        self.character.magic = self.character.magic_base
        self.character.attack_power = self.character.calculate_attack_power()
        self.character.speed = self.character.speed_base
        self.character.level = self.character.level_base
        self.character.exp = self.character.exp_base
        self.character.coins = self.character.coins_base
        self.character.exp_to_next = self.character.exp_to_next_base
        self.character.boss_level = self.character.boss_level_base

        self.hp_window.update_hp(self.character.hp, self.character.max_hp)
        self.hp_window.update_exp(self.character.level, self.character.exp, self.character.exp_to_next)
        self.hp_window.update_coin(self.character.coins)
        self.hp_window.update_status(self.character)

        self.character.character_alive = True
        self.monsters.clear()
        self.dropped_coins.clear()
        self.attacking = False
        self.attack_animation_playing = False
        self.facing_right = False
        self.current_pixmap = self.character.static_pixmap
        print("状態リセット")
        self.update()

    def show_message(self, text):
        if self.hp_window:
            self.hp_window.show_message(text)
#スキルアニメーションの攻撃処理
class SkillAnimation(QLabel):
    def __init__(self, parent, frames, pos, interval, damage, skill_type="throw", facing_right=True, facing_down = True):
        super().__init__(parent)
        self.parent = parent
        self.frames = frames
        self.index = 0
        self.interval = interval
        self.damage = damage
        self.skill_type = skill_type
        self.facing_right = facing_right
        self.facing_down = facing_down
        self.setPixmap(self.frames[self.index])
        self.resize(self.frames[0].size())
        self.move(pos)
        self.hitbox = QRect(pos, self.size())  # ヒットボックスの矩形
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(self.interval)
        self.show()

        if skill_type == "throw":
            self.dx = 20 if facing_right else -20 #毎フレーム向いてる方向に10PX移動する
        elif skill_type == "put":
            self.dx = 50 if facing_down else -50
        else:
            self.dx = 0

    def next_frame(self):
        if self.skill_type == "throw":
            self.move(self.x() + self.dx, self.y())
            self.hitbox.moveTo(self.x(), self.y())
            self.check_hit()
        if self.skill_type == "put":
            self.move(self.x(), self.y()+ self.dx)
            self.hitbox.moveTo(self.x(), self.y())
            self.check_hit()
        #throwじゃない場合は最初のフレームだけ当たり判定
        if self.index == 0:
            self.check_hit()
        #次のフレームに移行する
        self.index += 1
        #アニメーションのフレームを超えたら終了
        if self.index >= len(self.frames):
            self.timer.stop()
            self.deleteLater()
        else:
            self.setPixmap(self.frames[self.index])

    def check_hit(self):
        for m in self.parent.monsters:
            if not m["alive"]:
                continue
            m_rect = QRect(m["x"], m["y"], m["pixmap"].width(), m["pixmap"].height())
            if self.hitbox.intersects(m_rect):
                m["hp"] -= self.damage
                self.parent.hp_window.show_message(f"{m['display_name']} に {self.damage} ダメージ！")
                self.parent.hp_window.show_message(f"{m['display_name']} のHP: {m['hp']}/{m['max_hp']}")
                if m["hp"] <= 0 and m["alive"]:
                    self.parent.handle_monster_death(m)
