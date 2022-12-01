import os

import interactions
from utils.functions import log
from dotenv import load_dotenv


class Guess(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        load_dotenv()
        self.client: interactions.Client = client

    @interactions.extension_command(
        type=interactions.ApplicationCommandType.MESSAGE,
        name="Guess",
        scope=os.getenv("GENSHIN_GEOGUESSR_GUILD")
    )
    async def guess(self, ctx: interactions.CommandContext):
        log(f"guess utilisé")
        if ctx.user.id == 171028477682647040:
            send_channel = await interactions.get(self.client, interactions.Channel,  object_id=int(os.getenv("SEND_CHANNEL")))
            embed = interactions.Embed(
                title="Nouveau guess soumis!",
                description=f"Soumis par: <@{ctx.target.author.id}>"
            )
            embed.set_image(url=ctx.target.attachments[0].url)
            await send_channel.send(embeds=embed)
            await ctx.target.reply(f"<@{ctx.target.author.id}>", embeds=interactions.Embed(title="Votre guess a bien été envoyée aux modérateurs"))
            await ctx.target.delete()
        else:
            await ctx.send("Vous n'êtes pas autorisé à utiliser cette commande", ephemeral=True)


def setup(client):
    Guess(client)
