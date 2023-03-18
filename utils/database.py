import os
import mysql.connector
import interactions

from dotenv import load_dotenv
from utils.functions import remove_emojis

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


async def insert_message(msg: interactions.Message, modified=0) -> None:
    db = open_connection()
    msg_guild = await msg.get_guild()
    guild_name = remove_emojis(msg_guild.name)
    msg_channel = await msg.get_channel()
    channel_name = remove_emojis(msg_channel.name)
    author_name = remove_emojis(msg.author.username)
    msg_content = remove_emojis(msg.content)
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO Kazooha.Messages (id, guildId, guildName, channelId, channelName, authorId, authorName, sentTime, content, modified, deleted) VALUE ('{msg.id}', '{msg.guild_id}', '{guild_name}', '{msg.channel_id}', '{channel_name}', '{msg.author.id}', '{author_name}', CURRENT_TIMESTAMP, '{msg_content}', '{modified}', '0');")
    db.commit()
    cursor.close()
    db.close()
    print(f"[DB ] - Message inséré: {msg_content}")


def is_in_messages(msg_id: int) -> bool:
    db = open_connection()
    cursor = db.cursor()
    cursor.execute(f"SELECT id FROM Messages WHERE id='{msg_id}'")
    res = len(cursor.fetchall())
    cursor.close()
    db.close()
    return res != 0
