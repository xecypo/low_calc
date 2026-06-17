import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# ВСТАВТЕ ВАШ ТОКЕН ТУТ МІЖ ЛАПКАМИ
BOT_TOKEN = "8945913462:AAEUvXnMcL6yKYr-_ODmYK1ah0bb-B35tgE"

# --- ВАША ПОВНА БАЗА ДАНИХ ---
DATABASE = {
    "Зброя": {
        "Слідопит"       : {"Атака": 6,  "Захист": 0, "Сила": 0, "Спритність": 2, "Інтуїція": 1, "Витривалість": 0, "Ухилення": 2, "Точність": 4,  "Крит": 0, "Опір криту": 0},
        "Варвар"         : {"Атака": 7,  "Захист": 0, "Сила": 2, "Спритність": 0, "Інтуїція": 0, "Витривалість": 2, "Ухилення": 0, "Точність": 0,  "Крит": 2, "Опір криту": 0},
        "Меч Паладина"   : {"Атака": 18, "Захист": 0, "Сила": 4, "Спритність": 0, "Інтуїція": 0, "Витривалість": 2, "Ухилення": 0, "Точність": 5,  "Крит": 0, "Опір криту": 8},
        "Метеоритний меч": {"Атака": 20, "Захист": 0, "Сила": 0, "Спритність": 6, "Інтуїція": 0, "Витривалість": 0, "Ухилення": 8, "Точність": 10, "Крит": 0, "Опір криту": 0},
        "Сокира Дракона" : {"Атака": 20, "Захист": 0, "Сила": 0, "Спритність": 0, "Інтуїція": 6, "Витривалість": 0, "Ухилення": 0, "Точність": 7,  "Крит": 8, "Опір криту": 0}
    },
    "Щит": {
        "Слідопит"       : {"Атака": 0, "Захист": 4,  "Сила": 0, "Спритність": 0, "Інтуїція": 0, "Витривалість": 2, "Ухилення": 9, "Точність": 3, "Крит": 0, "Опір криту": 0},
        "Варвар"         : {"Атака": 0, "Захист": 5,  "Сила": 1, "Спритність": 0, "Інтуїція": 0, "Витривалість": 4, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 10},
        "Щит Паладина"   : {"Атака": 0, "Захист": 13, "Сила": 2, "Спритність": 0, "Інтуїція": 0, "Витривалість": 6, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 20},
        "Метеоритний щит": {"Атака": 0, "Захист": 10, "Сила": 0, "Спритність": 4, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 22, "Точність": 0, "Крит": 0, "Опір криту": 0},
        "Щит Дракона"    : {"Атака": 0, "Захист": 10, "Сила": 4, "Спритність": 0, "Інтуїція": 3, "Витривалість": 1, "Ухилення": 0, "Точність": 0, "Крит": 22, "Опір криту": 0}
    },
    "Шолом": {
        "Слідопит"         : {"Атака": 0, "Захист": 2, "Сила": 0, "Спритність": 1, "Інтуїція": 2, "Витривалість": 0, "Ухилення": 0, "Точність": 2, "Крит": 0, "Опір криту": 0},
        "Варвар"           : {"Атака": 0, "Захист": 3, "Сила": 1, "Спритність": 0, "Інтуїція": 3, "Витривалість": 0, "Ухилення": 0, "Точність": 0, "Крит": 2, "Опір криту": 0},
        "Шолом Паладина"   : {"Атака": 0, "Захист": 8, "Сила": 0, "Спритність": 0, "Інтуїція": 1, "Витривалість": 4, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 6},
        "Метеоритний шолом": {"Атака": 0, "Захист": 6, "Сила": 0, "Спритність": 3, "Інтуїція": 2, "Витривалість": 1, "Ухилення": 5, "Точність": 4, "Крит": 0, "Опір криту": 0},
        "Шолом Дракона"    : {"Атака": 0, "Захист": 6, "Сила": 0, "Спритність": 1, "Інтуїція": 3, "Витривалість": 1, "Ухилення": 0, "Точність": 0, "Крит": 5, "Опір криту": 0}
    },
    "Обладунок": {
        "Слідопит"             : {"Атака": 0, "Захист": 4,  "Сила": 0, "Спритність": 2, "Інтуїція": 0, "Витривалість": 2,  "Ухилення": 5,  "Точність": 2, "Крит": 0,  "Опір криту": 0},
        "Варвар"               : {"Атака": 0, "Захист": 6,  "Сила": 1, "Спритність": 0, "Інтуїція": 0, "Витривалість": 5,  "Ухилення": 0,  "Точність": 0, "Крит": 0,  "Опір криту": 8},
        "Обладунок Паладина"   : {"Атака": 0, "Захист": 14, "Сила": 1, "Спритність": 0, "Інтуїція": 0, "Витривалість": 12, "Ухилення": 0,  "Точність": 2, "Крит": 0,  "Опір криту": 16},
        "Метеоритний обладунок": {"Атака": 0, "Захист": 17, "Сила": 0, "Спритність": 8, "Інтуїція": 0, "Витривалість": 10, "Ухилення": 12, "Точність": 8, "Крит": 0,  "Опір криту": 0},
        "Обладунок Дракона"    : {"Атака": 0, "Захист": 17, "Сила": 0, "Спритність": 3, "Інтуїція": 6, "Витривалість": 11, "Ухилення": 0,  "Точність": 5, "Крит": 11, "Опір криту": 0}
    },
    "Рукавиці": {
        "Слідопит"           : {"Атака": 1, "Захист": 0, "Сила": 0, "Спритність": 2, "Інтуїція": 0, "Витривалість": 0, "Ухилення": 0, "Точність": 3, "Крит": 1, "Опір криту": 0},
        "Варвар"             : {"Атака": 1, "Захист": 0, "Сила": 1, "Спритність": 0, "Інтуїція": 0, "Витривалість": 2, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 3},
        "Рукавиці Паладина"  : {"Атака": 1, "Захист": 2, "Сила": 1, "Спритність": 0, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 0, "Точність": 2, "Крит": 0, "Опір криту": 7},
        "Метеоритні рукавиці": {"Атака": 5, "Захист": 0, "Сила": 0, "Спритність": 4, "Інтуїція": 0, "Витривалість": 2, "Ухилення": 5, "Точність": 0, "Крит": 5, "Опір криту": 0},
        "Рукавиці Дракона"   : {"Атака": 7, "Захист": 0, "Сила": 0, "Спритність": 2, "Інтуїція": 3, "Витривалість": 2, "Ухилення": 0, "Точність": 3, "Крит": 5, "Опір криту": 0}
    },
    "Взуття": {
        "Слідопит"         : {"Атака": 0, "Захист": 2, "Сила": 0, "Спритність": 3, "Інтуїція": 0, "Витривалість": 1, "Ухилення": 6, "Точність": 0, "Крит": 0, "Опір криту": 0},
        "Варвар"           : {"Атака": 0, "Захист": 1, "Сила": 0, "Спритність": 0, "Інтуїція": 0, "Витривалість": 2, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 4},
        "Чоботи Паладина"  : {"Атака": 0, "Захист": 5, "Сила": 0, "Спритність": 0, "Інтуїція": 0, "Витривалість": 6, "Ухилення": 0, "Точність": 1, "Крит": 0, "Опір криту": 8},
        "Метеоритні чоботи": {"Атака": 0, "Захист": 8, "Сила": 0, "Спритність": 4, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 8, "Точність": 3, "Крит": 0, "Опір криту": 0},
        "Чоботи Дракона"   : {"Атака": 0, "Захист": 9, "Сила": 0, "Спритність": 0, "Інтуїція": 4, "Витривалість": 6, "Ухилення": 0, "Точність": 2, "Крит": 4, "Опір криту": 0}
    },
    "Кільце": {
        "Слідопит"         : {"Атака": 0, "Захист": 0, "Сила": 0, "Спритність": 2, "Інтуїція": 1, "Витривалість": 0, "Ухилення": 2, "Точність": 4, "Крит": 0, "Опір криту": 0},
        "Варвар"           : {"Атака": 0, "Захист": 0, "Сила": 2, "Спритність": 0, "Інтуїція": 0, "Витривалість": 1, "Ухилення": 0, "Точність": 0, "Крит": 2, "Опір криту": 4},
        "Кільце Паладина"  : {"Атака": 0, "Захист": 0, "Сила": 2, "Спритність": 0, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 0, "Точність": 4, "Крит": 0, "Опір криту": 3},
        "Метеоритне кільце": {"Атака": 0, "Захист": 0, "Сила": 0, "Спритність": 4, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 5, "Точність": 6, "Крит": 0, "Опір криту": 0},
        "Кільце Дракона"   : {"Атака": 0, "Захист": 0, "Сила": 0, "Спритність": 0, "Інтуїція": 3, "Витривалість": 7, "Ухилення": 0, "Точність": 6, "Крит": 5, "Опір криту": 0}
    },
    "Підвіска": {
        "Слідопит"           : {"Атака": 0, "Захист": 0, "Сила": 0, "Спритність": 2, "Інтуїція": 2, "Витривалість": 1, "Ухилення": 4, "Точність": 2, "Крит": 0, "Опір криту": 0},
        "Варвар"             : {"Атака": 1, "Захист": 0, "Сила": 2, "Спритність": 0, "Інтуїція": 0, "Витривалість": 3, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 6},
        "Підвіска Паладина"  : {"Атака": 1, "Захист": 2, "Сила": 2, "Спритність": 0, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 0, "Точність": 4, "Крит": 0, "Опір криту": 2},
        "Метеоритна підвіска": {"Атака": 1, "Захист": 4, "Сила": 0, "Спритність": 4, "Інтуїція": 0, "Витривалість": 5, "Ухилення": 5, "Точність": 6, "Крит": 0, "Опір криту": 0},
        "Підвіска Дракона"   : {"Атака": 7, "Захист": 4, "Сила": 0, "Спритність": 0, "Інтуїція": 3, "Витривалість": 8, "Ухилення": 0, "Точність": 6, "Крит": 6, "Опір криту": 0}
    }
}

