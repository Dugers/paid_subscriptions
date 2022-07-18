from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


profile_keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Пополнить баланс", callback_data="add_balance"))

def cancel_keyboard(text="Вернуться обратно", callback_data="cancel", button=False):
    cancel_button = InlineKeyboardButton(text=text, callback_data=callback_data)
    if button:
        return cancel_button
    return InlineKeyboardMarkup().add(cancel_button)


def subscriptions_keyboard(subscriptions):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for subscription in subscriptions:
        keyboard.add(InlineKeyboardButton(text=subscription['name'], callback_data=f"buy_subscription_{subscription['id']}"))
    return keyboard