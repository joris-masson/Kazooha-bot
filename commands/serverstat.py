import os

from discord.ext import commands
from utils.functions import merge_dict, get_channel_stat
from utils.functions import log


class ServerStat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="serverStat")
    async def server_stat(self, ctx, server_id: int):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        the_guild = self.bot.get_guild(server_id)
        total_nb_of_messages = 0
        global_stats = {}
        for channel in the_guild.text_channels:
            log(f"Je suis en train d'analyser le salon <#{channel.id}>...")
            messages_nb, stats = await get_channel_stat(channel)
            total_nb_of_messages += messages_nb
            global_stats = merge_dict(global_stats, stats)
        log("J'ai finis d'analyser, organisation des résultats...")
        res = f"Voici les résultats, le test a été effectué sur tout le serveur.\nLes personnes avec moins de 5 messages sont ignorées, les bots aussi."
        for name in global_stats:
            if global_stats[name] > 5:
                res += f"{name} a laissé {global_stats[name]} messages soit {round((100 * global_stats[name]) / total_nb_of_messages, 2)}%\n"
        log(res)
        await ctx.message.delete()

    @commands.command(name="getImages")
    async def get_images(self, ctx, user_id: int):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                print(f"je cherche dans {guild.name}/{channel.name}")
                for message in await channel.history(limit=None).flatten():
                    if message.author.id == user_id and len(message.attachments) != 0:
                        try:
                            os.makedirs(rf"getImages/{user_id}")
                        except FileExistsError:
                            pass
                        for att in message.attachments:
                            await att.save(f"getImages/{user_id}/{att.filename}")


