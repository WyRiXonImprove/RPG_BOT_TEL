from aiogram import Bot, Dispatcher, executor, types
import asyncio
import sqlite3 as sq
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from text import *
import time


"""_____________________________Создание бд и ее функций__________________________"""


async def new_db(user_id):
    global db, cur
    db = sq.connect("new db1")
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS user_db(
                    user_id  INT,
                    class TEXT,
                    weapon TEXT,
                    level_user INT);""")
    db.commit()
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""SELECT user_id FROM user_db WHERE user_id = '{user_id}'""")
    if cur.fetchone() is None:
        user_info = (user_id, "", "", 1)
        cur.execute("""INSERT INTO user_db VALUES(?, ?, ?, ?)""", user_info)
        db.commit()
        for i in cur.execute("""SELECT * FROM user_db"""):
            print(i)


# функция проверки бд
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
    cur.execute(f"""UPDATE user_db SET class = '{dark_elf}' WHERE user_id = '{user_id}'""")
    db.commit()


async def update_class_knights(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET class = '{knights}' WHERE user_id = '{user_id}'""")
    db.commit()


"""________________________________________________________________________________"""
"""______________________________________апдейт оружий_____________________________"""


async def update_weapon_sword(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET weapon = '{"sword"}' WHERE user_id = '{user_id}'""")
    db.commit()


async def update_weapon_bow(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET weapon = '{"bow"}' WHERE user_id = '{user_id}'""")
    db.commit()


async def update_weapon_skipetr(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""UPDATE user_db SET weapon = '{"skipetr"}' WHERE user_id = '{user_id}'""")
    db.commit()


"""________________________________________________________________________________"""
"""_________________________создание бд с личными знач. пользователя_______________"""


async def db_farm(user_id):
    global db_table_farm, cur_table_farm
    db_table_farm = sq.connect("db from farm")
    cur_table_farm = db_table_farm.cursor()

    cur_table_farm.execute("""CREATE TABLE IF NOT EXISTS user_farm(
                        user_id  INT,
                        speed_farm INT,
                        mana INT,
                        time_farm INT,
                        mana_all INT);""")
    db_table_farm.commit()
    cur_table_farm.execute(f"""SELECT user_id FROM user_farm WHERE user_id = '{user_id}'""")
    if cur_table_farm.fetchone() is None:
        user_info = (user_id, 100, 300, 60, 300)
        cur_table_farm.execute("""INSERT INTO user_farm VALUES(?, ?, ?, ?, ?)""", user_info)
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)


"""_____________________________Создание бд и ее функций__________________________"""

"""_____________________________Создание бд для фрма и ее функций__________________________"""


async def db_lev(user_id):
    global db_l, cur_l
    db_l = sq.connect('level.db')
    cur_l = db_l.cursor()

    cur_l.execute("""CREATE TABLE IF NOT EXISTS level(
                    user_id  INT,
                    ex_level REAL,
                    ex REAL);""")
    db_l.commit()
    cur_l.execute(f"""SELECT user_id FROM level WHERE user_id = '{user_id}'""")
    if cur_l.fetchone() is None:
        user_info = (user_id, 25, 0)
        cur_l.execute("""INSERT INTO level VALUES(?, ?, ?)""", user_info)
        db_l.commit()
        for i in cur_l.execute("""SELECT * FROM level"""):
            print(i)


# add xp in table level
async def xp_add(user_id):
    global XP, XP_level
    db_l = sq.connect('level.db')
    cur_l = db_l.cursor()
    for i in cur_l.execute(f"""SELECT ex_level FROM level WHERE user_id = '{user_id}'"""):
        XP_level = i[0]
    for i in cur_l.execute(f"""SELECT ex FROM level WHERE user_id = '{user_id}'"""):
        XP = i[0]
        print(XP)
    XP = round(XP, 1)
    XP += 0.2
    XP = round(XP, 1)
    cur_l.execute(f"""UPDATE level SET ex = {XP} WHERE user_id = '{user_id}'""")
    db_l.commit()


