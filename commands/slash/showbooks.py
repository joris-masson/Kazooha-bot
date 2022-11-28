import interactions
from utils.functions import log
from interactions.ext.paginator import Page, Paginator
from data.dico_books import dico_books
from data.dico_quest_books import dico_quest_books


class ShowBooks(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="afficher_livres",
        options=[
            interactions.Option(
                name="archives",
                description="Affiche une liste des livres des archives, sélectionnez en un, et vous pourrez le lire!",
                type=interactions.OptionType.SUB_COMMAND,
                options=[interactions.Option(
                    name="page",
                    description="La page du sélecteur à afficher(il y en a 2)",
                    type=interactions.OptionType.INTEGER,
                    required=True
                )]
            ),
            interactions.Option(
                name="quetes",
                description="Affiche une liste des livres de quête, sélectionnez en un, et vous pourrez le lire!",
                type=interactions.OptionType.SUB_COMMAND
            ),
        ],
    )
    async def show_books(self, ctx: interactions.CommandContext, sub_command: str, page: int = None):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")

        if sub_command == "archives":
            await self.show_collection(ctx, page)
        elif sub_command == "quetes":
            await self.show_quest_books(ctx)

    async def show_collection(self, ctx: interactions.CommandContext, page: int):
        if page == 1:
            await ctx.send(
                "Veuillez selectionner un livre:",
                components=[
                    interactions.SelectMenu(
                        placeholder="Liste des collections disponibles",
                        options=[
                            interactions.SelectOption(label="Anthologie de la poésie Brutocollinus", value="Anthologie de la poesie Brutocollinus"),
                            interactions.SelectOption(label="Anthologie de poèmes Brutocollinus", value="Anthologie de poemes Brutocollinus"),
                            interactions.SelectOption(label="Archives de Jueyun", value="Archives de Jueyun"),
                            interactions.SelectOption(label="Ballade de l’écuyer", value="Ballade de l_ecuyer"),
                            interactions.SelectOption(label="Chroniques d’un ivrogne", value="Chroniques d_un ivrogne"),
                            interactions.SelectOption(label="Collection de Byakuyakoku", value="Collection de Byakuyakoku"),
                            interactions.SelectOption(label="Contes de l’Allée Toki", value="Contes de l_Allee Toki"),
                            interactions.SelectOption(label="Coutumes de Liyue", value="Coutumes de Liyue"),
                            interactions.SelectOption(label="Étude des coutumes Brutocollinus", value="etude des coutumes Brutocollinus"),
                            interactions.SelectOption(label="Fleurs pour la Princesse Fischl", value="Fleurs pour la Princesse Fischl"),
                            interactions.SelectOption(label="Forêt de bambou au clair de lune", value="Foret de bambou au clair de lune"),
                            interactions.SelectOption(label="Guide de voyage en Teyvat", value="Guide de voyage en Teyvat"),
                            interactions.SelectOption(label="Histoire du chevalier errant", value="Histoire du chevalier errant"),
                            interactions.SelectOption(label="Journal d'un inconnu", value="Journal d un inconnu"),
                            interactions.SelectOption(label="Journal de l’aventurier Roald", value="Journal de l aventurier Roald"),
                            interactions.SelectOption(label="Journal du vagabond", value="Journal du vagabond"),
                            interactions.SelectOption(label="L’Archon invisible", value="L Archon invisible"),
                            interactions.SelectOption(label="L’Épée solitaire du mont désolé", value="L epee solitaire du mont desole"),
                            interactions.SelectOption(label="La Brise de la Forêt", value="La Brise de la Foret"),
                            interactions.SelectOption(label="La Légende de Vennessa", value="La Legende de Vennessa"),
                            interactions.SelectOption(label="La Mélancolie de Véra", value="La Melancolie de Vera"),
                            interactions.SelectOption(label="La Princesse sanglier", value="La Princesse sanglier"),
                            interactions.SelectOption(label="La Renarde qui nageait dans la mer de pissenlits", value="La Renarde qui nageait dans la mer de pissenlits"),
                            interactions.SelectOption(label="La Tour de Mondstadt", value="La Tour de Mondstadt"),
                            interactions.SelectOption(label="Le Bris de l’arme divine", value="Le Bris de l arme divine"),
                        ],
                        custom_id="sel_collection"
                    )
                ],
                ephemeral=True
            )
        elif page == 2:
            await ctx.send(
                "Veuillez selectionner un livre:",
                components=[
                    interactions.SelectMenu(
                        placeholder="Liste des collections disponibles",
                        options=[
                            interactions.SelectOption(label="Le cœur de la source", value="Le coeur de la source"),
                            interactions.SelectOption(label="Les guerres d’Hamawaran", value="Les guerres d Hamawaran"),
                            interactions.SelectOption(label="Nouvelles chroniques des six Kitsunes", value="Nouvelles chroniques des six Kitsunes"),
                            interactions.SelectOption(label="Perle du cœur", value="Perle du coeur"),
                            interactions.SelectOption(label="Princesse Mina de la nation déchue", value="Princesse Mina de la nation dechue"),
                            interactions.SelectOption(label="Princesse Neige et les Six Nains", value="Princesse Neige et les Six Nains"),
                            interactions.SelectOption(label="Rêves brisés", value="Reves brises"),
                            interactions.SelectOption(label="Théories étranges du Kiyoshiken Shinkageuchi", value="Theories etranges du Kiyoshiken Shinkageuchi"),
                            interactions.SelectOption(label="Une légende d’épée", value="Une legende d epee"),
                        ],
                        custom_id="sel_collection"
                    )
                ],
                ephemeral=True
            )
        else:
            await ctx.send("Cette page n'existe pas(il y en a 2)")
            return

    async def show_quest_books(self, ctx: interactions.CommandContext):
        await ctx.send(
            "Veuillez selectionner un livre:",
            components=[
                interactions.SelectMenu(
                    placeholder="Liste des livres de quêtes disponibles",
                    options=[
                        interactions.SelectOption(label="Avec les dieux - Prologue", value="Avec les dieux Prologue"),
                        interactions.SelectOption(label="Aventures en montagne et en mer", value="Aventures en montagne et en mer"),
                        interactions.SelectOption(label="Biographie de Gunnhildr", value="Biographie de Gunnhildr"),
                        interactions.SelectOption(label="Chroniques de Sangonomiya", value="Chroniques de Sangonomiya"),
                        interactions.SelectOption(label="Débat sur le « Vice-roi de l'Est »", value="Debat sur le Vice roi de l Est"),
                        interactions.SelectOption(label="Histoire des rois et des clans", value="Histoire des rois et des clans"),
                        interactions.SelectOption(label="Inscriptions sur tablettes de pierres - I", value="Inscriptions sur tablettes de pierres I"),
                        interactions.SelectOption(label="Journal épais", value="Journal epais"),
                        interactions.SelectOption(label="La vie de la prêtresse Mouun", value="La vie de la pretresse Mouun"),
                        interactions.SelectOption(label="Les Yakshas, Gardiens Adeptes", value="Les Yakshas Gardiens Adeptes"),
                        interactions.SelectOption(label="Mille ans de solitude", value="Mille ans de solitude"),
                        interactions.SelectOption(label="Perle précieuse", value="Perle precieuse"),
                        interactions.SelectOption(label="Premier disciple du clan Guhua", value="Premier disciple du clan Guhua"),
                        interactions.SelectOption(label="Versets d'equilibrium", value="Versets d equilibrium"),
                    ],
                    custom_id="sel_quest_books"
                )
            ],
            ephemeral=True
        )

    @interactions.extension_component("sel_quest_books")
    async def quest_handler(self, ctx: interactions.ComponentContext, interaction):
        the_book = interaction[0].lower().replace(' ', '_')
        embeds = [interactions.Embed(title=f"{interaction[0]} - page {page}", description=dico_quest_books[the_book][page]) for page in range(1, len(dico_quest_books[the_book]) + 1)]
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

    @interactions.extension_component("sel_collection")
    async def collection_handler(self, ctx: interactions.ComponentContext, interaction):
        the_book = interaction[0].lower().replace(' ', '_')
        embeds = [interactions.Embed(title=f"{interaction[0]} - page {page}", description=dico_books[the_book][page]) for page in range(1, len(dico_books[the_book]) + 1)]
        if len(embeds) > 1:
            les_pages = []
            for embed in embeds:
                les_pages.append(Page(embeds=embed))
            try:
                await Paginator(
                    client=self.client,
                    ctx=ctx,
                    pages=les_pages,
                    disable_after_timeout=False,
                    use_select=False
                ).run()
            except interactions.api.LibraryException:
                pass
        else:
            await ctx.send(embeds=embeds, ephemeral=True)


def setup(client):
    ShowBooks(client)
