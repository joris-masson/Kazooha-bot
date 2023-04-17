import interactions

from interactions import Extension, Client, extension_command, Option, OptionType, CommandContext, SelectMenu, SelectOption, Embed, extension_component, ComponentContext
from interactions.ext.paginator import Page, Paginator
from utils.functions import log
from data.dico_artifacts import dico_artifacts


class ShowArtifacts(Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: Client = client

    @extension_command(
        name="afficher_les_artefacts",
        description="Affiche une liste des sets d'artéfacts, sélectionnez en un, et vous pourrez lire le lore autour!",
        options=[Option(
            name="page",
            description="La page du sélecteur à afficher(il y en a 2)",
            type=OptionType.INTEGER,
            required=True
        )]
    )
    async def show_quest_books(self, ctx: CommandContext, page: int):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        if page == 1:
            await ctx.send(
                "Veuillez selectionner un set d'artéfact:",
                components=[
                    SelectMenu(
                       placeholder="Liste des sets disponibles",
                       options=[
                           SelectOption(label="Âme des profondeurs", value="Ame des profondeurs"),
                           SelectOption(label="Amour chéri", value="Amour cheri"),
                           SelectOption(label="Ancien rituel royal", value="Ancien rituel royal"),
                           SelectOption(label="Artiste Martial", value="Artiste martial"),
                           SelectOption(label="Au-delà cinabrin", value="Au dela cinabrin"),
                           SelectOption(label="Aventurier", value="aventurier"),
                           SelectOption(label="Bande Vagabonde", value="Bande vagabonde"),
                           SelectOption(label="Berserker", value="Berserker"),
                           SelectOption(label="Briseur de glace", value="Briseur de glace"),
                           SelectOption(label="Chanceux", value="Chanceux"),
                           SelectOption(label="Chevalerie ensanglantée", value="Chevalerie ensanglantee"),
                           SelectOption(label="Chronique du Pavillon du désert", value="Chronique du Pavillon du desert"),
                           SelectOption(label="Coeur du brave", value="Coeur du brave"),
                           SelectOption(label="Coeur du gardien", value="Coeur du gardien"),
                           SelectOption(label="Coeur du voyageur", value="coeur du voyageur"),
                           SelectOption(label="Colère du tonnerre", value="Colere du tonerre"),
                           SelectOption(label="Coquille des rêves opulents", value="Coquille des reves opulents"),
                           SelectOption(label="Dompteur de foudre", value="Dompteur de foudre"),
                           SelectOption(label="Echos d'une offrande", value="Echos d une offrande"),
                           SelectOption(label="Emblème du destin brisé", value="Embleme du destin brise"),
                           SelectOption(label="Erudit", value="Erudit"),
                           SelectOption(label="Exilé", value="Exile"),
                           SelectOption(label="Flamme blème", value="Flamme bleme"),
                           SelectOption(label="Fleur du paradis perdu", value="Fleur du paradis perdu"),
                           SelectOption(label="Instructeur", value="Instruteur"),
                       ],
                       custom_id="sel_artifacts"
                    )
                ],
                ephemeral=True
            )
        elif page == 2:
            await ctx.send(
                "Veuillez selectionner un set d'artéfact:",
                components=[
                    SelectMenu(
                        placeholder="Liste des sets disponibles",
                        options=[
                            SelectOption(label="Lueur du Vourukasha", value="Lueur du Vourukasha"),
                            SelectOption(label="Marcheur du feu", value="Marcheur du feu"),
                            SelectOption(label="Médecin itinérant", value="Medecin itinerant"),
                            SelectOption(label="Metéore inversé", value="Meteore inverse"),
                            SelectOption(label="Miracle", value="Miracle"),
                            SelectOption(label="Ombre de la Verte Chasseuse", value="Ombre de la Verte Chasseuse"),
                            SelectOption(label="Palourde aux teintes océaniques", value="Palourde aux teintes oceaniques"),
                            SelectOption(label="Parieur", value="Parieur"),
                            SelectOption(label="Reminiscence Nostalgique", value="Reminiscence Nostalgique"),
                            SelectOption(label="Rêve de la Nymphe", value="Reve de la Nymphe"),
                            SelectOption(label="Rêve Doré", value="Reve Dore"),
                            SelectOption(label="Rideau du Gladiateur", value="Rideu du Gladiateur"),
                            SelectOption(label="Roche ancienne", value="Roche ancienne"),
                            SelectOption(label="Sorcière des flammes", value="Sorciere des flammes"),
                            SelectOption(label="Souvenir de forêt", value="Souvenir de foret"),
                            SelectOption(label="Ténacité du Millelithe", value="Tenacite du Millelithe"),
                        ],
                        custom_id="sel_artifacts"
                    )
                ],
                ephemeral=True
            )
        else:
            await ctx.send("Cette page n'existe pas(il y en a 2)")
            return

    @extension_component("sel_artifacts")
    async def handler(self, ctx: ComponentContext, interaction):
        the_book = interaction[0].lower().replace(' ', '_')
        embeds = []
        for page in range(1, len(dico_artifacts[the_book]) + 1):
            embed = Embed(title=f"{interaction[0]} - page {page}", description=dico_artifacts[the_book][page])
            embed.set_thumbnail(url=f"http://jo.narukami-edition.fr:53134/images/artifacts/icons/{the_book}/{page}.png")
            embeds.append(embed)
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


def setup(client):
    ShowArtifacts(client)
