import asyncio
import logging

# FIX: понятная ошибка, если зависимости не установлены
try:
    import aiohttp
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import CommandStart
except ModuleNotFoundError as exc:
    raise SystemExit(
        f"Не установлена зависимость: {exc.name}. "
        f"Установите её командой: pip install -r requirements.txt"
    ) from exc

import config

logging.basicConfig(level=logging.INFO)

# FIX: проверяем наличие токена бота до запуска polling
if not config.BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан. Проверьте файл .env или doc.env")

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


# FIX: функция погоды теперь не падает, если WEATHER_TOKEN отсутствует
async def get_weather():
    if not config.WEATHER_TOKEN:
        return "⚠️ Токен OpenWeather не настроен. Погода не будет показана."

    url = f"https://api.openweathermap.org/data/2.5/weather?q=Moscow&appid={config.WEATHER_TOKEN}&units=metric&lang=ru"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    temp = data["main"]["temp"]
                    desc = data["weather"][0]["description"]
                    humidity = data["main"]["humidity"]
                    return f"🌡 Температура: {temp}°C\n☁️ За окном: {desc}\n💧 Влажность: {humidity}%"
                return "⚠️ Не удалось получить данные о погоде (ошибка API)."
    except Exception as exc:
        return f"⚠️ Ошибка при подключении к сервису погоды: {exc}"


# FIX: безопасное имя пользователя, если full_name отсутствует
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_name = message.from_user.full_name or message.from_user.username or "друг" # type: ignore
    await message.answer(f"Привет, {user_name}! Собираю утреннюю сводку...")

    weather_report = await get_weather()

    await message.answer(
        f"📋 **Сводка на сегодня:**\n\n"
        f"{weather_report}\n\n"
        f"🤖 Каркас работает. Можешь собираться в зал, дождь скоро закончится!"
    )


async def main():
    print("[СИСТЕМА] Бот успешно запущен и слушает сервер...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())