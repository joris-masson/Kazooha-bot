import os

from interactions import Extension, Client, extension_command, CommandContext, SelectMenu, SelectOption, Embed, extension_component, ComponentContext
from interactions.ext.paginator import Page, Paginator
from utils.functions import log
from data.dico_artifacts import dico_artifacts
from dotenv import load_dotenv


class ShowBetaArtifacts(Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        load_dotenv()

        self.client: Client = client

    @extension_command(
        name="afficher_les_artefacts_beta",
        description="Affiche une liste des sets d'artéfacts, sélectionnez en un, et vous pourrez lire le lore autour!",
        scope=os.getenv("BETA_GUILD")
    )
    async def show_quest_books(self, ctx: CommandContext):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        await ctx.send(
            "Veuillez selectionner un set d'artéfact:",
            components=[
                SelectMenu(
                   placeholder="Liste des sets disponibles",
                   options=[
                       SelectOption(label="Neige et glace", value="Neige et glace"),
                   ],
                   custom_id="sel_artifacts"
                )
            ],
            ephemeral=True
        )

    @extension_component("sel_artifacts")
    async def handler(self, ctx: ComponentContext, interaction):
        the_book = interaction[0].lower().replace(' ', '_')
        embeds = []
        for page in range(1, len(dico_artifacts[the_book]) + 1):
            embed = Embed(title=f"{interaction[0]} - page {page}", description=dico_artifacts[the_book][page])
            embed.set_thumbnail(url=f"http://176.159.155.219:53134/images/artifacts/icons/beta/{the_book}/{page}.png")
            embeds.append(embed)
        les_pages = []
        for embed in embeds:
            les_pages.append(Page(embeds=embed))
        await Paginator(
            client=self.client,
            ctx=ctx,
            pages=les_pages,
            disable_after_timeout=False,
            use_select=False
        ).run()


def setup(client):
    ShowBetaArtifacts(client)
