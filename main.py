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

#функция проверки бд
def prov():
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute("""SELECT * FROM user_db"""):
        print(i)

"""_____________________________________апдейт классов_________________________________"""
async def update_class_white_elf(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = '{white_elf}' WHERE user_id = '{user_id}'""")
    db.commit()

async def update_class_dark_elf(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = {dark_elf} WHERE user_id = '{user_id}'""")
    db.commit()

async def update_class_knights(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = {knights} WHERE user_id = '{user_id}'""")
    db.commit()

"""________________________________________________________________________________"""
"""______________________________________апдейт оружий_____________________________"""

async def update_weapon_sword(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET weapon = '{sword}' WHERE user_id = '{user_id}'""")
    db.commit()

async def update_weapon_bow(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET weapon = {bow} WHERE user_id = '{user_id}'""")
    db.commit()

async def update_weapon_skipetr(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET weapon = {skipetr} WHERE user_id = '{user_id}'""")
    db.commit()




"""________________________________________________________________________________"""

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


"""_______________________________________клава ___________________________________"""
b_help = KeyboardButton('/help')
b_game = KeyboardButton('/game')
b_buy = KeyboardButton('/buy')
b_farm = KeyboardButton('/farm')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(b_help).insert(b_game).add(b_buy).insert(b_farm)
"""________________________________________________________________________________"""


bot = Bot(TOKEN)
dp = Dispatcher(bot)

async def on_start_up(_):
    print("Бот запущен!")


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=welcome,
                           parse_mode="HTML",
                           reply_markup=kb)
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
    upload_message = await bot.send_message(chat_id=message.chat.id, text="Начинаем загрузку...")
    await asyncio.sleep(1)
    sym = '▌'
    x = 10
    d = []
    for i in range(10):
        d.append(sym * 1)
        x += 10
        await upload_message.edit_text(text=''.join(d) + f"{i * 10 + 10}%")
        await asyncio.sleep(0.2)  # задаём время задежрки
    await asyncio.sleep(0.2)
    await upload_message.edit_text(text='<b>Успешно!</b>', parse_mode="HTML")
    await asyncio.sleep(0.5)# ждём
    await upload_message.delete()#удаляем сообщение

    await bot.send_message(chat_id=message.from_user.id,
                           text=vibor_classa,
                           parse_mode="HTML",
                           reply_markup=inl_button_class)

@dp.message_handler(commands=["farm"])
async def farm_start(message: types.Message):
    upload_message = await bot.send_message(chat_id=message.chat.id, text="Начинаем телепортацию🌍....")
    await asyncio.sleep(1)
    sym = '▌'
    x = 10
    d = []
    for i in range(10):
        d.append(sym * 1)
        x += 10
        await upload_message.edit_text(text=''.join(d) + f"{i * 10 + 10}%")
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.2)
    await upload_message.edit_text(text='<b>Телепортировано</b>', parse_mode="HTML")
    await asyncio.sleep(0.5)
    await upload_message.delete()

    upload_message = await bot.send_message(chat_id=message.chat.id,
                                            text="Фарм площади составляет: <b>20 секунд!</b>",
                                            parse_mode="HTML")
    await asyncio.sleep(1)
    sym = '▌'
    x = 10
    d = []
    for i in range(10):
        d.append(sym * 1)
        x += 10
        await upload_message.edit_text(text=''.join(d) + f"{i * 10 + 10}%")
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.2)
    await bot.send_message(chat_id=message.from_user.id,
                           text=XP_ADD,
                           parse_mode="HTML")
    await asyncio.sleep(0.5)
    # await asyncio.sleep(20)




"""______________________выбор класса для пользователя_______________"""
@dp.callback_query_handler(lambda c: c.data == 'white_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    # for i in cur.execute("""SELECT""")
    await update_class_white_elf(user_id=callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Светлых эльфов"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT class FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_class = i[0]
    if check_class == "":
        await update_class_white_elf(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                               text=vibor_weapon.format("Светлых эльфов"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<em><b>Вы уже выбрали класс!</b> Начинайте играть</em>",
                               parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data == 'dark_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT class FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_class = i[0]
    if check_class == "":
        await update_class_dark_elf(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                               text=vibor_weapon.format("Темных эльфов'"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<em><b>Вы уже выбрали класс!</b> Начинайте играть</em>",
                               parse_mode="HTML")


@dp.callback_query_handler(lambda c: c.data == 'knights')
async def add_class_for_user(callback_query: types.CallbackQuery):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT class FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_class = i[0]
    if check_class == "":
        await update_class_knights(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user .id,
                               text=vibor_weapon.format("Рыцарей"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<em><b>Вы уже выбрали класс!</b> Начинайте играть</em>",
                               parse_mode="HTML")
"""___________________________________________________________________"""

"""____________________инлайн кнопки для выбора оружия________________"""

weapon_count = 0
@dp.callback_query_handler(lambda c: c.data == 'sword')
async def add_class_for_user(callback_query: types.CallbackQuery):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT weapon FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_weapon = i[0]
    if check_weapon == "":
        await update_weapon_sword(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                                    text=start_farm.format("Меч"),
                                    parse_mode="HTML")
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'bow')
async def add_class_for_user(callback_query: types.CallbackQuery):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT weapon FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_weapon = i[0]
    if check_weapon == "":
        await update_weapon_bow(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                                   text=start_farm.format("Лук"),
                                   parse_mode="HTML")
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'skipetr')
async def add_class_for_user(callback_query: types.CallbackQuery):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT weapon FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_weapon = i[0]
    if check_weapon == "":
        await update_weapon_skipetr(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                                   text=start_farm.format("Магический Скипетр"),
                                   parse_mode="HTML")
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")


"""___________________________________________________________________"""


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start_up, skip_updates=True)