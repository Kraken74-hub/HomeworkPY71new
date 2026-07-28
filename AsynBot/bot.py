import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

TOKEN = "8899078001:AAE-xTxPTXP4nbBqJl6Tt6DCtBuBpUuO6SY"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот-напоминалка.\n"
        "Напиши команду в формате:\n"
        "/timer <секунды> <текст>\n"
        "Например: /timer 10 Проверить чайник"
    )


@dp.message(Command("timer"))
async def cmd_timer(message: types.Message):
    # Разбиваем сообщение на 3 части: /timer, время, текст
    parts = message.text.split(maxsplit=2)

    if len(parts) < 3:
        await message.answer("❌ Ошибка. Пиши так: /timer 10 Текст напоминания")
        return

    try:
        # Пытаемся превратить второе слово в число
        seconds = int(parts[1])
        text = parts[2]
    except ValueError:
        await message.answer("❌ Время должно быть числом (в секундах).")
        return

    await message.answer(f"⏳ Принято! Напомню через {seconds} сек.")


    await asyncio.sleep(seconds)

    # Время вышло - отправляем ответ на исходное сообщение
    await message.reply(f"⏰ Напоминание: {text}")


async def main():
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())