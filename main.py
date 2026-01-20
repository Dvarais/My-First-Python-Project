# --- 4. ОСНОВНОЙ ЦИКЛ (MAIN LOOP) | MAIN LOOP ---
from game_data import rooms
from game_utils import *

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