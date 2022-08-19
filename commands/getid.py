from discord.ext import commands
from utils.functions import log


class GetId(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="getId", aliases=["id"])
    async def id_to_time(self, ctx):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        message = f"Voici les IDs des objets présents dans ce message:\n" \
                  f"-Guilde: {ctx.guild.id}\n" \
                  f"Salon: {ctx.channel.id}\n" \
                  f"-Auteur: {ctx.message.author.id}\n" \
                  f"-Message: {ctx.message.id}\n"
        for mention in ctx.message.mentions:
            message += f"-Mention: {mention.id}\n"
        print(message)
        print(ctx.message.content)
