import os
import interactions

from dotenv import load_dotenv
# from discord_components import DiscordComponents
from utils.func import detect_message, save_attachment
from utils.database import *
from utils.functions import remove_emojis
from datetime import datetime

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
# DiscordComponents(kazooha)


kazooha.load('interactions.ext.files')

kazooha.load("commands.context.info")
kazooha.load("commands.context.rickroll")
# kazooha.load("commands.context.guess")

kazooha.load("commands.slash.idtotime")
kazooha.load("commands.slash.dossiers_confidentiels")
kazooha.load("commands.slash.showartifacts")
kazooha.load("commands.slash.showbetaartifacts")
# kazooha.load("commands.slash.genshingeoguessr")
kazooha.load("commands.slash.concours")
kazooha.load("commands.slash.showbooks")
kazooha.load("commands.slash.givemats")
kazooha.load("commands.slash.sendtext")
kazooha.load("commands.slash.help")
kazooha.load("commands.slash.admin")


@kazooha.event
async def on_message_create(msg: interactions.Message):

    # ma_led.set_color("cyan")
    await detect_message(msg, kazooha)
    if msg.type == interactions.MessageType.CHANNEL_PINNED_MESSAGE:
        await msg.delete()
    # elif msg.content.startswith("!guess") and len(msg.attachments) == 1 and msg.attachments[0].content_type.startswith("image"):
        # await guess(msg)
    # elif msg.content.startswith("!guess") and len(msg.attachments) != 1:
        # await msg.reply("il faut une image dans votre message")

    # ma_led.stop()


@kazooha.event
async def on_message_update(a, msg: interactions.Message):
    if not is_in_messages(int(msg.id)):
        await insert_message(msg, modified=True)
    else:
        msg_content = remove_emojis(msg.content)
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(f"UPDATE Messages SET content='{msg_content}', modified='1' WHERE id='{msg.id}'")
        db.commit()
        cursor.close()
        db.close()


@kazooha.event
async def on_message_delete(msg: interactions.Message):
    db = open_connection()
    cursor = db.cursor()
    cursor.execute(f"UPDATE Messages SET deleted='1' WHERE id='{msg.id}'")
    db.commit()
    cursor.close()
    db.close()


"""
async def guess(msg: interactions.Message):
    send_channel = await interactions.get(kazooha, interactions.Channel, object_id=int(os.getenv("SEND_CHANNEL")))
    embed = interactions.Embed(
        title="Nouveau guess soumis!",
        description=f"Soumis par: <@{msg.author.id}>"
    )
    ze_file = interactions.File(await save_attachment(kazooha, msg.attachments[0], f"data/games/geoguessr/guess/{msg.author.username}/{datetime.now().day}"))
    # TODO trouver comment récupérer le nom de l'image
    embed.set_image(url=f"attachment://{}")
    await send_channel.send(embeds=embed)
    await msg.reply(f"<@{msg.author.id}>", embeds=interactions.Embed(title="Votre guess a bien été envoyée aux modérateurs"))
    await msg.delete()
"""

kazooha.start()