async def mana_update(user_id):
    db_table_farm = sq.connect("db from farm")
    cur_table_farm = db_table_farm.cursor()
    for i in cur_table_farm.execute(f"""SELECT mana FROM user_farm WHERE user_id = {user_id}"""):
        mana_now = i[0]
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT level_user FROM user_db WHERE user_id = {user_id}"""):
        level = i[0]
    if level == 1:
        if mana_now >= 5:
            mana_now -= 5
            cur_table_farm.execute(f"""UPDATE user_farm SET mana = '{0}' WHERE user_id = {user_id}""")
            db_table_farm.commit()
            await bot.send_message(chat_id=user_id,
                                   text=f"""<em>Потрачено <b>5 маны!</b>
                                            Остаток: <b>{mana_now}</b></em>""",
                                   parse_mode="HTML")
        else:
            await bot.send_message(chat_id=user_id,
                                   text="Маны не осталось! Она обновляется в 7 часов утра по МСК!")


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
    if time.strftime("%X") >= '07:00:00' and time.strftime('%X') <= '10:00:00':
        await bot.send_message(chat_id=message.from_user.id,
                               text= 'Доброе утро\n' + welcome,
                               parse_mode="HTML",
                               reply_markup=kb)
    elif time.strftime("%X") >= '10:00:00' and time.strftime('%X') <= '17:00:00':
        await bot.send_message(chat_id=message.from_user.id,
                               text= 'Добрый день\n' + welcome,
                               parse_mode="HTML",
                               reply_markup=kb)
    elif time.strftime("%X") >= '17:00:00':
        await bot.send_message(chat_id=message.from_user.id,
                               text= 'Добрый вечер\n' + welcome,
                               parse_mode="HTML",
                               reply_markup=kb)

    await new_db(user_id=message.from_user.id)
    await db_lev(user_id=message.from_user.id)
    await db_farm(user_id=message.from_user.id)
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
    await asyncio.sleep(1)  # ждём
    await upload_message.delete()  # удаляем сообщение

    await bot.send_message(chat_id=message.from_user.id,
                           text=vibor_classa,
                           parse_mode="HTML",
                           reply_markup=inl_button_class)


@dp.message_handler(commands=["farm"])
async def farm_start(message: types.Message):
    await mana_update(user_id=message.from_user.id)
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
    db_table_farm = sq.connect("db from farm")
    cur_table_farm = db_table_farm.cursor()
    for i in cur_table_farm.execute(f"""SELECT speed_farm FROM user_farm WHERE user_id = '{message.from_user.id}'"""):
        speed_farm_user = i[0]
    for i in cur_table_farm.execute(f"""SELECT time_farm FROM user_farm WHERE user_id = '{message.from_user.id}'"""):
        time_farm_user = i[0]
    time_farm = time_farm_user - (speed_farm_user / 10)

    upload_message = await bot.send_message(chat_id=message.chat.id,
                                            text=f"Фарм площади составляет: <b>{time_farm} секунд!</b>",
                                            parse_mode="HTML")
    await asyncio.sleep(2)
    sym = '▌'
    x = 0
    d = []
    for i in range(9):
        d.append(sym * 1)
        x += 10
        await upload_message.edit_text(text=''.join(d) + f"{i * 10 + 10}%")
        await asyncio.sleep(time_farm / 10)
    await asyncio.sleep(0.5)
    await upload_message.delete()
    await xp_add(user_id=message.from_user.id)
    await bot.send_message(chat_id=message.from_user.id,
                           text=XP_ADD.format(0.2, XP, XP_level),
                           parse_mode="HTML")
    await asyncio.sleep(0.5)


"""______________________выбор класса для пользователя_______________"""


@dp.callback_query_handler(lambda c: c.data == 'white_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
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
        db_table_farm = sq.connect("db from farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT speed_farm FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            speed_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET speed_farm = {speed_farm + 40} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
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
        db_table_farm = sq.connect("db from farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT speed_farm FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            speed_farm = i[0]
        for i in cur_table_farm.execute(
                f"""SELECT mana_all FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            mana_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET speed_farm = {speed_farm + 60} WHERE user_id = '{callback_query.from_user.id}'""")
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana_all = {mana_farm - 10} WHERE user_id = '{callback_query.from_user.id}'""")
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana = {mana_farm - 10} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
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
        await bot.send_message(callback_query.from_user.id,
                               text=vibor_weapon.format("Рыцарей"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
        db_table_farm = sq.connect("db from farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT speed_farm FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            speed_farm = i[0]
        for i in cur_table_farm.execute(
                f"""SELECT mana_all FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            mana_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET speed_farm = {speed_farm + 70} WHERE user_id = '{callback_query.from_user.id}'""")
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana_all = {mana_farm - 15} WHERE user_id = '{callback_query.from_user.id}'""")
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana = {mana_farm - 15} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
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
        db_table_farm = sq.connect("db from farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT speed_farm FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            speed_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET speed_farm = {speed_farm + 10} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
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
        db_table_farm = sq.connect("db from farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT speed_farm FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            speed_farm = i[0]
        for i in cur_table_farm.execute(
                f"""SELECT mana_all FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            mana_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET speed_farm = {speed_farm + 20} WHERE user_id = '{callback_query.from_user.id}'""")
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana_all = {mana_farm - 5} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
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
        db_table_farm = sq.connect("db from farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT mana_all FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            mana_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana_all = {mana_farm + 10} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")


"""___________________________________________________________________"""

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start_up, skip_updates=True)
