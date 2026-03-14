"""
Шаблоны для синтетической генерации банковских диалогов с ПД.
Каждый шаблон — строка с {placeholder}, рядом функции-генераторы значений.
"""
import re
import random
import string
from datetime import date, timedelta
from faker import Faker

fake = Faker("ru_RU")


# ─── Генераторы значений ──────────────────────────────────────────────────────

def gen_full_name():
    return f"{fake.last_name()} {fake.first_name()} {fake.middle_name()}"

def gen_first_name():
    return fake.first_name()

def gen_last_name():
    return fake.last_name()

def gen_phone():
    n = "".join(random.choices(string.digits, k=10))
    formats = [
        f"+7{n}", f"8{n}", f"+7 ({n[:3]}) {n[3:6]}-{n[6:8]}-{n[8:]}",
        f"8-{n[:3]}-{n[3:6]}-{n[6:8]}-{n[8:]}",
    ]
    return random.choice(formats)

def gen_date(start_year=1950, end_year=2005):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    d = start + timedelta(days=random.randint(0, (end - start).days))
    fmt = random.choice(["%d.%m.%Y", "%d/%m/%Y", "%-d %B %Y года"])
    return d.strftime(fmt)

def gen_birth_date():
    return gen_date(1950, 2005)

def gen_expiry_date():
    month = random.randint(1, 12)
    year  = random.randint(25, 30)
    return random.choice([f"{month:02d}/{year}", f"{month:02d}/{2000 + year}"])

def gen_reg_date():
    return gen_date(1980, 2020)

def gen_card_number():
    groups = ["".join(random.choices(string.digits, k=4)) for _ in range(4)]
    return random.choice([
        " ".join(groups),
        "".join(groups),
        "-".join(groups),
    ])

def gen_cvv():
    return "".join(random.choices(string.digits, k=random.choice([3, 4])))

def gen_pin():
    return "".join(random.choices(string.digits, k=4))

def gen_account_number():
    return "4081" + "".join(random.choices(string.digits, k=16))

def gen_inn_personal():
    return "".join(random.choices(string.digits, k=12))

def gen_inn_org():
    return "".join(random.choices(string.digits, k=10))

def gen_kpp():
    return "".join(random.choices(string.digits, k=9))

def gen_ogrn():
    return "".join(random.choices(string.digits, k=13))

def gen_bik():
    return "04" + "".join(random.choices(string.digits, k=7))

def gen_snils():
    n = "".join(random.choices(string.digits, k=9))
    return f"{n[:3]}-{n[3:6]}-{n[6:9]} {random.randint(10,99)}"

def gen_passport():
    series = "".join(random.choices(string.digits, k=4))
    number = "".join(random.choices(string.digits, k=6))
    return random.choice([
        f"{series} {number}",
        f"{series[:2]} {series[2:]} {number}",
    ])

def gen_drivers_license():
    series = "".join(random.choices(string.digits, k=4))
    number = "".join(random.choices(string.digits, k=6))
    return f"{series} {number}"

def gen_temp_id():
    return "".join(random.choices(string.digits, k=9))

def gen_birth_cert():
    roman = random.choice(["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"])
    region = random.choice(["МО", "СПБ", "ЕКБ", "КРД", "НСК"])
    number = "".join(random.choices(string.digits, k=6))
    return f"{roman}-{region} №{number}"

def gen_residence_permit():
    series = "".join(random.choices(string.digits, k=2))
    number = "".join(random.choices(string.digits, k=7))
    return f"{series} {number}"

def gen_api_key():
    styles = [
        lambda: "sk-" + "".join(random.choices(string.ascii_letters + string.digits, k=40)),
        lambda: "bk_api_key_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=24)),
        lambda: "Bearer " + "".join(random.choices(string.ascii_letters + string.digits, k=32)),
        lambda: "".join(random.choices(string.ascii_letters + string.digits + "-_", k=36)),
    ]
    return random.choice(styles)()

def gen_password():
    chars = string.ascii_letters + string.digits + "!@#$%"
    return "".join(random.choices(chars, k=random.randint(8, 16)))

def gen_otp():
    return "".join(random.choices(string.digits, k=random.choice([4, 6])))

def gen_code_word():
    words = ["Солнышко", "Мурка", "Ласточка", "Победа", "Байкал",
             "Сибирь", "Надежда", "Гвоздика", "Простор", "Орёл"]
    return random.choice(words)

def gen_email():
    return fake.email()

def gen_address():
    return fake.address().replace("\n", ", ")

def gen_city():
    return fake.city()

def gen_country():
    countries = ["Россия", "Казахстан", "Беларусь", "Узбекистан",
                 "Армения", "Азербайджан", "Таджикистан", "Киргизия", "Украина"]
    return random.choice(countries)

def gen_visa_type():
    types = ["рабочая виза", "разрешение на работу", "патент на работу",
             "вид на жительство", "временное убежище", "РВП"]
    return random.choice(types)

