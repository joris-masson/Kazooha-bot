import os

import interactions.api.events
from interactions import Client, Intents, Activity, Status, listen
from dotenv import load_dotenv
from utils.util import log, open_db_connection

load_dotenv()
TOKEN = os.getenv("TOKEN")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")

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
kazooha.load_extension("commands.slash.send")


@listen()
async def on_ready():
    log("LOG", "Bot prêt.")


@kazooha.listen(event_name="on_message_create")
async def on_message_create(event: interactions.api.events.discord.MessageCreate):
    message_id = event.message.id
    author_id = event.message.author.id
    content = event.message.content

    db = open_db_connection()
    cursor = db.cursor()

    cursor.execute(f"INSERT INTO Kazooha.Message(id, discordUserId, content) VALUES ({message_id}, {author_id}, '{content}')")

    db.commit()

    cursor.close()
    db.close()


@kazooha.listen(event_name="on_message_delete")
async def on_message_delete(event: interactions.api.events.MessageDelete):
    log_channel = await kazooha.fetch_channel(LOG_CHANNEL_ID)

    embed = interactions.models.Embed(title=f"Message supprimé")

    try:
        embed.description = f"Le message de <@{event.message.author.id}> a été supprimé dans le salon <#{event.message.channel.id}>\n\n >>> {event.message.content}"
    except AttributeError:
        embed.description = f"Le message de quelqu'un a été supprimé dans le salon <#{event.message.channel.id}>\n\n *Message indisponible*"

    await log_channel.send(embeds=embed)


@kazooha.listen(event_name="on_message_update")
async def on_message_update(event: interactions.api.events.discord.MessageUpdate):
    log_channel = await kazooha.fetch_channel(LOG_CHANNEL_ID)

    embed = interactions.models.Embed(title=f"Message modifié")

    try:
        embed.description = f"Le message de <@{event.after.author.id}> a été modifié dans le salon <#{event.after.channel.id}>\n\n {event.before.content}\n __**en**__ \n{event.after.content}"
    except AttributeError:
        embed.description = f"Le message de quelqu'un a été modifié dans le salon <#{event.after.channel.id}>"

    await log_channel.send(embeds=embed)

log("PRELOAD", "Bot lancé.")
kazooha.start(TOKEN)
