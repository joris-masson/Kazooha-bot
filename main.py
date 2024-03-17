import os

from interactions import Client, Intents, Activity, Status, listen
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

kazooha = Client(
    status=Status.DND,
    activity=Activity("être mis à jour très fort"),
    intents=Intents.ALL
)


@listen()
async def on_ready():
    print("Le bot est prêt !")


kazooha.start(TOKEN)
