from discord.ext import commands


class ShowArtifacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="arte", aliases=["artes"])
    async def show_artifacts(self, ctx):
        await ctx.message.reply(f"Par manque de temps||~~(flemme surtout)~~||, je ne possède pas ces infos dans ma base de données, mais ces infos sont disponibles ici: <https://genshin.honeyhunterworld.com/db/artifact/?lang=FR>")


