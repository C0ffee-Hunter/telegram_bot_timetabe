from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import TOKEN
from parser import get_group_table
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pathlib import Path
import os.path
import sqlite3


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Близжайшее занятие группы"),
            types.KeyboardButton(text="Занятие группы в определенный день недели"),
            types.KeyboardButton(text="Расписание группы на следующий день"),
            types.KeyboardButton(text="Расписание группы на всю неделю")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        input_field_placeholder="Выбери одну из интересующих тебя кнопок и вперед!!!"
    )
    await message.answer("Привет!\nЗдесь ты можешь узнать расписание групп ЛЭТИ", reply_markup=keyboard)


@dp.message_handler(
    lambda message: message.text == "Близжайшее занятие группы" or message.text == "Расписание группы на следующий день" or message.text == "Расписание группы на всю неделю")
async def choice(message: types.Message, state: FSMContext):
    user_choice = 0
    if message.text == "Близжайшее занятие группы":
        user_choice = 1
    elif message.text == "Расписание группы на следующий день":
        user_choice = 3
    elif message.text == "Расписание группы на всю неделю":
        user_choice = 4
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = None
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler(lambda message: message.text == "Занятие группы в определенный день недели")
async def day_choice(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Понедельник"),
            types.KeyboardButton(text="Вторник"),
            types.KeyboardButton(text="Среда"),
            types.KeyboardButton(text="Четверг"),
            types.KeyboardButton(text="Пятница"),
            types.KeyboardButton(text="Суббота")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        one_time_keyboard=True,
        input_field_placeholder="Выбери одну из интересующих тебя кнопок и вперед!!!"
    )
    await message.answer("Выбери день недели!!!", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Понедельник")
async def monday(message: types.Message, state: FSMContext):
    day = "MON"
    user_choice = 2
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = day
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler(lambda message: message.text == "Вторник")
async def tuesday(message: types.Message, state: FSMContext):
    day = "TUE"
    user_choice = 2
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = day
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler(lambda message: message.text == "Среда")
async def wednesday(message: types.Message, state: FSMContext):
    day = "WEN"
    user_choice = 2
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = day
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler(lambda message: message.text == "Четверг")
async def thursday(message: types.Message, state: FSMContext):
    day = "THU"
    user_choice = 2
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = day
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler(lambda message: message.text == "Пятница")
async def friday(message: types.Message, state: FSMContext):
    day = "FRI"
    user_choice = 2
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = day
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler(lambda message: message.text == "Суббота")
async def saturday(message: types.Message, state: FSMContext):
    day = "SAT"
    user_choice = 2
    async with state.proxy() as data:
        data['choice'] = user_choice
        data['day'] = day
    await message.answer("Отлично! Теперь введи номер группы!")


@dp.message_handler()
async def group_choice(message: types.Message, state: FSMContext):
    group_number = message.text
    async with state.proxy() as data:
        user_choice = data['choice']
        day = data['day']
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username

    with sqlite3.connect("etu_table.db") as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO test(user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                       (us_id, us_name, us_sname, username))
        db.commit()

    if user_choice == 4:
        day = ''
        for week_day in range(1, 7):
            if week_day == 1:
                day = "MON"
                answer = "Понедельник\n" + get_group_table(group_number, user_choice, day)
                await message.answer(answer)
            elif week_day == 2:
                day = "TUE"
                answer = "Вторник\n" + get_group_table(group_number, user_choice, day)
                await message.answer(answer)
            elif week_day == 3:
                day = "WED"
                answer = "Среда\n" + get_group_table(group_number, user_choice, day)
                await message.answer(answer)
            elif week_day == 4:
                day = "THU"
                answer = "Четверг\n" + get_group_table(group_number, user_choice, day)
                await message.answer(answer)
            elif week_day == 5:
                day = "FRI"
                answer = "Пятница\n" + get_group_table(group_number, user_choice, day)
                await message.answer(answer)
            elif week_day == 6:
                day = "SAT"
                answer = "Суббота\n" + get_group_table(group_number, user_choice, day)
                await message.answer(answer)
    else:
        answer = get_group_table(group_number, user_choice, day)
        await message.answer(answer)


if __name__ == '__main__':
    executor.start_polling(dp)
