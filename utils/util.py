import os
import mysql.connector


from dotenv import load_dotenv
from datetime import datetime


def convert_discord_id_to_time(discord_id: int) -> int:
    return int((int(bin(discord_id)[:-22], 2) + 1420070400000) / 1000)


def open_db_connection() -> mysql.connector.MySQLConnection:
    load_dotenv()

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database="Kazooha"
    )


def log(prefix: str, thing: str):
    if thing is not None:
        date = datetime.now().strftime("%H:%M:%S")
        filename = datetime.now().strftime("%d-%m-%Y")
        ze_log = f"[{prefix}] - [{date}] - {thing}\n"
        print(ze_log, end='')
        with open(f"logs/{filename}.log", 'a', encoding='utf-8') as log_file:
            log_file.write(ze_log)
