import os

from dotenv import load_dotenv
from interactions import Client, Intents, Activity, Status, listen

load_dotenv()
TOKEN = os.getenv("TOKEN")

kazooha = Client(
    status=Status.ONLINE,
    activity=Activity("vous donner des infos sur le jeu."),
    intents=Intents.ALL
)


@listen()
async def on_ready():
    print("Bot prêt !")


kazooha.start(TOKEN)
