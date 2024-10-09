from pymongo import MongoClient

from app.core.config import config

client = MongoClient(f"{config.db_conn}://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}")
database = client[config.db_name]