
import wikipedia
from aiogram import types
from loader import dp
from states.state import Wikipedia
from aiogram.dispatcher import FSMContext
wikipedia.set_lang('uz')


@dp.message_handler(commands=['wikipedia'], state=None)
async def wki_command(message: types.Message):
    await message.reply("🌐Sizga qanday malumot kerak")
    await Wikipedia.wiki_text.set()


@dp.message_handler(state=Wikipedia.wiki_text)
async def sendWiki(message: types.Message, state: FSMContext):
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("Bu mavzuga oid maqola topilmadi")
    await state.finish()
