import os
import json
import random
from game_data import Enemy, Player

# --- 3. ФУНКЦИИ (ДВИЖОК) | FUNCTIONS (ENGINE) ---

script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(script_dir, "savefile.json")

def save_game(room, player, map_data):
    # 1. Готовим карту к сохранению (превращаем Enemies в словари) | Preparing the map for saving (turning Enemies into dictionaries)
    serializable_rooms = {}

    for room_name, room_info in map_data.items():
        # Делаем копию комнаты, чтобы не сломать текущую игру | Make a copy of the room to not break the current game
        new_info = room_info.copy()

        enemy_obj = room_info.get('enemy')
        if enemy_obj:
            # Есть ли враг, превращаем его в словарь | If there's an enemy, turn it into a dictionary
            new_info['enemy'] = {
                'name': enemy_obj.name,
                'hp': enemy_obj.hp,
                'damage': enemy_obj.damage,
                'is_enemy_object': True # Метка, чтобы при загрузке понять, что это был враг | A flag to understand during loading that this was an enemy
            }
        else:
            new_info['enemy'] = None

        serializable_rooms[room_name] = new_info

    # 2. Сохраняем все данные в файл | Saving all data to file
    data = {
        'current_room': room,
        'inventory': player.inventory,
        'hp': player.hp,
        'xp': player.xp,
        'level': player.level,
        'gold': player.gold,
        'rooms_data': serializable_rooms # Добавляем карту | Adding the map
    }
    # "w" означает write (запись) | "w" means write
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4) # indent для красоты файла | indent for file readability
    print("💾 Игра (и состояние врагов) сохранена!")

def load_game(player):
    try:
        # "r" означает read (чтение) | "r" means read
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        loaded_rooms = data['rooms_data']
        for room_name, room_info in loaded_rooms.items():
            enemy_data = room_info.get('enemy')
            if enemy_data and enemy_data.get('is_enemy_object'):
                # 1. Создаем переменную new_enemy | 1. Create variable new_enemy
                new_enemy = Enemy(
                    enemy_data['name'],
                    enemy_data['hp'],
                    enemy_data['damage']
                )
                # 2. Кладем её в словарь | 2. Put it in the dictionary
                loaded_rooms[room_name]['enemy'] = new_enemy


        player.inventory = data["inventory"]
        player.hp = data["hp"]
        player.xp = data["xp"]
        player.level = data["level"]
        player.gold = data["gold"]

        print("📂 Сохранение загружено полностью!")

        return data["current_room"], loaded_rooms

    except FileNotFoundError:
        # Если файла нет — просто скажем об этом, без ошибок | If the file doesn't exist - just inform without errors
        print("❌ Файл сохранения не найден. Сначала сохраните игру.")
        return None

def clear():
    """Очищает экран консоли | Clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_status(room, player, rooms):
    print("------------------------------------------------")
    print(f"📍 Вы находитесь: {rooms[room]['описание']}")
    print(f"🚪 Выходы: {rooms[room]['exits']}")
    print(f"👤 Герой: Уровень {player.level} (Опыт: {player.xp}/100)")
    print(f"❤️ Здоровье: {player.hp}%")
    print(f"💰 Золото: {player.gold}")
    print(f"🎒 Инвентарь: {player.inventory}")
    print("------------------------------------------------")

def shop(player, rooms):
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
                    player.inventory.append(item_name)
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
    enemy = map_data[room].get('enemy')
    if enemy:
        print(f"\n👀 Внимание! В комнате находится {enemy.name} (HP: {enemy.hp})!")

def move_player(current, direction, map_data, player):
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
    thing = map_data[room]['item']
    if thing is None:
        print("Здесь пусто.")
    else:
        player.inventory.append(thing)
        map_data[room]['item'] = None
        print(f"Вы взяли: {thing}")

def attack_enemy(room, player, map_data):
    enemy = map_data[room].get('enemy')
    if not enemy:
        print("Здесь никого нет.")
        return 
    # 1. Атака Игрока (с рандомом) | 1. Player Attack (randomized)
    if 'Боевой Топор' in player.inventory:
        damage = random.randint(35, 50) # Топор: 35-50 урона | Axe: 35-50 damage
        weapon_name = 'Боевой Топор'
    elif 'Меч' in player.inventory:
        damage = random.randint(20, 35) # Меч: 20-35 урона | Sword: 20-35 damage
        weapon_name = 'Меч'
    else:
        damage = random.randint(3, 8)   # Кулак: 3-8 урона | Fist: 3-8 damage
        weapon_name = 'Кулак'

    if random.random() < 0.20:  # 20% шанс критического удара | 20% chance of critical hit
        damage *= 2
        print(f"\n🔥 КРИТИЧЕСКИЙ УДАР! Вы нанесли {damage} урона {weapon_name}!")
    else:
        print(f"\n⚔️ Вы ударили {enemy.name} {weapon_name} на {damage} урона.")

    enemy.hp -= damage
    
    # 2. Проверка победы | 2. Check victory
    if enemy.hp <= 0:
        print(f"💀 {enemy.name} побежден!")
        map_data[room]['enemy'] = None 
        xp_gain = 60
        gold_gain = random.randint(20, 25)
        player.gold += gold_gain
        player.xp += xp_gain
        print(f"⭐ Вы получили {xp_gain} опыта и {gold_gain} золота!") 
        # Награда за победу | Reward for victory
        if player.xp >= 100:
            player.level += 1
            player.xp -= 100
            player.hp = 100  # Восстанавливаем здоровье при повышении уровня | Restore health on level up
            print(f"⬆️ Поздравляем! Вы достигли уровня {player.level}!")
            print("❤️ Ваше здоровье полностью восстановлено!")

        return # Возвращаем обновленные данные | Return updated data

    # 3. Ответный удар Врага (с рандомом) | 3. Enemy counter-attack (randomized)
    # Урон врага +/- 5 единиц | Enemy damage +/- 5 units
    enemy_dmg = random.randint(enemy.damage - 5, enemy.damage + 5)

    if 'Щит' in player.inventory:
        shield_block = random.randint(5, 10) # Щит блокирует 5-10 урона | Shield blocks 5-10 damage
        enemy_dmg -= shield_block
        print(f"🛡️ Ваш Щит блокировал {shield_block} урона!")

    if enemy_dmg < 0: enemy_dmg = 0
    player.hp -= enemy_dmg
    
    print(f"{enemy.name} еще стоит! (HP: {enemy.hp})")
    print(f"💥 {enemy.name} атакует вас в ответ на {enemy_dmg} урона!")
    