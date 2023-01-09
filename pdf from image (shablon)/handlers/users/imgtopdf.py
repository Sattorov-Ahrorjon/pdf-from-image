
from aiogram import types
from loader import dp, bot
from states.state import Send_pdf
from aiogram.dispatcher import FSMContext
import img2pdf
import os, shutil, asyncio
from keyboards.default.menu import menu



@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=None)
async def get_file_id(message: types.Message, state: FSMContext):
    
    user_id = message.from_user.id
    try:
        os.mkdir(f'handlers/users/{user_id}/')
    except:
        pass
    
    file_info = await bot.get_file(message.photo[-1].file_id)
    name = f'handlers/users/{user_id}/'+file_info.file_path.split('photos/')[1]
    await message.photo[-1].download(name)
    

    try:
        with open(f'handlers/users/{user_id}/{user_id}.txt', 'a') as file:
            file.write(name+'\n')
    except:
        pass
    
    await state.update_data(
        {'id':user_id}
    )
    await message.reply('✅✅', reply_markup=menu)
    # await Send_pdf.file_name.set()



# @dp.message_handler(state=Send_pdf.name)
# async def ask_name(message: types.Message, state:FSMContext):
#     await message.answer('Nom kiritasizmi📝', reply_markup=menu)
#     await Send_pdf.file_name.set()
    


@dp.message_handler(text='Nomini yozaman', state=None)
async def update_name(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer("Qanday nom ❓", reply_markup=types.ReplyKeyboardRemove())
    await Send_pdf.send_pdf.set()



@dp.message_handler(text="Kerak emas", state=None)
async def set_name(message: types.Message, state: FSMContext):
    very = await message.answer(text='👌', reply_markup=types.ReplyKeyboardRemove())
    await message.delete()
    await asyncio.sleep(2)
    await very.delete()
    page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
    layout = img2pdf.get_layout_fun(page_size)
    
    items = list()
    data = await state.get_data()
    user_id = data.get('id')
    
    try:
        file = open(f'handlers/users/{user_id}/{user_id}.txt', 'r')
        
        for i in file:
            items.append(i.replace('\n', ''))
        file.close()
        
        pdf = img2pdf.convert(items, layout_fun=layout)
        with open(f'handlers/users/{user_id}/{user_id}.pdf', 'wb') as f:
            f.write(pdf)
        
        doc = open(f'handlers/users/{user_id}/{user_id}' + '.pdf', 'rb')
        await bot.send_document(user_id, doc)
    except:
        pass
    try:
        shutil.rmtree(f'handlers/users/{user_id}/')
    except:
        pass
    await state.finish()



@dp.message_handler(state=Send_pdf.send_pdf, content_types = types.ContentType.TEXT)
async def send_pdf(message:types.Message, state: FSMContext):
    
    page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
    layout = img2pdf.get_layout_fun(page_size)
    
    items = list()
    data = await state.get_data()
    user_id = data.get('id')
    
    try:
        file = open(f'handlers/users/{user_id}/{user_id}.txt', 'r')
        
        for i in file:
            items.append(i.replace('\n', ''))
        file.close()
        
        pdf = img2pdf.convert(items, layout_fun=layout)
        with open(f'handlers/users/{user_id}/{user_id}.pdf', 'wb') as f:
            f.write(pdf)
        
        if len(message.text) >= 3:
            os.renames(f'handlers/users/{user_id}/{user_id}.pdf', f'handlers/users/{user_id}/{message.text}.pdf')
        doc = open(f'handlers/users/{user_id}/{message.text}' + '.pdf', 'rb')
        await bot.send_document(user_id, doc)
    except:
        pass
    
    
    try:
        shutil.rmtree(f'handlers/users/{user_id}/')
    except:
        pass
    await state.finish()
