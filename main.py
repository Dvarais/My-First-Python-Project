# Главный модуль: основной цикл игры | Main module: game loop
from game_data import rooms, Player
from items import Weapon, Item, Consumables, create_item
from game_utils import *

current_room = 'Холл'
player = Player()

clear()

while True:
    # Проверка условий завершения игры | Win/Loss conditions check
    if current_room == 'Сад' and rooms['Сад']['enemy'] is None:
        print("\n🏆 ПОБЕДА! Вы одолели Орка и стали героем подземелья!")
        break

    # Обновление интерфейса пользователя | UI update
    show_status(current_room, player, rooms)
    check_enemy(current_room, rooms)
    
    # Обработка ввода пользователя | User input handling
    command = input("\nДействие (Кухня, Чулан, Холл, Сад, Магазин, Побег, Взять, Атаковать, Поесть, Сохранить, Загрузить, Выход) > ").capitalize()
    
    clear() 

    # Логика команд и взаимодействия | Command and interaction logic
    if current_room == 'Магазин':
        shop(player, rooms)
        current_room = "Холл"
        input("Нажмите Enter...") 
    
    elif command == 'Выход':
        print("Спасибо за игру! Не забудьте сохраниться перед выходом.")
        break
    
    elif command == 'Сохранить':
        save_game(current_room, player, rooms)
        input("Нажмите Enter...") 

    elif command == 'Загрузить':
        result = load_game(player)
        if result:
            current_room, rooms = result
        input("Нажмите Enter...") 

    elif command == 'Побег':
        # Логика завершения игры через главный выход | Win condition via the main exit
        has_key = False
        for thing in player.inventory:
            if thing.name == 'Ключ':
                has_key = True
                break

        if has_key and current_room == 'Холл':
            print("\n🎉 ПОБЕДА! Вы открыли дверь ключом и сбежали!")
            break
        else:
            print("Вы не в Холле или у вас нет ключа от главной двери.")

    elif command == 'Взять':
        handle_item(current_room, player, rooms)
        
    elif command == 'Поесть':
        # Логика использования расходников | Consumables usage logic
        food_found = None
        for thing in player.inventory:
            if isinstance(thing, Consumables):
                food_found = thing
                break
        if food_found:
            player.inventory.remove(food_found)
            player.hp += food_found.heal_amount
            if player.hp > 100: player.hp = 100
            print(f"Ваше здоровье успешно восстановлено на {food_found.heal_amount}")
        else:
            print("У вас нет еды или зелья.")

    elif command == 'Атаковать':
        # Инициирование сражения | Combat initiation
        attack_enemy(current_room, player, rooms)
        if not player.is_alive(): 
            print("\n☠️ В ГЛАЗАХ ПОТЕМНЕЛО... GAME OVER")
            break
            
    else:
        # Перемещение по карте | Map movement
        current_room = move_player(current_room, command, rooms, player)
        if not player.is_alive(): 
            print("\n☠️ В ГЛАЗАХ ПОТЕМНЕЛО... GAME OVER")
            break