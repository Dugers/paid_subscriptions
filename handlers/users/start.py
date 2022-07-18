from loader import dp
from aiogram.types import Message
from keyboards.default import main_menu_keyboard


@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("Привет, я бот для приема платежей за подписки")
    await message.answer_sticker("CAACAgEAAxkBAAEFR95i0QdrYQq0Bmz8uhDcdbGjoS58OgACDwEAAjgOghG1zE1_4hSRgikE", reply_markup=main_menu_keyboard)