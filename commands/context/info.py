import interactions
from utils.functions import log


class Info(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        type=interactions.ApplicationCommandType.USER,
        name="C'est qui ça?",
    )
    async def info(self, ctx: interactions.CommandContext):
        log(f"Des infos sur {ctx.target.user.username} ont été demandées par {ctx.user.username}")
        if ctx.user.id == 171028477682647040:
            await ctx.send(
                f"C'est {ctx.target.user.username}#{ctx.target.discriminator}!\nID: `{ctx.target.id}\navatar_url: {ctx.target.avatar_url}`", ephemeral=True)
        else:
            await ctx.send(f"C'est {ctx.target.user.username}!", ephemeral=True)


def setup(client):
    Info(client)
