
from aiogram.dispatcher.filters.state import StatesGroup, State


class Wikipedia(StatesGroup):
    wiki_text = State()


class Rasm_Data(StatesGroup):
    rasm_id = State()
    rasm_text = State()
    rasm_channel_name = State()
    rasm_channel_link = State()


class Send_pdf(StatesGroup):
    create = State()
    name = State()
    file_name = State()
    send_pdf = State()
