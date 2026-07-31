import asyncio
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from sqlalchemy import BigInteger, String, Integer, select, desc
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Загрузка переменных окружения
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Токен не найден! Проверьте наличие файла .env")

# Настройка SQLAlchemy
engine = create_async_engine("sqlite+aiosqlite:///timers.db")
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Timer(Base):
    __tablename__ = "timers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(100))
    minutes: Mapped[int] = mapped_column(Integer)


# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Создание постоянной клавиатуры
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔄 Повторить последний")],
        [KeyboardButton(text="/timer Чайник 5"), KeyboardButton(text="/timer Духовка 15")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите или введите команду..."
)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот-напоминалка.\n"
        "Напиши команду в формате:\n"
        "/timer <Название> <минуты>\n"
        "Или воспользуйся кнопками ниже 👇",
        reply_markup=main_kb
    )


@dp.message(F.text == "🔄 Повторить последний")
async def repeat_last(message: types.Message):
    async with async_session() as session:
        # поиск последней запись пользователя (сортируем по id по убыванию)
        stmt = select(Timer).where(Timer.user_id == message.from_user.id).order_by(desc(Timer.id)).limit(1)
        result = await session.execute(stmt)
        last_timer = result.scalar_one_or_none()

    if not last_timer:
        await message.answer("🤷‍♂️ У вас еще нет сохраненных таймеров в базе.")
        return

    name = last_timer.name
    minutes = last_timer.minutes

    # Сохраняем этот повтор как новый таймер в базу
    async with async_session() as session:
        new_timer = Timer(user_id=message.from_user.id, name=name, minutes=minutes)
        session.add(new_timer)
        await session.commit()

    await message.answer(f"⏳ Повторяю! Напомню про «{name}» через {minutes} мин.")

    # Ожидание
    await asyncio.sleep(minutes * 60)

    await message.reply(f"⏰ Напоминание: {name}!")


@dp.message(Command("timer"))
async def cmd_timer(message: types.Message):
    # Разбиваем сообщение, пропуская саму команду
    args = message.text.split()[1:]

    if len(args) < 2:
        await message.answer("❌ Ошибка. Пиши так: /timer <Название> <минуты>\nПример: /timer Стирка 60")
        return

    try:
        minutes = int(args[-1])
        name = " ".join(args[:-1])
    except ValueError:
        await message.answer("❌ Время должно быть целым числом (в минутах) и стоять в конце.")
        return

    # Запись нового таймера в базу
    async with async_session() as session:
        new_timer = Timer(user_id=message.from_user.id, name=name, minutes=minutes)
        session.add(new_timer)
        await session.commit()

    await message.answer(f"⏳ Принято! Напомню про «{name}» через {minutes} мин.")

    # Ожидание
    await asyncio.sleep(minutes * 60)

    await message.reply(f"⏰ Напоминание: {name}!")


async def main():
    logging.basicConfig(level=logging.INFO)

    # Автоматическое создание таблиц базы данных при запуске
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())