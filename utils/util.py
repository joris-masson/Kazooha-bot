import os

import interactions
import mysql.connector
import json

from interactions import Embed, EmbedAuthor, EmbedFooter, EmbedAttachment
from dotenv import load_dotenv
from datetime import datetime

from utils.messagetosend import MessageToSend


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


def prepare_message(message_name: str) -> MessageToSend:
    loaded_json: dict = {}
    with open(message_name, 'r') as json_file:
        loaded_json: dict = json.load(json_file)

    embeds: list[Embed] = []
    if len(loaded_json["embeds"]) != 0:
        for embed in loaded_json["embeds"]:
            embed_to_add = Embed(
                title=embed["title"] if "title" in embed.keys() else None,
                url=embed["url"] if "url" in embed.keys() else None,
                description=embed["description"] if "description" in embed.keys() else None,
                author=EmbedAuthor(
                    name=embed["author"]["name"] if "name" in embed["author"].keys() else None,
                    url=embed["author"]["url"] if "url" in embed["author"].keys() else None,
                    icon_url=embed["author"]["icon_url"] if "icon_url" in embed["author"].keys() else None
                ) if "author" in embed.keys() else None,
                thumbnail=EmbedAttachment(
                    url=embed["thumbnail"]["url"]
                ) if "thumbnail" in embed.keys() else None,
                color=embed["color"] if "color" in embed.keys() else None,
                footer=EmbedFooter(
                    text=embed["footer"]["text"] if "text" in embed["footer"].keys() else None,
                    icon_url=embed["footer"]["icon_url"] if "icon_url" in embed["footer"].keys() else None
                ) if "footer" in embed.keys() else None,
                timestamp=embed["timestamp"] if "timestamp" in embed.keys() else None
            )
            if len(embed["fields"]) != 0:
                for field in embed["fields"]:
                    embed_to_add.add_field(
                        name=field["name"],
                        value=field["value"],
                        inline=field["inline"]
                    )
            embeds.append(embed_to_add)

    return MessageToSend(loaded_json["content"], embeds)


def db_message_create(message: interactions.Message):
    message_id = message.id
    author_id = message.author.id
    guild_id = message.guild.id
    channel_id = message.channel.id
    content = message.content

    db = open_db_connection()
    cursor = db.cursor()

    cursor.execute(f"INSERT INTO Kazooha.Message(id, discordGuildId, discordChannelId, discordAuthorId, content) VALUES ({message_id}, {guild_id}, {channel_id}, {author_id}, '{content}')")

    db.commit()

    cursor.close()
    db.close()

    return db_get_message(message_id)


def db_message_delete(message: interactions.Message):
    db = open_db_connection()
    cursor = db.cursor()

    cursor.execute(f"UPDATE Kazooha.Message SET deleted=1 WHERE id={message.id}")

    db.commit()

    cursor.close()
    db.close()

    return db_get_message(message.id)


def db_message_update(message_after: interactions.Message):
    db = open_db_connection()
    cursor = db.cursor()

    db_before = db_get_message(message_after.id)
    if db_before is not None:
        cursor.execute(f"INSERT INTO Kazooha.Message(id, discordGuildId, discordChannelId, version, discordAuthorId, content, modified) VALUES({db_before[0]}, {db_before[1]}, {db_before[2]}, {db_before[3] + 1}, {db_before[4]}, '{message_after.content}', 1) ")

        db.commit()

        cursor.close()
        db.close()

        return db_before, db_get_message(message_after.id)


def db_get_message(message_id: int):
    db = open_db_connection()
    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM Kazooha.Message WHERE id={message_id} AND version={db_get_last_version_of_message(message_id)}")

    message = cursor.fetchone()

    cursor.close()
    db.close()

    return message


def db_get_last_version_of_message(message_id: int) -> int:
    db = open_db_connection()
    cursor = db.cursor()

    cursor.execute(f"SELECT version FROM Kazooha.Message WHERE id={message_id}")
    all_versions = cursor.fetchall()

    cursor.close()
    db.close()

    last = 1
    for version in all_versions:
        if version[0] > last:
            last = version[0]
    return last
