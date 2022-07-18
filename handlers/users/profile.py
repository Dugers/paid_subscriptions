from loader import dp, bot
from data import PROVIDER_TOKEN
from states import UserAddBalanceState
from utils.db import get_user, update_user, get_subscriptions
from keyboards.inline import profile_keyboard, cancel_keyboard
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from aiogram.types.message import ContentTypes
from aiogram.dispatcher import FSMContext


@dp.message_handler(lambda message: message.text.lower() == "мой профиль")
async def user_profile(message: Message, telegram_id=False):
    if telegram_id:
        user_info = await get_user(telegram_id)
    else:
        user_info = await get_user(message.from_user.id)
    if user_info['subscriptions_ids'] is None:
        text_subscriptions = "У вас нету активных подписок"
    else:
        text_subscriptions = "Название | Тип"
        for subscription in user_info['subscriptions_ids']:
            subscription = await get_subscriptions(subscription_id=subscription)
            subscription_type = "Рассылка в канале"
            if subscription['type'] == "bot":
                subscription_type = "Рассылка в боте"
            text_subscriptions += f"\n{subscription['name']} | {subscription_type}"
    await message.answer(f"Ваш баланс: {user_info['balance']}\nВаши подписки:\n\n\n{text_subscriptions}", reply_markup=profile_keyboard)


@dp.callback_query_handler(text="cancel", state=UserAddBalanceState.need_add)
async def user_cancel_add_balance(callback: CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.message.delete()
    await user_profile(callback.message, telegram_id=callback.from_user.id)


@dp.callback_query_handler(text="add_balance")
async def user_add_balance_set(callback: CallbackQuery):
    await callback.message.delete()
    await UserAddBalanceState.need_add.set()
    await callback.message.answer("Введите сумму", reply_markup=cancel_keyboard())


@dp.message_handler(lambda message: message.text.isdigit() and int(message.text) >= 60 and int(message.text) <= 1000, state=UserAddBalanceState.need_add)
async def user_add_balance(message: Message, state: FSMContext):
    await message.answer("Используйте тестовые данные\nНомер карты: 1111 1111 1111 1026\nДействует до: 12/22\nCVC: 000")
    await bot.send_invoice(message.from_user.id, title="Пополнение", description=f"Пополнение баланса на {message.text} рублей", payload="add_balance", provider_token=PROVIDER_TOKEN, currency="RUB", start_parameter="replenishment", prices=[{'label': 'руб', 'amount': int(message.text)*100}])
    await state.finish()

@dp.message_handler(state=UserAddBalanceState.need_add)
async def user_add_balance_invalide(message: Message, state: FSMContext):
    await message.answer("Сумма для пополнения введена неверно\nВозможные причины:\nСумма не является числом\nСумма является больше 1000\nСумма является меньше 60", reply_markup=cancel_keyboard())


@dp.pre_checkout_query_handler()
async def checkout(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: Message):
    try:
        payment_sum = int(message.successful_payment.total_amount/100)
    except:
        return
    await update_user(telegram_id=message.from_user.id, balance=payment_sum)
    await message.answer(f"Баланс успешно пополнен на {payment_sum}")
    await user_profile(message)