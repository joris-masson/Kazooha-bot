from discord.ext import commands
from utils.functions import log
from saucenao_api import SauceNao


class DetectImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="detectImage")
    async def detect_image(self, ctx):
        sauce = SauceNao('43ae64cdd682d11da5561eff5bccdd0c9707789b')
        results = sauce.from_url(ctx.message.attachments[0].url)

        if results[0].similarity >= 70.0:
            await ctx.reply(f"Auteur: {results[0].author}\nSauce: <{results[0].urls[0]}>\nSimilarité: {results[0].similarity}%")
        else:
            await ctx.reply("Désolé, j'ai pas trouvé de sauce convaincante")