def gen_car_info():
    brands  = ["Toyota", "Kia", "Hyundai", "Lada", "BMW", "Mercedes", "Renault"]
    models  = ["Camry", "Rio", "Solaris", "Vesta", "X5", "E200", "Logan"]
    letters = "АВЕКМНОРСТУХ"
    reg = (random.choice(letters)
           + "".join(random.choices(string.digits, k=3))
           + "".join(random.choices(letters, k=2))
           + str(random.randint(11, 199)))
    return random.choice([
        f"{random.choice(brands)} {random.choice(models)}, рег. номер {reg}",
        f"госномер {reg}",
        f"автомобиль {reg}",
    ])

def gen_org_data():
    name = fake.company()
    inn  = gen_inn_org()
    kpp  = gen_kpp()
    bik  = gen_bik()
    acc  = gen_account_number()
    return random.choice([
        f"ООО «{name}», ИНН {inn}, КПП {kpp}",
        f"{name}, БИК {bik}, р/с {acc}",
        f"ИНН {inn}, ОГРН {gen_ogrn()}",
    ])

def gen_bank_name():
    banks = ["Сбербанк", "Тинькофф", "Альфа-Банк", "ВТБ", "Газпромбанк",
             "Росбанк", "Открытие", "Совкомбанк", "Промсвязьбанк", "Райффайзен"]
    return random.choice(banks)

def gen_magnetic_stripe():
    return "%" + "".join(random.choices(string.digits, k=37)) + "?"


# ─── Диалоговые контексты ─────────────────────────────────────────────────────
# Оборачивают сгенерированное сообщение в реплику поддержки / чата.
# {} — место для вставки тела сообщения.

DIALOG_CONTEXTS = [
    "{}",
    "Клиент: {}",
    "Здравствуйте! {}",
    "Добрый день. {}",
    "Оператор, помогите пожалуйста. {}",
    "Обращаюсь в поддержку: {}",
    "Срочный вопрос! {}",
]


# ─── Шаблоны по меткам ───────────────────────────────────────────────────────
# Первый placeholder — целевая сущность. Остальные — контекстное наполнение.

