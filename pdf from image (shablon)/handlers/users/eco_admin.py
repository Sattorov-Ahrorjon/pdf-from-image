from aiogram import types
from data.config import ADMINS

from loader import dp, bot


# Echo bot
@dp.message_handler(state=None, chat_id=ADMINS[0])
async def bot_echo(message: types.Message):
    await message.answer(message.text)
