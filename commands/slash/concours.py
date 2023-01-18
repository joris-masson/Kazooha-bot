import os

import interactions

from utils.classes.demandchannel_concours import DemandChannelConcours
from utils.functions import log
from dotenv import load_dotenv


class Concours(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        load_dotenv()

        self.client: interactions.Client = client
        self.demand_channels = []
    @interactions.extension_command(
        name="concours",
        options=[
            interactions.Option(
                name="soumettre",
                description="Soumettre votre participation",
                type=interactions.OptionType.SUB_COMMAND
            )
        ],
        scope=int(os.getenv("GENSHIN_GEOGUESSR_GUILD"))
    )
    async def concours(self, ctx: interactions.CommandContext, sub_command: str):
        channel = await interactions.get(self.client, interactions.Channel, object_id=int(ctx.channel_id))
        if channel.type != interactions.ChannelType.PRIVATE_THREAD and channel.type != interactions.ChannelType.PUBLIC_THREAD:
            if sub_command == "soumettre":
                log(f"{__name__} -> soumettre_nouvelle_image utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
                await self.soumettre(ctx)
        else:
            await ctx.send("Cette commande n'est pas utilisable dans un fil", ephemeral=True)

    async def soumettre(self, ctx: interactions.CommandContext):
        if self.get_demand_channel(int(ctx.author.id)) is None:
            verif_channel = await ctx.channel.create_thread(f"{ctx.author.id}", type=interactions.ChannelType.PRIVATE_THREAD)
            le_salon_de_demande = DemandChannelConcours(self.client, ctx, verif_channel)
            await le_salon_de_demande.send_demand_msg()
            self.demand_channels.append(le_salon_de_demande)
        else:
            await ctx.send("Vous avez déjà une soumission en cours", ephemeral=True)

    @interactions.extension_component("but_accept")
    async def accept_handler(self, ctx: interactions.ComponentContext):
        demand_channel = self.get_demand_channel(int(ctx.channel.name))
        image_message = await self.get_image_message(demand_channel, )
        await ctx.send("Image acceptée", ephemeral=True)
        filename = f"data/other/concours_photo_desert_2/{demand_channel.ctx.author.id}.png"
        image_message.attachments[0]._client = self.client._http
        att_data = await image_message.attachments[0].download()
        with open(filename, 'wb') as outfile:
            outfile.write(att_data.getbuffer())
        message_lines = []
        line = ''
        for char in image_message.content:
            if char == '\n':
                message_lines.append(line)
                line = ''
            else:
                line += char
        message_lines.append(line)
        with open(f"data/other/concours_photo_desert_2/participations/{ctx.author.id}.json", 'w', encoding="utf-8") as file:
            file.write(
                f"""{{
    "title": "{message_lines[0]}",
    "description": "{' '.join(message_lines[1:])}",
    "image": "/../images/{demand_channel.ctx.author.id}.png"
                }}"""
            )
        await self.delete_demand_channel(int(ctx.channel.name))

    @interactions.extension_component("but_refuse")
    async def refuse_handler(self, ctx: interactions.ComponentContext):
        await ctx.send("Image refusée", ephemeral=True)
        await self.delete_demand_channel(int(ctx.channel.name))

    async def delete_demand_channel(self, author_id: int):
        demand_channel = self.get_demand_channel(author_id)
        await demand_channel.delete()
        self.demand_channels.remove(demand_channel)

    def get_demand_channel(self, author_id: int) -> DemandChannelConcours or None:
        for demand_channel in self.demand_channels:
            if demand_channel.ID == author_id:
                return demand_channel
        return None

    async def get_image_message(self, demand_channel: DemandChannelConcours) -> interactions.Message:
        for message in await demand_channel.channel.history(start_at=demand_channel.demand_message.id, reverse=True).flatten():
            if len(message.attachments) == 1 and message.attachments[0].content_type.startswith("image"):
                return message


def setup(client):
    Concours(client)
