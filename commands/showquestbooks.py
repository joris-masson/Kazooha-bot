import discord

from discord.ext import commands
from discord_components import Select, SelectOption
from discord_components_paginator import Paginator, PaginatorStyle
from utils.functions import log


class ShowQuestBooks(commands.Cog):
    def __init__(self, bot: commands.Bot, dico_quest_books: dict):
        self.bot = bot
        self.dico_quest_books = dico_quest_books
        log(f"'{__name__}' initialisé")

    @commands.command(name="questBooks", aliases=["questBook", "qb"])
    async def show_quest_books(self, ctx):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        await ctx.message.delete()
        selector = await ctx.send(
            "Veuillez selectionner un livre:",
            components=[
                Select(
                    placeholder="Liste des livres de quêtes disponibles",
                    options=[
                        SelectOption(label="Avec les dieux - Prologue", value="Avec les dieux Prologue"),
                        SelectOption(label="Aventures en montagne et en mer", value="Aventures en montagne et en mer"),
                        SelectOption(label="Biographie de Gunnhildr", value="Biographie de Gunnhildr"),
                        SelectOption(label="Chroniques de Sangonomiya", value="Chroniques de Sangonomiya"),
                        SelectOption(label="Débat sur le « Vice-roi de l'Est »", value="Debat sur le Vice roi de l Est"),
                        SelectOption(label="Histoire des rois et des clans", value="Histoire des rois et des clans"),
                        SelectOption(label="Inscriptions sur tablettes de pierres - I", value="Inscriptions sur tablettes de pierres I"),
                        SelectOption(label="Journal épais", value="Journal epais"),
                        SelectOption(label="La vie de la prêtresse Mouun", value="La vie de la pretresse Mouun"),
                        SelectOption(label="Les Yakshas, Gardiens Adeptes", value="Les Yakshas Gardiens Adeptes"),
                        SelectOption(label="Mille ans de solitude", value="Mille ans de solitude"),
                        SelectOption(label="Perle précieuse", value="Perle precieuse"),
                        SelectOption(label="Premier disciple du clan Guhua", value="Premier disciple du clan Guhua"),
                        SelectOption(label="Versets d'equilibrium", value="Versets d equilibrium"),

                    ]
                )
            ]
        )

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel and res.message.id == selector.id

        interaction = await self.bot.wait_for("select_option", check=check)

        await selector.delete()

        the_book = interaction.values[0].lower().replace(' ', '_')

        embeds = [
            discord.Embed(title=f"{interaction.values[0]} - page {page}", description=self.dico_quest_books[the_book][page]) for page in range(1, len(self.dico_quest_books[the_book]) + 1)
        ]

        paginator = Paginator(self.bot, ctx, PaginatorStyle.FIVE_BUTTONS_WITH_COUNT, embeds)

        await paginator.start()