TEMPLATES = {

    "ФИО": [
        ("Хочу уточнить статус заявки на кредит. Заявка оформлена на имя {fio}, номер договора уточните, пожалуйста.",
         {"fio": gen_full_name}),
        ("Переведите 12 000 рублей на счёт получателя {fio}, это мой родственник.",
         {"fio": gen_full_name}),
        ("У меня блокировка счёта. Владелец — {fio}, паспорт в порядке, прошу разблокировать срочно.",
         {"fio": gen_full_name}),
        ("Ипотека оформлена на {fio}. Прошу прислать график платежей на почту.",
         {"fio": gen_full_name}),
        ("Мои данные в личном кабинете устарели. Полное ФИО: {fio}. Прошу обновить.",
         {"fio": gen_full_name}),
        ("Карта была утеряна, восстанавливаю по паспорту. Данные владельца: {fio}.",
         {"fio": gen_full_name}),
    ],

    "Номер телефона": [
        ("Не приходит СМС с кодом подтверждения на номер {phone}. Проверьте, пожалуйста, привязку.",
         {"phone": gen_phone}),
        ("Хочу сменить номер в профиле. Новый номер для привязки: {phone}.",
         {"phone": gen_phone}),
        ("Кто-то пытался войти в мой аккаунт. Мой номер {phone} — прошу проверить историю входов.",
         {"phone": gen_phone}),
        ("Восстановление доступа — отправьте код на {phone}, это актуальный контакт.",
         {"phone": gen_phone}),
        ("Оформляю доверенность, укажите мой телефон {phone} как контактный в договоре.",
         {"phone": gen_phone}),
    ],

    "Дата рождения": [
        ("Для подтверждения личности: дата рождения {dob}. Прошу подтвердить операцию.",
         {"dob": gen_birth_date}),
        ("Открываю вклад. Мои данные: {fio}, дата рождения {dob}, гражданство РФ.",
         {"dob": gen_birth_date, "fio": gen_full_name}),
        ("При верификации система не принимает дату {dob} — говорит, что не совпадает с базой.",
         {"dob": gen_birth_date}),
        ("Исправьте дату рождения в профиле: правильная — {dob}, в системе стоит другая.",
         {"dob": gen_birth_date}),
        ("Оформляю детскую карту на ребёнка. Дата рождения {dob}, нужна карта Мир.",
         {"dob": gen_birth_date}),
    ],

    "Паспортные данные": [
        ("Для оформления кредита предоставляю паспортные данные: серия и номер {passport}.",
         {"passport": gen_passport}),
        ("Паспорт {passport}, выдан в городе {city}. Прошу обновить данные в профиле.",
         {"passport": gen_passport, "city": gen_city}),
        ("Сменил паспорт, новые данные: {passport}. Старый был утерян.",
         {"passport": gen_passport}),
        ("Верификация для снятия лимитов: {fio}, паспорт {passport}.",
         {"passport": gen_passport, "fio": gen_full_name}),
        ("При подаче заявки на ипотеку укажите паспорт {passport} как основной документ.",
         {"passport": gen_passport}),
    ],

    "Полный адрес": [
        ("Прошу доставить новую карту по адресу {address}. Удобное время — с 10 до 18.",
         {"address": gen_address}),
        ("Адрес регистрации для оформления ипотеки: {address}.",
         {"address": gen_address}),
        ("Фактическое место проживания отличается от прописки. Живу по адресу {address}.",
         {"address": gen_address}),
        ("Для договора укажите мой адрес: {address}. Индекс правильный.",
         {"address": gen_address}),
        ("Не приходят бумажные выписки. Мой актуальный адрес {address}, проверьте доставку.",
         {"address": gen_address}),
    ],

    "Email": [
        ("Выписку за последние три месяца прошу прислать на {email}.",
         {"email": gen_email}),
        ("Уведомления о транзакциях не приходят на {email} уже неделю, проверьте настройки.",
         {"email": gen_email}),
        ("Привяжите личный кабинет к адресу {email}, хочу получать документы туда.",
         {"email": gen_email}),
        ("Забыл пароль, ссылку для сброса отправьте на {email}.",
         {"email": gen_email}),
        ("Смена email: новый адрес {email}. Старый больше не актуален, потерял доступ.",
         {"email": gen_email}),
    ],

    "Номер карты": [
        ("Карта {card} заблокирована после трёх неверных попыток ввода ПИН. Прошу разблокировать.",
         {"card": gen_card_number}),
        ("Перевод на карту {card} завис в статусе «в обработке» уже 3 часа.",
         {"card": gen_card_number}),
        ("Подозрительное списание с карты {card} на сумму 4 500 рублей — я эту операцию не совершал.",
         {"card": gen_card_number}),
        ("Хочу перевыпустить карту {card} в связи с истечением срока действия.",
         {"card": gen_card_number}),
        ("Привяжите карту {card} к Apple Pay, инструкция не помогает.",
         {"card": gen_card_number}),
    ],

    "CVV/CVC": [
        ("При оплате онлайн система запрашивает CVV. Код с обратной стороны: {cvv}. Почему не проходит?",
         {"cvv": gen_cvv}),
        ("Уточните: у меня карта Visa, CVV {cvv} — три цифры, верно?",
         {"cvv": gen_cvv}),
        ("Для верификации карты в магазине ввёл CVC {cvv}, но операция отклоняется.",
         {"cvv": gen_cvv}),
        ("Подозреваю утечку данных. Мой CVV {cvv} мог стать известен третьим лицам.",
         {"cvv": gen_cvv}),
    ],

    "ПИН код": [
        ("Три раза ввёл неверный ПИН, карта заблокировалась. Последний ПИН который помню — {pin}.",
         {"pin": gen_pin}),
        ("Хочу сменить ПИН карты. Текущий ПИН {pin}, новый выберу сам в банкомате.",
         {"pin": gen_pin}),
        ("Мошенники могли узнать мой ПИН {pin} — прошу срочно заблокировать карту.",
         {"pin": gen_pin}),
    ],

    "Дата окончания срока действия карты": [
        ("Карта заканчивается в {expiry}, а перевыпуск так и не пришёл. Когда ждать?",
         {"expiry": gen_expiry_date}),
        ("При оплате в интернете ввожу срок действия {expiry}, сайт говорит что карта недействительна.",
         {"expiry": gen_expiry_date}),
        ("Подтвердите данные карты: номер — последние 4 цифры 3421, срок действия {expiry}.",
         {"expiry": gen_expiry_date}),
        ("Карта {card} действует до {expiry}, автоперевыпуск включён? Хочу уточнить.",
         {"expiry": gen_expiry_date, "card": gen_card_number}),
    ],

    "Имя держателя карты": [
        ("На карте написано {holder}, но при оплате за рубежом имя не совпадает с загранпаспортом.",
         {"holder": lambda: fake.first_name().upper() + " " + fake.last_name().upper()}),
        ("Имя держателя карты {holder} написано с ошибкой, прошу перевыпустить.",
         {"holder": lambda: fake.first_name().upper() + " " + fake.last_name().upper()}),
        ("Для оплаты в зарубежном магазине нужно имя на карте: {holder}.",
         {"holder": lambda: fake.first_name().upper() + " " + fake.last_name().upper()}),
    ],

    "Номер банковского счета": [
        ("Прошу перевести зарплату на расчётный счёт {account}. Реквизиты актуальны.",
         {"account": gen_account_number}),
        ("Счёт {account} был заморожен по ошибке, прошу срочно снять ограничения.",
         {"account": gen_account_number}),
        ("Работодатель запрашивает реквизиты для перечисления. Счёт {account}, банк Альфа.",
         {"account": gen_account_number}),
        ("На счёт {account} должно было прийти пополнение от {fio}, но средства не поступили.",
         {"account": gen_account_number, "fio": gen_full_name}),
    ],

    "Содержимое магнитной полосы": [
        ("Мошенники скопировали данные магнитной полосы карты: {stripe}. Требую блокировки.",
         {"stripe": gen_magnetic_stripe}),
        ("Технический запрос: дамп магнитной полосы для диагностики — {stripe}.",
         {"stripe": gen_magnetic_stripe}),
        ("Считанные данные с ридера: {stripe}. Прошу проверить подлинность карты.",
         {"stripe": gen_magnetic_stripe}),
    ],

    "API ключи": [
        ("Интеграция с вашим платёжным API перестала работать. Токен {api_key} возвращает 401.",
         {"api_key": gen_api_key}),
        ("Прошу сгенерировать новый ключ. Текущий {api_key} скомпрометирован, нашли в логах.",
         {"api_key": gen_api_key}),
        ("Для подключения эквайринга передаю API ключ {api_key}, настройте, пожалуйста, вебхук.",
         {"api_key": gen_api_key}),
        ("Bearer-токен {api_key} истёк раньше срока, система выдаёт ошибку авторизации.",
         {"api_key": gen_api_key}),
    ],

    "Пароли": [
        ("Пароль {password} от личного кабинета перестал подходить после вашего обновления системы.",
         {"password": gen_password}),
        ("Подозреваю взлом — кто-то менял пароль. Мой пароль был {password}, сейчас не входит.",
         {"password": gen_password}),
        ("Для верификации по телефону назову текущий пароль: {password}. Прошу подтвердить.",
         {"password": gen_password}),
    ],

    "Одноразовые коды": [
        ("Получил СМС с кодом {otp}, но операцию я не инициировал. Это мошенники?",
         {"otp": gen_otp}),
        ("Ввожу код из СМС {otp}, а система говорит «код недействителен». Уже третий раз.",
         {"otp": gen_otp}),
        ("Код подтверждения для перевода: {otp}. Прошу ускорить обработку.",
         {"otp": gen_otp}),
        ("Код {otp} пришёл с задержкой 10 минут, операция уже отменилась. Помогите повторить.",
         {"otp": gen_otp}),
    ],

    "Кодовые слова": [
        ("Для идентификации по телефону называю кодовое слово: {code_word}. Прошу продолжить.",
         {"code_word": gen_code_word}),
        ("Забыл кодовое слово — помню только что оно было {code_word}, но система не принимает.",
         {"code_word": gen_code_word}),
        ("Установите новое кодовое слово {code_word} взамен утраченного.",
         {"code_word": gen_code_word}),
    ],

    "Сведения об ИНН": [
        ("Для налогового вычета по ипотеке предоставляю ИНН: {inn}.",
         {"inn": gen_inn_personal}),
        ("При оформлении самозанятости нужен ИНН {inn} — подтвердите, что данные совпадают.",
         {"inn": gen_inn_personal}),
        ("Работодатель требует реквизиты. Мой ИНН {inn}, счёт в вашем банке.",
         {"inn": gen_inn_personal}),
        ("Обновите ИНН в профиле на {inn}, в системе стоит старый номер.",
         {"inn": gen_inn_personal}),
    ],

    "СНИЛС клиента": [
        ("Для перевода накоплений в НПФ нужен СНИЛС {snils}. Помогите оформить заявку.",
         {"snils": gen_snils}),
        ("При подаче на пособие система запрашивает СНИЛС, у меня {snils}.",
         {"snils": gen_snils}),
        ("Прошу добавить СНИЛС {snils} в профиль клиента для оформления страховки.",
         {"snils": gen_snils}),
    ],

    "Водительское удостоверение": [
        ("Оформляю автокредит, предоставляю водительское удостоверение {dl} как второй документ.",
         {"dl": gen_drivers_license}),
        ("При открытии счёта использовал ВУ {dl} вместо паспорта, возможно ли это?",
         {"dl": gen_drivers_license}),
        ("Права {dl} были предъявлены при верификации, но оператор их не принял.",
         {"dl": gen_drivers_license}),
    ],

    "Временное удостоверение личности": [
        ("Паспорт на замене, есть временное удостоверение личности №{tmp_id}. Могу открыть счёт?",
         {"tmp_id": gen_temp_id}),
        ("Предъявляю временное УЛ {tmp_id} для проведения операции, паспорт в МВД.",
         {"tmp_id": gen_temp_id}),
        ("Временное удостоверение {tmp_id} действует ещё 30 дней, успею получить карту?",
         {"tmp_id": gen_temp_id}),
    ],

    "Свидетельство о рождении": [
        ("Оформляю детский счёт. Свидетельство о рождении ребёнка: {birth_cert}.",
         {"birth_cert": gen_birth_cert}),
        ("Серия и номер свидетельства о рождении: {birth_cert}. Нужна детская карта.",
         {"birth_cert": gen_birth_cert}),
        ("При оформлении материнского капитала потребовался {birth_cert}, всё сделал.",
         {"birth_cert": gen_birth_cert}),
    ],

    "Серия и номер вида на жительство": [
        ("Являюсь резидентом РФ, вид на жительство серии {rp}. Прошу открыть расчётный счёт.",
         {"rp": gen_residence_permit}),
        ("ВНЖ №{rp} действителен до {expiry}. Могу ли я оформить ипотеку с этим документом?",
         {"rp": gen_residence_permit, "expiry": gen_expiry_date}),
        ("Обновил ВНЖ, новые данные: {rp}. Прошу обновить в профиле.",
         {"rp": gen_residence_permit}),
    ],

    "Гражданство и названия стран": [
        ("Я гражданин {country}, хочу открыть валютный счёт. Какие документы нужны?",
         {"country": gen_country}),
        ("Гражданство {country}, паспорт иностранный. Принимаете такие документы?",
         {"country": gen_country}),
        ("Перевод за рубеж — в {country}. Есть ли ограничения по сумме?",
         {"country": gen_country}),
        ("Нерезидент из {country}, интересует открытие депозита в рублях.",
         {"country": gen_country}),
    ],

    "Место рождения": [
        ("В паспорте указано место рождения {city}, но система его не принимает при верификации.",
         {"city": gen_city}),
        ("Родился в {city}, сейчас живу в Москве. Нужно ли обновлять место рождения в профиле?",
         {"city": gen_city}),
        ("В анкете на кредит написал место рождения {city} — оператор сказал проверить правильность.",
         {"city": gen_city}),
    ],

    "Разрешение на работу / визу": [
        ("Имею {visa_type} и хочу открыть счёт для получения зарплаты.",
         {"visa_type": gen_visa_type}),
        ("Предъявил {visa_type} при оформлении карты, но оператор отказал. Законно ли это?",
         {"visa_type": gen_visa_type}),
        ("Документ для верификации — {visa_type}. Других удостоверений с собой нет.",
         {"visa_type": gen_visa_type}),
        ("Срок {visa_type} истекает через месяц, успею получить дебетовую карту?",
         {"visa_type": gen_visa_type}),
    ],

    "Данные об автомобиле клиента": [
        ("Оформляю КАСКО, данные о ТС: {car}. Прошу рассчитать стоимость страховки.",
         {"car": gen_car_info}),
        ("Подаю заявку на автокредит. Желаемый автомобиль: {car}.",
         {"car": gen_car_info}),
        ("ДТП произошло с участием ТС {car}. Куда направить документы для выплаты?",
         {"car": gen_car_info}),
        ("Застрахованный автомобиль {car} угнали. Прошу открыть страховой случай.",
         {"car": gen_car_info}),
    ],

    "Данные об организации/юридическом лице (ИНН, КПП, ОГРН, БИК, адреса, расчётный счёт)": [
        ("Реквизиты нашей организации для договора эквайринга: {org}.",
         {"org": gen_org_data}),
        ("Входящий платёж от контрагента не поступил. Данные плательщика: {org}.",
         {"org": gen_org_data}),
        ("Открываю расчётный счёт для ООО. Реквизиты юрлица: {org}.",
         {"org": gen_org_data}),
        ("Прошу подтвердить зачисление от {org}. Сумма 250 000 рублей, дата — сегодня.",
         {"org": gen_org_data}),
    ],

    "Наименование банка": [
        ("Переводил средства из {bank}, но деньги до вас не дошли уже двое суток.",
         {"bank": gen_bank_name}),
        ("Ранее обслуживался в {bank}, хочу перейти к вам. Как перенести зарплатный проект?",
         {"bank": gen_bank_name}),
        ("Счёт для погашения кредита открыт в {bank}, принимаете оплату оттуда?",
         {"bank": gen_bank_name}),
        ("Рефинансирование ипотеки из {bank}: какие документы подготовить?",
         {"bank": gen_bank_name}),
    ],

    "Дата регистрации по месту жительства или пребывания": [
        ("Дата регистрации по месту жительства: {reg_date}. Прошу внести в анкету.",
         {"reg_date": gen_reg_date}),
        ("В документах указано, что прописан с {reg_date}, а система ставит другую дату.",
         {"reg_date": gen_reg_date}),
        ("Временная регистрация с {reg_date}, постоянной прописки нет. Могу оформить карту?",
         {"reg_date": gen_reg_date}),
    ],
}


