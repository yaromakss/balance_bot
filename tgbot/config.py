from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    db_uri: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token="1753718100:AAEzZOqjo9D_g5XNeOXkVguM9ChC805CumA",
            admin_ids=[578706671],
            use_redis=False,
        ),
        db=DbConfig(
            host='localhost',
            password='538feijer',
            user='postgres',
            database='balance_bot',
            db_uri='jdbc:postgresql://localhost:5432/balance_bot'
        ),
        misc=Miscellaneous()
    )
