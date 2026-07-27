import datetime
from peewee import Model, CharField, IntegerField, BooleanField, ForeignKeyField, DateTimeField
from database import db

class BaseModel(Model):

    class Meta:
        database = db

class User(BaseModel):

    username = CharField(max_length=30, unique=True) # [cite: 174]
    password = CharField(max_length=30) # [cite: 178]
    points = IntegerField(default=0) # [cite: 182]

    @staticmethod
    def is_exist(username: str) -> bool:

        try:
            User.get(User.username == username) # [cite: 45]
            return True # [cite: 49]
        except User.DoesNotExist: # [cite: 46]
            return False # [cite: 48]

    def orders(self) -> list:

        return list(Order.select().where(Order.user == self))

class Product(BaseModel):

    name = CharField(max_length=255) # [cite: 193]
    cost = IntegerField()
    count = IntegerField()

class Ticket(BaseModel):

    uuid = CharField(max_length=36, unique=True)
    available = BooleanField(default=True)
    user = ForeignKeyField(User, backref='tickets', null=True)

    @staticmethod
    def valid_ticket(ticket_uuid: str) -> bool:

        try:
            ticket = Ticket.get(Ticket.uuid == ticket_uuid)
            return ticket.available
        except Ticket.DoesNotExist:
            return False

class Order(BaseModel):

    user = ForeignKeyField(User, backref='orders') # [cite: 172]
    product = ForeignKeyField(Product, backref='orders') # [cite: 176]
    count = IntegerField() # [cite: 180]
    order_datetime = DateTimeField(default=datetime.datetime.now) # [cite: 184]