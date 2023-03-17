import os
import mysql.connector
import interactions

from dotenv import load_dotenv
from utils.functions import convert_discord_id_to_time

load_dotenv()
HOST = os.getenv("DATABASE_HOST")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE = os.getenv("DATABASE_NAME")


def open_connection() -> mysql.connector.connection.MySQLConnection:
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )


async def insert_message(msg: interactions.Message) -> None:
    db = open_connection()
    msg_guild = await msg.get_guild()
    guild_name = msg_guild.name.replace("'", "")
    msg_channel = await msg.get_channel()
    channel_name = msg_channel.name.replace("'", "")
    author_name = msg.author.username.replace("'", "")
    msg_content = msg.content.replace("'", '')
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO Kazooha.Messages (id, guildId, guildName, channelId, channelName, authorId, authorName, sentTime, content) VALUE ('{msg.id}', '{msg.guild_id}', '{guild_name}', '{msg.channel_id}', '{channel_name}', '{msg.author.id}', '{author_name}', '{convert_discord_id_to_time(int(msg.id))}', '{msg_content}');")
    db.commit()
    cursor.close()
    db.close()
