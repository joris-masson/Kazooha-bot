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
kazooha.load("commands.slash.showartifacts")
kazooha.load("commands.slash.showcollection")
kazooha.load("commands.slash.help")


@kazooha.command(
    type=interactions.ApplicationCommandType.USER,
    name="C'est qui ça?",
)
async def test(ctx: interactions.CommandContext):
    if ctx.user.id == 171028477682647040:
        await ctx.send(f"Bonjour admin!\nC'est {ctx.target.user.username}#{ctx.target.discriminator}!\nID: `{ctx.target.id}`", ephemeral=True)
    else:
        await ctx.send(f"C'est {ctx.target.user.username}!", ephemeral=True)

kazooha.start()
