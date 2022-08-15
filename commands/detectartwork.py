from discord.ext import commands
from utils.functions import log
from saucenao_api import SauceNao


class DetectArtwork(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="detect")
    async def detect_artwork(self, ctx, link: str):
        if link[0] == '<':
            link = link[1:-1]
        sauce = SauceNao('43ae64cdd682d11da5561eff5bccdd0c9707789b')
        results = sauce.from_url(link)

        if results[0].similarity >= 70.0:
            await ctx.reply(f"Auteur: {results[0].author}\nSauce: <{results[0].urls[0]}>\nSimilarité: {results[0].similarity}%")
        else:
            await ctx.reply("Désolé, j'ai pas trouvé de sauce convaincante")


