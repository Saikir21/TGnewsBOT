import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import config

# Включаем логирование, чтобы видеть ошибки в консоли
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
if not config.BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан. Проверьте файл .env или doc.env и переменные окружения")

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! "
        f"Каркас утреннего дашборда готов. Иди в зал, остальное допишем потом!"
    )

# Главная функция запуска
async def main():
    print("[СИСТЕМА] Бот успешно запущен и слушает сервер...")
    # Запускаем polling (процесс непрерывного опроса серверов Telegram)
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запуск асинхронного event loop
    asyncio.run(main())