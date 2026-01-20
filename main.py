# --- 4. ОСНОВНОЙ ЦИКЛ (MAIN LOOP) | MAIN LOOP ---
from game_data import rooms, Player
from game_utils import *

current_room = 'Холл'
player = Player()

clear()

while True:
    # --- Условия победы/поражения | Win/Loss conditions ---
    if current_room == 'Сад' and rooms['Сад']['enemy'] is None:
        # Если мы в Саду и убили Орка - это финальная победа | If we are in the Garden and killed the Orc - this is the final victory
        print("\n🏆 ПОБЕДА! Вы одолели Орка и стали героем подземелья!")
        break

    # --- Интерфейс | Interface ---
    show_status(current_room, player, rooms)
    check_enemy(current_room, rooms)
    
    # --- Ввод | Input ---
    command = input("\nДействие (Кухня, Чулан, Холл, Сад, Магазин, Побег, Взять, Атаковать, Поесть, Сохранить, Загрузить, Выход) > ").capitalize()
    
    clear() 

    # --- Логика | Logic ---
    
    if current_room == 'Магазин':
        shop(player, rooms)
        current_room = "Холл"
        input("Нажмите Enter...") # Чтобы игрок успел прочитать | So the player has time to read
    
    elif command == 'Выход':
        print("Спасибо за игру! Не забудьте сохраниться перед выходом.")
        break
    
    elif command == 'Сохранить':
        save_game(current_room, player, rooms)
        input("Нажмите Enter...") # Чтобы игрок успел прочитать | So the player has time to read

    elif command == 'Загрузить':
        result = load_game(player)
        if result:
            # Теперь распаковываем 4 переменные, включая rooms | Now unpacking 4 variables, including rooms
            current_room, rooms = result
        else:
            pass
        input("Нажмите Enter...") # Чтобы игрок успел прочитать | So the player has time to read 

    elif command == 'Побег':
        if current_room == 'Холл' and 'Ключ' in player.inventory:
            print("\n🎉 ПОБЕДА! Вы открыли дверь ключом и сбежали!")
            break
        else:
            print("Вы не в Холле или у вас нет ключа от главной двери.")

    elif command == 'Взять':
        handle_item(current_room, player, rooms)
        
    elif command == 'Поесть':
        if 'Яблоко' in player.inventory:
            player.inventory.remove('Яблоко')
            player.hp += 20
            if player.hp > 100: player.hp = 100
            print(f"🍏 Ням! Здоровье восстановлено до {player.hp}%")

        elif 'Лечебное зелье' in player.inventory:
            player.inventory.remove('Лечебное зелье')
            player.hp = 100
            print("🧪 Вы выпили Лечебное зелье. Здоровье полностью восстановлено!")

        else:
            print("У вас нет еды или зелья.")

    elif command == 'Атаковать':
        attack_enemy(current_room, player, rooms)
        if not player.is_alive(): # Проверка, не умер ли при побеге
            print("\n☠️ В ГЛАЗАХ ПОТЕМНЕЛО... GAME OVER")
            break
            
    else:
        current_room = move_player(current_room, command, rooms, player)
        if not player.is_alive(): # Проверка, не умер ли при побеге
            print("\n☠️ В ГЛАЗАХ ПОТЕМНЕЛО... GAME OVER")
            break
