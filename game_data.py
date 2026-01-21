# Модуль данных: сущности и карта | Data module: entities and map
from items import Item, Weapon, Consumables

class Enemy:
    # Определение параметров врага | Enemy parameters definition
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

class Player:
    # Определение состояния игрока | Player state definition
    def __init__(self):
        self.hp = 100
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.inventory = []

    def is_alive(self):
        return self.hp > 0

# Структура игрового мира (комнаты) | Game world structure (rooms)
rooms = {
    'Холл': {
        'описание': 'Вы в Холле. Двери ведут на Кухню и в Чулан и в Магазин.',
        'item': Item('Фонарик', 5),
        'enemy': None,
        'exits': ['Кухня', 'Чулан', 'Магазин']
    },
    'Кухня': {
        'описание': 'Здесь пахнет едой. На столе что-то блестит.',
        'item': Item('Ключ', 10),
        'enemy': Enemy("Скелет", 50, 15),
        'exits': ['Холл', 'Сад']
    },
    'Чулан': {
        'описание': 'Пыльная каморка с инструментами.',
        'item': Weapon('Меч', 50, 15),
        'enemy': None,
        'exits': ['Холл']
    },
    'Сад': {
        'описание': 'Вы в темном Саду. Здесь веет опасностью.',
        'item': Consumables('Яблоко', 5, 20),
        'enemy': Enemy("Орк", 80, 20),
        'exits': ['Кухня']
    },
    'Магазин': {
        'описание': 'Магазин торговца. Здесь можно купить разные вещи.',
        'item': None,
        'sale_items': {
            'Лечебное зелье': 20,
            'Боевой Топор': 50,
            'Щит': 40
        },
        'enemy': None,
        'exits': ['Холл']
    }
}