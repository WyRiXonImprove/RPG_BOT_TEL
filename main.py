import time
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import sqlite3 as sq
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from text import *


"""_____________________________Создание бд и ее функций__________________________"""
async def new_db():
    global db, cur
    db = sq.connect("new db1")
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS user_db(
                    user_id  INT,
                    class TEXT,
                    weapon TEXT);""")
    db.commit()

async def add_values_new_db(user_id):
    cur.execute(f"""SELECT user_id FROM user_db WHERE user_id = '{user_id}'""")
    if cur.fetchone() is None:
        user_info = (user_id, "", "")
        cur.execute("""INSERT INTO user_db VALUES(?, ?, ?)""", user_info)
        db.commit()
        for i in cur.execute("""SELECT * FROM user_db"""):
            print(i)

async def update_class_white_elf(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = '{white_elf}' WHERE user_id = '{user_id}'""")
    db.commit()

def prov():
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute("""SELECT * FROM user_db"""):
        print(i)

async def update_class_dark_elf(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = {"Темный эльф"} WHERE user_id = '{user_id}'""")
    db.commit()

async def update_class_knights(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = {"Рыцарь"} WHERE user_id = '{user_id}'""")
    db.commit()

"""______________________инлайн клава для выбора класса____________________________"""
inl_button_class = InlineKeyboardMarkup(row_width=3)
inl_button_white_elf = InlineKeyboardButton(text="Светлый эльф",
                                            callback_data="white_elf")
inl_button_dark_elf = InlineKeyboardButton(text="Темный эльф",
                                            callback_data="dark_elf")
inl_button_knights = InlineKeyboardButton(text="Рыцарь",
                                            callback_data="knights")
inl_button_class.add(inl_button_white_elf, inl_button_dark_elf, inl_button_knights)
"""________________________________________________________________________________"""

"""____________________инлайн клава для выбора оружия______________________________"""
inl_button_weapon = InlineKeyboardMarkup(row_width=3)
inl_button_sword = InlineKeyboardButton(text="Мечник",
                                            callback_data="sword")
inl_button_bow = InlineKeyboardButton(text="Лучник",
                                            callback_data="bow")
inl_button_skipetr = InlineKeyboardButton(text="Маг",
                                            callback_data="skipetr")
inl_button_weapon.add(inl_button_sword, inl_button_bow, inl_button_skipetr)
"""________________________________________________________________________________"""


bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def on_start_up(_):
    print("Бот запущен!")
    prov()

@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=welcome,
                           parse_mode="HTML")
    await new_db()
    await add_values_new_db(user_id=message.from_user.id)
    await message.delete()

@dp.message_handler(commands=["help"])
async def help_message(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=help,
                           parse_mode="HTML")


@dp.message_handler(commands=["game"])
async def game_start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=vibor_classa,
                           parse_mode="HTML",
                           reply_markup=inl_button_class)

@dp.message_handler(commands=["farm"])
async def farm_start(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Фарм площади составляет: <b>20 секунд!</b>",
                           parse_mode="HTML")
    time.sleep(20)
    await bot.send_message(chat_id=message.from_user.id,
                           text=XP_ADD,
                           parse_mode="HTML")



"""______________________выбор класса для пользователя_______________"""
@dp.callback_query_handler(lambda c: c.data == 'white_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await update_class_white_elf(user_id=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Светлых эльфов"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)

@dp.callback_query_handler(lambda c: c.data == 'dark_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await update_class_dark_elf(user_id=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Темных эльфов'"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)


@dp.callback_query_handler(lambda c: c.data == 'knights')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await update_class_knights(user_id=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Рыцарей"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)
"""___________________________________________________________________"""

"""____________________инлайн кнопки для выбора оружия________________"""

weapon_count = 0
@dp.callback_query_handler(lambda c: c.data == 'sword')
async def add_class_for_user(callback_query: types.CallbackQuery):
    global weapon_count
    if weapon_count == 0:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                                   text=start_farm.format("Меч"),
                                   parse_mode="HTML")
        weapon_count += 1
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'bow')
async def add_class_for_user(callback_query: types.CallbackQuery):
    global weapon_count
    if weapon_count == 0:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                                   text=start_farm.format("Лук"),
                                   parse_mode="HTML")
        weapon_count += 1
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'skipetr')
async def add_class_for_user(callback_query: types.CallbackQuery):
    global weapon_count
    if weapon_count == 0:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                                   text=start_farm.format("Магический Скипетр"),
                                   parse_mode="HTML")
        weapon_count += 1
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")

"""___________________________________________________________________"""


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start_up, skip_updates=True)