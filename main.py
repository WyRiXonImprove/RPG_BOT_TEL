from aiogram import Bot, Dispatcher, executor, types
import asyncio
import sqlite3 as sq
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from text import *


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
##
bot = Bot(TOKEN)
dp = Dispatcher(bot)


async def on_start_up(_):
    print("Бот запущен успешно!")

@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=welcome,
                           parse_mode="HTML")
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



@dp.callback_query_handler(lambda c: c.data == 'white_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Светлых эльфов"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)

@dp.callback_query_handler(lambda c: c.data == 'dark_elf')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Темных эльфов'"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)

@dp.callback_query_handler(lambda c: c.data == 'knights')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=vibor_weapon.format("Рыцарей"),
                           parse_mode="HTML",
                           reply_markup=inl_button_weapon)



@dp.callback_query_handler(lambda c: c.data == 'sword')
async def add_class_for_user(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id,
                           text=start_farm.format("Меч"),
                           parse_mode="HTML")




if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_start_up, skip_updates=True)