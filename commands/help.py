from discord.ext import commands
from utils.functions import log


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="help", aliases=["aide"])
    async def help_command(self, ctx):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        await ctx.message.delete()
        await ctx.send("""Bonjour, je suis le bot Kazooha, voici ma description:

    Celui-ci te permettra de lire les livres disponibles en jeu (Genshin Impact si jamais), directement sur discord !
    Voici les commandes :
    -Pour les livres des archives
    `;collections 1`
    `;collections 2`

    => alternatives : `;archives` / `;archive` / `;collection` fonctionnent également, toujours suivi des chiffres 1 ou 2
    Pour les livres de quête/inventaire
    `;questBooks`

    => alternatives : `;questBook` / `;qb`""")


