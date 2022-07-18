from loader import dp
from utils.db import get_subscriptions, get_user, update_user
from keyboards.inline import subscriptions_keyboard
from aiogram.types import Message, CallbackQuery


@dp.message_handler(lambda message: message.text.lower() == "подписки")
async def subscriptions_list(message: Message, telegram_id=None):
    if telegram_id:
        user = await get_user(telegram_id)
    else:
        user = await get_user(message.from_user.id)
    user_subscriptions_ids = user['subscriptions_ids']
    subscriptions = await get_subscriptions(user_subscriptions_ids)
    if len(subscriptions) == 0:
        text = "Пока нету подписок доступных для покупки"
        keyboard = None
    else:
        text = "Название | Тип | Цена"
        for subscription in subscriptions:
            subscription_type = "Рассылка в канале"
            if subscription['type'] == "bot":
                subscription_type = "Рассылка в боте"
            text += f"\n{subscription['name']} | {subscription_type} | {subscription['price']}"
        text += "\nДля покупки нажмите на кнопку с названием подписки"
        keyboard = subscriptions_keyboard(subscriptions)

    await message.answer(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data.startswith('buy_subscription'))
async def subscription_buy(callback: CallbackQuery):
    await callback.message.delete()
    user = await get_user(telegram_id=callback.from_user.id)
    if (not (user['subscriptions_ids'] is None)) and (int(callback.data.replace("buy_subscription_", "")) in user['subscriptions_ids']):
        await callback.message.answer("У вас уже есть эта подписка")
        await subscriptions_list(callback.message, telegram_id=callback.from_user.id)
        return
    subscription = await get_subscriptions(subscription_id=int(callback.data.replace("buy_subscription_", "")))
    if subscription['price'] > user['balance']:
        await callback.message.answer("Недостаточно средств для покупки подписки")
        return
    await update_user(callback.from_user.id, balance=-1*subscription['price'], subscription_id=int(callback.data.replace("buy_subscription_","")))
    await callback.message.answer("Подписка успешно куплена")
    if not (subscription['invite_link'] is None):
        await callback.message.answer(f"Ссылка для вступления {subscription['invite_link']}")
    else:
        await callback.message.answer("Ожидайте авторассылку от бота")