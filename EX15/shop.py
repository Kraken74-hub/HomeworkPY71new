import datetime
import uuid
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Настройка базы данных
Base = declarative_base()
engine = create_engine('sqlite:///shop_db.sqlite', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


#МОДЕЛИ ДАННЫХ

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(30), nullable=False)
    points = Column(Integer, default=0)

    orders_rel = relationship("Order", back_populates="user")

    @staticmethod
    def is_exist(username: str) -> bool:
        """Проверяет, существует ли пользователь в базе."""
        user = session.query(User).filter(User.username == username).first()
        return user is not None

    def orders(self) -> list:
        """Возвращает список всех заказов пользователя."""
        return self.orders_rel


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    cost = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True, nullable=False)
    available = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    @staticmethod
    def valid_ticket(ticket_uuid: str) -> bool:
        """Проверяет валидность и доступность тикета."""
        ticket = session.query(Ticket).filter(Ticket.uuid == ticket_uuid).first()
        if ticket and ticket.available:
            return True
        return False


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    count = Column(Integer)
    order_datetime = Column(DateTime, default=datetime.datetime.now)

    user = relationship("User", back_populates="orders_rel")
    product = relationship("Product")


# Создание таблиц
Base.metadata.create_all(engine)


#ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ

def seed_data():
    """Заполнение базы начальными данными (если пусто)."""
    if session.query(Product).count() == 0:
        p1 = Product(id=1, name="брелок", cost=20, count=50)
        p2 = Product(id=2, name="Наклейка молния макквин", cost=15, count=45)
        p3 = Product(id=324, name="Игральные кости с перевесом", cost=25, count=40)
        session.add_all([p1, p2, p3])

        # Создадим тестовый тикет
        t = Ticket(uuid="ebb94499-05c9-449f-9f4a-402c6543f244", available=True)
        session.add(t)
        session.commit()


#ГЛОБАЛЬНОЕ СОСТОЯНИЕ
current_user = None


#КОМАНДЫ МАГАЗИНА

def register():
    print("=== Регистрация ===")
    username = input("Введите логин > ")
    password = input("Введите пароль > ")

    if User.is_exist(username):
        print("Ошибка: Пользователь с таким именем уже существует!")
    else:
        new_user = User(username=username, password=password)
        session.add(new_user)
        session.commit()
        print(f"Пользователь {username} успешно зарегистрирован!")


def login():
    global current_user
    username = input("Введите логин > ")
    password = input("Введите пароль > ")
    user = session.query(User).filter(User.username == username, User.password == password).first()
    if user:
        current_user = user
        print(f"Добро пожаловать, {username}!")
    else:
        print("Ошибка: Неверный логин или пароль.")


def show_products():
    products = session.query(Product).filter(Product.count > 0).all()
    print(f"{'ID':<10}{'Стоимость':<12}{'Кол-во':<10}{'Название'}")
    print("=" * 60)
    for p in products:
        print(f"{p.id:<10}{p.cost:<12}{p.count:<10}{p.name}")


def buy_product(cmd_args):
    try:
        p_id = int(cmd_args[0])
        qty = int(cmd_args[1])
    except (IndexError, ValueError):
        print("Используйте: Купить <id_товара> <количество>")
        return

    product = session.query(Product).filter(Product.id == p_id).first()
    if not product:
        print("Товар не найден.")
        return

    total_cost = product.cost * qty
    if current_user.points < total_cost:
        print(f"Недостаточно поинтов! Нужно: {total_cost}, у вас: {current_user.points}")
    elif product.count < qty:
        print("Недостаточно товара на складе.")
    else:
        # Списываем поинты и товар
        current_user.points -= total_cost
        product.count -= qty
        # Создаем заказ
        new_order = Order(user_id=current_user.id, product_id=product.id, count=qty)
        session.add(new_order)
        session.commit()
        print(f"Вы успешно купили '{product.name}' в количестве: {qty}")
        print(f"У вас осталось - {current_user.points} поинтов")


def use_ticket(ticket_uuid):
    if Ticket.valid_ticket(ticket_uuid):
        ticket = session.query(Ticket).filter(Ticket.uuid == ticket_uuid).first()
        ticket.available = False
        ticket.user_id = current_user.id
        current_user.points += 20
        session.commit()
        print(f"Тикет {ticket_uuid} успешно применен!")
        print(f"Вы успешно обменяли тикет на 20 поинтов!")
        print(f"Теперь у вас - {current_user.points} поинтов")
    else:
        print("Ошибка: Данный тикет не существует или уже был использован.")


def show_profile():
    print(f"\n=== {current_user.username} ===")
    print(f"Поинтов: {current_user.points}")
    print("\nЗаказы:")
    orders = current_user.orders()
    if not orders:
        print("Заказов пока нет.")
    else:
        print(f"{'Дата заказа':<25}{'Кол-во':<10}{'Сумма':<10}{'Название'}")
        print("-" * 60)
        for o in orders:
            date_str = o.order_datetime.strftime("%H:%M %d.%m.%Y")
            total = o.count * o.product.cost
            print(f"{date_str:<25}{o.count:<10}{total:<10}{o.product.name}")


#главный цикл

def main():
    global current_user
    seed_data()
    print("=== Добро пожаловать в 'Не магазин' ===")
    print("Здесь вы можете обменивать тикеты для того, чтобы приобретать товары")

    while True:
        if not current_user:
            print("\nДоступные команды: Зарегистрироваться, Войти, Выход")
            cmd = input("> ").strip().lower()
            if cmd == "зарегистрироваться":
                register()
            elif cmd == "войти":
                login()
            elif cmd == "выход":
                break
        else:
            print("\nКоманды: Товары, Купить <id> <кол>, Профиль, Тикет <uuid>, Выйти")
            raw_input = input("> ").strip().split()
            if not raw_input: continue

            cmd = raw_input[0].lower()

            if cmd == "товары":
                show_products()
            elif cmd == "купить":
                buy_product(raw_input[1:])
            elif cmd == "профиль":
                show_profile()
            elif cmd == "тикет":
                if len(raw_input) > 1:
                    use_ticket(raw_input[1])
                else:
                    print("Введите UUID тикета.")
            elif cmd == "выйти":
                current_user = None
            else:
                print("Неизвестная команда.")


if __name__ == "__main__":
    main()