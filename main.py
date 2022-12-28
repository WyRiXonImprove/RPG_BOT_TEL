import random
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import sqlite3 as sq
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
from text import *
from slovari import *
import time
from datetime import datetime, timedelta

async def time_add():
    global welcome
    if time.strftime("%X") >= '07:00:00' and time.strftime('%X') <= '10:00:00':
        welcome = welcome_morning
    elif time.strftime("%X") >= '10:00:00' and time.strftime('%X') <= '17:00:00':
        welcome = welcome_day
    elif time.strftime("%X") >= '17:00:00':
        welcome = welcome_dinner
    else:
        welcome = welcome_night



"""_____________________________Создание бд и ее функций__________________________"""


async def new_db(user_id):
    global db, cur
    db = sq.connect("new db1")
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS user_db(
                    user_id  INT,
                    class TEXT,
                    weapon TEXT,
                    level_user INT,
                    gold INT);""")
    db.commit()
    db = sq.connect("new db1")
    cur = db.cursor()
    cur.execute(f"""SELECT user_id FROM user_db WHERE user_id = '{user_id}'""")
    if cur.fetchone() is None:
        user_info = (user_id, "", "", 1, 0)
        cur.execute("""INSERT INTO user_db VALUES(?, ?, ?, ?, ?)""", user_info)
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
    db_table_farm = sq.connect("table farm")
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

def prov_farm():
    db_table_farm = sq.connect("table farm")
    cur_table_farm = db_table_farm.cursor()
    for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
        print(i)


"""_____________________________Создание бд и ее функций__________________________"""

"""_____________________________Создание бд для фрма и ее функций__________________________"""


async def db_lev(user_id):
    global db_l, cur_l
    db_l = sq.connect("table level")
    cur_l = db_l.cursor()

    cur_l.execute("""CREATE TABLE IF NOT EXISTS level(
                    user_id  INT,
                    ex_level REAL,
                    ex REAL);""")
    db_l.commit()
    cur_l.execute(f"""SELECT user_id FROM level WHERE user_id = '{user_id}'""")
    if cur_l.fetchone() is None:
        user_info = (user_id, 5, 0)
        cur_l.execute("""INSERT INTO level VALUES(?, ?, ?)""", user_info)
        db_l.commit()
        for i in cur_l.execute("""SELECT * FROM level"""):
            print(i)



#add xp in table level
async def xp_add(user_id, level):
    global XP, XP_level, a
    db_l = sq.connect("table level")
    cur_l = db_l.cursor()
    for i in cur_l.execute(f"""SELECT ex_level FROM level WHERE user_id = '{user_id}'"""):
        XP_level = i[0]
    for i in cur_l.execute(f"""SELECT ex FROM level WHERE user_id = '{user_id}'"""):
        XP = i[0]
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT class FROM user_db WHERE user_id = '{user_id}'"""):
        check_class = i[0]
    db.close()
    XP = round(XP, 1)
    if check_class == "white_elf":
        a = random.randint(1, 20)
        if a == 4:
            XP += level_xp[level] * 2
            XP = round(XP, 1)
        else:
            XP += level_xp[level]
            XP = round(XP, 1)
    elif check_class == 'knights':
        b = random.randint(1, 10)
        if b == 4:
            XP += level_xp[level] * 1.5
            XP = round(XP, 1)
        else:
            XP += level_xp[level]
            XP = round(XP, 1)
    else:
        XP += level_xp[level]
        XP = round(XP, 1)
    cur_l.execute(f"""UPDATE level SET ex = {XP} WHERE user_id = '{user_id}'""")
    db_l.commit()


async def mana_update(level, user_id):
    db_table_farm = sq.connect("table farm")
    cur_table_farm = db_table_farm.cursor()
    for i in cur_table_farm.execute(f"""SELECT mana FROM user_farm WHERE user_id = '{user_id}'"""):
        mana_now = i[0]
    mana_now -= level_to_mana[level]
    cur_table_farm.execute(f"""UPDATE user_farm SET mana = {mana_now} WHERE user_id = '{user_id}'""")
    db_table_farm.commit()
    db_table_farm.close()
    await bot.send_message(chat_id=user_id,
                           text=f"""<em>Потрачено <b>{level_to_mana[level]} маны</b>
                                     Остаток: <b>{mana_now}</b></em>""",
                           parse_mode="HTML")


