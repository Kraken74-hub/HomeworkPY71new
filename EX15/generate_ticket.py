import uuid
from database import db
from models import Ticket

# Подключаемся к базе
db.connect()

# Генерируем случайный UUID
new_uuid = str(uuid.uuid4()) # Пример: ebb94499-05c9-494f-9f4a-402c6543f244

# Записываем его в базу данных как доступный (available=True)
Ticket.create(uuid=new_uuid, available=True)

print(f"✅ Новый тикет успешно создан и добавлен в базу данных!")
print(f"Скопируй этот UUID: {new_uuid}")

db.close()