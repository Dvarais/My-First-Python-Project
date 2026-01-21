# Мой первый проект на Python: Текстовый Квест
## 📦 Урок "Умные предметы" / Text Quest: "Smart Items" Lesson

**🇷🇺 Это мой первый проект по изучению Python.** Текстовая ролевая игра, в которой я практикую основы программирования и архитектуры кода. На данном этапе мы перешли от простого текста к полноценной **Объектно-Ориентированной Модели** предметов.

**🇺🇸 This is my first project for learning Python.** A text-based RPG where I practice programming basics and code architecture. At this stage, we moved from simple strings to a full **Object-Oriented Model** for items.

---

## 🇷🇺 Русский (Russian)

### 🛠 Изменения (Таблица рефакторинга)
| Файл | Что изменено | Результат |
| :--- | :--- | :--- |
| `items.py` | Создан новый модуль. Классы `Item`, `Weapon`, `Consumables`. | **Модульность:** логика предметов отделена от данных карты. |
| `items.py` | Реализована "Фабрика предметов" `create_item`. | **Безопасность:** централизованное создание объектов по их именам. |
| `game_data.py` | Очищены классы предметов, обновлен словарь `rooms`. | **Чистота:** карта теперь содержит объекты, а не текст. |
| `game_utils.py` | Переписаны функции `attack_enemy` и `shop`. | **Полиморфизм:** игра сама вычисляет урон по типу предмета. |
| `game_utils.py` | Обновлена система сохранений (сериализация имен). | **Стабильность:** объекты корректно переводятся в JSON. |
| `main.py` | Обновлена логика команд "Поесть" и "Побег". | **Гибкость:** поиск по типу предмета, а не по слову. |

### 🐞 Решенные Баги
*   **🔴 Критические:** Ошибки наследования (`super()`), краш при сохранении объектов в JSON, ошибки распаковки данных в Фабрике, неверный порядок создания предметов в магазине.
*   **🟠 Логические:** Привязка магазина к локации, устранение несоответствий имен (например, "Топор" vs "Боевой Топор").
*   **🟡 UI/UX:** Исправлен вывод объектов в инвентаре (теперь выводятся имена), добавлена проверка `isdigit()` в магазине.

---

## 🇺🇸 Английский (English)

### 🛠 Changes (Refactoring Table)
| File | What's Changed | Result |
| :--- | :--- | :--- |
| `items.py` | Created new module. `Item`, `Weapon`, `Consumables` classes. | **Modularity:** item logic is separated from map data. |
| `items.py` | Implemented "Item Factory" `create_item`. | **Safety:** centralized object creation by name. |
| `game_data.py` | Cleaned item classes, updated `rooms` dictionary. | **Cleanliness:** map now contains objects instead of text. |
| `game_utils.py` | Rewrote `attack_enemy` and `shop` functions. | **Polymorphism:** damage is calculated based on item type. |
| `game_utils.py` | Updated save system (name serialization). | **Stability:** objects correctly translate to JSON and back. |
| `main.py` | Updated "Eat" and "Escape" logic. | **Flexibility:** search by item type instead of specific word. |

### 🐞 Fixed Bugs
*   **🔴 Critical:** Inheritance errors (`super()`), JSON save crashes, data unpacking errors in the Factory, incorrect item creation order in the shop.
*   **🟠 Logic:** Bound shop to location, fixed name mismatches (e.g., "Axe" vs "Battle Axe").
*   **🟡 UI/UX:** Fixed technical object display in inventory (now shows names), added `isdigit()` check for shop input.

---

### Структура проекта / Project Structure:
- `main.py` — Основной цикл / Main loop.
- `items.py` — Классы предметов и Фабрика / Item classes & Factory.
- `game_data.py` — Карта и сущности / Map & Entities.
- `game_utils.py` — Логика (Бой, Магазин, Сохранения) / Logic (Combat, Shop, Saves).

### Как запустить / How to Run:
1. Install Python.
2. Run: `python main.py`.
