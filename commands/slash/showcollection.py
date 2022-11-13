from interactions import Extension, Client, extension_command, Option, OptionType, CommandContext, SelectMenu, SelectOption, Embed, extension_component, ComponentContext
from interactions.ext.paginator import Page, Paginator
from utils.functions import log
from data.dico_books import dico_books


class ShowCollections(Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: Client = client

    @extension_command(
        name="afficher_les_livres_des_archives",
        description="Affiche une liste des livres des archives, sélectionnez en un, et vous pourrez le lire!",
        options=[Option(
            name="page",
            description="La page du sélecteur à afficher(il y en a 2)",
            type=OptionType.INTEGER,
            required=True
        )]
    )
    async def show_collection(self, ctx: CommandContext, page: int):
        log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        if page == 1:
            await ctx.send(
                "Veuillez selectionner un livre:",
                components=[
                    SelectMenu(
                        placeholder="Liste des collections disponibles",
                        options=[
                            SelectOption(label="Anthologie de la poésie Brutocollinus", value="Anthologie de la poesie Brutocollinus"),
                            SelectOption(label="Anthologie de poèmes Brutocollinus", value="Anthologie de poemes Brutocollinus"),
                            SelectOption(label="Archives de Jueyun", value="Archives de Jueyun"),
                            SelectOption(label="Ballade de l’écuyer", value="Ballade de l_ecuyer"),
                            SelectOption(label="Chroniques d’un ivrogne", value="Chroniques d_un ivrogne"),
                            SelectOption(label="Collection de Byakuyakoku", value="Collection de Byakuyakoku"),
                            SelectOption(label="Contes de l’Allée Toki", value="Contes de l_Allee Toki"),
                            SelectOption(label="Coutumes de Liyue", value="Coutumes de Liyue"),
                            SelectOption(label="Étude des coutumes Brutocollinus", value="etude des coutumes Brutocollinus"),
                            SelectOption(label="Fleurs pour la Princesse Fischl", value="Fleurs pour la Princesse Fischl"),
                            SelectOption(label="Forêt de bambou au clair de lune", value="Foret de bambou au clair de lune"),
                            SelectOption(label="Guide de voyage en Teyvat", value="Guide de voyage en Teyvat"),
                            SelectOption(label="Histoire du chevalier errant", value="Histoire du chevalier errant"),
                            SelectOption(label="Journal d'un inconnu", value="Journal d un inconnu"),
                            SelectOption(label="Journal de l’aventurier Roald", value="Journal de l aventurier Roald"),
                            SelectOption(label="Journal du vagabond", value="Journal du vagabond"),
                            SelectOption(label="L’Archon invisible", value="L Archon invisible"),
                            SelectOption(label="L’Épée solitaire du mont désolé", value="L epee solitaire du mont desole"),
                            SelectOption(label="La Brise de la Forêt", value="La Brise de la Foret"),
                            SelectOption(label="La Légende de Vennessa", value="La Legende de Vennessa"),
                            SelectOption(label="La Mélancolie de Véra", value="La Melancolie de Vera"),
                            SelectOption(label="La Princesse sanglier", value="La Princesse sanglier"),
                            SelectOption(label="La Renarde qui nageait dans la mer de pissenlits", value="La Renarde qui nageait dans la mer de pissenlits"),
                            SelectOption(label="La Tour de Mondstadt", value="La Tour de Mondstadt"),
                            SelectOption(label="Le Bris de l’arme divine", value="Le Bris de l arme divine"),
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
                    SelectMenu(
                        placeholder="Liste des collections disponibles",
                        options=[
                            SelectOption(label="Le cœur de la source", value="Le coeur de la source"),
                            SelectOption(label="Les guerres d’Hamawaran", value="Les guerres d Hamawaran"),
                            SelectOption(label="Nouvelles chroniques des six Kitsunes", value="Nouvelles chroniques des six Kitsunes"),
                            SelectOption(label="Perle du cœur", value="Perle du coeur"),
                            SelectOption(label="Princesse Mina de la nation déchue", value="Princesse Mina de la nation dechue"),
                            SelectOption(label="Princesse Neige et les Six Nains", value="Princesse Neige et les Six Nains"),
                            SelectOption(label="Rêves brisés", value="Reves brises"),
                            SelectOption(label="Théories étranges du Kiyoshiken Shinkageuchi", value="Theories etranges du Kiyoshiken Shinkageuchi"),
                            SelectOption(label="Une légende d’épée", value="Une legende d epee"),
                        ],
                        custom_id="sel_collection"
                    )
                ],
                ephemeral=True
            )
        else:
            await ctx.send("Cette page n'existe pas(il y en a 2)")
            return

    @extension_component("sel_collection")
    async def handler(self, ctx: ComponentContext, interaction):
        the_book = interaction[0].lower().replace(' ', '_')
        embeds = [Embed(title=f"{interaction[0]} - page {page}", description=dico_books[the_book][page]) for page in range(1, len(dico_books[the_book]) + 1)]
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
    ShowCollections(client)
