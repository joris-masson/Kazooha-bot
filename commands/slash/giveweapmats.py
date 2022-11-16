import interactions
from utils.functions import log
from utils.classes.imagemaker import ImageMaker
from datetime import datetime
from data.genshin_db import weapons_time


class GiveWeapMats(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="afficher_armes_farmables",
        description="Affiche les matériaux d'armes pouvant être farmés aujourd'hui!"
    )
    async def give_weap_mats(self, ctx: interactions.CommandContext):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        ImageMaker(weapons_time[datetime.today().weekday()], mode=1)  # créé l'image
        file = interactions.File("data/out/final_w.png")
        embed = interactions.Embed(title="Les armes dont vous pouvez farmer les matériaux aujourd'hui")
        embed.set_image(url="attachment://final_w.png")
        await ctx.send(embeds=embed, files=file, ephemeral=True)


def setup(client):
    GiveWeapMats(client)
