from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from carzona72_bot_operator import CarZonaBot, SERVICE_MENU


# ============================================================
# НАСТРОЙКИ
# ============================================================

# ВСТАВЬ СЮДА НОВЫЙ ТОКЕН ОТ BOTFATHER.
# Старый токен, который был прислан в чат, больше не используй.
TOKEN = "8803903429:AAHwyNDZYcOc6Gw9EPoYBca0eNLcnd7w0rA"

# Отдельное состояние CarZonaBot для каждого пользователя Telegram.
users = {}


# ============================================================
# СОСТОЯНИЕ ПОЛЬЗОВАТЕЛЯ
# ============================================================

def get_bot(user_id):
    if user_id not in users:
        users[user_id] = CarZonaBot()

    return users[user_id]


# ============================================================
# ГЛАВНОЕ МЕНЮ
# ============================================================

def main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔧 ТО и масла", callback_data="cat:1"),
            InlineKeyboardButton("🔍 Диагностика", callback_data="cat:2"),
        ],
        [
            InlineKeyboardButton("🔥 Двигатель", callback_data="cat:3"),
            InlineKeyboardButton("🛑 Тормоза", callback_data="cat:4"),
        ],
        [
            InlineKeyboardButton("🔩 Подвеска", callback_data="cat:5"),
            InlineKeyboardButton("⚙️ Коробка передач", callback_data="cat:6"),
        ],
        [
            InlineKeyboardButton("🎯 Рулевое управление", callback_data="cat:7"),
            InlineKeyboardButton("🛞 Шиномонтаж", callback_data="cat:8"),
        ],
        [
            InlineKeyboardButton("🌡️ Охлаждение", callback_data="cat:9"),
            InlineKeyboardButton("❄️ Кондиционер", callback_data="cat:10"),
        ],
        [
            InlineKeyboardButton("🔥 Выхлоп", callback_data="cat:11"),
        ],
        [
            InlineKeyboardButton("📅 Записаться", callback_data="booking"),
            InlineKeyboardButton("🧩 Запчасти", callback_data="parts"),
        ],
        [
            InlineKeyboardButton("ℹ️ Информация", callback_data="info"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def category_keyboard(category_number):
    category = SERVICE_MENU[category_number]

    keyboard = []

    for index, item in enumerate(category["items"], 1):
        button_text = "✏️ Другое" if item == "Другое" else item

        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"service:{category_number}:{index}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton("◀️ Назад", callback_data="menu"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
    ])

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# КНОПКИ ДЛЯ ЗАПИСИ
# ============================================================

