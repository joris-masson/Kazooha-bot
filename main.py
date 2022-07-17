import os
import discord

from discord.ext import commands
from discord_components import DiscordComponents, Select, SelectOption
from discord_components_paginator import Paginator, PaginatorStyle
from dotenv import load_dotenv

from books import la_renarde_qui_nageait_dans_la_mer_de_pissenlits, anthologie_de_la_poesie_brutocollinus, la_melancolie_de_vera, collection_de_byakuyakoku, chroniques_d_un_ivrogne, ballade_de_l_ecuyer, archives_de_jueyun, anthologie_de_poemes_brutocollinus, fleurs_pour_la_princesse_fischl, princesse_neige_et_les_six_nains, foret_de_bambou_au_clair_de_lune, contes_de_l_allee_toki, coutumes_de_liyue, guide_de_voyage_en_teyvat, etude_des_coutumes_brutocollinus, nouvelles_chroniques_des_six_kitsunes, histoire_du_chevalier_errant, journal_d_un_inconnu, journal_de_l_aventurier_roald
from quest_books import avec_les_dieux_prologue, aventures_en_montagne_et_en_mer, biographie_de_gunnhildr, chroniques_de_sangonomiya, debat_sur_le_vice_roi_de_l_est, inscriptions_sur_tablettes_de_pierres_i, journal_d_inspection_ancien, journal_epais, la_vie_de_la_pretresse_mouun, les_yakshas_gardiens_adeptes, mille_ans_de_solitude, perle_precieuse, premier_disciple_du_clan_guhua, versets_d_equilibrium, histoire_des_rois_et_des_clans

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
    "etude_des_coutumes_brutocollinus": etude_des_coutumes_brutocollinus.book,
    "nouvelles_chroniques_des_six_kitsunes": nouvelles_chroniques_des_six_kitsunes.book,
    "histoire_du_chevalier_errant": histoire_du_chevalier_errant.book,
    "journal_d_un_inconnu": journal_d_un_inconnu.book,
    "journal_de_l_aventurier_roald": journal_de_l_aventurier_roald.book,
}

dico_quest_books = {
    "avec_les_dieux_prologue": avec_les_dieux_prologue.book,
    "aventures_en_montagne_et_en_mer": aventures_en_montagne_et_en_mer.book,
    "biographie_de_gunnhildr": biographie_de_gunnhildr.book,
    "chroniques_de_sangonomiya": chroniques_de_sangonomiya.book,
    "debat_sur_le_vice_roi_de_l_est": debat_sur_le_vice_roi_de_l_est.book,
    "inscriptions_sur_tablettes_de_pierres_i": inscriptions_sur_tablettes_de_pierres_i.book,
    "journal_d_inspection_ancien": journal_d_inspection_ancien.book,
    "journal_epais": journal_epais.book,
    "la_vie_de_la_pretresse_mouun": la_vie_de_la_pretresse_mouun.book,
    "les_yakshas_gardiens_adeptes": les_yakshas_gardiens_adeptes.book,
    "mille_ans_de_solitude": mille_ans_de_solitude.book,
    "perle_precieuse": perle_precieuse.book,
    "premier_disciple_du_clan_guhua": premier_disciple_du_clan_guhua.book,
    "versets_d_equilibrium": versets_d_equilibrium.book,
    "histoire_des_rois_et_des_clans": histoire_des_rois_et_des_clans.book
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
    global dico_quest_books

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

    interaction = await kazooha.wait_for("select_option")

    await selector.delete()

    the_book = interaction.values[0].lower().replace(' ', '_')
    print(f"Demande d'accès à {the_book}...\nAccès donné!")

    embeds = [
        discord.Embed(title=f"{interaction.values[0]} - page {page}", description=dico_quest_books[the_book][page]) for page in
        range(1, len(dico_quest_books[the_book]) + 1)
    ]

    paginator = Paginator(kazooha, ctx, PaginatorStyle.FIVE_BUTTONS_WITH_COUNT, embeds)

    await paginator.start()


@kazooha.command(name="collections")
async def show_collection(ctx):
    global dico_book

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
                    SelectOption(label="Histoire du chevalier errant", value="Histoire du chevalier errant"),
                    SelectOption(label="Journal d'un inconnu", value="Journal d un inconnu"),
                    SelectOption(label="Journal de l’aventurier Roald", value="Journal de l aventurier Roald"),

                    SelectOption(label="Fleurs pour la Princesse Fischl", value="Fleurs pour la Princesse Fischl"),
                    SelectOption(label="Forêt de bambou au clair de lune", value="Foret de bambou au clair de lune"),
                    SelectOption(label="La Mélancolie de Véra", value="La Melancolie de Vera"),
                    SelectOption(label="La Renarde qui nageait dans la mer de pissenlits", value="La Renarde qui nageait dans la mer de pissenlits"),
                    SelectOption(label="Nouvelles chroniques des six Kitsunes", value="Nouvelles chroniques des six Kitsunes"),
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
