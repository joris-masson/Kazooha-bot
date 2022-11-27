import os
import interactions

from dotenv import load_dotenv
from discord_components import DiscordComponents
from utils.func import detect_message
from datetime import datetime
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
#kazooha.load("commands.slash.genshingeoguessr")
kazooha.load("commands.slash.showbooks")
kazooha.load("commands.slash.givemats")
kazooha.load("commands.slash.help")


@kazooha.event
async def on_message_create(msg: interactions.Message):
    # ma_led.set_color("cyan")
    await detect_message(msg, kazooha)
    if msg.content.startswith("!guess") and len(msg.attachments) == 1 and msg.attachments[0].content_type.startswith("image"):
        await guess(msg)
    elif msg.content.startswith("!guess") and len(msg.attachments) != 1:
        await msg.reply("il faut une image dans votre message")

    # ma_led.stop()


async def guess(msg: interactions.Message):
    send_channel = await interactions.get(kazooha, interactions.Channel, object_id=1046076775442174033)
    embed = interactions.Embed(
        title="Nouveau guess soumis!",
        description=f"Soumis par: <@{msg.author.id}>"
    )
    embed.set_image(url=msg.attachments[0].url)
    await send_channel.send(embeds=embed)
    await msg.reply(f"<@{msg.author.id}>", embeds=interactions.Embed(title="Votre guess a bien été envoyée aux modérateurs"))
    await msg.delete()


kazooha.start()
