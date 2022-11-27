# prog par Dr.Emma(retire ça et jte pete les genoux)
import interactions

from utils.classes.demandchannel import DemandChannel
from interactions.ext.tasks import IntervalTrigger, create_task


class GenshinGeoguessr(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
        self.demand_channels = []
        self.guess_channel = interactions.Channel

        self.method = create_task(IntervalTrigger(1))(self.method)
        self.method.start()

    @interactions.extension_command(
        name="genshin_geoguessr",
        options=[
            interactions.Option(
                name="soumettre_nouvelle_image",
                description="Soumettre une photo d'un lieu",
                type=interactions.OptionType.SUB_COMMAND
            )
        ]
    )
    async def genshin_geoguessr(self, ctx: interactions.CommandContext, sub_command: str):
        if sub_command == "soumettre_nouvelle_image":
            await self.soumettre(ctx)

    async def soumettre(self, ctx: interactions.CommandContext):
        """
        si image, envoie dans salon/fil dédie un message
        message: contient image et deux boutons(yes, no)
        bouton oui: enregistre dans un rep commun l image et des infos autour(auteur)
        //     non: envoie un dm à l auteur(ou ailleurs) pour annoncer refus
        """
        verif_channel = await ctx.channel.create_thread(f"{ctx.author.id}", type=interactions.ChannelType.PRIVATE_THREAD)
        le_salon_de_demande = DemandChannel(self.client, ctx, verif_channel)
        await le_salon_de_demande.send_demand_msg()
        self.demand_channels.append(le_salon_de_demande)

    @interactions.extension_component("but_accept")
    async def accept_handler(self, ctx: interactions.ComponentContext):
        await ctx.send("Image acceptée", ephemeral=True)
        await self.delete_demand_channel(int(ctx.channel.name))

    @interactions.extension_component("but_refuse")
    async def refuse_handler(self, ctx: interactions.ComponentContext):
        await ctx.send("Image refusée", ephemeral=True)
        await self.delete_demand_channel(int(ctx.channel.name))

    async def delete_demand_channel(self, author_id: int):
        for demand_channel in self.demand_channels:
            if demand_channel.ID == author_id:
                await demand_channel.delete()
                self.demand_channels.remove(demand_channel)

    async def method(self):
        channel = await interactions.get(self.client, interactions.Channel, object_id=1046409306729353336)
        await channel.send("<@783075596280004659> c'est cadeau")


def setup(client):
    GenshinGeoguessr(client)
