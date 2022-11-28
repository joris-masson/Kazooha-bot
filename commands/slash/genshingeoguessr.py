# prog par Dr.Emma(retire ça et jte pete les genoux)
import os

import interactions

from utils.classes.demandchannel import DemandChannel
from utils.func import save_attachment
from utils.functions import log, has_at_least_one_role
from interactions.ext.tasks import IntervalTrigger, create_task
from random import randint
from datetime import datetime
from dotenv import load_dotenv


class GenshinGeoguessr(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        load_dotenv()

        self.client: interactions.Client = client
        self.demand_channels = []
        self.guess_channel = interactions.Channel

        self.method = create_task(IntervalTrigger(10))(self.method)
        self.method.start()

        self.start_hour = 8
        self.last_day = datetime.now()

    @interactions.extension_command(
        name="genshin_geoguessr",
        options=[
            interactions.Option(
                name="soumettre_nouvelle_image",
                description="Soumettre une photo d'un lieu",
                type=interactions.OptionType.SUB_COMMAND
            ),
            interactions.Option(
                name="aide",
                description="Comment qu'il marche ce jeu?",
                type=interactions.OptionType.SUB_COMMAND
            )
        ],
        scope=int(os.getenv("GENSHIN_GEOGUESSR_GUILD"))
    )
    async def genshin_geoguessr(self, ctx: interactions.CommandContext, sub_command: str):
        channel = await interactions.get(self.client, interactions.Channel, object_id=int(ctx.channel_id))
        if channel.type != interactions.ChannelType.PRIVATE_THREAD and channel.type != interactions.ChannelType.PUBLIC_THREAD:
            if sub_command == "soumettre_nouvelle_image":
                log(f"{__name__} -> soumettre_nouvelle_image utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
                await self.soumettre(ctx)
            elif sub_command == "aide":
                log(f"{__name__} -> aide utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
                await self.help(ctx)
        else:
            await ctx.send("Cette commande n'est pas utilisable dans un fil", ephemeral=True)

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

        await ctx.send(embeds=help_embed, ephemeral=True)

    @interactions.extension_component("but_accept")
    async def accept_handler(self, ctx: interactions.ComponentContext):
        if has_at_least_one_role(ctx.author, [952595865846046750, 956165233536294942, 967155907937042462]):
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
        else:
            await ctx.send("Désolé, vous n'êtes pas autorisé à faire cela.", ephemeral=True)

    @interactions.extension_component("but_refuse")
    async def refuse_handler(self, ctx: interactions.ComponentContext):
        if has_at_least_one_role(ctx.author, [952595865846046750, 956165233536294942, 967155907937042462]):
            await ctx.send("Image refusée", ephemeral=True)
            await self.delete_demand_channel(int(ctx.channel.name))
        else:
            await ctx.send("Désolé, vous n'êtes pas autorisé à faire cela.", ephemeral=True)

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
        if (self.start_hour <= datetime.now().hour < self.start_hour + 1) and not self.is_same_day():
            channel = await interactions.get(self.client, interactions.Channel, object_id=int(os.getenv("IMAGE_CHANNEL_ID")))
            images = os.listdir(r"data/games/geoguessr/submissions")
            if len(images) != 0:
                image_name = images[randint(0, len(images) - 1)]
                ze_file = interactions.File(rf"data/games/geoguessr/submissions/{image_name}")
                if int(image_name[:18]) != 783075596280004659:
                    embed = interactions.Embed(
                        title="Nouvelle image!",
                        description=f"Image soumise par <@{image_name[:18]}>\nC'est maintenant à vous de jouer :eyes:"
                    )
                else:
                    embed = interactions.Embed(
                        title="Nouvelle image!",
                        description=f"Image soumise par <@{image_name[:18]}>(aka Claude <:NE_yaeSmug:955592857765421166>)\nC'est maintenant à vous de jouer :eyes:"
                    )
                embed.set_image(url=f"attachment://{image_name}")
                await channel.send(embeds=embed, files=ze_file)
                self.last_day = datetime.now()

    def is_same_day(self):
        return datetime.now().day == self.last_day.day


def setup(client):
    GenshinGeoguessr(client)
