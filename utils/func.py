import datetime
import time

import interactions
import discord
import os

from utils.functions import log


async def detect_message(msg: interactions.Message, client: interactions.Client) -> None:
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    if not msg.author.bot and not len(msg.content) == 0:
        guild = await msg.get_guild()
        channel = await msg.get_channel()
        ze_time = datetime.datetime.now().strftime("%H:%M:%S")

        ze_log = f"[{ze_time}] - {msg.author.username} a dit: {msg.content}\n"
        print(f"[MSG] - {ze_log}", end='')
        try:
            path = f"message_logs/{date}/{guild.name}/{channel.name}.txt"
        except AttributeError:
            path = f"message_logs/{date}/{msg.author.username}.txt"
        await image_log(msg, date, client)
        try:
            try:
                with open(path, 'a') as log_file:
                    log_file.write(ze_log)
            except FileNotFoundError:
                os.makedirs(rf"message_logs/{date}/{guild.name}")
                with open(path, 'a') as log_file:
                    log_file.write(ze_log)
        except UnicodeEncodeError:
            try:
                with open(path, 'a', encoding='utf-8') as log_file:
                    log_file.write(ze_log)
            except FileNotFoundError:
                os.makedirs(rf"message_logs/{date}/{guild.name}")
                with open(path, 'a', encoding='utf-8') as log_file:
                    log_file.write(ze_log)
    elif not msg.author.bot:
        await image_log(msg, date, client)


async def image_log(msg: interactions.Message, date: str, client: interactions.Client) -> None:
    guild = await msg.get_guild()
    if len(msg.attachments) != 0:
        try:
            os.makedirs(rf"image_logs/{msg.author.username}/{date}/{guild.name}")
        except FileExistsError:
            pass
        for att in msg.attachments:
            await save_attachment(client, att, rf"image_logs/{msg.author.username}/{date}/{guild.name}/{att.filename}")


async def save_attachment(client: interactions.Client, att: interactions.Attachment, filename: str):
    att._client = client._http
    att_data = await att.download()
    if not os.path.exists(filename):
        with open(filename, 'wb') as outfile:
            outfile.write(att_data.getbuffer())
    else:
        ze_filename = list(filename)
        del ze_filename[-4:]
        extension = filename[-4:]
        for i in range(1, 101):
            if not os.path.exists(f"{''.join(ze_filename)}_{i}{extension}"):
                with open(f"{''.join(ze_filename)}_{i}{extension}", 'wb') as outfile:
                    outfile.write(att_data.getbuffer())
                break


def contain_image(msg: discord.Message) -> bool:
    try:
        return len(msg.embeds[0].image) > 0
    except IndexError:
        return False


async def delete_if_not_noice_image(msg: discord.Message):
    time.sleep(2)
    if msg.guild.id == 950118071425724466 and msg.author.id == 1025308201824026644 and not contain_image(msg):
        log(f"Message supprimé: {msg.content}")
        await msg.delete()
