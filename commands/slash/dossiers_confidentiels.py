from interactions import Extension, Client, extension_command, CommandContext, SelectMenu, SelectOption, File, Embed, extension_component, ComponentContext
from utils.functions import log


class DossiersConfidentiels(Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: Client = client

    @extension_command(
        name="dossiers_confidentiels",
        description="Affiche une image contenant des informations sur un personnage du lore de Genshin Impact",
    )
    async def dossiers_confidentiels(self, ctx: CommandContext):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        await ctx.send(
            "(Tous les dossiers sont réalisés par Amalia)\nVeuillez selectionner un dossier:",
            components=[
                SelectMenu(
                    placeholder="Liste des dossiers disponibles",
                    options=[
                        SelectOption(label="Alice", value="Alice"),
                        SelectOption(label="Asmoday", value="Asmoday"),
                        SelectOption(label="Columbina", value="Columbina"),
                        SelectOption(label="Dainsleif", value="Dainsleif"),
                        SelectOption(label="Istaroth", value="Istaroth"),
                        SelectOption(label="Nabu Malikata", value="Nabu_malikata"),
                        SelectOption(label="La Mère de la Nuit", value="Night_mother"),
                        SelectOption(label="Le Sibling", value="Traveler_sibling"),
                        SelectOption(label="Le Traveler", value="Travelerp"),
                        SelectOption(label="Paimon", value="Paimon"),
                        SelectOption(label="Phanes", value="Phanes"),
                        SelectOption(label="Pierro", value="Pierro"),
                        SelectOption(label="Pushpavatika", value="Pushpavatika"),
                        SelectOption(label="Rhinedottir", value="Rhinedottir"),
                    ],
                    custom_id="sel_dossiers",
                )
            ],
            ephemeral=True
        )

    @extension_component("sel_dossiers")
    async def handler(self, ctx: ComponentContext, interaction):
        file = File(f"data/dossiers/{interaction[0]}.png")
        embed = Embed(title=f"Dossier confidentiel: {interaction[0]}")
        embed.set_image(url=f"attachment://{interaction[0]}.png")
        await ctx.send(embeds=embed, files=file, ephemeral=True)


def setup(client):
    DossiersConfidentiels(client)
