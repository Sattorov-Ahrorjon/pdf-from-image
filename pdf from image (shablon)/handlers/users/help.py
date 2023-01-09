from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state=None)
async def bot_help(message: types.Message):
    text = (
            "Rasmlarni PDF - faylga aylantirib beraman")
    
    await message.answer("\n".join(text))
