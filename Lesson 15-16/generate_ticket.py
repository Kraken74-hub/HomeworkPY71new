import uuid
from database import db
from models import Ticket


db.connect()


new_uuid = str(uuid.uuid4())

Ticket.create(uuid=new_uuid, available=True)

print(f"Новый тикет успешно создан и добавлен в базу данных!")
print(f"Скопируй этот UUID: {new_uuid}")

db.close()