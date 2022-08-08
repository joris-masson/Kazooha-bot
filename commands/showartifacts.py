import discord

from discord.ext import commands
from discord_components import Select, SelectOption
from discord_components_paginator import Paginator, PaginatorStyle
from utils.functions import log


class ShowArtifacts(commands.Cog):
    def __init__(self, bot, dico_artifacts: dict):
        self.bot = bot
        self.dico_artifacts = dico_artifacts
        log(f"'{__name__}' initialisé")

    @commands.command(name="arte", aliases=["artes"])
    async def show_artifacts(self, ctx, num: int):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        await ctx.message.delete()

        if num == 1:
            selector = await ctx.send(
                "Veuillez selectionner un livre:",
                components=[
                    Select(
                        placeholder="Liste des collections disponibles",
                        options=[
                            SelectOption(label="Aventurier", value="aventurier"),
                        ]
                    )
                ]
            )
        else:
            await ctx.send("Cette page n'existe pas(il y en a 1)")
            return

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel and res.message.id == selector.id

        interaction = await self.bot.wait_for("select_option", check=check)

        await selector.delete()

        the_book = interaction.values[0].lower().replace(' ', '_')

        embeds = [
            discord.Embed(title=f"{interaction.values[0]} - page {page}", description=self.dico_artifacts[the_book][page])
            for page in range(1, len(self.dico_artifacts[the_book]) + 1)
        ]

        paginator = Paginator(self.bot, ctx, PaginatorStyle.FIVE_BUTTONS_WITH_COUNT, embeds)

        await paginator.start()


