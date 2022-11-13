from interactions import Extension, Client, extension_command, CommandContext, SelectMenu, SelectOption, Embed, extension_component, ComponentContext
from interactions.ext.paginator import Page, Paginator
from utils.functions import log
from data.dico_quest_books import dico_quest_books


class ShowQuestBooks(Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: Client = client

    @extension_command(
        name="afficher_les_livres_de_quete",
        description="Affiche une liste des livres de quête, sélectionnez en un, et vous pourrez le lire!",
    )
    async def show_quest_books(self, ctx: CommandContext):
        log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        await ctx.send(
            "Veuillez selectionner un livre:",
            components=[
                SelectMenu(
                    placeholder="Liste des livres de quêtes disponibles",
                    options=[
                        SelectOption(label="Avec les dieux - Prologue", value="Avec les dieux Prologue"),
                        SelectOption(label="Aventures en montagne et en mer", value="Aventures en montagne et en mer"),
                        SelectOption(label="Biographie de Gunnhildr", value="Biographie de Gunnhildr"),
                        SelectOption(label="Chroniques de Sangonomiya", value="Chroniques de Sangonomiya"),
                        SelectOption(label="Débat sur le « Vice-roi de l'Est »", value="Debat sur le Vice roi de l Est"),
                        SelectOption(label="Histoire des rois et des clans", value="Histoire des rois et des clans"),
                        SelectOption(label="Inscriptions sur tablettes de pierres - I", value="Inscriptions sur tablettes de pierres I"),
                        SelectOption(label="Journal épais", value="Journal epais"),
                        SelectOption(label="La vie de la prêtresse Mouun", value="La vie de la pretresse Mouun"),
                        SelectOption(label="Les Yakshas, Gardiens Adeptes", value="Les Yakshas Gardiens Adeptes"),
                        SelectOption(label="Mille ans de solitude", value="Mille ans de solitude"),
                        SelectOption(label="Perle précieuse", value="Perle precieuse"),
                        SelectOption(label="Premier disciple du clan Guhua", value="Premier disciple du clan Guhua"),
                        SelectOption(label="Versets d'equilibrium", value="Versets d equilibrium"),
                    ],
                    custom_id="sel_quest_books"
                )
            ],
            ephemeral=True
        )

    @extension_component("sel_quest_books")
    async def handler(self, ctx: ComponentContext, interaction):
        the_book = interaction[0].lower().replace(' ', '_')
        embeds = [Embed(title=f"{interaction[0]} - page {page}", description=dico_quest_books[the_book][page]) for page in range(1, len(dico_quest_books[the_book]) + 1)]
        if len(embeds) > 1:
            les_pages = []
            for embed in embeds:
                les_pages.append(Page(embeds=embed))
            await Paginator(
                client=self.client,
                ctx=ctx,
                pages=les_pages,
                disable_after_timeout=False,
                use_select=False,
                index=True
            ).run()
        else:
            await ctx.send(embeds=embeds)


def setup(client):
    ShowQuestBooks(client)
