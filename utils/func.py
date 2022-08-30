import datetime
import discord
import os


async def detect_message(msg: discord.Message) -> None:
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    if not msg.author.bot and not len(msg.content) == 0:
        time = datetime.datetime.now().strftime("%H:%M:%S")

        ze_log = f"[{time}] - {msg.author.name} a dit: {msg.content}\n"
        print(f"[MSG] - {ze_log}", end='')
        try:
            path = f"message_logs/{date}/{msg.guild.name}/{msg.channel.name}.txt"
        except AttributeError:
            path = f"message_logs/{date}/{msg.author.name}.txt"
        await image_log(msg, date)
        try:
            try:
                with open(path, 'a') as log_file:
                    log_file.write(ze_log)
            except FileNotFoundError:
                os.makedirs(rf"message_logs/{date}/{msg.guild.name}")
                with open(path, 'a') as log_file:
                    log_file.write(ze_log)
        except UnicodeEncodeError:
            try:
                with open(path, 'a', encoding='utf-8') as log_file:
                    log_file.write(ze_log)
            except FileNotFoundError:
                os.makedirs(rf"message_logs/{date}/{msg.guild.name}")
                with open(path, 'a', encoding='utf-8') as log_file:
                    log_file.write(ze_log)
    elif not msg.author.bot:
        await image_log(msg, date)


async def image_log(msg: discord.Message, date: str) -> None:
    if len(msg.attachments) != 0:
        try:
            os.makedirs(rf"image_logs/{date}/{msg.guild.name}/{msg.channel.name}/{msg.author.name}")
        except FileExistsError:
            pass
        for att in msg.attachments:
            await att.save(f"image_logs/{date}/{msg.guild.name}/{msg.channel.name}/{msg.author.name}/{att.filename}")