SLOTS = ["Права рука", "Ліва рука", "Шолом", "Обладунок", "Рукавиці", "Взуття", "Кільце", "Підвіска"]

users_db = {}

# --- FSM СТАН ДЛЯ ОЧІКУВАННЯ ТЕКСТУ ---
class CalcStates(StatesGroup):
    waiting_for_stats = State()

def get_formatted_output(totals):
    emojis = {
        "Атака": "⚔️", "Мінімальна атака": "🗡️", "Максимальна атака": "⚔️",
        "Захист": "🛡️", "Сила": "💪", "Спритність": "🏃", 
        "Інтуїція": "🔮", "Витривалість": "🏋️‍♂️", "Ухилення": "🌀", 
        "Точність": "🎯", "Крит": "🩸", "Опір криту": "🔰", "Здоров'я": "❤️"
    }

    # 1. Зчитуємо загальні базові статти (база користувача + предмети)
    сила = totals.get("Сила", 0)
    спритність = totals.get("Спритність", 0)
    інтуїція = totals.get("Інтуїція", 0)
    витривалість = totals.get("Витривалість", 0)
    
    # 2. Зчитуємо бойові параметри, які ВЖЕ безпосередньо дали предмети
    атака_з_речей = totals.get("Атака", 0)
    захист_з_речей = totals.get("Захист", 0)
    крит_з_речей = totals.get("Крит", 0)
    ухилення_з_речей = totals.get("Ухилення", 0)
    опір_криту_з_речей = totals.get("Опір криту", 0)
    точність_з_речей = totals.get("Точність", 0)

    # 3. Рахуємо: Формула (від загальних статів) + Бонус від речей
    totals["Мінімальна атака"] = round(сила * 1 + атака_з_речей, 1)
    totals["Максимальна атака"] = round(сила * 2 + атака_з_речей, 1)
    totals["Захист"] = round(захист_з_речей * 1, 1)
    totals["Крит"] = round(інтуїція * 1.5 + крит_з_речей, 1)
    totals["Ухилення"] = round(спритність * 1 + ухилення_з_речей, 1)
    totals["Опір криту"] = round(витривалість * 0.1 + інтуїція * 0.5 + опір_криту_з_речей, 1)
    totals["Точність"] = round(спритність * 0.3 + точність_з_речей, 1)
    
    # --- Формування тексту ---
    res = "<b>--- ХАРАКТЕРИСТИКИ ---</b>\n"
    for stat in ["Сила", "Спритність", "Інтуїція", "Витривалість"]:
        val = totals.get(stat, 0)
        res += f"{emojis.get(stat, '')} {stat}: {val}\n"
        
    res += "\n<b>--- БОЙОВІ ПАРАМЕТРИ ---</b>\n"
    order = ["Здоров'я", "Мінімальна атака", "Максимальна атака", "Захист", "Ухилення", "Точність", "Крит", "Опір криту"]
    for stat in order:
        if stat in totals:
            val = totals.get(stat, 0)
            res += f"{emojis.get(stat, '')} {stat}: {val}\n"
    return res

