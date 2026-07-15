import uuid
from database import db
from models import User, Product, Ticket, Order

# Глобальная переменная для хранения авторизованного пользователя
current_user = None


def init_db():
    """Создает таблицы и наполняет БД ровно 3 стартовыми товарами"""
    db.connect()
    db.create_tables([User, Product, Ticket, Order])

    # Проверяем, пуста ли таблица товаров.
    # Если пуста — создаем ровно 3 товара из условия задания
    if Product.select().count() == 0:
        Product.create(name="Картинка с котиком", cost=20, count=50)
        Product.create(name="Наклейка синего цвета", cost=15, count=45)
        Product.create(name="Игральные кости (белые)", cost=25, count=40)

    # Генерируем 3 тестовых тикета для проверки функционала поинтов
    if Ticket.select().count() == 0:
        print("\n--- ТЕСТОВЫЕ ТИКЕТЫ (Скопируйте для проверки) ---")
        for _ in range(3):
            new_uuid = str(uuid.uuid4())
            Ticket.create(uuid=new_uuid)
            print(f"Сгенерирован тикет: {new_uuid}")
        print("--------------------------------------------------\n")
    db.close()


def show_products():
    """Выводит список доступных товаров (кол-во больше 0) с выравниванием по левому краю"""
    products = Product.select().where(Product.count > 0)

    # Выравнивание столбцов по левому краю согласно ТЗ
    print(f"{'ID':<10}{'Стоимость':<10}{'Кол-во':<10}{'Название'}")
    print("=" * 55)
    for p in products:
        print(f"{p.id:<10}{p.cost:<10}{p.count:<10}{p.name}")


def register():
    """Регистрация нового пользователя"""
    global current_user
    username = input("Введите логин > ")
    password = input("Введите пароль > ")

    # Проверка существования пользователя в БД
    if User.is_exist(username):
        print("Пользователь с таким логином уже существует!")
    else:
        current_user = User.create(username=username, password=password)
        print("Регистрация успешна! Вы вошли в систему.")


def login():
    """Авторизация существующего пользователя"""
    global current_user
    username = input("Введите логин > ")
    password = input("Введите пароль > ")

    try:
        user = User.get((User.username == username) & (User.password == password))
        current_user = user
        print("Успешный вход в систему!")
    except User.DoesNotExist:
        print("Неверный логин или пароль.")


def apply_ticket(command: str):
    """Обмен тикета на 20 поинтов"""
    parts = command.split()
    if len(parts) < 2:
        print("Пожалуйста, введите UUID тикета после команды.")
        return

    ticket_uuid = parts[1]

    # Проверяем валидность тикета через метод в Ticket
    if Ticket.valid_ticket(ticket_uuid):
        ticket = Ticket.get(Ticket.uuid == ticket_uuid)
        ticket.available = False  # Делаем тикет неактивным
        ticket.user = current_user  # Привязываем к текущему юзеру
        ticket.save()

        # Начисляем поинты
        current_user.points += 20
        current_user.save()
        print(f"Вы успешно обменяли тикет на 20 поинтов!\nТеперь у вас {current_user.points} поинтов")
    else:
        print("Данный тикет не существует или уже был использован.")


def buy(command: str):
    """Покупка товара с использованием поинтов"""
    parts = command.split()
    if len(parts) < 3:
        print("Формат команды: Купить <ID> <Кол-во>")
        return

    try:
        product_id = int(parts[1])
        count = int(parts[2])
    except ValueError:
        print("ID товара и количество должны быть числами.")
        return

    try:
        product = Product.get(Product.id == product_id)
        if product.count < count:
            print("На складе нет такого количества товара.")
            return

        total_cost = product.cost * count

        # Проверяем баланс поинтов пользователя
        if current_user.points < total_cost:
            print("Недостаточно поинтов для покупки.")
            return

        # Списываем поинты, уменьшаем остаток товара и фиксируем покупку
        current_user.points -= total_cost
        current_user.save()

        product.count -= count
        product.save()

        Order.create(user=current_user, product=product, count=count)

        print(f'Вы успешно купили "{product.name}" in количестве: {count}')
        print(f"У вас осталось {current_user.points} поинтов")

    except Product.DoesNotExist:
        print("Товар с таким ID не найден.")


def profile():
    """Отображение профиля пользователя и истории его заказов"""
    print(f"=== {current_user.username} ===")
    print(f"Поинтов: {current_user.points}")
    print("Заказы:")
    print(f"{'Дата заказа':<20}{'Кол-во':<10}{'Сумма':<10}{'Название'}")

    # Вызываем метод orders() из модели User
    orders = current_user.orders()
    for o in orders:
        dt = o.order_datetime.strftime("%H:%M %d.%m.%Y")
        total_sum = o.count * o.product.cost
        print(f"{dt:<20}{o.count:<10}{total_sum:<10}{o.product.name}")


def main():
    init_db()

    # Бесконечный цикл консольного интерфейса
    while True:
        print('\n=== Добро пожаловать в "Не магазин" ===')
        print('Здесь вы можете обменивать тикеты для того, чтобы приобретать товары')
        print('Для взаимодействия используйте команды:')

        if current_user is None:
            # Команды для гостя
            print('> Товары')
            print('> Зарегистрироваться')
            print('> Войти')
        else:
            # Команды для авторизованного пользователя
            print('> Товары')
            print('> Купить')
            print('> Профиль')
            print('> Тикет')

        print('> Выход')

        command = input("\n> ").strip()
        cmd_lower = command.lower()

        # Роутинг команд
        if cmd_lower == "выход":
            break
        elif cmd_lower == "товары":
            show_products()
        elif cmd_lower == "зарегистрироваться" and current_user is None:
            register()
        elif cmd_lower == "войти" and current_user is None:
            login()
        elif cmd_lower.startswith("тикет") and current_user is not None:
            apply_ticket(command)
        elif cmd_lower.startswith("купить") and current_user is not None:
            buy(command)
        elif cmd_lower == "профиль" and current_user is not None:
            profile()
        else:
            print("Команда не распознана или недоступна.")


if __name__ == "__main__":
    main()