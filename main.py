# imports des modules principaux
import os
import discord

# imports des modules secondaires
from discord.ext import commands
from discord_components import DiscordComponents
from dotenv import load_dotenv
from utils.functions import log
from utils.func import detect_message
from utils.classes.recherche import Recherche

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

maintenance = False  # si le bot est en maintenance
connected = False  # si le bot est connecté, pour éviter que les logs fassent n'importe quoi


# ----- events -----
@kazooha.event
async def on_connect():
    global connected

    connected = True
    log(f'{kazooha.user.name} est connecté!')


@kazooha.event
async def on_ready():
    global maintenance

    for guild in kazooha.guilds:
        log(f"{kazooha.user.name} est prêt dans {guild.name}({guild.id})!")

    if maintenance:
        await kazooha.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(f"être mis à jour"))  # Défini le jeu du bot
    else:
        await kazooha.change_presence(status=discord.Status.online, activity=discord.Game(f"vous donner des infos sur le jeu"))  # Défini le jeu du bot


@kazooha.event
async def on_disconnect():
    global connected
    if connected:
        log(f"{kazooha.user.name} a été déconnecté de Discord")
        connected = False


@kazooha.event
async def on_message(msg: discord.Message):
    global kazooha
    await Recherche(msg, kazooha).reply_with_sauce()
    await kazooha.process_commands(msg)

# ----- commandes -----
kazooha.add_cog(ShowArtifacts(kazooha, dico_artifacts))
kazooha.add_cog(ShowCollection(kazooha, dico_books))
kazooha.add_cog(ShowQuestBooks(kazooha, dico_quest_books))
kazooha.add_cog(Help(kazooha))
kazooha.add_cog(IdToTime(kazooha))
kazooha.add_cog(ServerStat(kazooha))
kazooha.add_cog(Magie(kazooha))
kazooha.add_cog(GetId(kazooha))
#  kazooha.add_cog(Vote(kazooha))
kazooha.add_cog(SendLink(kazooha))

kazooha.run(TOKEN)  # lance le bot