# ─── Генерация примера ────────────────────────────────────────────────────────

def generate_example(label: str) -> dict:
    """
    Возвращает dict: text, target (формат тренировочного датасета), entity.
    Текст случайно оборачивается в диалоговый контекст.
    """
    template, generators = random.choice(TEMPLATES[label])
    values = {key: fn() for key, fn in generators.items()}

    placeholders = re.findall(r"\{(\w+)\}", template)
    target_placeholder = placeholders[0]

    body = template
    for key, val in values.items():
        body = body.replace(f"{{{key}}}", val, 1)

    # Случайная диалоговая обёртка (смещение спана считается автоматически)
    text = random.choice(DIALOG_CONTEXTS).format(body)

    target_value = values[target_placeholder]
    start = text.index(target_value)
    end   = start + len(target_value)

    return {
        "text":   text,
        "target": f"[({start}, {end}, '{label}')]",
        "entity": target_value,
    }


# ─── Комбо-шаблоны (2–3 ПД в одном тексте) ───────────────────────────────────
# Формат: (шаблон, {placeholder: (generator_fn, label)})
# Placeholder-ы перечислены в порядке их появления в шаблоне.

def _holder():
    return fake.first_name().upper() + " " + fake.last_name().upper()

COMBO_TEMPLATES = [
    # ── Идентификация личности ──
    (
        "Для верификации сообщаю данные: {fio}, дата рождения {dob}, паспорт {passport}.",
        {"fio": (gen_full_name, "ФИО"), "dob": (gen_birth_date, "Дата рождения"),
         "passport": (gen_passport, "Паспортные данные")},
    ),
    (
        "Меня зовут {fio}, родился {dob}. Прошу восстановить доступ к личному кабинету.",
        {"fio": (gen_full_name, "ФИО"), "dob": (gen_birth_date, "Дата рождения")},
    ),
    (
        "ФИО клиента: {fio}, паспорт {passport}. Подтвердите личность для проведения операции.",
        {"fio": (gen_full_name, "ФИО"), "passport": (gen_passport, "Паспортные данные")},
    ),
    (
        "{fio}, паспорт {passport}, адрес доставки карты: {address}.",
        {"fio": (gen_full_name, "ФИО"), "passport": (gen_passport, "Паспортные данные"),
         "address": (gen_address, "Полный адрес")},
    ),
    (
        "Полные данные: {fio}, СНИЛС {snils}, паспорт {passport}. Нужна расширенная верификация.",
        {"fio": (gen_full_name, "ФИО"), "snils": (gen_snils, "СНИЛС клиента"),
         "passport": (gen_passport, "Паспортные данные")},
    ),

    # ── Контактные данные ──
    (
        "Мои контакты: {fio}, телефон {phone}, email {email}. Прошу обновить профиль.",
        {"fio": (gen_full_name, "ФИО"), "phone": (gen_phone, "Номер телефона"),
         "email": (gen_email, "Email")},
    ),
    (
        "Для связи: {fio}, номер {phone}. Перезвоните, пожалуйста.",
        {"fio": (gen_full_name, "ФИО"), "phone": (gen_phone, "Номер телефона")},
    ),
    (
        "Уведомления не приходят. Проверьте телефон {phone} и почту {email} в профиле.",
        {"phone": (gen_phone, "Номер телефона"), "email": (gen_email, "Email")},
    ),

    # ── Открытие счёта / KYC ──
    (
        "Открываю счёт. {fio}, телефон {phone}, дата рождения {dob}.",
        {"fio": (gen_full_name, "ФИО"), "phone": (gen_phone, "Номер телефона"),
         "dob": (gen_birth_date, "Дата рождения")},
    ),
    (
        "{fio}, ИНН {inn}, СНИЛС {snils} — все данные для пенсионного перевода.",
        {"fio": (gen_full_name, "ФИО"), "inn": (gen_inn_personal, "Сведения об ИНН"),
         "snils": (gen_snils, "СНИЛС клиента")},
    ),
    (
        "Для налогового вычета: {fio}, ИНН {inn}, счёт {account}.",
        {"fio": (gen_full_name, "ФИО"), "inn": (gen_inn_personal, "Сведения об ИНН"),
         "account": (gen_account_number, "Номер банковского счета")},
    ),

    # ── Данные карты ──
    (
        "Карта {card}, срок действия {expiry}. Онлайн-оплата не проходит.",
        {"card": (gen_card_number, "Номер карты"),
         "expiry": (gen_expiry_date, "Дата окончания срока действия карты")},
    ),
    (
        "Данные карты: номер {card}, CVV {cvv}, срок {expiry}. Почему отклоняется платёж?",
        {"card": (gen_card_number, "Номер карты"), "cvv": (gen_cvv, "CVV/CVC"),
         "expiry": (gen_expiry_date, "Дата окончания срока действия карты")},
    ),
    (
        "Имя на карте {holder}, номер {card}. За рубежом платёж не принимают.",
        {"holder": (_holder, "Имя держателя карты"), "card": (gen_card_number, "Номер карты")},
    ),
    (
        "Перевод получателю {fio} на счёт {account} из {bank}.",
        {"fio": (gen_full_name, "ФИО"), "account": (gen_account_number, "Номер банковского счета"),
         "bank": (gen_bank_name, "Наименование банка")},
    ),

    # ── Аутентификация ──
    (
        "Пароль {password} не подходит, а код из СМС {otp} уже истёк. Как войти?",
        {"password": (gen_password, "Пароли"), "otp": (gen_otp, "Одноразовые коды")},
    ),
    (
        "Кодовое слово {code_word}, одноразовый код {otp}. Прошу провести операцию.",
        {"code_word": (gen_code_word, "Кодовые слова"), "otp": (gen_otp, "Одноразовые коды")},
    ),
    (
        "Токен {api_key} и пароль {password} скомпрометированы. Прошу заблокировать доступ.",
        {"api_key": (gen_api_key, "API ключи"), "password": (gen_password, "Пароли")},
    ),

    # ── Адрес + регистрация ──
    (
        "Адрес регистрации: {address}. Прописан с {reg_date}.",
        {"address": (gen_address, "Полный адрес"),
         "reg_date": (gen_reg_date, "Дата регистрации по месту жительства или пребывания")},
    ),
    (
        "Фактический адрес: {address}. Дата регистрации {reg_date}, место рождения {city}.",
        {"address": (gen_address, "Полный адрес"),
         "reg_date": (gen_reg_date, "Дата регистрации по месту жительства или пребывания"),
         "city": (gen_city, "Место рождения")},
    ),

    # ── Иностранный гражданин ──
    (
        "Гражданство {country}, имею {visa_type}. Хочу открыть счёт.",
        {"country": (gen_country, "Гражданство и названия стран"),
         "visa_type": (gen_visa_type, "Разрешение на работу / визу")},
    ),
    (
        "Я гражданин {country}, ВНЖ серии {rp}. Могу оформить кредитную карту?",
        {"country": (gen_country, "Гражданство и названия стран"),
         "rp": (gen_residence_permit, "Серия и номер вида на жительство")},
    ),

    # ── Автомобиль ──
    (
        "Оформляю КАСКО. Владелец: {fio}, автомобиль {car}.",
        {"fio": (gen_full_name, "ФИО"), "car": (gen_car_info, "Данные об автомобиле клиента")},
    ),

    # ── Организация + банк ──
    (
        "Реквизиты контрагента: {org}. Счёт открыт в {bank}.",
        {"org": (gen_org_data, "Данные об организации/юридическом лице (ИНН, КПП, ОГРН, БИК, адреса, расчётный счёт)"),
         "bank": (gen_bank_name, "Наименование банка")},
    ),
    (
        "Входящий платёж от {org} не поступил. Отправляли из {bank}.",
        {"org": (gen_org_data, "Данные об организации/юридическом лице (ИНН, КПП, ОГРН, БИК, адреса, расчётный счёт)"),
         "bank": (gen_bank_name, "Наименование банка")},
    ),

    # ── Свидетельство о рождении ──
    (
        "Для детской карты: свидетельство {birth_cert}, дата рождения {dob}.",
        {"birth_cert": (gen_birth_cert, "Свидетельство о рождении"),
         "dob": (gen_birth_date, "Дата рождения")},
    ),
]