async def up_level(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT level_user FROM user_db WHERE user_id = {user_id}"""):
        level = i[0]

    db_l = sq.connect("table level")
    cur_l = db_l.cursor()
    for i in cur_l.execute(f"""SELECT ex FROM level WHERE user_id = {user_id}"""):
        ex = i[0]
    for i in cur_l.execute(f"""SELECT ex_level FROM level WHERE user_id = '{user_id}'"""):
        ex_level = i[0]

    if ex_level <= ex:
        cur_l.execute(f"""UPDATE level SET ex = {ex - ex_level} WHERE user_id = '{user_id}'""")
        db_l.commit()
        db_l.close()

        level += 1
        cur.execute(f"""UPDATE user_db SET level_user = {level} WHERE user_id = {user_id}""")
        db.commit()
        db.close()

        db_table_farm = sq.connect("table farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(f"""SELECT speed_farm FROM user_farm WHERE user_id = {user_id}"""):
            speed_farm = i[0]
        for i in cur_table_farm.execute(f"""SELECT mana_all FROM user_farm WHERE user_id = '{user_id}'"""):
            mana_all = i[0]
        speed_farm += reward_sf[level]
        mana_all += reward_mana[level]
        cur_table_farm.execute(f"""UPDATE user_farm SET speed_farm = '{speed_farm}'""")
        cur_table_farm.execute(f"""UPDATE user_farm SET mana_all = '{mana_all}'""")
        cur_table_farm.execute(f"""UPDATE user_farm SET time_farm = '{xp_to_time[level]}'""")
        db_table_farm.commit()
        db_table_farm.close()
        await bot.send_message(chat_id=user_id,
                               text=f"XP полон! Ваш уровень увеличен до {level}\n"
                                    f"Скорость фарма увеличена на {reward_sf[level]}, мана увеличина на {mana_all[level]}")
        db_l = sq.connect("table level")
        cur_l = db_l.cursor()
        cur_l.execute(f"""UPDATE level SET ex_level = '{level_to_xp[level]}' WHERE user_id = '{user_id}'""")
        db_l.commit()
        db_l.close()
        prov()


"""_______________________________________GOLD system______________________________"""
async def gold_add_user(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT gold FROM user_db WHERE user_id = '{user_id}'"""):
        gold = i[0]
    for i in cur.execute(f"""SELECT level_user FROM user_db WHERE user_id = '{user_id}'"""):
        level = i[0]
    if level == 1:
        gold_add = random.randint(5, 10)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 2:
        gold_add = random.randint(11, 18)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 3:
        gold_add = random.randint(19, 30)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 4:
        gold_add = random.randint(31, 45)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 5:
        gold_add = random.randint(46, 62)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 6:
        gold_add = random.randint(63, 80)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 7:
        gold_add = random.randint(81, 100)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 8:
        gold_add = random.randint(101, 124)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    elif level == 9:
        gold_add = random.randint(125, 150)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")
    else:
        gold_add = random.randint(151, 181)
        gold += gold_add
        cur.execute(f"""UPDATE user_db Set gold = {gold} WHERE user_id = '{user_id}'""")
        db.commit()
        db.close()
        await bot.send_message(chat_id=user_id,
                               text=GOLD_ADD.format(gold_add),
                               parse_mode="HTML")

"""_________________________________Профиль_________________________________________"""
async def select_profile(user_id):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT class FROM user_db WHERE user_id = {user_id}"""):
        class_user = i[0]
        if class_user == "white_elf":
            class_user = "Светлый эльф"
        elif class_user == "dark_elf":
            class_user = "Темный эльф"
        else:
            class_user = "Рыцарь"
    for i in cur.execute(f"""SELECT weapon FROM user_db WHERE user_id = {user_id}"""):
        weapon = i[0]
        if weapon == "bow":
            weapon = "Лук"
        elif weapon == "skipetr":
            weapon = "Магический скипетр"
        else:
            weapon = "Меч"
    for i in cur.execute(f"""SELECT level_user FROM user_db WHERE user_id = {user_id}"""):
        level = i[0]
    for i in cur.execute(f"""SELECT gold FROM user_db WHERE user_id = {user_id}"""):
        gold = i[0]
    db.close()
    await bot.send_message(chat_id=user_id,
                           text=PROFILE.format(class_user, weapon, level, gold),
                           parse_mode="HTML")

"""______________________инлайн клава для выбора класса____________________________"""
"""______________________инлайн клава для выбора класа____________________________"""
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
b_profile = KeyboardButton('/profile')
b_game = KeyboardButton('/game')
b_buy = KeyboardButton('/buy')
b_farm = KeyboardButton('/farm')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(b_game).insert(b_farm).add(b_buy).insert(b_profile)
"""________________________________________________________________________________"""

bot = Bot(TOKEN)
dp = Dispatcher(bot)
k = 0

async def on_start_up(_):
    print("Бот запущен!")


@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await time_add()
    await bot.send_message(chat_id=message.from_user.id,
                           text=welcome,
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
    await bot.send_message(chat_id=message.from_user.id,
                           text=vibor_classa,
                           parse_mode="HTML",
                           reply_markup=inl_button_class)

@dp.message_handler(commands=["profile"])
async def profile(message: types.Message):
    await select_profile(user_id=message.chat.id)
    await message.delete()



@dp.message_handler(commands=["farm"])
async def farm_start(message: types.Message):
    global k, time_o, mana_now
    while k == 0:
        time_o = datetime.now()
        k+=1
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT level_user FROM user_db WHERE user_id = '{message.from_user.id}'"""):
        level = i[0]
    db_table_farm = sq.connect("table farm")
    cur_table_farm = db_table_farm.cursor()
    for i in cur_table_farm.execute(f"""SELECT mana FROM user_farm WHERE user_id = '{message.from_user.id}'"""):
        mana_now = i[0]
    if mana_now >= level_to_mana[level]:
        for i in cur_table_farm.execute(
                f"""SELECT speed_farm FROM user_farm WHERE user_id = '{message.from_user.id}'"""):
            speed_farm_user = i[0]
        for i in cur_table_farm.execute(
                f"""SELECT time_farm FROM user_farm WHERE user_id = '{message.from_user.id}'"""):
            time_farm_user = i[0]
        db_table_farm.close()
        time_farm = time_farm_user - (speed_farm_user / 10)
        if (datetime.now() - time_o).seconds > time_farm:
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Сначала окончите предыдущий фарм!")
            return
        time_o = datetime.now() + timedelta(seconds=time_farm)
        upload_message = await bot.send_message(chat_id=message.chat.id,
                                                text=f"Фарм площади составляет: <b>{int(time_farm)} секунд!</b>",
                                                parse_mode="HTML")
        await asyncio.sleep(2)
        sym = '▌'
        x = 0
        d = []
        for i in range(9):
            d.append(sym * 1)
            x += 10
            await upload_message.edit_text(text=''.join(d) + f"{i * 10 + 10}%")
            await asyncio.sleep(0.1)  # time_farm / 10)
        await upload_message.delete()
        await xp_add(user_id=message.from_user.id, level=level)
        await bot.send_message(chat_id=message.from_user.id,
                                text=XP_ADD.format(level_xp[level], XP, XP_level),
                                parse_mode="HTML")

        await mana_update(level=level, user_id=message.from_user.id)
        await up_level(user_id=message.chat.id)
        await gold_add_user(user_id=message.chat.id)
        time_o = datetime.now()
        prov()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="Маны не осталось! Она обновляется в 7 часов утра по МСК!")


