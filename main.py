import os

from interactions import Client, Intents, Activity, Status, listen
from dotenv import load_dotenv
from utils.util import log

load_dotenv()
TOKEN = os.getenv("TOKEN")

kazooha = Client(
    status=Status.DND,
    activity=Activity("être mis à jour très fort"),
    intents=Intents.ALL
)

log("PRELOAD", "Chargement des extensions...")

log("PRELOAD", "Chargement des commandes de contexte...")
kazooha.load_extension("commands.context.uid")

log("PRELOAD", "Chargement des évènements...")
kazooha.load_extension("commands.event.leak")

log("PRELOAD", "Chargement des commandes slash...")
kazooha.load_extension("commands.slash.dossiers")
kazooha.load_extension("commands.slash.idtotime")
# kazooha.load_extension("commands.slash.ia")
kazooha.load_extension("commands.slash.uid")
# kazooha.load_extension("commands.slash.test")


@listen()
async def on_ready():
    log("LOG", "Bot prêt.")


log("PRELOAD", "Bot lancé.")
kazooha.start(TOKEN)
