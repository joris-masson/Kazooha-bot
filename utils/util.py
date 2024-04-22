import os
import mysql.connector


from dotenv import load_dotenv


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
