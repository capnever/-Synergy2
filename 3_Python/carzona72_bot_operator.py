# CarZona72 Bot
# Учебный проект для производственной практики

PHONE = "+7 932 630-70-40"
ADDRESS = "г. Тюмень, ул. Малышева, 25"
WORKING_HOURS = "понедельник–суббота, 10:00–20:00"

SERVICE_MENU = {
    "1": {
        "name": "ТО и масла",
        "items": [
            "Замена масла",
            "Полное техническое обслуживание",
            "Другое",
        ],
    },
    "2": {
        "name": "Диагностика",
        "items": [
            "Компьютерная диагностика",
            "Диагностика автомобиля",
            "Другое",
        ],
    },
    "3": {
        "name": "Двигатель",
        "items": [
            "Диагностика двигателя",
            "Ремонт двигателя",
            "Другое",
        ],
    },
    "4": {
        "name": "Тормозная система",
        "items": [
            "Замена тормозных колодок",
            "Замена тормозных дисков",
            "Обслуживание тормозной системы",
            "Другое",
        ],
    },
    "5": {
        "name": "Подвеска",
        "items": [
            "Диагностика подвески",
            "Амортизаторы и стойки",
            "Шаровые и сайлентблоки",
            "Рычаги",
            "Ступичные подшипники",
            "Другое",
        ],
    },
    "6": {
        "name": "Коробка передач",
        "items": [
            "Диагностика коробки",
            "АКПП",
            "МКПП",
            "Вариатор",
            "Другое",
        ],
    },
    "7": {
        "name": "Рулевое управление",
        "items": [
            "Диагностика рулевого управления",
            "Замена рулевой рейки",
            "Другое",
        ],
    },
    "8": {
        "name": "Шиномонтаж",
        "items": [
            "Шиномонтаж",
            "Балансировка колес",
            "Другое",
        ],
    },
    "9": {
        "name": "Охлаждение и радиаторы",
        "items": [
            "Мойка радиаторов",
            "Диагностика системы охлаждения",
            "Другое",
        ],
    },
    "10": {
        "name": "Кондиционер",
        "items": [
            "Заправка фреоном",
            "Диагностика кондиционера",
            "Другое",
        ],
    },
    "11": {
        "name": "Выхлопная система",
        "items": [
            "Удаление катализатора без прошивки",
            "Другое",
        ],
    },
}


def main_menu_text():
    lines = ["Главное меню:"]
    
    for number, category in SERVICE_MENU.items():
        lines.append(f"{number}. {category['name']}")

    lines.extend([
        "12. Информация об автосервисе",
        "13. Записаться на обслуживание",
        "14. Подбор запчастей",
        "",
        "Команды: «назад», «начало», «отмена», «выход»."
    ])

    return "\n".join(lines)


def print_main_menu():
    print(main_menu_text())


def submenu_text(category_number):
    category = SERVICE_MENU[category_number]

    lines = [f"{category['name']}:"]

    for number, item in enumerate(category["items"], 1):
        lines.append(f"{number}. {item}")

    return "\n".join(lines)


def print_submenu(category_number):
    print(submenu_text(category_number))

def normalize_time(value):
    value = value.strip().replace(".", ":").replace("-", ":")

    if value.isdigit():
        hour = int(value)

        if 0 <= hour <= 23:
            return f"{hour:02d}:00"

        return None

    parts = value.split(":")

    if len(parts) != 2:
        return None

    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        return None

    if 0 <= hour <= 23 and 0 <= minute <= 59:
        return f"{hour:02d}:{minute:02d}"

    return None

from datetime import datetime, date, timedelta

