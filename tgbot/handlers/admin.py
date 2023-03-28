from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from magic_filter import F

import time
import datetime
import requests
import asyncio

from tgbot.services.del_message import delete_message
from tgbot.misc.states import AdminControlBalanceState

from tgbot.keyboards.inlineBtn import CastomCallback
# CastomCallback.filter(F.action == "") // callback_query: types.CallbackQuery, callback_data: SellersCallbackFactory, state: FSMContext

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from aiogram.filters import Command, Text
from tgbot.filters.admin import AdminFilter

from tgbot.misc.functions import get_balance

admin_router = Router()
admin_router.message.filter(AdminFilter())

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

base = psycopg2.connect(
    dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,
)
cur = base.cursor()


@admin_router.message(Command("check_balance"))
async def cmd_get_user_balance(message: Message, state: FSMContext):
    await message.reply("Приветствую, админ!")
    await message.answer("Введите ID пользователя у которого хотите узнать баланс")
    await state.set_state(AdminControlBalanceState.check_balance)


@admin_router.message(Text, AdminControlBalanceState.check_balance)
async def get_id_for_check_balance(m: Message, state: FSMContext):
    user_id = m.text
    try:
        user_balance = get_balance(user_id)
        await m.answer(f"Баланс пользователя ( {user_id} ): {user_balance}")
    except Exception:
        await m.answer("Пользователь с таким ID не найден")
    finally:
        await state.clear()


@admin_router.message(Command("add_balance"))
async def cmd_add_balance(m: Message, state: FSMContext):
    await m.reply("Приветствую, админ!")
    await m.answer("Введите ID пользователя которому хотите подсыпать деньжат")
    await state.set_state(AdminControlBalanceState.add_balance_get_id)


@admin_router.message(Text, AdminControlBalanceState.add_balance_get_id)
async def get_id_for_add_balance(m: Message, state: FSMContext):
    user_id = m.text
    cur.execute('SELECT * FROM "user"')
    users = cur.fetchall()
    t = False
    for user in users:
        if user_id == str(user[0]):
            t = True
            await state.update_data(user_id=user_id)
            await m.answer(f"Введите кол-во монет которое желаете подкинуть пользователю ( {user_id} )\n"
                           f"Пример: 10.08 или 10")
            await state.set_state(AdminControlBalanceState.add_balance)
    if not t:
        await m.answer("Пользователь с таким ID не найден")
        await state.clear()


@admin_router.message(Text, AdminControlBalanceState.add_balance)
async def add_balance(m: Message, state: FSMContext):
    amount = m.text
    try:
        data = await state.get_data()
        id_user = data['user_id']
        cur.execute('UPDATE "user" SET balance = balance + %s WHERE id = %s', (amount, id_user))
        base.commit()
        await m.answer("Данные обновлены")
    except Exception:
        await m.answer("Число должно быть валидным")
    finally:
        await state.clear()


@admin_router.message(Command("minus_balance"))
async def cmd_add_balance(m: Message, state: FSMContext):
    await m.reply("Приветствую, админ!")
    await m.answer("Введите ID пользователя у которого хотите отжать деньги")
    await state.set_state(AdminControlBalanceState.minus_balance_get_id)


@admin_router.message(Text, AdminControlBalanceState.minus_balance_get_id)
async def get_id_for_add_balance(m: Message, state: FSMContext):
    user_id = m.text
    cur.execute('SELECT * FROM "user"')
    users = cur.fetchall()
    t = False
    for user in users:
        if user_id == str(user[0]):
            t = True
            await state.update_data(user_id=user_id)
            await m.answer(f"Введите кол-во монет которое желаете отжать у пользователя ( {user_id} )\n"
                           f"Пример: 10.08 или 10")
            await state.set_state(AdminControlBalanceState.minus_balance)
    if not t:
        await m.answer("Пользователь с таким ID не найден")
        await state.clear()


@admin_router.message(Text, AdminControlBalanceState.minus_balance)
async def add_balance(m: Message, state: FSMContext):
    amount = m.text
    try:
        data = await state.get_data()
        id_user = data['user_id']
        cur.execute('UPDATE "user" SET balance = balance - %s WHERE id = %s', (amount, id_user))
        base.commit()
        await m.answer("Данные обновлены")
    except Exception:
        await m.answer("Число должно быть валидным")
    finally:
        await state.clear()


@admin_router.message(Command("change_balance"))
async def cmd_add_balance(m: Message, state: FSMContext):
    await m.reply("Приветствую, админ!")
    await m.answer("Введите ID пользователя которому нужно подкорректировать баланс")
    await state.set_state(AdminControlBalanceState.change_balance_get_id)


@admin_router.message(Text, AdminControlBalanceState.change_balance_get_id)
async def get_id_for_add_balance(m: Message, state: FSMContext):
    user_id = m.text
    cur.execute('SELECT * FROM "user"')
    users = cur.fetchall()
    t = False
    for user in users:
        if user_id == str(user[0]):
            t = True
            await state.update_data(user_id=user_id)
            await m.answer(f"Введите новый баланс пользователя ( {user_id} )\n"
                           f"Пример: 76.08 или 76")
            await state.set_state(AdminControlBalanceState.change_balance)
    if not t:
        await m.answer("Пользователь с таким ID не найден")
        await state.clear()


@admin_router.message(Text, AdminControlBalanceState.change_balance)
async def add_balance(m: Message, state: FSMContext):
    new_balance = m.text
    try:
        data = await state.get_data()
        id_user = data['user_id']
        cur.execute('UPDATE "user" SET balance = %s WHERE id = %s', (new_balance, id_user))
        base.commit()
        await m.answer("Данные обновлены")
    except Exception:
        await m.answer("Число должно быть валидным")
    finally:
        await state.clear()
