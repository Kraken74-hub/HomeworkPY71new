import datetime
from typing import List, Optional
from database import Base, db_session
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    points: Mapped[int] = mapped_column(Integer, default=0)

    # Связи (Relationship)
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    tickets: Mapped[List["Ticket"]] = relationship(back_populates="user")

    @classmethod
    def is_exist(cls, username: str) -> bool:
        stmt = select(cls).where(cls.username == username)
        return db_session.scalar(stmt) is not None


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    cost: Mapped[int] = mapped_column(Integer)
    count: Mapped[int] = mapped_column(Integer)

    orders: Mapped[List["Order"]] = relationship(back_populates="product")


class Ticket(Base):
    __tablename__ = 'tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    available: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('users.id'), nullable=True)
    user: Mapped[Optional["User"]] = relationship(back_populates="tickets")

    @classmethod
    def valid_ticket(cls, ticket_uuid: str) -> bool:
        stmt = select(cls).where(cls.uuid == ticket_uuid)
        ticket = db_session.scalar(stmt)
        return ticket.available if ticket else False


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'))

    count: Mapped[int] = mapped_column(Integer)
    order_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship(back_populates="orders")