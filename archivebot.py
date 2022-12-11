import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from utils.archive_bot.classes.archive import Archive

intents = discord.Intents.all()
intents.members = True

archiver = commands.Bot(command_prefix=";", help_command=None, intents=intents)

load_dotenv()
TOKEN = os.getenv("TOKEN")


@archiver.event
async def on_ready():
    print(f'{archiver.user.name} s\'est connecté à Discord')


@archiver.command(name="archive_channel")
async def archive(ctx, channel: discord.TextChannel):
    await ctx.message.delete()
    archive = Archive(channel)
    await archive.make_archive()
    print("fini")
    return
    with open(rf"data/out/{channel.name}.txt", 'w', encoding='utf-8') as outfile:
        messages = await channel.history(limit=None, oldest_first=True).flatten()
        for message in messages:
            to_write = f"""{message.author.name}({message.author.id})
{message.content}\n\n
    """
            if len(message.attachments) != 0:
                if not os.path.exists(rf"out/{ctx.guild.name}/{ctx.channel.name}/attachments/"):
                    os.mkdir(rf"out/{ctx.guild.name}/{ctx.channel.name}/attachments/")
                for attachment in message.attachments:
                    filename = f"out/{ctx.guild.name}/{ctx.channel.name}/attachments/{attachment.filename}"
                    if not os.path.exists(filename):
                        await attachment.save(filename)
                    else:
                        ze_filename = list(filename)
                        del ze_filename[-4:]
                        extension = filename[-4:]
                        for i in range(1, 101):
                            if not os.path.exists(f"{''.join(ze_filename)}_{i}{extension}"):
                                await attachment.save(f"{''.join(ze_filename)}_{i}{extension}")
                                break
            outfile.write(to_write)
    print("J'ai fini")


archiver.run(TOKEN)
