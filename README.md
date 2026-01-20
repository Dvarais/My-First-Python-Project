# Текстовая RPG на Python / Text-based RPG in Python

Это мой первый проект на Python. Консольная ролевая игра с элементами RPG. 
This is my first Python project. A console-based role-playing game with RPG elements.

---

## 🇷🇺 Русский (Russian)

### 🛠 Журнал исправлений
| Баг | Классификация | Решение |
|:---|:---|:---|
| Магазин доступен из любой точки | **Logic** | Привязка к локации |
| Нет авто-запуска магазина при входе | **Flow** | Авто-вызов `shop()` в комнате |
| Ошибка при вводе букв в магазине | **UX** | Проверка `isdigit()` |
| Урон при опечатках в бою | **Gameplay** | Проверка валидности пути |
| Мгновенная победа в Холле | **Logic** | Команда «Побег» |

### Функционал:
- 🗺️ **Перемещение** по локациям (Холл, Кухня, Чулан, Сад, Магазин).
- ⚔️ **Боевая система**: Сражения, критические удары, блоки щитом.
- 🎒 **Инвентарь**: Сбор предметов, использование еды и зелий.
- 💰 **Экономика**: Магазин с динамическим ассортиментом.
- 📈 **Прокачка**: Уровни героя и восстановление здоровья.
- 💾 **Сохранения**: Запись и чтение JSON-файла.

### Структура проекта:
- `main.py` — Основной цикл игры.
- `game_data.py` — Данные о комнатах и врагах.
- `game_utils.py` — Логика: бой, магазин, сохранения.

### Как запустить:
1. Установить Python.
2. Скачать все файлы проекта.
3. Запустить: `python main.py`.

---

## 🇺🇸 Английский (English)

### 🛠 Bug Fix Log
| Bug | Classification | Solution |
|:---|:---|:---|
| Shop available everywhere | **Logic** | Bind to location |
| No auto-start for shop | **Flow** | Auto-call `shop()` in room |
| Error on letter input in shop | **UX** | Added `isdigit()` check |
| Damage on typos during movement | **Gameplay** | Path validity check |
| Instant win in Hall | **Logic** | Added "Escape" command |

### Features:
- 🗺️ **Movement** through locations (Hall, Kitchen, Closet, Garden, Shop).
- ⚔️ **Combat System**: Battles, critical hits, shield blocks.
- 🎒 **Inventory**: Collecting items, using food and potions.
- 💰 **Economy**: Shop with dynamic assortment.
- 📈 **Progression**: Hero levels and health recovery.
- 💾 **Saves**: Save and load world state via JSON.

### Project Structure:
- `main.py` — Main game loop.
- `game_data.py` — Data about rooms and enemies.
- `game_utils.py` — Game logic: combat, shop, saves.

### How to Run:
1. Install Python.
2. Download all project files.
3. Run in the terminal: `python main.py`.