def get_items_for_slot(slot):
    if slot == "Права рука": return list(DATABASE["Зброя"].keys())
    elif slot == "Ліва рука": return list(DATABASE["Зброя"].keys()) + list(DATABASE["Щит"].keys())
    else: return list(DATABASE.get(slot, {}).keys())

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu_keyboard(user_id):
    builder = InlineKeyboardBuilder()
    selection = users_db.get(user_id, {s: None for s in SLOTS})
    
    # Кнопки з предметами
    for i, slot in enumerate(SLOTS):
        item = selection.get(slot)
        text = f"{slot}: {item}" if item else f"{slot}: Не обрано"
        builder.button(text=text, callback_data=f"slot_{i}")
    
    # Кнопки режимів
    builder.button(text="✅ РОЗРАХУНОК: ПО ПРЕДМЕТАХ", callback_data="calc_items")
    builder.button(text="🔢 РОЗРАХУНОК: ВРУЧНУ (Тільки база)", callback_data="calc_manual")
    builder.button(text="⚖️ РОЗРАХУНОК: ЗМІШАНИЙ (База + Предмети)", callback_data="calc_mixed")
    
    # КНОПКА ДОНАТУ
    builder.button(text="💳 Допомогти розробнику калькулятора закрити кредит", url="https://send.monobank.ua/jar/8xP2vZiaR5")
    
    builder.adjust(1) # Всі кнопки йтимуть в один стовпчик одна під одною
    return builder.as_markup()

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear() # Очищуємо стан, якщо юзер був у процесі вводу
    user_id = message.from_user.id
    if user_id not in users_db:
        users_db[user_id] = {s: None for s in SLOTS}
        
    await message.answer("Привіт! Це калькулятор білдів Lands of War.\nОбери предмети або режим розрахунку нижче:", 
                         reply_markup=main_menu_keyboard(user_id))

