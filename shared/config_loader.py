import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "catalog" / "entity.json"

with open(CONFIG_FILE, "r") as file:
    config = json.load(file)

def get_mysql_master():
    return config["mysql"]["master"]


def get_mysql_slave():
    return config["mysql"]["slave"]


def get_redis_cache():
    return config["redis"]["cache"]


def get_rabbitmq():
    return config["rabbitmq"]["default"]