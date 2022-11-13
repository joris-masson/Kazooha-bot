from interactions import Extension, Client, extension_command, CommandContext, SelectMenu, SelectOption, File, Embed, extension_component, ComponentContext, Message
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
        log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        await ctx.send(
            "Veuillez selectionner un dossier:",
            components=[
                SelectMenu(
                    placeholder="Liste des dossiers disponibles",
                    options=[
                        SelectOption(label="Alice", value="Alice"),
                        SelectOption(label="Asmoday", value="Asmoday"),
                        SelectOption(label="Dainsleif", value="Dainsleif"),
                        SelectOption(label="Paimon", value="Paimon"),
                        SelectOption(label="Phanes", value="Phanes"),
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
