import os
import json
import random

# --- ОПРЕДЕЛЯЕМ ПУТЬ К ФАЙЛУ --- | --- DEFINING THE FILE PATH ---
# Получаем папку, где лежит скрипт game.py | Getting the folder where the game.py script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Склеиваем путь к папке + имя файла. Получится что-то типа C:\Users\tik26\Desktop\test\savefile.json | Joining the folder path + file name. It will look like C:\Users\tik26\Desktop\test\savefile.json
SAVE_FILE = os.path.join(script_dir, "savefile.json")

# --- 1. КЛАССЫ (ЧЕРТЕЖИ) | CLASSES (BLUEPRINTS) --- 
class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

# --- 2. ДАННЫЕ (КАРТА) | DATA (MAP) ---
rooms = {
    'Холл': {
        'описание': 'Вы в Холле. Двери ведут на Кухню и в Чулан.',
        'item': 'Фонарик',
        'enemy': None,
        'exits': ['Кухня', 'Чулан']
    },
    'Кухня': {
        'описание': 'Здесь пахнет едой. На столе что-то блестит.',
        'item': 'Ключ',
        # Скелет: 50 HP, бьет на 15 | Skeleton: 50 HP, hits for 15
        'enemy': Enemy("Скелет", 50, 15),
        'exits': ['Холл', 'Сад']
    },
    'Чулан': {
        'описание': 'Пыльная каморка с инструментами.',
        'item': 'Меч',
        'enemy': None,
        'exits': ['Холл']
    },
    'Сад': {
        'описание': 'Вы в темном Саду. Здесь веет опасностью.',
        'item': 'Яблоко',
        # Босс Орк: 80 HP, бьет на 20 | Boss Orc: 80 HP, hits for 20
        'enemy': Enemy("Орк", 80, 20),
        'exits': ['Кухня']
    },
    'Магазин': {
        'описание': 'Магазин торговца. Здесь можно купить разные вещи.',
        'item': None,
        'sale_items': {
            'Лечебное зелье': 20,
            'Топор': 50,
            'Щит': 40
        },
        'enemy': None,
        'exits': ['Холл']
    }
}

# --- 3. ФУНКЦИИ (ДВИЖОК) | FUNCTIONS (ENGINE) ---

def save_game(room, inv, hp, xp, level, gold, map_data):
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
        'inventory': inv,
        'hp': hp,
        'xp': xp,
        'level': level,
        'gold': gold,
        'rooms_data': serializable_rooms # Добавляем карту | Adding the map
    }
    # "w" означает write (запись) | "w" means write
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4) # indent для красоты файла | indent for file readability
    print("💾 Игра (и состояние врагов) сохранена!")

def load_game():
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

        print("📂 Сохранение загружено полностью!")

        # 3. Возвращение данных | 3. Return the loaded data
        return data["current_room"], data["inventory"], data["hp"], data["xp"], data["level"], data["gold"], loaded_rooms

    except FileNotFoundError:
        # Если файла нет — просто скажем об этом, без ошибок | If the file doesn't exist - just inform without errors
        print("❌ Файл сохранения не найден. Сначала сохраните игру.")
        return None

