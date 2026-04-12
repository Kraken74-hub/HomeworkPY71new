import datetime
from peewee import *

# Настройка базы данных
db = SqliteDatabase('shop.db')


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    username = CharField(max_length=30, unique=True)
    password = CharField(max_length=30)
    points = IntegerField(default=0)

    @staticmethod
    def is_exist(username):
        return Users.select().where(Users.username == username).exists()

    def orders(self):
        return list(Orders.select().where(Orders.user == self))


class Products(BaseModel):
    name = CharField(max_length=255)
    cost = IntegerField()
    count = IntegerField()


class Orders(BaseModel):
    user = ForeignKeyField(Users, backref='orders')
    product = ForeignKeyField(Products, backref='orders')
    count = IntegerField()
    order_datetime = DateTimeField(default=datetime.datetime.now)


class Tickets(BaseModel):
    uuid = CharField(max_length=36, unique=True)
    available = BooleanField(default=True)
    user = ForeignKeyField(Users, backref='tickets', null=True)


# Инициализация таблиц
db.connect()
db.create_tables([Users, Products, Orders, Tickets])

# Наполнение товарами (если база пустая)
if Products.select().count() == 0:
    Products.insert_many([
        {'name': "Картинка с котиком", 'cost': 20, 'count': 50},
        {'name': "Наклейка синего цвета", 'cost': 15, 'count': 45},
        {'name': "Игральные кости (белые)", 'cost': 25, 'count': 40}
    ]).execute()

# Создание тестового тикета для проверки
test_uuid = "ebb94499-05c9-494f-9f4a-402c6543f244"
Tickets.get_or_create(uuid=test_uuid, defaults={'available': True})


# 2. Вспомогательные функции

def show_products():
    print("\n" + "=" * 55)
    print(f"{'ID':<8} {'Стоимость':<12} {'Кол-во':<10} {'Название':<20}")
    print("-" * 55)
    for p in Products.select().where(Products.count > 0):
        print(f"{p.id:<8} {p.cost:<12} {p.count:<10} {p.name:<20}")
    print("=" * 55)


# 3. Главный цикл программы
current_user = None

while True:
    if not current_user:
        print("\n=== Добро пожаловать в 'Не магазин' ===")
        print("> Товары | Зарегистрироваться | Войти")

        user_input = input("\nКоманда: ").strip().lower()

        if user_input == "товары":
            show_products()

        elif user_input == "зарегистрироваться":
            login = input("Введите логин > ").strip()
            if Users.is_exist(login):
                print("--- Ошибка: Пользователь уже существует! ---")
            else:
                password = input("Введите пароль > ").strip()
                current_user = Users.create(username=login, password=password)
                print(f"* Успешная регистрация! Добро пожаловать, {login}! *")

        elif user_input == "войти":
            login = input("Введите логин > ").strip()
            password = input("Введите пароль > ").strip()
            try:
                user = Users.get((Users.username == login) & (Users.password == password))
                current_user = user
                print(f"* Вы вошли как {login} *")
            except DoesNotExist:
                print("--- Ошибка: Неверный логин или пароль! ---")
        else:
            print("--- Команда не распознана. Попробуйте: товары, войти или зарегистрироваться ---")

    else:
        # Меню авторизованного пользователя
        print(f"\n[{current_user.username.upper()} | Поинты: {current_user.points}]")
        print("> Товары | Купить [ID] [Кол-во] | Профиль | Тикет [Код] | Выйти")

        raw_input = input("Команда: ").strip().lower()
        parts = raw_input.split()

        if not parts: continue
        cmd = parts[0]

        if cmd == "товары":
            show_products()

        elif cmd == "купить":
            if len(parts) < 3:
                print("--- Ошибка! Используйте: купить [ID] [количество] ---")
            else:
                try:
                    p_id, p_count = int(parts[1]), int(parts[2])
                    product = Products.get_or_none(Products.id == p_id)

                    if not product:
                        print("--- Ошибка: Товар не найден! ---")
                    elif product.count < p_count:
                        print(f"--- Ошибка: На складе только {product.count} шт. ---")
                    elif current_user.points < (product.cost * p_count):
                        print(f"--- Ошибка: Недостаточно поинтов! Нужно {product.cost * p_count} ---")
                    else:
                        product.count -= p_count
                        product.save()
                        current_user.points -= (product.cost * p_count)
                        current_user.save()
                        Orders.create(user=current_user, product=product, count=p_count)
                        print(f"* Успешно куплено: {product.name} ({p_count} шт.) *")
                except ValueError:
                    print("--- Ошибка: ID и количество должны быть числами! ---")

        elif cmd == "профиль":
            print(f"\n=== Профиль: {current_user.username} ===")
            print(f"Поинтов: {current_user.points}")
            print("\nВаши заказы:")
            my_orders = current_user.orders()
            if not my_orders:
                print("Список пуст.")
            else:
                print(f"{'Дата':<18} {'Кол-во':<8} {'Сумма':<8} {'Название':<20}")
                for o in my_orders:
                    date = o.order_datetime.strftime("%d.%m %H:%M")
                    print(f"{date:<18} {o.count:<8} {o.count * o.product.cost:<8} {o.product.name:<20}")

        elif cmd == "тикет":
            if len(parts) < 2:
                print("--- Ошибка! Введите: тикет [код] ---")
            else:
                t_uuid = parts[1]
                ticket = Tickets.get_or_none(Tickets.uuid == t_uuid)
                if ticket and ticket.available:
                    ticket.available = False
                    ticket.user = current_user
                    ticket.save()
                    current_user.points += 20
                    current_user.save()
                    print(f"* Тикет активирован! +20 поинтов (Всего: {current_user.points}) *")
                else:
                    print("--- Ошибка: Тикет не существует или уже использован ---")

        elif cmd == "выйти":
            current_user = None
            print("* Вы вышли из аккаунта *")

        else:
            print(f"--- Команда '{cmd}' не поддерживается в этом меню ---")