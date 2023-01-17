import os

import interactions

from utils.classes.demandchannel import DemandChannel
from utils.func import save_attachment
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
            ),
            interactions.Option(
                name="aide",
                description="Comment que ça marche tout ça?",
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
            elif sub_command == "aide":
                log(f"{__name__} -> aide utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
                await self.help(ctx)
        else:
            await ctx.send("Cette commande n'est pas utilisable dans un fil", ephemeral=True)

    async def soumettre(self, ctx: interactions.CommandContext):
        if self.get_demand_channel(int(ctx.author.id)) is None:
            verif_channel = await ctx.channel.create_thread(f"{ctx.author.id}", type=interactions.ChannelType.PRIVATE_THREAD)
            le_salon_de_demande = DemandChannel(self.client, ctx, verif_channel)
            await le_salon_de_demande.send_demand_msg()
            self.demand_channels.append(le_salon_de_demande)
        else:
            await ctx.send("Vous avez déjà une soumission en cours", ephemeral=True)

    async def help(self, ctx: interactions.CommandContext):
        help_embed = interactions.Embed(
            title="Alors, vous vous demandez comment qu'on joue hein",
            description="Voici la commande d'aide, qui va vous expliquer les règles et le comment que tout ça ça marche!"
        )

        help_embed.add_field(
            name="Tous les jours, une nouvelle image d'un lieu",
            value="Et oui, tous les jours, vous aurez une nouvelle photo(belle ou non, c'est à vous de juger <:NE_yaeSmug:955592857765421166>).\n"
                  "Et vous devrez identifier le lieu présent sur la photo!"
        )

        help_embed.add_field(
            name="...Et après?!",
            value="Et après, vous prenez votre map dans le jeu, et vous marquez avec un marqueur l'endroit présent dans la photo.\n"
                  "Le marqueur doit être à l'endroit d'**où est prise la photo**\n"
                  "Une fois votre marqueur posé, prenez un screen et chargez le avec le petit **+**, sans l'envoyer, marquez `!guess`, et envovez le tout!\n"
                  "\n"
                  "Après tout ceci, nos modérateurs s'occuperont de vous départager!\n"
        )

        help_embed.add_field(
            name="Vous pouvez envoyer vos propres photos!",
            value="ET OUI ~~JAMIE~~!!\n"
                  "Vous avez accès à une commande: </genshin_geoguessr soumettre_nouvelle_image:1046515635812827277>\n"
                  "Qui vous permettra tout simplement d'envoyer vos propres images!\n"
                  "\n"
                  "Pour ce faire, commencez déjà par lancer cette commande, puis ensuite, un fil pour vous sera créé, envoyez votre image dedans, et les modérateurs se chargeront de déciser si, oui ou non, cette image sera enregistrée.\n"
                  "\n"
                  "Condition:\n"
                  "    -l'image ne doit pas contenir de minimap"
        )

        help_embed.add_field(
            name="Pour voir vos points",
            value="La commande </genshin_geoguessr leaderboard:1046515635812827277> est là pour vous :eyes:"
        )

        await ctx.send(embeds=help_embed, ephemeral=True)

    @interactions.extension_component("but_accept")
    async def accept_handler(self, ctx: interactions.ComponentContext):
        demand_channel = self.get_demand_channel(int(ctx.channel.name))
        image_message = await self.get_image_message(demand_channel, )
        await ctx.send("Image acceptée", ephemeral=True)
        await save_attachment(self.client, image_message.attachments[0], f"data/other/concours_photo_desert_2/{demand_channel.ctx.author.id}.png")
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

    def get_demand_channel(self, author_id: int) -> DemandChannel or None:
        for demand_channel in self.demand_channels:
            if demand_channel.ID == author_id:
                return demand_channel
        return None

    async def get_image_message(self, demand_channel: DemandChannel) -> interactions.Message:
        for message in await demand_channel.channel.history(start_at=demand_channel.demand_message.id, reverse=True).flatten():
            if len(message.attachments) == 1 and message.attachments[0].content_type.startswith("image"):
                return message


def setup(client):
    Concours(client)
