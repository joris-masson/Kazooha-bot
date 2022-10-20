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
                            SelectOption(label="Âme des profondeurs", value="Ame des profondeurs"),
                            SelectOption(label="Amour chéri", value="Amour cheri"),
                            SelectOption(label="Ancien rituel royal", value="Ancien rituel royal"),
                            SelectOption(label="Artiste Martial", value="Artiste martial"),
                            SelectOption(label="Aventurier", value="aventurier"),
                            SelectOption(label="Bande Vagabonde", value="Bande vagabonde"),
                            SelectOption(label="Berserker", value="Berserker"),
                            SelectOption(label="Briseur de glace", value="Briseur de glace"),
                            SelectOption(label="Chanceux", value="Chanceux"),
                            SelectOption(label="Chevalerie ensanglantée", value="Chevalerie ensanglantee"),
                            SelectOption(label="Coeur du brave", value="Coeur du brave"),
                            SelectOption(label="Coeur du gardien", value="Coeur du gardien"),
                            SelectOption(label="Coeur du voyageur", value="coeur_du_voyageur"),
                            SelectOption(label="Colère du tonnerre", value="Colere du tonerre"),
                            SelectOption(label="Coquille des rêves opulents", value="Coquille des reves opulents"),
                            SelectOption(label="Dompteur de foudre", value="Dompteur de foudre"),
                            SelectOption(label="Echos d'une offrande", value="Echos d une offrande"),
                            SelectOption(label="Erudit", value="Erudit"),
                            SelectOption(label="Instructeur", value="Instruteur"),
                            SelectOption(label="Marcheur du feu", value="Marcheur du feu"),
                            SelectOption(label="Médecin itinérant", value="Medecin itinerant"),
                            SelectOption(label="Miracle", value="Miracle"),
                            SelectOption(label="Ombre de la Verte Chasseuse", value="Ombre de la Verte Chasseuse"),
                            SelectOption(label="Palourde aux teintes océaniques", value="Palourde aux teintes oceaniques"),
                            SelectOption(label="Parieur", value="Parieur"),
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
                            SelectOption(label="Rêve Doré", value="Reve Dore"),
                            SelectOption(label="Rideau du Gladiateur", value="Rideu du Gladiateur"),
                            SelectOption(label="Roche ancienne", value="Roche ancienne"),
                            SelectOption(label="Sorcière des flammes", value="Sorciere des flammes"),
                            SelectOption(label="Souvenir de forêt", value="Souvenir de foret"),
                            SelectOption(label="Ténacité du Millelithe", value="Tenacite du Millelithe"),
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

        embeds = []
        for page in range(1, len(self.dico_artifacts[the_book]) + 1):
            embed = discord.Embed(title=f"{interaction.values[0]} - page {page}", description=self.dico_artifacts[the_book][page])
            embed.set_thumbnail(url=f"http://176.159.155.219:53134/images/artifacts/icons/{interaction.values[0]}/{page}.png")
            embeds.append(embed)

        paginator = Paginator(self.bot, ctx, PaginatorStyle.FIVE_BUTTONS_WITH_COUNT, embeds)

        await paginator.start()


