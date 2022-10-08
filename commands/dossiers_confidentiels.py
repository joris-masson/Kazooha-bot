import discord

from discord.ext import commands
from utils.functions import log
from discord_components import Select, SelectOption


class DossiersConfidentiels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="dossiersConfidentiels", aliases=["dc", "dossiers", "dossier", "dossierConfidentiel"])
    async def dossier_confidentiels(self, ctx):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        await ctx.message.delete()
        selector = await ctx.send(
            "Veuillez selectionner un dossier:",
            components=[
                Select(
                    placeholder="Liste des dossiers disponibles",
                    options=[
                        SelectOption(label="Alice", value="Alice"),
                        SelectOption(label="Dainsleif", value="Dainsleif"),
                        SelectOption(label="Paimon", value="Paimon"),
                        SelectOption(label="Rhinedottir", value="Rhinedottir"),
                        ]
                )
            ]
        )

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel and res.message.id == selector.id

        interaction = await self.bot.wait_for("select_option", check=check)

        await selector.delete()
        file = discord.File(f"data/dossiers/{interaction.values[0]}.png", filename=f"{interaction.values[0]}.png")
        embed = discord.Embed(title=f"Dossier confidentiel: {interaction.values[0]}")
        embed.set_image(url=f"attachment://{interaction.values[0]}.png")

        await ctx.send(file=file, embed=embed)
