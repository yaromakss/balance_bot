import psycopg2
from psycopg2 import sql
from psycopg2.extensions import AsIs
from tgbot.config import load_config

import logging
config = load_config(".env")

async def postgre_start():
    base = psycopg2.connect(dbname=config.db.database,
    user=config.db.user,
    password=config.db.password,
    host=config.db.host,)
    cur = base.cursor()
    if base:
        logging.info(f"data base connect success!")
    cur.execute('''CREATE TABLE IF NOT EXISTS "user"
                (
                id        bigint            not null
                    constraint user_pk
                        primary key,
                user_name text              not null,
                name      text              not null,
                balance   numeric default 0 not null
                );
        ''')
    
    
    base.commit()
    cur.close()
    base.close()