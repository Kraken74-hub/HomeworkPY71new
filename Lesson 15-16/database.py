from peewee import SqliteDatabase

# Создаем соединение с базой данных SQLite
# База данных будет создана в текущей папке при первом запуске
db = SqliteDatabase('not_shop.db')