def generate_combo_example() -> dict:
    """
    Генерирует пример с 2–3 ПД из COMBO_TEMPLATES.
    Возвращает dict: text, target (несколько спанов), entity (первая сущность).
    """
    template, ph_map = random.choice(COMBO_TEMPLATES)
    ordered_phs = re.findall(r"\{(\w+)\}", template)

    values = {ph: fn() for ph, (fn, _) in ph_map.items()}

    # Строим текст и собираем спаны, заменяя placeholder-ы по порядку
    text = template
    spans = []
    for ph in ordered_phs:
        val   = values[ph]
        label = ph_map[ph][1]
        ph_str = "{" + ph + "}"
        idx   = text.index(ph_str)
        text  = text[:idx] + val + text[idx + len(ph_str):]
        spans.append((idx, idx + len(val), label))

    # Диалоговая обёртка — сдвигаем все спаны на длину префикса
    ctx = random.choice(DIALOG_CONTEXTS)
    prefix_len = ctx.index("{}")
    text = ctx.format(text)
    spans = [(s + prefix_len, e + prefix_len, lbl) for s, e, lbl in spans]

    target_str = "[" + ", ".join(f"({s}, {e}, '{lbl}')" for s, e, lbl in spans) + "]"
    return {
        "text":   text,
        "target": target_str,
        "entity": spans[0][2],  # метка первой сущности
    }




