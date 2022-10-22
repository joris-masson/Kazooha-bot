import discord
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
        help_embed = discord.Embed(title="__Aide pour Kazooha__", description="Voici un petit recap des commandes du bot")

        help_embed.add_field(name="__**Afficher les artéfacts**__", value="""
        Nom de la commande: `arte` ou `artes`
        Paramètre: `numero_de_page`
        Valeurs possibles pour `numero_de_page`: `1` ou `2`
        
        Exemples: `artes 1` | `arte 2`
        """, inline=False)

        help_embed.add_field(name="__**Afficher les livres des archives**__", value="""
        Nom de la commande: `collections` ou `collection` ou `archives` ou `archive`
        Paramètre: `numero_de_page`
        Valeurs possibles pour `numero_de_page`: `1` ou `2`
        
        Exemples: `collections 1` | `archive 2`
        """, inline=False)

        help_embed.add_field(name="__**Afficher les livres de quêtes**__", value="""
        Nom de la commande: `questBooks` ou `questBook` ou `qb`
        
        Exemples: `qb` | `questBook`
        """, inline=False)

        help_embed.add_field(name="__**Afficher un dossier confidentiel**__", value="""
        Nom de la commande: `dossiersConfidentiels` ou `dossierConfidentiel` ou `dossiers` ou `dossier` ou `dc`
        
        Exemples: `dossiersConfidentiels` | `dc` | `dossiers`
        """, inline=False)

        await ctx.send(embed=help_embed)
