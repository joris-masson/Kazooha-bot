import os

import interactions.api.events
from interactions import Client, Intents, Activity, Status, listen
from dotenv import load_dotenv
from utils.util import log, db_message_create, db_message_delete, db_message_update, db_get_message

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
    if not event.message.author.bot:
        db_message_create(event.message)


@kazooha.listen(event_name="on_message_delete")
async def on_message_delete(event: interactions.api.events.MessageDelete):
    if not event.message.author.bot:
        message = db_message_delete(event.message)
        log_channel = await kazooha.fetch_channel(LOG_CHANNEL_ID)

        embed = interactions.models.Embed(title=f"Message supprimé")

        try:
            embed.description = f"Le message de <@{event.message.author.id}> a été supprimé dans le salon <#{event.message.channel.id}>\n\n >>> {event.message.content}"
        except AttributeError:
            try:
                embed.description = f"Le message de <@{message[4]}> a été supprimé dans le salon <#{message[2]}>\n\n >>> {message[5]}"
            except TypeError:
                embed.description = f"Le message de quelqu'un a été supprimé dans le salon <#{message[2]}>\n\n *Message indisponible"

        await log_channel.send(embeds=embed)


@kazooha.listen(event_name="on_message_update")
async def on_message_update(event: interactions.api.events.discord.MessageUpdate):
    if not event.after.author.bot:
        messages = db_message_update(event.after)
        log_channel = await kazooha.fetch_channel(LOG_CHANNEL_ID)

        embed = interactions.models.Embed(title=f"Message modifié")

        try:
            embed.description = f"Le message de <@{event.after.author.id}> a été modifié dans le salon <#{event.after.channel.id}>\n\n {event.before.content}\n __**en**__ \n{event.after.content}"
        except AttributeError:
            try:
                message_before = messages[0]
                message_after = messages[1]
                embed.description = f"Le message de <@{message_after[4]}> a été modifié dans le salon <#{message_after[2]}>\n\n {message_before[5]}\n __**en**__ \n{message_after[5]}"
            except TypeError:
                embed.description = f"Le message de quelqu'un a été modifié dans le salon <#{event.after.channel.id}>\n\n *Comparaison indisponible*"

        await log_channel.send(embeds=embed)

log("PRELOAD", "Bot lancé.")
kazooha.start(TOKEN)