# ─── Негативные примеры (без ПД) ─────────────────────────────────────────────

def _rnd_amount():
    return f"{random.choice([500, 1000, 1500, 2000, 3000, 5000, 10000, 15000, 25000, 50000])} рублей"

def _rnd_period():
    return random.choice(["3 месяца", "6 месяцев", "9 месяцев", "1 год", "2 года", "3 года"])

def _rnd_product():
    return random.choice([
        "дебетовую карту", "кредитную карту", "вклад", "накопительный счёт",
        "ипотеку", "потребительский кредит", "автокредит", "страховку",
    ])

def _rnd_channel():
    return random.choice(["в мобильном приложении", "на сайте", "в банкомате", "в отделении"])

def _rnd_wait():
    return random.choice(["час", "два часа", "полдня", "сутки", "три дня", "неделю"])

def _rnd_error():
    return random.choice(["ошибку 403", "ошибку 500", "«Сервис недоступен»",
                          "«Операция отклонена»", "«Неверный запрос»", "пустой экран"])

def _rnd_fee():
    return random.choice(["комиссию", "списание", "штраф", "пени", "неожиданное удержание"])


# Каждый шаблон — строка с {placeholder}, generators — вспомогательные (не ПД)
NEGATIVE_TEMPLATES = [

    # Проблемы со входом
    "Не могу войти {channel}, приложение выдаёт {error}. Что делать?",
    "После обновления приложения перестал работать вход {channel}.",
    "Двухфакторная аутентификация не работает уже {wait}.",
    "Сессия постоянно сбрасывается {channel}, приходится заходить заново каждые 10 минут.",
    "При попытке войти через Face ID получаю {error}.",

    # Переводы и платежи
    "Отправил перевод {wait} назад, деньги до сих пор не дошли. Что происходит?",
    "Перевод завис в статусе «в обработке» уже {wait}.",
    "Оплата {channel} не проходит, хотя баланс достаточный.",
    "Хочу отменить перевод — возможно ли это, если он ещё не исполнен?",
    "Платёж за коммунальные услуги прошёл дважды, как вернуть лишнее списание?",
    "Не могу оплатить покупку {channel}, терминал говорит «Отклонено банком».",
    "Автоплатёж за интернет не сработал в этом месяце, хотя деньги на счёте есть.",

    # Карты
    "Карта {channel} не читается, хотя физически не повреждена.",
    "Банкомат забрал карту и не вернул. Как её получить обратно?",
    "Бесконтактная оплата перестала работать после смены чехла на телефоне.",
    "Карта заблокирована после трёх неверных попыток ввода, как разблокировать?",
    "Хочу перевыпустить карту досрочно — сколько это стоит?",
    "Установил лимит на снятие наличных, но он не применяется.",

    # Продукты и условия
    "Какой процент по вкладу на {period}?",
    "Хочу оформить {product} — какие документы нужны?",
    "Можно ли досрочно погасить {product} без штрафов?",
    "Изменились ли условия по моему вкладу после последнего обновления тарифов?",
    "Как рассчитывается кешбэк по этой карте?",
    "Работает ли карта за границей без предварительного уведомления банка?",
    "Каков минимальный взнос для открытия накопительного счёта?",
    "Есть ли у вас программа рефинансирования кредита из другого банка?",

    # Технические проблемы
    "Приложение зависает на экране загрузки после последнего обновления.",
    "История операций {channel} не отображается за прошлый месяц.",
    "Push-уведомления о транзакциях перестали приходить две недели назад.",
    "Не могу загрузить выписку — кнопка скачивания неактивна.",
    "График платежей по кредиту не открывается {channel}.",
    "QR-код для оплаты не сканируется в магазине.",

    # Жалобы
    "Списали {fee} без предупреждения. Прошу объяснить основание.",
    "Оператор на горячей линии не смог ответить на мой вопрос и повесил трубку.",
    "Уже третий раз обращаюсь с одной проблемой, и её никто не решает.",
    "Получил отказ в {product} без объяснения причин, хочу знать почему.",
    "Обещали перезвонить {wait} назад — никто так и не позвонил.",

    # Общие вопросы
    "Как подключить автоплатёж за ЖКХ {channel}?",
    "Как установить индивидуальный лимит на онлайн-покупки?",
    "Можно ли открыть совместный счёт на двух владельцев?",
    "Как получить справку о наличии счёта для визы?",
    "В каком отделении можно открыть {product} прямо сегодня?",
    "Сколько времени занимает проверка заявки на {product}?",
]

