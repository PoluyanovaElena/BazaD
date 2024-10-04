from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *
from admin import *

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
KeyboardButton1 = KeyboardButton(text="Рассчитать")
KeyboardButton2 = KeyboardButton(text="Информация")
KeyboardButton3 = KeyboardButton(text="Купить")
kb.row(KeyboardButton1, KeyboardButton2)
kb.add(KeyboardButton3)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет", reply_markup=kb)


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ]
)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    await message.answer(f"Выберите продукт для покупки:", reply_markup=catalog_kb)
    for item in get_all_products():
        await message.answer(f"Название: {item[1]} | Описание: {item[2]} | Цена: {item[3]}")
        with open(f'files/{item[0]}.jpeg', 'rb') as photo:
            await message.answer_photo(photo)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(f"Вы успешно приобрели продукт!")
    # await call.answer


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)