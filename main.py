import os
import interactions

from dotenv import load_dotenv
from discord_components import DiscordComponents
from utils.func import detect_message
from utils.classes.ledrgb import LedRgb

load_dotenv()  # prépare le chargement du token
TOKEN = os.getenv("TOKEN")  # charge le token

kazooha = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.ALL,
    presence=interactions.ClientPresence(
        status=interactions.StatusType.ONLINE,
        activities=[
            interactions.PresenceActivity(
                name="vous donner des infos sur le jeu",
                type=interactions.PresenceActivityType.GAME
            )
        ]
    )
)
DiscordComponents(kazooha)

# ma_led = LedRgb(16, 20, 26)  # définition de la led


kazooha.load('interactions.ext.files')

kazooha.load("commands.context.info")
kazooha.load("commands.context.rickroll")

kazooha.load("commands.slash.idtotime")
kazooha.load("commands.slash.dossiers_confidentiels")
kazooha.load("commands.slash.showartifacts")
kazooha.load("commands.slash.showbetaartifacts")
# kazooha.load("commands.slash.genshingeoguessr")
kazooha.load("commands.slash.showbooks")
kazooha.load("commands.slash.givemats")
kazooha.load("commands.slash.help")


@kazooha.event
async def on_message_create(msg: interactions.Message):
    # ma_led.set_color("cyan")
    await detect_message(msg, kazooha)
    # ma_led.stop()

kazooha.start()