_NEG_GENERATORS = {
    "channel":  _rnd_channel,
    "error":    _rnd_error,
    "wait":     _rnd_wait,
    "period":   _rnd_period,
    "product":  _rnd_product,
    "fee":      _rnd_fee,
    "amount":   _rnd_amount,
}


def generate_negative_example() -> dict:
    """Генерирует пример без ПД. target=[], entity=''."""
    template = random.choice(NEGATIVE_TEMPLATES)
    placeholders = re.findall(r"\{(\w+)\}", template)

    text = template
    for ph in placeholders:
        text = text.replace("{" + ph + "}", _NEG_GENERATORS[ph](), 1)

    ctx = random.choice(DIALOG_CONTEXTS)
    text = ctx.format(text)

    return {"text": text, "target": "[]", "entity": ""}


def generate_df(
    n_total: int = 1000,
    neg_frac: float = 0.3,
    combo_frac: float = 0.2,
) -> "pl.DataFrame":
    """
    n_total     — общее число примеров
    neg_frac    — доля примеров без ПД     (0.0–1.0), по умолчанию 30 %
    combo_frac  — доля комбо-примеров (2–3 ПД) среди позитивных, по умолчанию 20 %

    Оставшиеся позитивные примеры распределяются равномерно по одиночным меткам.
    """
    import polars as pl

    n_negative = round(n_total * neg_frac)
    n_positive = n_total - n_negative
    n_combo    = round(n_positive * combo_frac)
    n_single   = n_positive - n_combo

    # одиночные: равномерно по меткам
    per_label, remainder = divmod(n_single, len(TEMPLATES))
    labels = list(TEMPLATES.keys())
    single_labels = labels * per_label + labels[:remainder]

    rows  = [generate_example(lbl) for lbl in single_labels]
    rows += [generate_combo_example()    for _ in range(n_combo)]
    rows += [generate_negative_example() for _ in range(n_negative)]

    random.shuffle(rows)
    return pl.DataFrame(rows)


if __name__ == "__main__":
    import polars as pl
    df = generate_df(n_total=4000, neg_frac=0.2, combo_frac=0.5)
    df.write_csv("synthetic.csv")
    print(df.head(5))