@dp.callback_query(F.data.startswith("slot_"))
async def process_slot(callback: types.CallbackQuery):
    slot_index = int(callback.data.split("_")[1])
    slot_name = SLOTS[slot_index]
    items = get_items_for_slot(slot_name)
    
    builder = InlineKeyboardBuilder()
    for item_index, item_name in enumerate(items):
        builder.button(text=item_name, callback_data=f"item_{slot_index}_{item_index}")
    
    builder.button(text="❌ Зняти предмет", callback_data=f"clear_{slot_index}")
    builder.button(text="⬅️ Назад", callback_data="menu")
    builder.adjust(1)
    
    await callback.message.edit_text(f"Оберіть предмет для слоту: <b>{slot_name}</b>", 
                                     reply_markup=builder.as_markup(), parse_mode="HTML")
    await callback.answer()

@dp.callback_query(F.data.startswith("item_"))
async def process_item(callback: types.CallbackQuery):
    _, slot_idx, item_idx = callback.data.split("_")
    slot_name = SLOTS[int(slot_idx)]
    items = get_items_for_slot(slot_name)
    item_name = items[int(item_idx)]
    
    user_id = callback.from_user.id
    users_db[user_id][slot_name] = item_name
    
    await callback.message.edit_text("Меню екіпірування:", reply_markup=main_menu_keyboard(user_id))
    await callback.answer()

@dp.callback_query(F.data.startswith("clear_"))
async def process_clear(callback: types.CallbackQuery):
    slot_index = int(callback.data.split("_")[1])
    slot_name = SLOTS[slot_index]
    user_id = callback.from_user.id
    users_db[user_id][slot_name] = None
    await callback.message.edit_text("Меню екіпірування:", reply_markup=main_menu_keyboard(user_id))
    await callback.answer()

