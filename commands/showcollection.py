import discord

from discord.ext import commands
from discord_components import Select, SelectOption
from discord_components_paginator import Paginator, PaginatorStyle
from utils.functions import log


class ShowCollection(commands.Cog):
    def __init__(self, bot: commands.Bot, dico_books: dict):
        self.bot = bot
        self.dico_books = dico_books
        log(f"'{__name__}' initialisé")

    @commands.command(name="collections", aliases=["collection", "archives", "archive"])
    async def show_collection(self, ctx, num: int):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        await ctx.message.delete()

        if num == 1:
            selector = await ctx.send(
                "Veuillez selectionner un livre:",
                components=[
                    Select(
                        placeholder="Liste des collections disponibles",
                        options=[
                            SelectOption(label="Anthologie de la poésie Brutocollinus", value="Anthologie de la poesie Brutocollinus"),
                            SelectOption(label="Anthologie de poèmes Brutocollinus", value="Anthologie de poemes Brutocollinus"),
                            SelectOption(label="Archives de Jueyun", value="Archives de Jueyun"),
                            SelectOption(label="Ballade de l’écuyer", value="Ballade de l_ecuyer"),
                            SelectOption(label="Chroniques d’un ivrogne", value="Chroniques d_un ivrogne"),
                            SelectOption(label="Collection de Byakuyakoku", value="Collection de Byakuyakoku"),
                            SelectOption(label="Contes de l’Allée Toki", value="Contes de l_Allee Toki"),
                            SelectOption(label="Coutumes de Liyue", value="Coutumes de Liyue"),
                            SelectOption(label="Étude des coutumes Brutocollinus", value="etude des coutumes Brutocollinus"),
                            SelectOption(label="Fleurs pour la Princesse Fischl", value="Fleurs pour la Princesse Fischl"),
                            SelectOption(label="Forêt de bambou au clair de lune", value="Foret de bambou au clair de lune"),
                            SelectOption(label="Guide de voyage en Teyvat", value="Guide de voyage en Teyvat"),
                            SelectOption(label="Histoire du chevalier errant", value="Histoire du chevalier errant"),
                            SelectOption(label="Journal d'un inconnu", value="Journal d un inconnu"),
                            SelectOption(label="Journal de l’aventurier Roald", value="Journal de l aventurier Roald"),
                            SelectOption(label="Journal du vagabond", value="Journal du vagabond"),
                            SelectOption(label="L’Archon invisible", value="L Archon invisible"),
                            SelectOption(label="L’Épée solitaire du mont désolé", value="L epee solitaire du mont desole"),
                            SelectOption(label="La Brise de la Forêt", value="La Brise de la Foret"),
                            SelectOption(label="La Légende de Vennessa", value="La Legende de Vennessa"),
                            SelectOption(label="La Mélancolie de Véra", value="La Melancolie de Vera"),
                            SelectOption(label="La Princesse sanglier", value="La Princesse sanglier"),
                            SelectOption(label="La Renarde qui nageait dans la mer de pissenlits", value="La Renarde qui nageait dans la mer de pissenlits"),
                            SelectOption(label="La Tour de Mondstadt", value="La Tour de Mondstadt"),
                            SelectOption(label="Le Bris de l’arme divine", value="Le Bris de l arme divine"),
                        ]
                    )
                ]
            )
        elif num == 2:
            selector = await ctx.send(
                "Veuillez selectionner un livre:",
                components=[
                    Select(
                        placeholder="Liste des collections disponibles",
                        options=[
                            SelectOption(label="Le cœur de la source", value="Le coeur de la source"),
                            SelectOption(label="Les guerres d’Hamawaran", value="Les guerres d Hamawaran"),
                            SelectOption(label="Nouvelles chroniques des six Kitsunes", value="Nouvelles chroniques des six Kitsunes"),
                            SelectOption(label="Perle du cœur", value="Perle du coeur"),
                            SelectOption(label="Princesse Mina de la nation déchue", value="Princesse Mina de la nation dechue"),
                            SelectOption(label="Princesse Neige et les Six Nains", value="Princesse Neige et les Six Nains"),
                            SelectOption(label="Rêves brisés", value="Reves brises"),
                            SelectOption(label="Théories étranges du Kiyoshiken Shinkageuchi", value="Theories etranges du Kiyoshiken Shinkageuchi"),
                            SelectOption(label="Une légende d’épée", value="Une legende d epee"),
                        ]
                    )
                ]
            )
        else:
            await ctx.send("Cette page n'existe pas(il y en a 2)")
            return

        def check(res):
            return ctx.author == res.user and res.channel == ctx.channel and res.message.id == selector.id

        interaction = await self.bot.wait_for("select_option", check=check)

        await selector.delete()

        the_book = interaction.values[0].lower().replace(' ', '_')

        embeds = [
            discord.Embed(title=f"{interaction.values[0]} - page {page}", description=self.dico_books[the_book][page]) for page in range(1, len(self.dico_books[the_book]) + 1)
        ]

        paginator = Paginator(self.bot, ctx, PaginatorStyle.FIVE_BUTTONS_WITH_COUNT, embeds)

        await paginator.start()
