import interactions
from utils.functions import log


class Info(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        type=interactions.ApplicationCommandType.USER,
        name="Appuyez, c'est rigolo!"
    )
    async def rick(self, ctx: interactions.CommandContext):
        log("UN RICKROLL A ETE UTILISE!!!!!!!!!")
        await ctx.target.send("<https://www.youtube.com/watch?v=dQw4w9WgXcQ>")
        await ctx.send("C'est fait!", ephemeral=True)


def setup(client):
    Info(client)
