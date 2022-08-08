from discord.ext import commands
from utils.functions import log


class ShowArtifacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="arte", aliases=["artes"])
    async def show_artifacts(self, ctx):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        await ctx.message.reply(f"Par manque de temps||~~(flemme surtout)~~||, je ne possède pas ces infos dans ma base de données, mais ces infos sont disponibles ici: <https://genshin.honeyhunterworld.com/db/artifact/?lang=FR>")


