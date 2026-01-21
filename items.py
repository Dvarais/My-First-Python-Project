# Модуль предметов и их создания | Items and factory module

class Item:
    # Базовый класс предмета | Base item class
    def __init__(self, name, Value):
        self.name = name
        self.Value = Value
    
    def __str__(self):
        return self.name
    
class Weapon(Item):
    # Класс оружия (наследует Item) | Weapon class (inherits Item)
    def __init__(self, name, Value, damage):
        super().__init__(name, Value)
        self.damage = damage

class Consumables(Item):
    # Класс расходников (наследует Item) | Consumables class (inherits Item)
    def __init__(self, name, Value, heal_amount):
        super().__init__(name, Value)
        self.heal_amount = heal_amount

# Справочник параметров для создания предметов | Item parameters database
ITEM_DATABASE = {
    'Меч': (Weapon, 50, 25),
    'Боевой Топор': (Weapon, 50, 40),
    'Яблоко': (Consumables, 5, 20),
    'Лечебное зелье': (Consumables, 20, 100),
    'Фонарик': (Item, 5),
    'Ключ': (Item, 10),
    'Щит': (Item, 40)
    }

def create_item(name):
    # Фабрика для преобразования строки в объект класса | Factory to convert string to class object
    if name not in ITEM_DATABASE:
        return None
    
    cls, value, extra = ITEM_DATABASE[name]
    if cls == Item:
        return cls(name, value)
    return cls(name, value, extra)
