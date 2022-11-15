import interactions
from utils.functions import log
from utils.classes.imagemaker import ImageMaker
from datetime import datetime
from data.genshin_db import aptitudes_time


class GiveCharMats(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="afficher_persos_farmables",
        description="Affiche les personnages pouvant être farmés aujourd'hui!"
    )
    async def give_char_mats(self, ctx: interactions.CommandContext):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        ImageMaker(aptitudes_time[datetime.today().weekday()])  # créé l'image
        await ctx.send(files=interactions.File("data/out/final.png"), content="Les personnages dont vous pouvez farmer les aptitudes aujourd'hui sont:", ephemeral=True)


def setup(client):
    GiveCharMats(client)
