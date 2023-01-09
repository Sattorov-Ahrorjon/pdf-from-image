import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp, db, bot


@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(id=message.from_user.id, name=name)
    except sqlite3.IntegrityError as err:
        pass
    
    text = ("\nBotga Xush kelibsiz!\n",
            "Rasmlarni PDF - faylga aylantirib beraman")
    await message.answer("\n".join(text))
    
    # Adminga habar beramiz
    count = db.count_users()[0]
    msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
    await bot.send_message(chat_id=ADMINS[0], text=msg)