def normalize_date(value):
    value = value.strip().lower()

    today = date.today()

    # Сегодня
    if value == "сегодня":
        return today.strftime("%d.%m.%Y")

    # Завтра
    if value == "завтра":
        return (today + timedelta(days=1)).strftime("%d.%m.%Y")

    # Послезавтра
    if value == "послезавтра":
        return (today + timedelta(days=2)).strftime("%d.%m.%Y")

    # Дни недели
    weekdays = {
        "понедельник": 0,
        "вторник": 1,
        "среда": 2,
        "четверг": 3,
        "пятница": 4,
        "суббота": 5,
        "воскресенье": 6,
    }

    # Нормализуем фразы:
    # "в субботу", "в среду", "в пятницу" и т. п.
    weekday_forms = {
        "понедельнику": "понедельник",
        "понедельник": "понедельник",
        "вторнику": "вторник",
        "вторник": "вторник",
        "среду": "среда",
        "среда": "среда",
        "четвергу": "четверг",
        "четверг": "четверг",
        "пятницу": "пятница",
        "пятница": "пятница",
        "субботу": "суббота",
        "суббота": "суббота",
        "воскресенье": "воскресенье",
    }

    value = value.replace("в ", "").replace("на ", "").strip()

    if value in weekday_forms:
        value = weekday_forms[value]

    if value in weekdays:
        target_weekday = weekdays[value]
        days_ahead = (target_weekday - today.weekday()) % 7

        if days_ahead == 0:
            days_ahead = 7

        selected_date = today + timedelta(days=days_ahead)

        return selected_date.strftime("%d.%m.%Y")

    # Формат 25.08.2026
    try:
        parsed = datetime.strptime(value, "%d.%m.%Y").date()

        if parsed >= today:
            return parsed.strftime("%d.%m.%Y")

        return None

    except ValueError:
        pass

    # Формат 25.08
    try:
        parsed = datetime.strptime(
            f"{value}.{today.year}",
            "%d.%m.%Y"
        ).date()

        if parsed >= today:
            return parsed.strftime("%d.%m.%Y")

        return None

    except ValueError:
        pass

    # Только число: 25
    if value.isdigit():
        day = int(value)

        if 1 <= day <= 31:
            try:
                parsed = date(today.year, today.month, day)

                if parsed >= today:
                    return parsed.strftime("%d.%m.%Y")

            except ValueError:
                return None

    return None
       
