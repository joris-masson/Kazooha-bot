import interactions
from utils.functions import log
from PIL import Image, ImageFont, ImageDraw


class SendText(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="send_text",
        description="Envoit du texte avec une police au choix sous forme d'image",
        options=[
            interactions.Option(
                name="texte",
                description="Le texte à envoyer",
                type=interactions.OptionType.STRING,
                required=True
            ),
            interactions.Option(
                name="police",
                description="La police à utiliser",
                type=interactions.OptionType.STRING,
                required=False
            )
        ]
    )
    async def send_text(self, ctx: interactions.CommandContext, texte: str, police: str="Tevyat"):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        image = Image.new("RGB", (500, 500), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(f"data/fonts/{police}.ttf", 30)
        draw.text((250, 250), texte, (0, 0, 0), font=font)
        image.save("data/out/text/oui.jpg")

        file = interactions.File("data/out/text/oui.jpg")
        embed = interactions.Embed(title=texte)
        embed.set_image(url=f"attachment://oui.jpg")
        await ctx.send(embeds=embed, files=file, ephemeral=True)



def setup(client):
    SendText(client)