# TODO Доработка значений класса = добавить - !!сделано!!
# TODO Платежка
# TODO Босс
# TODO Автообновление значений
# TODO Донат
# TODO Сервак


"""______________________выбор класса для пользователя_______________"""


@dp.callback_query_handler(lambda c: c.data == 'white_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    db = sq.connect("new db1")
    cur = db.cursor()
    for i in cur.execute(f"""SELECT class FROM user_db WHERE user_id = '{callback_query.from_user.id}'"""):
        check_class = i[0]
    db.close()
    if check_class == "":
        await update_class_white_elf(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                               text=vibor_weapon.format("Светлых эльфов"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
        db_table_farm = sq.connect("table farm")
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
    db.close()
    if check_class == "":
        await update_class_dark_elf(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                               text=vibor_weapon.format("Темных эльфов'"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
        db_table_farm = sq.connect("table farm")
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
        db.close()
        await update_class_knights(user_id=callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,
                               text=vibor_weapon.format("Рыцарей"),
                               parse_mode="HTML",
                               reply_markup=inl_button_weapon)
        db_table_farm = sq.connect("table farm")
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
        db_table_farm = sq.connect("table farm")
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
        db_table_farm = sq.connect("table farm")
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
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana = {mana_farm - 5} WHERE user_id = '{callback_query.from_user.id}'""")
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
        db_table_farm = sq.connect("table farm")
        cur_table_farm = db_table_farm.cursor()
        for i in cur_table_farm.execute(
                f"""SELECT mana_all FROM user_farm WHERE user_id = '{callback_query.from_user.id}'"""):
            mana_farm = i[0]
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana_all = {mana_farm + 30} WHERE user_id = '{callback_query.from_user.id}'""")
        cur_table_farm.execute(
            f"""UPDATE user_farm SET mana = {mana_farm + 30} WHERE user_id = '{callback_query.from_user.id}'""")
        db_table_farm.commit()
        for i in cur_table_farm.execute("""SELECT * FROM user_farm"""):
            print(i)
    else:
        await bot.send_message(callback_query.from_user.id,
                               text="<b>Вы уже брали оружие!</b>",
                               parse_mode="HTML")


def update():
    time_now = time.strftime("%X")
    count = 0
    db_table_farm = sq.connect("table farm")
    cur_table_farm = db_table_farm.cursor()
    for i in cur_table_farm.execute("""SELECT user_id FROM user_farm"""):
        print(i)
    for n in cur_table_farm.execute(f"""SELECT mana_all FROM user_farm WHERE user_id = '{i[count]}'"""):
        mana_all = n[0]
        print(mana_all)
        cur_table_farm.execute(f"""UPDATE user_farm SET mana = {mana_all} WHERE user_id = '{i[count]}'""")
        db_table_farm.commit()
        count += 1
    prov_farm()



"""___________________________________________________________________"""

if __name__ == "__main__":
    RepeatTimer(10, update).start()
    executor.start_polling(dp, on_startup=on_start_up, skip_updates=True)
