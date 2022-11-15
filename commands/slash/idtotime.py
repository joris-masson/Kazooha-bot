import interactions
from utils.functions import log, convert_discord_id_to_time


class IdToTime(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="idtotime",
        description="Oui",
        options=[interactions.Option(
            name="discord_id",
            description="L'ID d'un truc dont tu veux connaître la date de création",
            type=interactions.OptionType.STRING,
            required=True
        )]
    )
    async def id_to_time(self, ctx: interactions.CommandContext, discord_id: str):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        converted_id = convert_discord_id_to_time(int(discord_id))
        await ctx.send(f"L'objet a été créé le: <t:{converted_id}>\nTimestamp discord: `<t:{converted_id}>`", ephemeral=True)


def setup(client):
    IdToTime(client)
