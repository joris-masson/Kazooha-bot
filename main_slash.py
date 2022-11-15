import os
import interactions

from dotenv import load_dotenv
from discord_components import DiscordComponents
from utils.func import detect_message
from utils.classes.recherche import Recherche
from utils.classes.ledrgb import LedRgb
from utils.functions import log


load_dotenv()  # prépare le chargement du token
TOKEN = os.getenv("TOKEN")  # charge le token

kazooha = interactions.Client(token=TOKEN, intents=interactions.Intents.ALL)
DiscordComponents(kazooha)

ma_led = LedRgb(16, 20, 26)  # définition de la led

kazooha.load('interactions.ext.files')

kazooha.load("commands.slash.idtotime")
kazooha.load("commands.slash.dossiers_confidentiels")
kazooha.load("commands.slash.showquestbooks")
kazooha.load("commands.slash.showartifacts")
kazooha.load("commands.slash.showcollection")
kazooha.load("commands.slash.givecharmats")
kazooha.load("commands.slash.help")


@kazooha.event
async def on_message_create(msg: interactions.Message):
    ma_led.set_color("cyan")
    await detect_message(msg, kazooha)
    # await Recherche(msg, kazooha, ma_led).reply_with_sauce()
    ma_led.stop()


@kazooha.command(
    type=interactions.ApplicationCommandType.USER,
    name="C'est qui ça?",
)
async def test(ctx: interactions.CommandContext):
    if ctx.user.id == 171028477682647040:
        await ctx.send(f"Bonjour admin!\nC'est {ctx.target.user.username}#{ctx.target.discriminator}!\nID: `{ctx.target.id}`", ephemeral=True)
    else:
        await ctx.send(f"C'est {ctx.target.user.username}!", ephemeral=True)


@kazooha.command(
    type=interactions.ApplicationCommandType.USER,
    name="Appuyez, c'est rigolo!"
)
async def rick(ctx: interactions.CommandContext):
    log("UN RICKROLL A ETE UTILISE!!!!!!!!!")
    await ctx.target.send("<https://urlz.fr/4nf>")
    await ctx.send("C'est fait!", ephemeral=True)

kazooha.start()
