# imports des modules principaux
import os
import discord

# imports des modules secondaires
from discord.ext import commands
from discord_components import DiscordComponents
from dotenv import load_dotenv
from utils.functions import log

# imports des commandes
from commands import*

intents = discord.Intents.all()  # définit les permissions je crois
intents.members = True  # euh... je ne comprends pas pourquoi je dois le préciser alors que normalement elles y sont toutes

kazooha = commands.Bot(command_prefix=';', help_command=None, intents=intents)  # créé l'instance du bot
DiscordComponents(kazooha)  # fait en sorte que le bot puisse utiliser les composants

load_dotenv()  # prépare le chargement du token
TOKEN = os.getenv("TOKEN")  # charge le token

connected = False  # si le bot est connecté, pour éviter que les logs fassent n'importe quoi


# ----- events -----
@kazooha.event
async def on_connect():
    global connected
    connected = True
    log(f"{kazooha.user.name} est connecté!")


@kazooha.event
async def on_ready():
    for guild in kazooha.guilds:
        log(f"{kazooha.user.name} est prêt dans {guild.name}({guild.id})!")

    await kazooha.change_presence(status=discord.Status.online, activity=discord.Game(f"vous donner des infos sur le jeu"))  # Définit le jeu du bot


@kazooha.event
async def on_disconnect():
    global connected
    if connected:
        log(f"{kazooha.user.name} a été déconnecté de Discord")
        connected = False

# ----- commandes -----
kazooha.add_cog(ServerStat(kazooha))

kazooha.run(TOKEN)  # lance le bot