def booking_category_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🔧 ТО и масла", callback_data="bookcat:1"),
            InlineKeyboardButton("🔍 Диагностика", callback_data="bookcat:2"),
        ],
        [
            InlineKeyboardButton("🔥 Двигатель", callback_data="bookcat:3"),
            InlineKeyboardButton("🛑 Тормоза", callback_data="bookcat:4"),
        ],
        [
            InlineKeyboardButton("🔩 Подвеска", callback_data="bookcat:5"),
            InlineKeyboardButton("⚙️ Коробка", callback_data="bookcat:6"),
        ],
        [
            InlineKeyboardButton("🎯 Рулевое", callback_data="bookcat:7"),
            InlineKeyboardButton("🛞 Шиномонтаж", callback_data="bookcat:8"),
        ],
        [
            InlineKeyboardButton("🌡️ Охлаждение", callback_data="bookcat:9"),
            InlineKeyboardButton("❄️ Кондиционер", callback_data="bookcat:10"),
        ],
        [
            InlineKeyboardButton("🔥 Выхлоп", callback_data="bookcat:11"),
        ],
        [
            InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def booking_service_keyboard(category_number):
    category = SERVICE_MENU[category_number]

    keyboard = []

    for index, item in enumerate(category["items"], 1):
        button_text = "✏️ Другое" if item == "Другое" else item

        keyboard.append([
            InlineKeyboardButton(
                button_text,
                callback_data=f"bookservice:{category_number}:{index}",
            )
        ])

    keyboard.append([
        InlineKeyboardButton("◀️ Назад", callback_data="booking"),
        InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
    ])

    return InlineKeyboardMarkup(keyboard)


def parts_source_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Запчасти уже есть",
                callback_data="parts_source:1",
            )
        ],
        [
            InlineKeyboardButton(
                "🔎 Нужно подобрать",
                callback_data="parts_source:2",
            )
        ],
        [
            InlineKeyboardButton("◀️ Назад", callback_data="menu"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def yes_no_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("✅ Да", callback_data="yes"),
            InlineKeyboardButton("❌ Нет", callback_data="no"),
        ],
        [
            InlineKeyboardButton("◀️ Назад", callback_data="back"),
            InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def simple_navigation_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("◀️ Назад", callback_data="back"),
            InlineKeyboardButton("🏠 Главное меню", callback_data="menu"),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# /START
# ============================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = get_bot(user_id)

    bot.reset()

    await update.message.reply_text(
        "🚗 <b>CarZona72</b>\n\n"
        "Здравствуйте! Вас приветствует CarZona72.\n\n"
        "Выберите нужное действие:",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ============================================================
# КНОПКИ TELEGRAM
# ============================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    bot = get_bot(user_id)
    data = query.data

    # Главное меню
    if data == "menu":
        bot.reset()

        await query.message.edit_text(
            "🚗 <b>CarZona72</b>\n\n"
            "Выберите нужное действие:",
            parse_mode="HTML",
            reply_markup=main_keyboard(),
        )
        return

    # Обычный просмотр категории
    if data.startswith("cat:"):
        category_number = data.split(":", 1)[1]

        bot.handle(category_number)

        category_name = SERVICE_MENU[category_number]["name"]

        await query.message.edit_text(
            f"🔧 <b>{category_name}</b>\n\n"
            "Выберите услугу:",
            parse_mode="HTML",
            reply_markup=category_keyboard(category_number),
        )
        return

    # Выбор конкретной услуги при обычном просмотре
    if data.startswith("service:"):
        _, category_number, service_number = data.split(":")
        item_number = int(service_number)

        response = bot.handle(service_number)
        item_name = SERVICE_MENU[category_number]["items"][item_number - 1]

        # Другое
        if item_name == "Другое":
            await query.message.edit_text(
                "✏️ <b>Другое</b>\n\n"
                "Опишите своими словами, какая услуга вам нужна.",
                parse_mode="HTML",
                reply_markup=simple_navigation_keyboard(),
            )
            return

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📅 Записаться",
                    callback_data="booking_selected",
                )
            ],
            [
                InlineKeyboardButton(
                    "◀️ Назад",
                    callback_data=f"cat:{category_number}",
                ),
                InlineKeyboardButton(
                    "🏠 Главное меню",
                    callback_data="menu",
                ),
            ],
        ])

        await query.message.edit_text(
            f"✅ {response}",
            reply_markup=keyboard,
        )
        return

    # Начало записи
    if data == "booking":
        bot.start_booking()

        await query.message.edit_text(
            "📅 <b>Запись на обслуживание</b>\n\n"
            "Выберите категорию услуги:",
            parse_mode="HTML",
            reply_markup=booking_category_keyboard(),
        )
        return

    # Запись на уже выбранную услугу
    if data == "booking_selected":
        if "service" in bot.data:
            bot.state = "booking_date"

            await query.message.edit_text(
                "📅 На какой день хотите записаться?\n\n"
                "Можно написать: завтра, в субботу, 25.08 и т. д.",
                reply_markup=simple_navigation_keyboard(),
            )
        else:
            await query.message.edit_text(
                "Сначала выберите услугу.",
                reply_markup=main_keyboard(),
            )
        return

    # Категория при записи
    if data.startswith("bookcat:"):
        category_number = data.split(":", 1)[1]

        bot.data["category"] = category_number
        bot.history = ["booking_service"]
        bot.state = "booking_subservice"

        category_name = SERVICE_MENU[category_number]["name"]

        await query.message.edit_text(
            f"📅 <b>{category_name}</b>\n\n"
            "Выберите конкретную услугу:",
            parse_mode="HTML",
            reply_markup=booking_service_keyboard(category_number),
        )
        return

    # Конкретная услуга при записи
    if data.startswith("bookservice:"):
        _, category_number, service_number = data.split(":")
        service_number_int = int(service_number)

        response = bot.handle(service_number)
        item_name = SERVICE_MENU[category_number]["items"][service_number_int - 1]

        if item_name == "Другое":
            await query.message.edit_text(
                "✏️ <b>Своя услуга</b>\n\n"
                "Опишите своими словами, какая услуга вам нужна.",
                parse_mode="HTML",
                reply_markup=simple_navigation_keyboard(),
            )
            return

        await query.message.edit_text(
            f"✅ {response}",
            reply_markup=simple_navigation_keyboard(),
        )
        return

    # Подбор запчастей
    if data == "parts":
        bot.start_parts_request()

        await query.message.edit_text(
            "🧩 <b>Запчасти</b>\n\n"
            "Выберите вариант:",
            parse_mode="HTML",
            reply_markup=parts_source_keyboard(),
        )
        return

    # Выбор запчастей
    if data.startswith("parts_source:"):
        choice = data.split(":", 1)[1]

        response = bot.handle(choice)

        if bot.state == "booking_vin" or bot.state == "parts_vin":
            await query.message.edit_text(
                response,
                reply_markup=simple_navigation_keyboard(),
            )
        else:
            await query.message.edit_text(
                response,
                reply_markup=main_keyboard(),
            )
        return

    # Информация
    if data == "info":
        await query.message.edit_text(
            "ℹ️ <b>CarZona72</b>\n\n"
            "Автосервис выполняет ремонт и техническое обслуживание автомобилей.\n\n"
            "❌ Электрика — не выполняется\n"
            "❌ Кузовные работы — не выполняются\n"
            "❌ Сход-развал — нет стенда\n"
            "🔧 Рулевые рейки — только замена\n\n"
            "📍 г. Тюмень, ул. Малышева, 25\n"
            "📞 +7 932 630-70-40\n"
            "🕙 Пн–Сб: 10:00–20:00\n"
            "Воскресенье — выходной.",
            parse_mode="HTML",
            reply_markup=simple_navigation_keyboard(),
        )
        return

    # Подтверждение
    if data == "yes":
        response = bot.handle("да")

        await query.message.edit_text(
            response,
            reply_markup=main_keyboard(),
        )
        return

    if data == "no":
        response = bot.handle("нет")

        await query.message.edit_text(
            response,
            reply_markup=main_keyboard(),
        )
        return

    # Назад
    if data == "back":
        response = bot.handle("назад")

        await query.message.edit_text(
            response,
            reply_markup=main_keyboard(),
        )
        return


