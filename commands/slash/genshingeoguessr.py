# prog par Dr.Emma(retire ça et jte pete les genoux)
import os

import interactions

from utils.classes.demandchannel import DemandChannel
from utils.func import save_attachment
from interactions.ext.tasks import IntervalTrigger, create_task
from random import randint
from datetime import datetime


class GenshinGeoguessr(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
        self.demand_channels = []
        self.guess_channel = interactions.Channel

        self.method = create_task(IntervalTrigger(1800))(self.method)
        self.method.start()

        self.start_hour = 21

    @interactions.extension_command(
        name="genshin_geoguessr",
        options=[
            interactions.Option(
                name="soumettre_nouvelle_image",
                description="Soumettre une photo d'un lieu",
                type=interactions.OptionType.SUB_COMMAND
            )
        ],
        scope=952557533514592286
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
        demand_channel = self.get_demand_channel(int(ctx.channel.name))
        image_message = await self.get_image_message(demand_channel, )
        await ctx.send("Image acceptée", ephemeral=True)
        if not os.path.exists(f"data/games/geoguessr/submissions/{demand_channel.ctx.author.id}.png"):
            await save_attachment(self.client, image_message.attachments[0], f"data/games/geoguessr/submissions/{demand_channel.ctx.author.id}.png")
        else:
            for i in range(1, 101):
                if not os.path.exists(f"data/games/geoguessr/submissions/{demand_channel.ctx.author.id}_{i}.png"):
                    await save_attachment(self.client, image_message.attachments[0], f"data/games/geoguessr/submissions/{demand_channel.ctx.author.id}_{i}.png")
                    break
        await self.delete_demand_channel(int(ctx.channel.name))

    @interactions.extension_component("but_refuse")
    async def refuse_handler(self, ctx: interactions.ComponentContext):
        await ctx.send("Image refusée", ephemeral=True)
        await self.delete_demand_channel(int(ctx.channel.name))

    async def delete_demand_channel(self, author_id: int):
        demand_channel = self.get_demand_channel(author_id)
        await demand_channel.delete()
        self.demand_channels.remove(demand_channel)

    def get_demand_channel(self, author_id: int) -> DemandChannel or None:
        for demand_channel in self.demand_channels:
            if demand_channel.ID == author_id:
                return demand_channel
        return None

    async def get_image_message(self, demand_channel: DemandChannel) -> interactions.Message:
        for message in await demand_channel.channel.history(start_at=demand_channel.demand_message.id, reverse=True).flatten():
            if len(message.attachments) == 1 and message.attachments[0].content_type.startswith("image"):
                return message

    async def method(self):
        if self.start_hour <= datetime.now().hour < self.start_hour + 1:
            channel = await interactions.get(self.client, interactions.Channel, object_id=1046514872826986517)
            images = os.listdir(r"data/games/geoguessr/submissions")
            if len(images) != 0:
                image_name = images[randint(0, len(images) - 1)]
                ze_file = interactions.File(rf"data/games/geoguessr/submissions/{image_name}")
                embed = interactions.Embed(
                    title="Nouvelle image!",
                    description="C'est maintenant à vous de jouer :eyes:"
                )
                embed.set_image(url=f"attachment://{image_name}")
                await channel.send(embeds=embed, files=ze_file)


def setup(client):
    GenshinGeoguessr(client)
