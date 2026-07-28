import uuid
from database import engine, Base, db_session
from models import User, Product, Ticket, Order
from sqlalchemy import select, func

current_user: User | None = None


def init_db():
    Base.metadata.create_all(bind=engine)

    count = db_session.scalar(select(func.count(Product.id)))
    if count == 0:
        p1 = Product(name="Картинка с котиком", cost=20, count=50)
        p2 = Product(name="Наклейка синего цвета", cost=15, count=45)
        p3 = Product(name="Игральные кости (белые)", cost=25, count=40)

        db_session.add_all([p1, p2, p3])
        db_session.commit()


def show_products():
    stmt = select(Product).where(Product.count > 0)
    products = db_session.scalars(stmt).all()

    print(f"{'ID':<10}{'Стоимость':<10}{'Кол-во':<10}{'Название'}")
    print("=" * 55)
    for p in products:
        print(f"{p.id:<10}{p.cost:<10}{p.count:<10}{p.name}")


def register():
    global current_user
    username = input("Введите логин > ").strip()
    password = input("Введите пароль > ").strip()

    if User.is_exist(username):
        print("Пользователь с таким логином уже существует!")
    else:
        current_user = User(username=username, password=password)
        db_session.add(current_user)
        db_session.commit()
        print("Регистрация успешна! Вы вошли в систему.")


def login():
    global current_user
    username = input("Введите логин > ").strip()
    password = input("Введите пароль > ").strip()

    stmt = select(User).where(
        (User.username == username) & (User.password == password)
    )
    user = db_session.scalar(stmt)

    if user:
        current_user = user
        print("Успешный вход в систему!")
    else:
        print("Неверный логин или пароль.")


def apply_ticket(command: str):
    parts = command.split()
    if len(parts) < 2:
        print("Пожалуйста, введите UUID тикета после команды.")
        return

    ticket_uuid = parts[1]

    if Ticket.valid_ticket(ticket_uuid):
        ticket = db_session.scalar(select(Ticket).where(Ticket.uuid == ticket_uuid))

        if ticket and current_user:
            ticket.available = False
            ticket.user = current_user
            current_user.points += 20

            db_session.commit()
            print(f"Вы успешно обменяли тикет на 20 поинтов!\nТеперь у вас {current_user.points} поинтов")
    else:
        print("Данный тикет не существует или уже был использован.")


def buy(command: str):
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

    product = db_session.get(Product, product_id)

    if not product:
        print("Товар с таким ID не найден.")
        return

    if product.count < count:
        print("На складе нет такого количества товара.")
        return

    total_cost = product.cost * count

    if current_user.points < total_cost:
        print("Недостаточно поинтов для покупки.")
        return

    current_user.points -= total_cost
    product.count -= count

    order = Order(user=current_user, product=product, count=count)
    db_session.add(order)

    db_session.commit()

    print(f'Вы успешно купили "{product.name}" в количестве: {count}')
    print(f"У вас осталось {current_user.points} поинтов")


def profile():
    if not current_user:
        return

    print(f"=== {current_user.username} ===")
    print(f"Поинтов: {current_user.points}")
    print("Заказы:")
    print(f"{'Дата заказа':<20}{'Кол-во':<10}{'Сумма':<10}{'Название'}")

    for o in current_user.orders:
        dt = o.order_datetime.strftime("%H:%M %d.%m.%Y")
        total_sum = o.count * o.product.cost
        print(f"{dt:<20}{o.count:<10}{total_sum:<10}{o.product.name}")


def main():
    init_db()

    while True:
        print('\n=== Добро пожаловать в "Не магазин" ===')
        print('Здесь вы можете обменивать тикеты для того, чтобы приобретать товары')
        print('Для взаимодействия используйте команды:')

        if current_user is None:
            print('> Товары')
            print('> Зарегистрироваться')
            print('> Войти')
        else:
            print('> Товары')
            print('> Купить')
            print('> Профиль')
            print('> Тикет')

        print('> Выход')

        command = input("\n> ").strip()
        cmd_lower = command.lower()

        if cmd_lower == "выход":
            db_session.remove()  # Закрываем сессию при выходе
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