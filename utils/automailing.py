from loader import bot
from utils.db import get_user
from asyncio import sleep


async def start_automailing():
    users = await get_user(subscription_id=2)
    for user in users:
        await bot.send_message(user['telegram_id'], "Это авторассылка на которую вы подписались")
        await sleep(10000)