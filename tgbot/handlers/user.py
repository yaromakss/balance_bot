from aiogram import Router, Bot, types
from aiogram.filters import Command, Text, StateFilter
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
# from magic_filter import F
from aiogram import F

from tgbot.misc.states import GalleryState, ProfileState

import time
import datetime
import requests
import asyncio

from tgbot.services.del_message import delete_message
from tgbot.misc.functions import auth_status, add_user, random_photo, get_balance
from tgbot.keyboards.textBtn import home_btn, gallery_btn, profile_btn


from tgbot.keyboards.inlineBtn import CastomCallback
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs


user_router = Router()
config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()


@user_router.message(Command("start"))
async def user_start(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    name = message.from_user.first_name
    msg = await bot.send_message(user_id, "Hi, user!")
    asyncio.create_task(delete_message(msg, 20))
    auth = await auth_status(user_id)
    if auth:
        await bot.send_message(user_id, 'Congratulations, you have in the database',
                               reply_markup=home_btn().as_markup(resize_keyboard=True))
    else:
        await bot.send_message(user_id, 'You are not registered in the bot')
        await bot.send_message(user_id, 'Attempt to register in the database....')
        try:
            await add_user(user_id, user_name, name)
            await bot.send_message(user_id, 'registration completed successfully')
        except():
            await bot.send_message(user_id, 'Registration failed. Contact Support')


@user_router.message(Command("menu"))
async def user_start(message: Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Main menu", reply_markup=home_btn().as_markup(resize_keyboard=True))


@user_router.message(F.text == 'Time')
async def bt_current_time(message: types.Message):
    user_id = message.from_user.id
    cur_day = datetime.datetime.now().strftime("%d-%m-%Y")
    cur_time = datetime.datetime.now().strftime("%H:%M:%S")
    await bot.send_message(user_id, f'Текущая дата: {cur_day}\n'
                                    f'Текущее время: {cur_time}')


@user_router.message(F.text == 'Gallery')
async def bt_gallery(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await bot.send_message(user_id, 'random photo from server',
                           reply_markup=gallery_btn().as_markup(resize_keyboard=True))
    await state.set_state(GalleryState.photo)


@user_router.message(F.text == 'New photo', GalleryState.photo)
async def bt_get_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    img_path = random_photo()
    photo = FSInputFile(img_path)
    await bot.send_photo(user_id, photo, reply_markup=gallery_btn().as_markup(resize_keyboard=True))
    await state.set_state(GalleryState.photo)


@user_router.message(F.text == 'Menu', GalleryState.photo)
async def bt_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    await bot.send_message(user_id, "You`re in the main menu",
                           reply_markup=home_btn().as_markup(resize_keyboard=True))


@user_router.message(F.text == 'Profile')
async def bt_profile(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name = message.from_user.first_name
    user_name = message.from_user.username
    await bot.send_message(user_id, f'Name: {name}\nUsername: {user_name}\nYour id: {user_id}',
                           reply_markup=profile_btn().as_markup(resize_keyboard=True))
    await state.set_state(ProfileState.profile)


@user_router.message(F.text == 'Check balance', ProfileState.profile)
async def bt_check_balance(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_balance = get_balance(user_id)
    await bot.send_message(user_id, f"Balance: {user_balance}", reply_markup=profile_btn().as_markup(resize_keyboard=True))
    await state.set_state(ProfileState.profile)


@user_router.message(F.text == 'Menu', ProfileState.profile)
async def bt_menu(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.clear()
    await bot.send_message(user_id, "You`re in the main menu",
                           reply_markup=home_btn().as_markup(resize_keyboard=True))





# hanldler for text messages
# 1 version
# @user_router.message(Text('Главное меню'))
# async def user_start(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
    
    
# 2 version
# @user_router.message(F.text == 'Главное меню')
# async def user_start(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id

# version for some text messages
# @user_router.message(F.text.in_({'Покупка акаунтов бирж', 'Покупка кошелька Юмани'}))


