# -*- coding: utf-8 -*-
# module_14_4.py
# План написания админ панели
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from crud_functions import get_all_products as g_a_p

api = "АБВГД"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Инициализируем "ОБЫЧНУЮ" клавиатуру, которая подстраивается под размеры интерфейса устройства
# Кнопки на клавиатуре, в 2 ряда
kb_start = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Рассчитать'),
        KeyboardButton(text='Информация'),
    ],
    [KeyboardButton(text='Купить')]
], resize_keyboard=True)
# Инициализируем "INLINE" клавиатуру, которая подстраивается под размеры интерфейса устройства
kb_formulas = InlineKeyboardMarkup()
# Кнопки на клавиатуре, в один ряд
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_formulas.row(button4, button5)

# Инициализируем "INLINE" клавиатуру, которая подстраивается под размеры интерфейса устройства
kb_products = InlineKeyboardMarkup()
# Кнопки на клавиатуре, в один ряд
button6 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
button9 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
kb_products.row(button6, button7, button8, button9)


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Ну что ж, пожалуй приступим!', reply_markup=kb_start)  # Показать клавиатуру


# ------------------------------------------
@dp.message_handler(text=['Информация'])
async def information(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.')


@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer('Выберите опцию:', reply_markup=kb_formulas)  # Показать клавиатуру "kb2"


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    messages01_04 = g_a_p()  # Список сообщений: "get_all_products()"
    # Выводим в боте
    with open("images/img01.jpg", "rb") as img1:
        await message.answer_photo(img1, messages01_04[0])  # Показать Товар1
    with open("images/img02.jpg", "rb") as img2:
        await message.answer_photo(img2, messages01_04[1])  # Показать Товар2
    with open("images/img03.jpg", "rb") as img3:
        await message.answer_photo(img3, messages01_04[2])  # Показать Товар3
    with open("images/img04.jpg", "rb") as img4:
        await message.answer_photo(img4, messages01_04[3])  # Показать Товар4
    await message.answer('Выберите продукт для покупки', reply_markup=kb_products)  # Показать клавиатуру "kb_products"


# ------------------------------------------
# Покупка товара
@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer(f'Вы успешно приобрели продукт')
    await call.answer()


# ------------------------------------------
# Обработчик callback-запроса с callback_data 'formulas'
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):   # : types.CallbackQuery
    await call.message.answer('Формула Миффлина-Сан Жеора')
    await call.message.answer("Для мужчины: \n10 * weight + 6.25 * growth - 5 * age + 5")
    await call.message.answer("Для женщины: \n10 * weight + 6.25 * growth - 5 * age - 161")
    await call.answer(text='abcd')  # Завершение вызова


# Обработчик callback-запроса с callback_data 'calories'
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer(text='abcd')  # Завершение вызова
    await UserState.age.set()


# ------------------------------------------

# Обработчик машины состояний: UserState.age
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age1=message.text)
    data = await state.get_data()
    await message.answer(f"Получено: ваш возраст = {data['age1']}")
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


# Обработчик машины состояний: UserState.growth
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth1=message.text)
    data = await state.get_data()
    await message.answer(f"Получено: ваш рост = {data['growth1']}")
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


# Обработчик машины состояний: UserState.weight
# И собственно расчёт по формуле Миффлина-Сан Жеора
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight1=message.text)
    data = await state.get_data()
    await message.answer(f"Получено: ваш вес = {data['weight1']} ")
    # Расчёт калорий по формуле Миффлина-Сан Жеора
    w1 = float(data['weight1'])  # Вес
    g1 = float(data['growth1'])  # Рост
    a1 = float(data['age1'])  # Возраст
    calories_male = 10 * w1 + 6.25 * g1 - 5 * a1 + 5
    calories_female = 10 * w1 + 6.25 * g1 - 5 * a1 - 161
    # Выдаём результат вычислений
    await message.answer(f"Расчёт калорий для оптимального похудения или сохранения нормального веса")
    await message.answer(f"по формуле Нефелина-Сан Жеора")
    await message.answer(f"Для мужчины: \n10 * {w1} + 6.25 * {g1} - 5 * {a1} + 5 = {calories_male}")
    await message.answer(f"Для женщины: \n10 * {w1} + 6.25 * {g1} - 5 * {a1} - 161 = {calories_female}")
    await message.answer(
        "В принципе, это всё, что вам нужно знать, — \nДля оптимального похудения или сохранения нормального веса")
    await state.finish()


@dp.message_handler()  # Прочие неопознанные сообщения от человека
async def all_message(message):
    await message.answer(message.text)  # Отправим человеку его же сообщение обратно
    await message.answer("Введите команду /start чтобы начать общение")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
