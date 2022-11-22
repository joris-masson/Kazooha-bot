import interactions
from utils.functions import log
from utils.classes.imagemaker import ImageMaker
from datetime import datetime
from data.genshin_db import aptitudes_time, weapons_time


class GiveMats(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="afficher_farmables",
        options=[
            interactions.Option(
                name="persos",
                description="Affiche les personnages pouvant être farmés aujourd'hui!",
                type=interactions.OptionType.SUB_COMMAND
            ),
            interactions.Option(
                name="armes",
                description="Affiche les matériaux d'armes pouvant être farmés aujourd'hui!",
                type=interactions.OptionType.SUB_COMMAND
            ),
        ],
    )
    async def give_mats(self, ctx: interactions.CommandContext, sub_command: str):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")

        image_name = ""
        embed_title = ""

        if sub_command == "persos":
            ImageMaker(aptitudes_time[datetime.today().weekday()], mode=0)  # créé l'image
            image_name = "final"
            embed_title = "Les personnages dont vous pouvez farmer les aptitudes aujourd'hui"
        elif sub_command == "armes":
            ImageMaker(weapons_time[datetime.today().weekday()], mode=1)  # créé l'image
            image_name = "final_w"
            embed_title = "Les armes dont vous pouvez farmer les matériaux aujourd'hui"

        file = interactions.File(f"data/out/{image_name}.png")
        embed = interactions.Embed(title=embed_title)
        embed.set_image(url=f"attachment://{image_name}.png")
        await ctx.send(embeds=embed, files=file, ephemeral=True)


def setup(client):
    GiveMats(client)
