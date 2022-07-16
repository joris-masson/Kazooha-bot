import os
import discord

from discord.ext import commands
from discord_components import DiscordComponents, Select, SelectOption
from discord_components_paginator import Paginator, PaginatorStyle
from dotenv import load_dotenv

from books import la_renarde_qui_nageait_dans_la_mer_de_pissenlits, anthologie_de_la_poesie_brutocollinus, la_melancolie_de_vera, collection_de_byakuyakoku, chroniques_d_un_ivrogne, ballade_de_l_ecuyer, archives_de_jueyun, anthologie_de_poemes_brutocollinus, fleurs_pour_la_princesse_fischl, princesse_neige_et_les_six_nains, foret_de_bambou_au_clair_de_lune, contes_de_l_allee_toki, coutumes_de_liyue, guide_de_voyage_en_teyvat, etude_des_coutumes_brutocollinus

dico_book = {
    "la_renarde_qui_nageait_dans_la_mer_de_pissenlits": la_renarde_qui_nageait_dans_la_mer_de_pissenlits.book,
    "anthologie_de_poemes_brutocollinus": anthologie_de_poemes_brutocollinus.book,
    "la_melancolie_de_vera": la_melancolie_de_vera.book,
    "collection_de_byakuyakoku": collection_de_byakuyakoku.book,
    "chroniques_d_un_ivrogne": chroniques_d_un_ivrogne.book,
    "anthologie_de_la_poesie_brutocollinus": anthologie_de_la_poesie_brutocollinus.book,
    "ballade_de_l_ecuyer": ballade_de_l_ecuyer.book,
    "archives_de_jueyun": archives_de_jueyun.book,
    "fleurs_pour_la_princesse_fischl": fleurs_pour_la_princesse_fischl.book,
    "foret_de_bambou_au_clair_de_lune": foret_de_bambou_au_clair_de_lune.book,
    "princesse_neige_et_les_six_nains": princesse_neige_et_les_six_nains.book,
    "contes_de_l_allee_toki": contes_de_l_allee_toki.book,
    "coutumes_de_liyue": coutumes_de_liyue.book,
    "guide_de_voyage_en_teyvat": guide_de_voyage_en_teyvat.book,
    "etude_des_coutumes_brutocollinus": etude_des_coutumes_brutocollinus.book
}

dico_quest_books = {

}

kazooha = commands.Bot(command_prefix=";", help_command=None)
DiscordComponents(kazooha)

load_dotenv()
TOKEN = os.getenv("TOKEN")


@kazooha.event
async def on_ready():
    print(f'{kazooha.user.name} s\'est connecté à Discord')
    await kazooha.change_presence(status=discord.Status.online, activity=discord.Game("être mis à jour..."))  # Défini le jeu du bot


@kazooha.command(name="questBooks")
async def show_quest_books(ctx):
    pass


@kazooha.command(name="collections")
async def show_collection(ctx):
    global dico_book, dico_quest_books

    await ctx.message.delete()

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
                    SelectOption(label="Guide de voyage en Teyvat", value="Guide de voyage en Teyvat"),

                    SelectOption(label="Fleurs pour la Princesse Fischl", value="Fleurs pour la Princesse Fischl"),
                    SelectOption(label="Forêt de bambou au clair de lune", value="Foret de bambou au clair de lune"),
                    SelectOption(label="La Mélancolie de Véra", value="La Melancolie de Vera"),
                    SelectOption(label="La Renarde qui nageait dans la mer de pissenlits", value="La Renarde qui nageait dans la mer de pissenlits"),
                    SelectOption(label="Princesse Neige et les Six Nains", value="Princesse Neige et les Six Nains")
                ]
            )
        ]
    )

    interaction = await kazooha.wait_for("select_option")

    await selector.delete()

    the_book = interaction.values[0].lower().replace(' ', '_')
    print(f"Demande d'accès à {the_book}...\nAccès donné!")

    embeds = [
        discord.Embed(title=f"{interaction.values[0]} - page {page}", description=dico_book[the_book][page]) for page in range(1, len(dico_book[the_book]) + 1)
    ]

    paginator = Paginator(kazooha, ctx, PaginatorStyle.FIVE_BUTTONS_WITH_COUNT, embeds)

    await paginator.start()

kazooha.run(TOKEN)
