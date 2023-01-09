from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Nomini yozaman"),
            KeyboardButton(text="Kerak emas"),
        ],
    ],
    resize_keyboard=True
)