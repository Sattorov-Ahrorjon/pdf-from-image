from aiogram import Bot, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
import asyncio, img2pdf, shutil, sqlite3, os



################################################################

TOKEN = 'TOKEN'
ADMINS='MAIN_ADMIN_ID','SECOND_ADMIN_ID'

########################################################################################



class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db
    
    
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)
    
    def execute(self, sql: str, parameters: tuple = None, fetchone = False, fetchall = False, commit = False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        
        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data
    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            Name VARCHAR(255) NOT NULL,
            email VARCHAR(255),
            PRIMARY KEY (id)
            );
    """
        self.execute(sql, commit=True)
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
    
    def add_user(self, id: int, name: str, email: str = None):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        
        sql = "INSERT INTO Users(id, Name, email) VALUES(?, ?, ?)"
        self.execute(sql, parameters=(id, name, email), commit=True)
    
    def select_all_users(self):
        sql = """
        SELECT * FROM Users;
        """
        return self.execute(sql, fetchall=True)
    
    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.formar_args(sql, kwargs)
        
        return self.execute(sql, parameters=parameters, fetchone=True)
    
    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)
    
    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"
        
        sql = f"""
        UPDATE Users SET email=? WHERE id=?
        """
        
        return self.execute(sql, parameters=(email, id), commit=True)
    
    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)
    
    
    def get_id(self):
        sql = """
        SELECT id FROM Users;
        """
        return self.execute(sql, fetchall=True)
    

def logger(statement):
    print(f"""
----------------------------------------------------
Executing:
{statement}
----------------------------------------------------
""")

##############################

class Send_pdf(StatesGroup):
    create = State()
    name = State()
    file_name = State()
    send_pdf = State()


################################################


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Nomini yozaman"),
            KeyboardButton(text="Kerak emas"),
        ],
    ],
    resize_keyboard=True
)

#########################################################################################


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database(path_to_db="main.db")


##############################################################################

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
        await asyncio.sleep(1)


# # Foydalanuvchilar soni
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

########################################################################################


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



##################################################################################################################################




@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=None)
async def get_file_id(message: types.Message, state: FSMContext):
    
    await asyncio.sleep(1)
    user_id = message.from_user.id
    try:
        os.mkdir(f'{user_id}/')
    except:
        pass
    
    # await message.answer("✔️")
    
    
    file_info = await bot.get_file(message.photo[-1].file_id)
    name = f'{user_id}/'+file_info.file_path.split('photos/')[1]
    await message.photo[-1].download(name)
    

    try:
        with open(f'{user_id}/{user_id}.txt', 'a') as file:
            file.write(name+'\n')
    except:
        pass
    
    await state.update_data(
        {'id':user_id}
    )
    
    
    await message.reply('✔️✔️✔️', reply_markup=menu)



@dp.message_handler(text='Nomini yozaman', state=None)
async def update_name(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer("Qanday nom ❓", reply_markup=types.ReplyKeyboardRemove())
    await Send_pdf.send_pdf.set()



@dp.message_handler(text="Kerak emas", state=None)
async def set_name(message: types.Message, state: FSMContext):
    very = await message.answer(text='😉', reply_markup=types.ReplyKeyboardRemove())
    await message.delete()
    await asyncio.sleep(3)
    await very.delete()
    page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
    layout = img2pdf.get_layout_fun(page_size)
    
    items = list()
    data = await state.get_data()
    user_id = data.get('id')
    
    try:
        file = open(f'{user_id}/{user_id}.txt', 'r')
        
        for i in file:
            items.append(i.replace('\n', ''))
        file.close()
        
        pdf = img2pdf.convert(items, layout_fun=layout)
        with open(f'{user_id}/{user_id}.pdf', 'wb') as f:
            f.write(pdf)
        
        doc = open(f'{user_id}/{user_id}' + '.pdf', 'rb')
        await bot.send_document(user_id, doc)
    except:
        pass
    try:
        shutil.rmtree(f'{user_id}/')
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
        file = open(f'{user_id}/{user_id}.txt', 'r')
        
        for i in file:
            items.append(i.replace('\n', ''))
        file.close()
        
        pdf = img2pdf.convert(items, layout_fun=layout)
        with open(f'{user_id}/{user_id}.pdf', 'wb') as f:
            f.write(pdf)
        
        if len(message.text) >= 3:
            os.renames(f'{user_id}/{user_id}.pdf', f'{user_id}/{message.text}.pdf')
        doc = open(f'{user_id}/{message.text}' + '.pdf', 'rb')
        await bot.send_document(user_id, doc)
    except:
        pass
    
    
    try:
        shutil.rmtree(f'{user_id}/')
    except:
        pass
    await state.finish()


############################################################################################################################


# Bot kamandalari
async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni qayta ishga tushurish"),
            types.BotCommand("help", "Yordam"),
        ]
    )



async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    
    # Malumotlar bazasini yaratish:
    try:
        db.create_table_users()
    except Exception as err:
        # print(err)
        pass



if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