# ============================================================
# ОБЫЧНЫЙ ТЕКСТ
# ============================================================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text.strip()
    normalized = user_message.lower()

    bot = get_bot(user_id)

    # Быстрый возврат в красивое главное меню.
    if normalized in (
        "меню",
        "начало",
        "главное меню",
        "главное",
    ):
        bot.reset()

        await update.message.reply_text(
            "🚗 <b>CarZona72</b>\n\n"
            "Выберите нужное действие:",
            parse_mode="HTML",
            reply_markup=main_keyboard(),
        )
        return

    response = bot.handle(user_message)

    if not response:
        return

    # Свободный ввод своей услуги
    if bot.state == "custom_service_confirm":
        await update.message.reply_text(
            response,
            reply_markup=yes_no_keyboard(),
        )
        return

    # Выбор запчастей при записи
    if bot.state == "booking_parts":
        await update.message.reply_text(
            response,
            reply_markup=parts_source_keyboard(),
        )
        return

    # Подтверждение записи / подбора
    if bot.state in ("booking_confirm", "parts_request_confirm"):
        await update.message.reply_text(
            response,
            reply_markup=yes_no_keyboard(),
        )
        return

    # Выбор категории при ручном вводе номера
    if bot.state.startswith("category:"):
        category_number = bot.state.split(":", 1)[1]

        await update.message.reply_text(
            f"🔧 <b>{SERVICE_MENU[category_number]['name']}</b>\n\n"
            "Выберите услугу:",
            parse_mode="HTML",
            reply_markup=category_keyboard(category_number),
        )
        return

    # Выбор услуги при записи
    if bot.state == "booking_subservice":
        category_number = bot.data.get("category")

        if category_number in SERVICE_MENU:
            await update.message.reply_text(
                f"📅 <b>{SERVICE_MENU[category_number]['name']}</b>\n\n"
                "Выберите конкретную услугу:",
                parse_mode="HTML",
                reply_markup=booking_service_keyboard(category_number),
            )
            return

    await update.message.reply_text(response)


# ============================================================
# ЗАПУСК
# ============================================================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    # TEXT здесь оставляем без ~filters.COMMAND,
    # чтобы существующие команды ядра вроде /оператор и /бот
    # тоже можно было передавать в CarZonaBot.
    app.add_handler(MessageHandler(filters.TEXT, message_handler))

    print("CarZona72 Telegram Bot запущен...")

    app.run_polling()


if __name__ == "__main__":
    main()