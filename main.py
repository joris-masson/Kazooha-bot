# imports des modules principaux
import os
import discord

# imports des modules secondaires
from discord.ext import commands
from discord_components import DiscordComponents
from dotenv import load_dotenv
from utils.functions import log

# données additionnelles
from data.dico_quest_books import dico_quest_books
from data.dico_books import dico_books
from data.dico_artifacts import dico_artifacts

# imports des commandes
from commands import*

intents = discord.Intents.all()  # définis les permissions je crois
intents.members = True  # euh... je comprends pas pourquoi je dois le préciser alors que normalement elles y sont toutes

kazooha = commands.Bot(command_prefix=";", help_command=None, intents=intents)  # créé l'instance du bot
DiscordComponents(kazooha)  # fait en sorte que le bot puisse utiliser les composants

load_dotenv()  # prépare le chargement du token
TOKEN = os.getenv("TOKEN")  # charge le token

launched = False  # si la commande pour afficher les livres est lancée
maintenance = False  # si le bot est en maintenance


# ----- events -----
@kazooha.event
async def on_ready():
    global maintenance

    log(f'{kazooha.user.name} s\'est connecté à Discord')
    if maintenance:
        await kazooha.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"être mis à jour"))  # Défini le jeu du bot
    else:
        await kazooha.change_presence(status=discord.Status.online, activity=discord.Game(f"vous donner des infos sur le jeu"))  # Défini le jeu du bot


# ----- commandes -----
kazooha.add_cog(ShowArtifacts(kazooha, dico_artifacts))
kazooha.add_cog(ShowCollection(kazooha, dico_books))
kazooha.add_cog(ShowQuestBooks(kazooha, dico_quest_books))
kazooha.add_cog(Help(kazooha))
kazooha.add_cog(IdToTime(kazooha))
kazooha.add_cog(ServerStat(kazooha))
kazooha.add_cog(Magie(kazooha))


kazooha.run(TOKEN)  # lance le bot
