import os

from interactions import Client, Intents, Activity, Status, listen
from dotenv import load_dotenv
from utils.util import log

load_dotenv()
TOKEN = os.getenv("TOKEN")

kazooha = Client(
    status=Status.ONLINE,
    activity=Activity("vous donner des infos sur le jeu."),
    intents=Intents.ALL
)

log("PRELOAD", "Chargement des extensions...")

# ---- events -----
log("PRELOAD", "Chargement des évènements...")
kazooha.load_extension("commands.event.leak")
kazooha.load_extension("commands.event.givemats")

# ----- context commands ----
log("PRELOAD", "Chargement des commandes de contexte...")
kazooha.load_extension("commands.context.contextuid")

# ----- slash commands -----
log("PRELOAD", "Chargement des commandes slash...")
kazooha.load_extension("commands.slash.dossiers")
kazooha.load_extension("commands.slash.idtotime")
# kazooha.load_extension("commands.slash.ia")
kazooha.load_extension("commands.slash.uid")
kazooha.load_extension("commands.slash.showbooks")
kazooha.load_extension("commands.slash.genshininfo")


@listen()
async def on_ready():
    log("LOG", "Bot prêt.")


log("PRELOAD", "Bot lancé.")
kazooha.start(TOKEN)
