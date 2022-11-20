import interactions
from utils.functions import log


class Archive(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="archive",
        description="Oui",
    )
    async def id_to_time(self, ctx: interactions.CommandContext):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        base_string = "Bonjour!\nJe vais maintenant archiver le salon entier, veuillez patienter lonnnnnnngtemps(ce message sera mis à jour au fur et à mesure de l'avancement).\n\n"
        msg = await ctx.send(base_string + "Je vais commencer par compter tous les messages du salon...")
        await msg.edit(content=base_string + f"Il y a {len(await ctx.channel.history().flatten())} messages")


def setup(client):
    Archive(client)
