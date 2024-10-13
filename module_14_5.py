from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

initiate_db()

api = "7833663712:AAFr6YylIeIL8j5yh44CRcnnrA7rXjkW8HU"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup(resize_keyboard=True)
KeyboardButton1 = KeyboardButton(text="Рассчитать")
KeyboardButton2 = KeyboardButton(text="Информация")
KeyboardButton3 = KeyboardButton(text="Купить")
KeyboardButton4 = KeyboardButton(text="Регистрация")
kb.row(KeyboardButton1, KeyboardButton2)
kb.add(KeyboardButton3)
kb.add(KeyboardButton4)


catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ]
)

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State('1000')

@dp.message_handler(text = 'Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    if 110 >= int(message.text) >= 0:
        await state.update_data(age=message.text)
        data = await state.get_data()
        add_user(data['username'], data['email'], data['age'])
        await message.answer('Регистрация прошла успешно')
        await state.finish()
    else:
        await message.answer("Укажите возраст от 0 до 110")
        await RegistrationState.age.set()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


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


# old
InlineKeyboardMarkup = InlineKeyboardMarkup()
InlineKeyboardButton1 = KeyboardButton('Рассчитать норму калорий', callback_data='calories')
InlineKeyboardButton2 = KeyboardButton('Формулы расчёта', callback_data='formulas')
InlineKeyboardMarkup.add(InlineKeyboardButton1, InlineKeyboardButton2)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=InlineKeyboardMarkup)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(f"для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;"
                              f"для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    await message.answer(f"Ваша норма калорий: "
                         f"{10 * int(data['third']) + 6.25 * int(data['second'])- 5 * int(data['first']) + 5}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)