# Модуль игровых механик и утилит | Game mechanics and utilities module
import os
import json
import random
from items import Weapon, Item, Consumables, create_item
from game_data import Enemy, Player

script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(script_dir, "savefile.json")

def save_game(room, player, map_data):
    # Логика сериализации данных и записи в JSON | Data serialization and JSON writing logic
    serializable_rooms = {}

    for room_name, room_info in map_data.items():
        new_info = room_info.copy()

        enemy_obj = room_info.get('enemy')
        if enemy_obj:
            new_info['enemy'] = {
                'name': enemy_obj.name,
                'hp': enemy_obj.hp,
                'damage': enemy_obj.damage,
                'is_enemy_object': True 
            }
        else:
            new_info['enemy'] = None

        serializable_rooms[room_name] = new_info

    data = {
        'current_room': room,
        'inventory': [item.name for item in player.inventory if hasattr(item, 'name')],
        'hp': player.hp,
        'xp': player.xp,
        'level': player.level,
        'gold': player.gold,
        'rooms_data': serializable_rooms 
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4) 
    print("💾 Игра (и состояние врагов) сохранена!")

def load_game(player):
    # Логика чтения файла и десериализации объектов | File reading and object deserialization logic
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        loaded_rooms = data['rooms_data']
        for room_name, room_info in loaded_rooms.items():
            enemy_data = room_info.get('enemy')
            if enemy_data and enemy_data.get('is_enemy_object'):
                new_enemy = Enemy(
                    enemy_data['name'],
                    enemy_data['hp'],
                    enemy_data['damage']
                )
                loaded_rooms[room_name]['enemy'] = new_enemy


        loaded_names = data.get("inventory", [])
        player.inventory = [create_item(name) for name in loaded_names if create_item(name)]
        player.hp = data["hp"]
        player.xp = data["xp"]
        player.level = data["level"]
        player.gold = data["gold"]

        print("📂 Сохранение загружено полностью!")

        return data["current_room"], loaded_rooms

    except FileNotFoundError:
        print("❌ Файл сохранения не найден. Сначала сохраните игру.")
        return None

def clear():
    # Очистка консоли (кроссплатформенная) | Console clearing (cross-platform)
    os.system('cls' if os.name == 'nt' else 'clear')

def show_status(room, player, rooms):
    # Отображение информации о герое и локации | Hero and location info display
    print("------------------------------------------------")
    print(f"📍 Вы находитесь: {rooms[room]['описание']}")
    print(f"🚪 Выходы: {rooms[room]['exits']}")
    print(f"👤 Герой: Уровень {player.level} (Опыт: {player.xp}/100)")
    print(f"❤️ Здоровье: {player.hp}%")
    print(f"💰 Золото: {player.gold}")
    print(f"🎒 Инвентарь: {[item.name for item in player.inventory]}")
    print("------------------------------------------------")

def shop(player, rooms):
    # Меню взаимодействия с торговцем | Interaction menu with the merchant
    while True:
        clear()
        print("\n🏪 Добро пожаловать в магазин!")
        print(f"В вашем кошельке сейчас: {player.gold} золота.")
        print("--- ЛАВКА ТОРГОВЦА ---")
        items_for_sale = rooms['Магазин']['sale_items']
        item_names = list(items_for_sale.keys())

        for i, name in enumerate(item_names, 1):
            price = items_for_sale[name]
            print(f"{i}. {name} ({price} золота)")
        print(f"{len(item_names) + 1}. Выйти")
        
        choice = input("Выберите номер: ")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(item_names):
                item_name = item_names[idx]
                price = items_for_sale[item_name]
                if player.gold >= price:
                    player.gold -= price
                    new_item = create_item(item_name)
                    player.inventory.append(new_item)
                    print(f"Вы купили {item_name}")
                    input("\n Нажмите Enter, чтобы продолжить...")
                else:
                    print("Недостаточно золота.")
                    input("\n Нажмите Enter, чтобы продолжить...")
            elif idx == len(item_names):
                print("Выход...")
                input("\n Нажмите Enter, чтобы продолжить...")
                break
        else:
            print("Пожалуйста, введите число")

def check_enemy(room, map_data):
    # Проверка наличия противника в комнате | Checking for an enemy in the room
    enemy = map_data[room].get('enemy')
    if enemy:
        print(f"\n👀 Внимание! В комнате находится {enemy.name} (HP: {enemy.hp})!")

def move_player(current, direction, map_data, player):
    # Логика перемещения и штраф за побег | Movement logic and escape penalty
    enemy = map_data[current].get('enemy')
    
    if direction in map_data[current]['exits']:

        if enemy:
            escape_damage = random.randint(15, 20)
            print(f"\n💥 Вы пытаетесь убежать, но {enemy.name} наносит вам {escape_damage} урона!")
            player.hp -= escape_damage
            input("Нажмите Enter...")

            if not player.is_alive():
                return current

        return direction
        
        
    elif direction not in map_data[current]['exits']:
        print("Туда нет прохода.")
        input("Нажмите Enter...")
        return current

def handle_item(room, player, map_data):
    # Логика подбора предмета из комнаты | Room item pickup logic
    thing = map_data[room]['item']
    if thing is None:
        print("Здесь пусто.")
    else:
        player.inventory.append(thing)
        map_data[room]['item'] = None
        print(f"Вы взяли: {thing}")

def attack_enemy(room, player, map_data):
    # Обработка боя, выбор оружия и расчет урона | Combat processing, weapon selection and damage calculation
    enemy = map_data[room].get('enemy')
    if not enemy:
        print("Здесь никого нет.")
        return 

    damage = 5
    weapon_name = 'кулаки'
    for thing in player.inventory:
        if isinstance(thing, Weapon):
            if thing.damage > damage:
                damage = thing.damage
                weapon_name = thing.name

    if random.random() < 0.20:  # 20% шанс критического удара | 20% chance of critical hit
        damage *= 2
        print(f"\n🔥 КРИТИЧЕСКИЙ УДАР! Вы нанесли {damage} урона {weapon_name}!")
    else:
        print(f"\n⚔️ Вы ударили {enemy.name} {weapon_name} на {damage} урона.")

    enemy.hp -= damage
    
    if enemy.hp <= 0:
        print(f"💀 {enemy.name} побежден!")
        map_data[room]['enemy'] = None 
        xp_gain = 60
        gold_gain = random.randint(20, 25)
        player.gold += gold_gain
        player.xp += xp_gain
        print(f"⭐ Вы получили {xp_gain} опыта и {gold_gain} золота!") 
        if player.xp >= 100:
            player.level += 1
            player.xp -= 100
            player.hp = 100 
            print(f"⬆️ Поздравляем! Вы достигли уровня {player.level}!")
            print("❤️ Ваше здоровье полностью восстановлено!")
        return 

    enemy_dmg = random.randint(enemy.damage - 5, enemy.damage + 5)

    if 'Щит' in [i.name for i in player.inventory]:
        shield_block = random.randint(5, 10) 
        enemy_dmg -= shield_block
        print(f"🛡️ Ваш Щит блокировал {shield_block} урона!")

    if enemy_dmg < 0: enemy_dmg = 0
    player.hp -= enemy_dmg
    
    print(f"{enemy.name} еще стоит! (HP: {enemy.hp})")
    print(f"💥 {enemy.name} атакует вас в ответ на {enemy_dmg} урона!")