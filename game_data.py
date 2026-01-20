# --- 1. КЛАССЫ (ЧЕРТЕЖИ) | CLASSES (BLUEPRINTS) --- 
class Enemy:
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

class Player:
    def __init__(self):
        self.hp = 100
        self.xp = 0
        self.level = 1
        self.gold = 0
        self.inventory = []

    def is_alive(self):
        return self.hp > 0
        

# --- 2. ДАННЫЕ (КАРТА) | DATA (MAP) ---
rooms = {
    'Холл': {
        'описание': 'Вы в Холле. Двери ведут на Кухню и в Чулан и в Магазин.',
        'item': 'Фонарик',
        'enemy': None,
        'exits': ['Кухня', 'Чулан', 'Магазин']
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