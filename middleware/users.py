from utils.db import create_user, get_user
from aiogram.types import Update
from aiogram.dispatcher.middlewares import BaseMiddleware


class RegistrationUserMiddleware(BaseMiddleware):
    async def on_pre_process_update(self, update: Update, data):
        try:
            try:
                user_id = update.message.from_user.id
            except:
                user_id = update.callback_query.from_user.id
        except:
            return
        user = await get_user(user_id)
        if user is None:
            await create_user(user_id)