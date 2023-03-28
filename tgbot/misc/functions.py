import random

from aiogram import Router, Bot, types
from aiogram.types import Message, FSInputFile
from tgbot.config import load_config
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs

from datetime import datetime
import asyncio
import os

config = load_config(".env")
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
# bot2 = Bot(token=config.tg_bot.token2, parse_mode="HTML")


async def auth_status(user_id):
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
    )
    cur = base.cursor()
    user_id = str(user_id)
    cur.execute('SELECT * FROM "user"')
    users = cur.fetchall()
    answer = False
    for user in users:
        if str(user[0]) == user_id:
            answer = True
    base.commit()
    cur.close()
    base.close()
    return answer


async def add_user(user_id, user_name, name):
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
    )
    cur = base.cursor()
    data = (user_id, user_name, name)
    cur.execute('INSERT INTO "user" (id, user_name, name) VALUES (%s,%s,%s)', data)
    base.commit()
    cur.close()
    base.close()


def random_photo():
    directory = 'tgbot/photos'
    img = os.path.join(directory, random.choice(os.listdir(directory)))
    return img


def get_balance(user_id):
    base = psycopg2.connect(
        dbname=config.db.database,
        user=config.db.user,
        password=config.db.password,
        host=config.db.host,
    )
    cur = base.cursor()
    cur.execute('SELECT balance FROM "user" WHERE id = %s', (user_id,))
    user_balance = cur.fetchone()
    return user_balance[0]
