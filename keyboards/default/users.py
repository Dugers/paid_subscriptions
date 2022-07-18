from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
my_profile_button = KeyboardButton("Мой профиль")
subscrations_button = KeyboardButton("Подписки")
main_menu_keyboard.add(my_profile_button, subscrations_button)