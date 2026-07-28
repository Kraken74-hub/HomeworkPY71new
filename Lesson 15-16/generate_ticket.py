import uuid
from database import SessionLocal
from models import Ticket

with SessionLocal() as db:
    new_uuid = str(uuid.uuid4())

    new_ticket = Ticket(uuid=new_uuid, available=True)

    db.add(new_ticket)
    db.commit()

    print(f"Новый тикет успешно создан и добавлен в базу данных!")
    print(f"Скопируй этот UUID: {new_uuid}")