class CarZonaBot:
    def __init__(self):
        self.state = "main"
        self.data = {}
        self.history = []
        self.chat_mode = "bot"

    def reset(self):
        self.state = "main"
        self.data = {}
        self.history = []
        self.chat_mode = "bot"

    def back(self):
        if self.history:
            previous_state = self.history.pop()
            self.state = previous_state

            if self.state == "main":
                print_main_menu()
                return "Вернулись в главное меню."

            if self.state.startswith("category:"):
                category_number = self.state.split(":", 1)[1]
                print_submenu(category_number)
                return "Вернулись к выбору услуги."

            if self.state == "booking_service":
                print_main_menu()
                return "Вернулись к выбору категории услуги."

            if self.state == "booking_subservice":
                category_number = self.data.get("category")

                if category_number in SERVICE_MENU:
                    print_submenu(category_number)

                return "Вернулись к выбору конкретной услуги."

            if self.state == "booking_custom_service":
                return "Вернулись к вводу своей услуги."

            if self.state == "booking_date":
                return "Вернулись к выбору даты."

            if self.state == "booking_time":
                return "Вернулись к выбору времени."

            if self.state == "booking_parts":
                return (
                    "Вернулись к выбору запчастей.\n\n"
                    "1. Запчасти уже есть\n"
                    "2. Запчасти нужно подобрать"
                )

            if self.state == "booking_vin":
                return "Вернулись к вводу VIN или номера кузова."

            if self.state == "booking_part_name":
                return "Вернулись к вводу названия запчасти."

            if self.state == "parts_source":
                return (
                    "Вернулись к выбору запчастей.\n\n"
                    "1. Запчасти уже есть\n"
                    "2. Запчасти нужно подобрать"
                )

            if self.state == "parts_vin":
                return "Вернулись к вводу VIN или номера кузова."

            if self.state == "parts_part_name":
                return "Вернулись к вводу названия запчасти."

            if self.state == "custom_service":
                return "Вернулись к вводу своей услуги."

            if self.state == "custom_service_confirm":
                return (
                    "Вернулись к подтверждению своей услуги.\n"
                    "1. Да\n"
                    "2. Нет"
                )

            if self.state == "parts_request_confirm":
                return "Вернулись к подтверждению заявки на подбор запчасти."

            return "Вернулись на предыдущий этап."

        self.reset()
        print_main_menu()
        return "Вы уже в главном меню."

    def start_booking(self):
        self.data = {}
        self.history = []
        self.state = "booking_service"
        print_main_menu()
        return "Выберите категорию услуги для записи."

    def start_parts_request(self):
        self.data = {}
        self.history = []
        self.state = "parts_source"
        return (
            "Запчасти:\n\n"
            "1. Запчасти уже есть\n"
            "2. Запчасти нужно подобрать"
        )

    def handle(self, message):
        message = message.strip()
        normalized = message.lower()

        # Команды режима оператора
        if normalized in ("/оператор", "оператор подключен", "подключи оператора"):
            self.chat_mode = "operator"
            return "Оператор подключён. Теперь автоматические ответы бота отключены."

        if normalized in ("/бот", "/bot", "вернуть бота", "оператор завершил"):
           self.chat_mode = "bot"
           return "Хорошо. Автоматический режим бота снова включён."

        # В режиме оператора бот не отвечает на обычные сообщения клиента.
        # Команду оператора можно имитировать через префикс "оператор:".
        if self.chat_mode == "operator":
            if normalized.startswith("оператор:"):
                reply = message.split(":", 1)[1].strip()
                return f"Оператор: {reply}" if reply else "Оператор не написал сообщение."
            return f"[Оператору] Клиент: {message}"

        # Универсальные команды
        if normalized in ("отмена", "отменить"):
            self.reset()
            return "Хорошо, текущая заявка отменена."

        if normalized in ("начало", "главное меню", "главное", "меню"):
            self.reset()
            return main_menu_text()

        if normalized == "назад":
            return self.back()

        if normalized in ("пока", "до свидания", "выйти", "выход"):
            self.state = "exit"
            return "До свидания! Будем рады помочь."

        if normalized in (
            "привет",
            "здравствуйте",
            "здравствуй",
            "добрый день",
            "доброе утро",
            "добрый вечер",
        ):
            return "Здравствуйте! Вас приветствует CarZona72. Чем могу помочь?"

        # Главное меню
        if self.state == "main":
            if normalized in (
                "меню",
                "услуги",
                "что делаете",
                "что ремонтируете",
                "что чините"
            ):
                return main_menu_text()

            if normalized in ("адрес", "где вы", "где находитесь", "как вас найти"):
                return f"CarZona72 находится по адресу: {ADDRESS}."

            if normalized in ("телефон", "номер", "как позвонить", "позвонить"):
                return f"Телефон CarZona72: {PHONE}."

            if normalized in (
                "график",
                "режим работы",
                "время работы",
                "когда работаете",
                "во сколько работаете",
                "часы работы",
            ):
                return f"CarZona72 работает {WORKING_HOURS}. Воскресенье — выходной."

            if normalized in ("запись", "записаться", "хочу записаться", "хочу запись"):
                return self.start_booking()

            if normalized in ("запчасти", "подбор запчастей", "нужны запчасти"):
                return self.start_parts_request()

            if message == "13":
                return self.start_booking()

            if message == "14":
                return self.start_parts_request()

            if message == "12":
                return (
                    "CarZona72 выполняет ремонт и техническое обслуживание автомобилей.\n"
                    "Кузовные работы, электрика и сход-развал не выполняются.\n"
                    "Рулевые рейки не ремонтируются — выполняется их замена."
                )

            if message.isdigit() and message in SERVICE_MENU:
                self.history.append("main")
                self.state = f"category:{message}"
                return submenu_text(message)

            return (
                "Я не понял запрос. Выберите пункт из главного меню "
                "или напишите «услуги», «запись», «запчасти», "
                "«адрес», «телефон» или «график»."
            )

       # Просмотр категории
        if self.state.startswith("category:"):
            category_number = self.state.split(":", 1)[1]
            items = SERVICE_MENU[category_number]["items"]

            # Пользователь написал "другое"
            if normalized == "другое":
                self.history.append(self.state)
                self.state = "custom_service"
                return "Опишите своими словами, какая услуга вам нужна."

            # Пользователь выбрал номер
            if normalized in ("записаться", "запись", "хочу записаться"):
                if "service" in self.data:
                    self.state = "booking_date"
                    return "На какой день хотите записаться?"

                return "Сначала выберите услугу."
            if message.isdigit():
                number = int(message)

                if 1 <= number <= len(items):
                    item = items[number - 1]

                    if item == "Другое":
                        self.history.append(self.state)
                        self.state = "custom_service"
                        return "Опишите своими словами, какая услуга вам нужна."

                    self.data["service"] = item
                    return (
                        f"Вы выбрали: {item}.\n"
                        "Для записи на эту услугу напишите «записаться»."
                    )

            return f"Введите номер услуги от 1 до {len(items)}."

        # Начало записи: категория
        if self.state == "booking_service":
            if message.isdigit() and message in SERVICE_MENU:
                self.data["category"] = message
                self.history.append("booking_service")
                self.state = "booking_subservice"
                return submenu_text(message)

            return "Введите номер категории услуги."

        # Запись: подуслуга
        if self.state == "booking_subservice":
            category_number = self.data["category"]
            items = SERVICE_MENU[category_number]["items"]

            if message.isdigit():
                number = int(message)
                if 1 <= number <= len(items):
                    item = items[number - 1]

                    if item == "Другое":
                        self.history.append(self.state)
                        self.state = "booking_custom_service"
                        return "Опишите своими словами, какая услуга вам нужна."

                    self.data["service"] = item
                    self.history.append(self.state)
                    self.state = "booking_date"
                    return "На какой день хотите записаться?"

            return f"Введите номер услуги от 1 до {len(items)}."

        # Запись: своя услуга
        if self.state == "booking_custom_service":
            self.data["service"] = message
            self.history.append(self.state)
            self.state = "booking_date"
            return "На какой день хотите записаться?"

        # Запись: дата
        if self.state == "booking_date":
            normalized_date = normalize_date(message)

            if normalized_date is None:
                return (
                    "Не удалось распознать дату.\n"
                    "Введите дату, например: «завтра», «25.08» "
                    "или «25.08.2026»."
                )

            self.data["date"] = normalized_date
            self.history.append(self.state)
            self.state = "booking_time"

            return (
                f"Дата записи: {normalized_date}\n"
                "В какое время вам удобно?"
            )
         # Запись: время
        if self.state == "booking_time":
            normalized_time = normalize_time(message)

            if normalized_time is None:
                return (
                    "Не удалось распознать время.\n"
                    "Введите время в формате 14:00 или просто 14."
                )

            hour, minute = map(int, normalized_time.split(":"))

            # Проверяем рабочее время автосервиса
            if hour < 10 or hour > 20:
                return (
                    "Автосервис работает с 10:00 до 20:00.\n"
                    "Пожалуйста, выберите время в этом диапазоне."
                )

            # В 20:00 запись ещё возможна
            self.data["time"] = normalized_time
            self.history.append(self.state)
            self.state = "booking_parts"

            return (
                f"Время записи: {normalized_time}\n\n"
                "Запчасти:\n"
                "1. Запчасти уже есть\n"
                "2. Запчасти нужно подобрать"
            )

        # Запись: запчасти
        if self.state == "booking_parts":
            if message == "1":
                self.data["parts"] = "Запчасти уже есть"
                self.history.append(self.state)
                self.state = "booking_confirm"
                return self.booking_summary()

            if message == "2":
                self.data["parts"] = "Запчасти нужно подобрать"
                self.history.append(self.state)
                self.state = "booking_vin"
                return "Пришлите VIN автомобиля или номер кузова."

            return "Введите 1 или 2."

        # Запись: VIN
        if self.state == "booking_vin":
            self.data["vin"] = message
            self.history.append(self.state)
            self.state = "booking_part_name"
            return "Какая запчасть вам нужна?"

        # Запись: название детали
        if self.state == "booking_part_name":
            self.data["part_name"] = message
            self.history.append(self.state)
            self.state = "parts_request_confirm"
            return self.parts_request_summary()

        # Подтверждение подбора запчасти
        if self.state == "parts_request_confirm":
            if normalized in ("да", "подтверждаю", "верно", "подтвердить"):
                vin = self.data["vin"]
                part_name = self.data["part_name"]

                self.reset()

                return (
                    "Заявка на подбор запчасти принята.\n\n"
                    f"VIN / номер кузова: {vin}\n"
                    f"Запчасть: {part_name}\n\n"
                    "Заявка передана оператору для подбора вариантов и брендов."
                )

            if normalized in ("нет", "изменить"):
                self.state = "booking_vin"
                return "Хорошо. Пришлите VIN автомобиля или номер кузова ещё раз."

            return "Напишите «да», если всё верно, или «нет», если хотите изменить заявку."

        # Подтверждение обычной записи
        if self.state == "booking_confirm":
            if normalized in ("да", "подтверждаю", "верно", "подтвердить"):
                result = self.booking_summary(prefix="Запись подтверждена!")
                self.reset()
                return result + f"\nДля связи: {PHONE}\nCarZona72 ждёт вас!"

            if normalized in ("нет", "изменить"):
                self.history.append(self.state)
                self.state = "booking_service"
                print_main_menu()
                return "Хорошо, давайте изменим запись. Выберите категорию услуги."

            return "Напишите «да», если всё верно, или «нет», если хотите изменить запись."

        # Подбор запчастей вне записи
        if self.state == "parts_source":
            if message == "1":
                self.data["parts"] = "Запчасти уже есть"
                self.reset()
                return "Хорошо. При необходимости укажите услугу, для которой у вас уже есть запчасти."

            if message == "2":
                self.data["parts"] = "Запчасти нужно подобрать"
                self.state = "parts_vin"
                return "Пришлите VIN автомобиля или номер кузова."

            return "Введите 1 или 2."

        if self.state == "parts_vin":
            self.data["vin"] = message
            self.state = "parts_part_name"
            return "Какая запчасть вам нужна?"

        if self.state == "parts_part_name":
            self.data["part_name"] = message
            self.state = "parts_request_confirm"
            return self.parts_request_summary()

          # Свободное описание услуги
        if self.state == "custom_service":
            self.data["service"] = message
            self.state = "custom_service_confirm"

            return (
                f"Понял: «{message}».\n\n"
                "Хотите записаться на эту услугу?\n"
                "1. Да\n"
                "2. Нет"
            )

        # Подтверждение своей услуги
        if self.state == "custom_service_confirm":
            if message == "1" or normalized in (
                "да",
                "записаться",
                "записать",
                "хочу записаться",
                "запись",
                "записаться?",
                "запись?"
            ):
                self.state = "booking_date"
                return "На какой день хотите записаться?"

            if message == "2" or normalized in (
                "нет",
                "отмена",
                "не надо"
            ):
                self.reset()
                print_main_menu()
                return "Хорошо. Возвращаемся в главное меню."

            return "Введите 1 для записи или 2 для отмены."

    def booking_summary(self, prefix="Проверьте данные записи:"):
        return (
            f"{prefix}\n\n"
            f"Услуга: {self.data.get('service', 'не указана')}\n"
            f"День: {self.data.get('date', 'не указан')}\n"
            f"Время: {self.data.get('time', 'не указано')}\n"
            f"Запчасти: {self.data.get('parts', 'не указаны')}\n\n"
            "Всё верно?\n"
            "Напишите: да или нет."
        )

    def parts_request_summary(self, prefix="Заявка на подбор запчасти:"):
        return (
            f"{prefix}\n\n"
            f"VIN / номер кузова: {self.data.get('vin', 'не указан')}\n"
            f"Запчасть: {self.data.get('part_name', 'не указана')}\n\n"
            "Всё верно?\n"
            "Напишите: да или нет."
        )


def main():
    bot = CarZonaBot()

    print("=" * 60)
    print("CarZona72 — чат-бот автосервиса")
    print("=" * 60)
    print("Здравствуйте! Я виртуальный помощник CarZona72.")
    print("Напишите «меню», чтобы открыть главное меню.")
    print("Для выхода напишите «выход».")
    print("Для теста режима оператора: /оператор")
    print("Для возврата к боту: /бот\n")

    print_main_menu()

    while bot.state != "exit":
        user_message = input("\nВы: ")
        response = bot.handle(user_message)

        if response:
            print("Бот:", response)


if __name__ == "__main__":
    main()