@dp.callback_query(F.data == "menu")
async def back_to_menu(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    await callback.message.edit_text("Меню екіпірування:", reply_markup=main_menu_keyboard(user_id))
    await callback.answer()

# --- РЕЖИМ 1: ТІЛЬКИ ПРЕДМЕТИ ---
@dp.callback_query(F.data == "calc_items")
async def process_calculate_items(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    selection = users_db.get(user_id, {s: None for s in SLOTS})
    
    totals = {"Атака": 0, "Захист": 0, "Сила": 0, "Спритність": 0, "Інтуїція": 0, "Витривалість": 0, "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 0}
    weapon_attack_counted = False
    
    for slot, item_name in selection.items():
        if item_name:
            cat = "Зброя" if item_name in DATABASE.get("Зброя", {}) else ("Щит" if item_name in DATABASE.get("Щит", {}) else slot)
            is_weapon = (cat == "Зброя")
            for stat, val in DATABASE.get(cat, {}).get(item_name, {}).items():
                if stat in totals: 
                    if is_weapon and stat == "Атака":
                        if weapon_attack_counted: continue
                        else:
                            totals[stat] += val
                            weapon_attack_counted = True
                    else:
                        totals[stat] += val
    
    totals["Здоров'я"] = totals.get("Витривалість", 0) * 6
    result_text = get_formatted_output(totals)
    
    await callback.message.answer(f"<b>📊 РЕЗУЛЬТАТ (Тільки предмети):</b>\n\n{result_text}", parse_mode="HTML")
    await callback.answer()

# --- ПІДГОТОВКА ДО РЕЖИМІВ 2 ТА 3 ---
@dp.callback_query(F.data.in_(["calc_manual", "calc_mixed"]))
async def process_start_input(callback: types.CallbackQuery, state: FSMContext):
    mode = "manual" if callback.data == "calc_manual" else "mixed"
    await state.update_data(calc_mode=mode)
    
    text = (
        "Надішліть мені ваші базові характеристики <b>одним повідомленням через пробіл</b> у такому порядку:\n\n"
        "💪 Сила\n"
        "🏃 Спритність\n"
        "🔮 Інтуїція\n"
        "🏋️‍♂️ Витривалість\n\n"
        "<i>Наприклад, якщо у вас всього по 5, напишіть:</i>\n"
        "<code>5 5 5 5</code>"
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Скасувати", callback_data="menu")
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    await state.set_state(CalcStates.waiting_for_stats)
    await callback.answer()

# --- ОТРИМАННЯ ТЕКСТУ ТА РОЗРАХУНОК (Режими 2 та 3) ---
@dp.message(CalcStates.waiting_for_stats)
async def process_stats_input(message: types.Message, state: FSMContext):
    try:
        parts = message.text.strip().split()
        if len(parts) != 4:
            raise ValueError
        
        sila = int(parts[0])
        sprint = int(parts[1])
        intui = int(parts[2])
        vitr = int(parts[3])
        
    except ValueError:
        await message.answer("❌ Помилка! Будь ласка, введіть рівно 4 числа через пробіл.\nПриклад: <code>5 10 3 12</code>", parse_mode="HTML")
        return

    data = await state.get_data()
    mode = data.get("calc_mode")
    
    user_id = message.from_user.id
    selection = users_db.get(user_id, {s: None for s in SLOTS})
    
    totals = {
        "Атака": 0, "Захист": 0,
        "Сила": sila, "Спритність": sprint,
        "Інтуїція": intui, "Витривалість": vitr,
        "Ухилення": 0, "Точність": 0, "Крит": 0, "Опір криту": 0
    }
    
    if mode == "mixed":
        weapon_attack_counted = False
        for slot, item_name in selection.items():
            if item_name:
                cat = "Зброя" if item_name in DATABASE.get("Зброя", {}) else ("Щит" if item_name in DATABASE.get("Щит", {}) else slot)
                is_weapon = (cat == "Зброя")
                for stat, val in DATABASE.get(cat, {}).get(item_name, {}).items():
                    if stat in totals:
                        if is_weapon and stat == "Атака":
                            if weapon_attack_counted: continue
                            else:
                                totals[stat] += val
                                weapon_attack_counted = True
                        else:
                            totals[stat] += val
                            
    totals["Здоров'я"] = totals.get("Витривалість", 0) * 6
    result_text = get_formatted_output(totals)
    
    title = "Вручну (Тільки база)" if mode == "manual" else "Змішаний (База + Предмети)"
    await message.answer(f"<b>📊 РЕЗУЛЬТАТ: {title}</b>\n\n{result_text}", parse_mode="HTML")
    await state.clear()

async def main():
    print("Бот успішно запущено! Перейдіть у Telegram та напишіть йому /start")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
