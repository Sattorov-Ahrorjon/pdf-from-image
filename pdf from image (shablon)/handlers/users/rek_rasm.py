from aiogram import types
from loader import dp, db, bot
from data.config import ADMINS
from aiogram.utils.markdown import hlink
from states.state import Rasm_Data
from aiogram.dispatcher import FSMContext



@dp.message_handler(chat_id=ADMINS[0], commands='reklama_rasm', state=None)
async def get_photo(message:types.Message):
    await message.reply(" Rasm yuboring")
    await Rasm_Data.rasm_id.set()


@dp.message_handler(state=Rasm_Data.rasm_id, content_types=types.ContentTypes.PHOTO)
async def get_file_id(msg: types.Message, state : FSMContext):
    f_id = msg.photo[-1].file_id
    await state.update_data(
        {'id':f_id}
    )
    await msg.answer("Rasm osti matnini yuboring")
    await Rasm_Data.rasm_text.set()


@dp.message_handler(state=Rasm_Data.rasm_text)
async def get_file_text(msg:types.Message, state:FSMContext):
    msg_text = msg.text
    await state.update_data(
        {'text':msg_text}
    )
    await msg.answer(" Kanal yoki Guruh nomini kiriting")
    await Rasm_Data.rasm_channel_name.set()


@dp.message_handler(state=Rasm_Data.rasm_channel_name)
async def get_file_name(msg:types.Message, state:FSMContext):
    nomi = msg.text
    await state.update_data(
        {'name':nomi}
    )
    await msg.answer("Kanal yoki Guruh linkini kiriting")
    await Rasm_Data.rasm_channel_link.set()


@dp.message_handler(state=Rasm_Data.rasm_channel_link)
async def get_file_link(msg:types.Message, state:FSMContext):
    link = msg.text
    await state.update_data(
        {'link':link}
    )
    await msg.answer("Xabar to'liq yuklandi")
    data = await state.get_data()
    file_id = data.get('id')
    text = data.get('text')
    name = data.get('name')
    link = data.get('link')
    
    text += '\n\n' + hlink(name, link)
    
    a=0
    b=0 
    cl = db.get_id()
    for i in cl:
        try:
            await bot.send_photo(chat_id=i[0], photo=file_id, caption=text)
            a+=1
        except:
            b+=1
    await bot.send_message(chat_id=ADMINS[0], text=f"Yuborildi {a} ta Yuborilmadi {b} ta")
    await state.finish()
