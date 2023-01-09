from aiogram import types
from loader import dp, db, bot
from aiogram.dispatcher.filters import Text
from data.config import ADMINS
import time




dp.message_handler(commands='admin', chat_id=ADMINS[0], state=None)
async def get_count(msg: types.Message):
    text = "/users - foydalanuvchilar\n"
    text += "/count - soni\n"
    text += "/online - foydalanuvchilar haqida\n"
    
    await bot.send_message(chat_id=ADMINS[0], text=text)



# # Foydalanuvchilar haqida 
@dp.message_handler(commands='users', chat_id=ADMINS[0], state=None)
async def get_people(msg: types.Message):
    for i in db.select_all_users():
        await bot.send_message(chat_id=ADMINS[0], text=i)
        time.sleep(1)


# # FOydalanuvchilar soni
@dp.message_handler(commands='count', chat_id=ADMINS[0], state=None)
async def get_count(msg: types.Message):
    await bot.send_message(chat_id=ADMINS[0], text=db.count_users()[0])


# # Biror foydalanuvchiga yozish
@dp.message_handler(Text(startswith='write'), state=None)
async def get_write(msg: types.Message):
    try:
        await bot.send_message(chat_id=int(msg.text[5:15]), text=msg.text[15:])
    except:
        pass


# # Online va Block holdagi foydalanuvchilar
@dp.message_handler(commands='online', chat_id=ADMINS[0], state=None)
async def get_reklama(msg: types.Message):
    users_id = db.get_id()
    online=0
    block=0
    for i in users_id:
        try:
            await bot.send_message(chat_id=i[0], text="Assalomu alaykum\nBu bot bilan ba'zi muammolar o'z yechimini topgan bo'lsa hursandmiz !")
            online+=1
        except Exception as err:
            block+=1
            pass
    await msg.reply(f"Online - {online}, Block - {block}")