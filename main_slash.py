import os
import interactions

from dotenv import load_dotenv
from discord_components import DiscordComponents


load_dotenv()  # prépare le chargement du token
TOKEN = os.getenv("TOKEN")  # charge le token

kazooha = interactions.Client(token=TOKEN)
DiscordComponents(kazooha)

kazooha.load('interactions.ext.files')

kazooha.load("commands.slash.idtotime")
kazooha.load("commands.slash.dossiers_confidentiels")
kazooha.load("commands.slash.showquestbooks")


@kazooha.command(
    type=interactions.ApplicationCommandType.USER,
    name="C'est qui ça?",
)
async def test(ctx):
    await ctx.send(f"C'est {ctx.target.user.username}!", ephemeral=True)

kazooha.start()