def clear():
    """Очищает экран консоли | Clears the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_status(room, inv, hp, level, xp, gold):
    print("------------------------------------------------")
    print(f"📍 Вы находитесь: {rooms[room]['описание']}")
    print(f"🚪 Выходы: {rooms[room]['exits']}")
    print(f"👤 Герой: Уровень {level} (Опыт: {xp}/100)")
    print(f"❤️ Здоровье: {hp}%")
    print(f"💰 Золото: {gold}")
    print(f"🎒 Инвентарь: {inv}")
    print("------------------------------------------------")

def shop(gold, inv):
    if current_room != 'Холл':
        print("Магазин недоступен.")
        print("Магазин доступен только из Холла.")
        return gold, inv
    clear()
    print("\n🏪 Добро пожаловать в магазин!")
    print(f"В вашем кошельке сейчас: {gold} золота.")
    print("--- ЛАВКА ТОРГОВЦА ---")
    print("1. Лечебное зелье (20 золота) - восстанавливает 100% здоровья")
    print("2. Боевой Топор (50 золота) - Урон 35-50")
    print("3. Щит (40 золота) - Защита 5-10")
    print("4. Выйти из магазина")
    
    choice = input("Выберите товар (1-4): ")
    
    if choice == '1':
        if gold >= 20:
            gold -= 20
            inv.append('Лечебное зелье')
            print("Вы купили Лечебное зелье!")
        else:
            print("Недостаточно золота.")
    elif choice == '2':
        if gold >= 50:
            if 'Боевой Топор' not in inv:
                gold -= 50
                inv.append('Боевой Топор')
                print("Вы купили Боевой Топор!")
            else:
                print("У вас уже есть Боевой Топор.")
        else:
            print("Недостаточно золота.")
    
    elif choice == '3':
        if gold >= 40:
            if 'Щит' not in inv:
                gold -= 40
                inv.append('Щит')
                print("Вы купили Щит!")
            else:
                print("У вас уже есть Щит.")
        else:
            print("Недостаточно золота.")

    elif choice == '4':
        print("Вы вышли из магазина.") # Выходим из магазина обратно в игру | Exiting the shop back to the game
    else:
        print("Неверный выбор.")
    
    return gold, inv # Возвращаем остаток денег и обновленный инвентарь | Return remaining gold and updated inventory

def check_enemy(room, map_data):
    enemy = map_data[room].get('enemy')
    if enemy:
        print(f"\n👀 Внимание! В комнате находится {enemy.name} (HP: {enemy.hp})!")

def move_player(current, direction, map_data, hp):
    enemy = map_data[current].get('enemy')
    if enemy:
        escape_damage = random.randint(15, 20)
        print(f"\n💥 Вы пытаетесь убежать, но {enemy.name} наносит вам {escape_damage} урона!")
        input("Нажмите Enter...")
        return current, hp - escape_damage

    if direction in map_data[current]['exits']:
        return direction, hp
    elif direction not in map_data[current]['exits']:
        print("Туда нет прохода.")
        input("Нажмите Enter...")
        return current, hp

def handle_item(room, inv, map_data):
    thing = map_data[room]['item']
    if thing is None:
        print("Здесь пусто.")
    else:
        inv.append(thing)
        map_data[room]['item'] = None
        print(f"Вы взяли: {thing}")

def attack_enemy(room, inv, map_data, player_hp, player_level, player_xp, player_gold):
    enemy = map_data[room].get('enemy')
    if not enemy:
        print("Здесь никого нет.")
        return player_hp, player_xp, player_level, player_gold
    # 1. Атака Игрока (с рандомом) | 1. Player Attack (randomized)
    if 'Боевой Топор' in inv:
        damage = random.randint(35, 50) # Топор: 35-50 урона | Axe: 35-50 damage
        weapon_name = 'Боевой Топор'
    elif 'Меч' in inv:
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
        player_gold += gold_gain
        player_xp += xp_gain
        print(f"⭐ Вы получили {xp_gain} опыта и {gold_gain} золота!") 
        # Награда за победу | Reward for victory
        if player_xp >= 100:
            player_level += 1
            player_xp -= 100
            player_hp = 100  # Восстанавливаем здоровье при повышении уровня | Restore health on level up
            print(f"⬆️ Поздравляем! Вы достигли уровня {player_level}!")
            print("❤️ Ваше здоровье полностью восстановлено!")

        return player_hp, player_xp, player_level, player_gold # Возвращаем обновленные данные | Return updated data

    # 3. Ответный удар Врага (с рандомом) | 3. Enemy counter-attack (randomized)
    # Урон врага +/- 5 единиц | Enemy damage +/- 5 units
    enemy_dmg = random.randint(enemy.damage - 5, enemy.damage + 5)

    if 'Щит' in inv:
        Shield_block = random.randint(5, 10) # Щит блокирует 5-10 урона | Shield blocks 5-10 damage
        enemy_dmg -= Shield_block
        print(f"🛡️ Ваш Щит блокировал {Shield_block} урона!")

    if enemy_dmg < 0: enemy_dmg = 0
    
    print(f"{enemy.name} еще стоит! (HP: {enemy.hp})")
    print(f"💥 {enemy.name} атакует вас в ответ на {enemy_dmg} урона!")
    
    return player_hp - enemy_dmg, player_xp, player_level, player_gold

# --- 4. ОСНОВНОЙ ЦИКЛ (MAIN LOOP) | MAIN LOOP ---

current_room = 'Холл'
inventory = []
player_hp = 100
player_xp = 0
player_level = 1
player_gold = 0

clear()

while True:
    # --- Условия победы/поражения | Win/Loss conditions ---
    if current_room == 'Сад' and rooms['Сад']['enemy'] is None:
        # Если мы в Саду и убили Орка - это финальная победа | If we are in the Garden and killed the Orc - this is the final victory
        print("\n🏆 ПОБЕДА! Вы одолели Орка и стали героем подземелья!")
        break
    
    # Старый вариант победы (через дверь в Холле) | Old victory variant (via the Hall door)
    if current_room == 'Холл' and 'Ключ' in inventory:
        print("\n🎉 ПОБЕДА! Вы открыли дверь ключом и сбежали!")
        break

    # --- Интерфейс | Interface ---
    show_status(current_room, inventory, player_hp, player_level, player_xp, player_gold)
    check_enemy(current_room, rooms)
    
    # --- Ввод | Input ---
    command = input("\nДействие (Кухня, Чулан, Холл, Сад, Магазин, Взять, Атаковать, Поесть, Сохранить, Загрузить, Выход) > ").capitalize()
    
    clear() 

    # --- Логика | Logic ---
    if command == 'Выход':
        print("Игра сохранена (шутка, сохранения мы еще не проходили). Пока!")
        break
    
    elif command == 'Сохранить':
        save_game(current_room, inventory, player_hp, player_xp, player_level, player_gold, rooms)
        input("Нажмите Enter...") # Чтобы игрок успел прочитать | So the player has time to read

    elif command == 'Магазин':
        if current_room == 'Холл':
            player_gold, inventory = shop(player_gold, inventory)
        else:
            print("Торговец ждет вас в Холле.")
            input("Нажмите Enter...") # Чтобы игрок успел прочитать | So the player has time to read

    elif command == 'Загрузить':
        result = load_game()
        if result:
            # Теперь распаковываем 4 переменные, включая rooms | Now unpacking 4 variables, including rooms
            current_room, inventory, player_hp, player_xp, player_level, player_gold, rooms = result
        else:
            pass
        input("Нажмите Enter...") # Чтобы игрок успел прочитать | So the player has time to read 

    elif command == 'Взять':
        handle_item(current_room, inventory, rooms)
        
    elif command == 'Поесть':
        if 'Яблоко' in inventory:
            inventory.remove('Яблоко')
            player_hp += 20
            if player_hp > 100: player_hp = 100
            print(f"🍏 Ням! Здоровье восстановлено до {player_hp}%")

        elif 'Лечебное зелье' in inventory:
            inventory.remove('Лечебное зелье')
            player_hp = 100
            print("🧪 Вы выпили Лечебное зелье. Здоровье полностью восстановлено!")

        else:
            print("У вас нет еды или зелья.")

    elif command == 'Атаковать':
        player_hp, player_xp, player_level, player_gold = attack_enemy(current_room, inventory, rooms, player_hp, player_level, player_xp , player_gold)
        if player_hp <= 0:
            print("\n☠️ В ГЛАЗАХ ПОТЕМНЕЛО... GAME OVER")
            break
            
    else:
        current_room, player_hp = move_player(current_room, command, rooms, player_hp)
        if player_hp <= 0:
            print("\n☠️ В ГЛАЗАХ ПОТЕМНЕЛО... GAME OVER")
            break