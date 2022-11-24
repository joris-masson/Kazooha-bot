# prog par Dr.Emma(retire ça et jte pete les genoux)
import interactions
import os

from utils.func import save_attachment


class GenshinGeoguessr(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
        self.VERIF_CHANNEL = interactions.Channel
        self.base_message = interactions.Message
        self.demand_message = interactions.Message

    @interactions.extension_command(name="genshin_geoguessr", options=[interactions.Option(name="submit", description="Soumettre une photo d un lieu", type=interactions.OptionType.SUB_COMMAND), interactions.Option(name="guess", description="Soumettre votre idee de lieu present dans la photo", type=interactions.OptionType.SUB_COMMAND)])
    async def genshin_geoguessr(self, ctx: interactions.CommandContext, sub_command: str):
        if sub_command == "submit":
            await self.soumettre(ctx)
        elif sub_command == "guess":
            pass

    @interactions.extension_command(
        type=interactions.ApplicationCommandType.MESSAGE,
        name="Soumettre une image"
    )
    async def soumettre(self, ctx: interactions.CommandContext):
        """
        si image, envoie dans salon/fil dédie un message
        message: contient image et deux boutons(yes, no)
        bouton oui: enregistre dans un rep commun l image et des infos autour(auteur)
        //     non: envoie un dm à l auteur(ou ailleurs) pour annoncer refus
        """
        self.VERIF_CHANNEL = await interactions.get(self.client, interactions.Channel, object_id=1019989051496992839)
        if ctx.target.attachments[0].content_type.startswith("image"):
            self.base_message = ctx.target
            embed = interactions.Embed(
                title="Nouvelle image soumise!",
                description=f"Image soumise par: <@{ctx.target.author.id}>"
            )
            embed.set_image(url=ctx.target.attachments[0].url)

            button_accept = interactions.Button(
                label="Accepter",
                custom_id="but_accept",
                style=3
            )
            button_refuse = interactions.Button(
                label="Refuser",
                custom_id="but_refuse",
                style=4
            )
            self.demand_message = await self.VERIF_CHANNEL.send(embeds=embed, components=interactions.spread_to_rows(button_accept, button_refuse))
            await ctx.send("Cette image a bien été envoyée aux modérateurs", ephemeral=True)

    async def guess(self, ctx: interactions.CommandContext):
        """
        ctx doit contenir image de carte
        envoie dans salon/fil dedie l image et ping la personne l ayant proposee
        demerdez vous pour comparer les res de tout le monde
        """
        pass

    @interactions.extension_component("but_accept")
    async def accept_handler(self, ctx: interactions.ComponentContext):
        await ctx.send("Image acceptée", ephemeral=True)
        if not os.path.exists(f"data/games/geoguessr/submissions/{self.base_message.author.id}.png"):
            await save_attachment(self.client, self.base_message.attachments[0], f"data/games/geoguessr/submissions/{self.base_message.author.id}.png")
        else:
            for i in range(1, 101):
                if not os.path.exists(f"data/games/geoguessr/submissions/{self.base_message.author.id}_{i}.png"):
                    await save_attachment(self.client, self.base_message.attachments[0], f"data/games/geoguessr/submissions/{self.base_message.author.id}_{i}.png")
                    break
        await self.demand_message.delete()

    @interactions.extension_component("but_refuse")
    async def refuse_handler(self, ctx: interactions.ComponentContext):
        await ctx.send("Image refusée", ephemeral=True)
        await self.base_message.reply(content="Votre image n'a pas été retenue, voici les critères:\n*insérer critères...*")
        await self.demand_message.delete()


def setup(client):
    GenshinGeoguessr(client)
