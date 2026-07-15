import datetime
from peewee import Model, CharField, IntegerField, BooleanField, ForeignKeyField, DateTimeField
from database import db

class BaseModel(Model):
    """Базовый класс для моделей, указывающий на нашу БД"""
    class Meta:
        database = db

class User(BaseModel):
    """Таблица пользователей [cite: 167]"""
    username = CharField(max_length=30, unique=True) # [cite: 174]
    password = CharField(max_length=30) # [cite: 178]
    points = IntegerField(default=0) # [cite: 182]

    @staticmethod
    def is_exist(username: str) -> bool:
        """Проверяет, есть ли пользователь в БД [cite: 40, 41]"""
        try:
            User.get(User.username == username) # [cite: 45]
            return True # [cite: 49]
        except User.DoesNotExist: # [cite: 46]
            return False # [cite: 48]

    def orders(self) -> list:
        """Возвращает список всех заказов пользователя [cite: 163, 164]"""
        return list(Order.select().where(Order.user == self))

class Product(BaseModel):
    """Таблица товаров [cite: 186]"""
    name = CharField(max_length=255) # [cite: 193]
    cost = IntegerField() # mediumint в peewee можно заменить обычным IntegerField [cite: 197]
    count = IntegerField() # [cite: 201]

class Ticket(BaseModel):
    """Таблица тикетов [cite: 185]"""
    uuid = CharField(max_length=36, unique=True) # [cite: 191]
    available = BooleanField(default=True) # [cite: 195]
    user = ForeignKeyField(User, backref='tickets', null=True) # Внешний ключ на юзера [cite: 199]

    @staticmethod
    def valid_ticket(ticket_uuid: str) -> bool:
        """Проверяет наличие тикета и не использовал ли его уже кто-то [cite: 120, 122]"""
        try:
            ticket = Ticket.get(Ticket.uuid == ticket_uuid)
            return ticket.available
        except Ticket.DoesNotExist:
            return False

class Order(BaseModel):
    """Таблица заказов [cite: 166]"""
    user = ForeignKeyField(User, backref='orders') # [cite: 172]
    product = ForeignKeyField(Product, backref='orders') # [cite: 176]
    count = IntegerField() # [cite: 180]
    order_datetime = DateTimeField(default=datetime.datetime.now) # [cite: 184]