import asyncio
from data import ADMIN_IDS, WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT
from middleware import setup_middleware
from handlers import dp
from aiogram import executor
from loader import bot
from utils.db import create_tables
from utils.automailing import start_automailing


async def on_startup(dp):
    setup_middleware(dp)
    await create_tables()
    asyncio.create_task(start_automailing())
    for admin in ADMIN_IDS:
        await bot.send_message(admin, "Bot started working")
    await bot.set_webhook(WEBHOOK_URL)



if __name__ == '__main__':
    # executor.start_polling(dp, on_startup=on_startup)
    executor.start_webhook(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        webhook_path=WEBHOOK_PATH,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT
    )