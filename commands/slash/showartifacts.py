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
    async def show_artifacts(self, ctx: CommandContext, page: int):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        emojis = await self.get_emoji_dict()
        if page == 1:
            await ctx.send(
                "Veuillez selectionner un set d'artéfact:",
                components=[
                    SelectMenu(
                       placeholder="Liste des sets disponibles",
                       options=[
                           SelectOption(label="Âme des profondeurs", value="Ame des profondeurs", emoji=emojis["ame_des_profondeurs"]),
                           SelectOption(label="Amour chéri", value="Amour cheri", emoji=emojis["amour_cheri"]),
                           SelectOption(label="Ancien rituel royal", value="Ancien rituel royal", emoji=emojis["ancien_rituel_royal"]),
                           SelectOption(label="Artiste Martial", value="Artiste martial", emoji=emojis["artiste_martial"]),
                           SelectOption(label="Au-delà cinabrin", value="Au dela cinabrin", emoji=emojis["au_dela_cinabrin"]),
                           SelectOption(label="Aventurier", value="aventurier", emoji=emojis["aventurier"]),
                           SelectOption(label="Bande Vagabonde", value="Bande vagabonde", emoji=emojis["bande_vagabonde"]),
                           SelectOption(label="Berserker", value="Berserker", emoji=emojis["berserker"]),
                           SelectOption(label="Briseur de glace", value="Briseur de glace", emoji=emojis["briseur_de_glace"]),
                           SelectOption(label="Chanceux", value="Chanceux", emoji=emojis["chanceux"]),
                           SelectOption(label="Chanson des jours d'antan", value="Chanson des jours d antan", emoji=emojis["chanson_des_jours_d_antan"]),
                           SelectOption(label="Chasseur de la Maréchaussée", value="Chasseur de la Marechaussee", emoji=emojis["chasseur_de_la_marechaussee"]),
                           SelectOption(label="Chevalerie ensanglantée", value="Chevalerie ensanglantee", emoji=emojis["chevalerie_ensanglantee"]),
                           SelectOption(label="Chronique du Pavillon du désert", value="Chronique du Pavillon du desert", emoji=emojis["chronique_du_pavillon_du_desert"]),
                           SelectOption(label="Coeur du brave", value="Coeur du brave", emoji=emojis["coeur_du_brave"]),
                           SelectOption(label="Coeur du gardien", value="Coeur du gardien", emoji=emojis["coeur_du_gardien"]),
                           SelectOption(label="Coeur du voyageur", value="coeur du voyageur", emoji=emojis["coeur_du_voyageur"]),
                           SelectOption(label="Colère du tonnerre", value="Colere du tonerre", emoji=emojis["colere_du_tonnerre"]),
                           SelectOption(label="Coquille des rêves opulents", value="Coquille des reves opulents", emoji=emojis["coquille_des_reves_opulents"]),
                           SelectOption(label="Dompteur de foudre", value="Dompteur de foudre", emoji=emojis["dompteur_de_foudre"]),
                           SelectOption(label="Echos d'une offrande", value="Echos d une offrande", emoji=emojis["echos_d_une_offrande"]),
                           SelectOption(label="Emblème du destin brisé", value="Embleme du destin brise", emoji=emojis["embleme_du_destin_brise"]),
                           SelectOption(label="Erudit", value="Erudit", emoji=emojis["erudit"]),
                           SelectOption(label="Exilé", value="Exile", emoji=emojis["exile"]),
                           SelectOption(label="Flamme blème", value="Flamme bleme", emoji=emojis["flamme_bleme"])
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
                            SelectOption(label="Fleur du paradis perdu", value="Fleur du paradis perdu", emoji=emojis["fleur_du_paradis_perdu"]),
                            SelectOption(label="Instructeur", value="Instruteur", emoji=emojis["instructeur"]),
                            SelectOption(label="Lueur du Vourukasha", value="Lueur du Vourukasha", emoji=emojis["lueur_du_vourukasha"]),
                            SelectOption(label="Marcheur du feu", value="Marcheur du feu", emoji=emojis["marcheur_du_feu"]),
                            SelectOption(label="Médecin itinérant", value="Medecin itinerant", emoji=emojis["medecin_itinerant"]),
                            SelectOption(label="Metéore inversé", value="Meteore inverse", emoji=emojis["meteore_inverse"]),
                            SelectOption(label="Miracle", value="Miracle", emoji=emojis["miracle"]),
                            SelectOption(label="Murmure nocturne en forêt d'échos", value="Murmure nocturne en foret d echos", emoji=emojis["murmure_nocturne_en_foret_d_echo"]),
                            SelectOption(label="Ombre de la Verte Chasseuse", value="Ombre de la Verte Chasseuse", emoji=emojis["ombre_de_la_verte_chasseuse"]),
                            SelectOption(label="Palourde aux teintes océaniques", value="Palourde aux teintes oceaniques", emoji=emojis["palourde_aux_teintes_oceaniques"]),
                            SelectOption(label="Parieur", value="Parieur", emoji=emojis["parieur"]),
                            SelectOption(label="Reminiscence Nostalgique", value="Reminiscence Nostalgique", emoji=emojis["reminiscence_nostalgique"]),
                            SelectOption(label="Rêve de la Nymphe", value="Reve de la Nymphe", emoji=emojis["reve_de_la_nymphe"]),
                            SelectOption(label="Rêve Doré", value="Reve Dore", emoji=emojis["reve_dore"]),
                            SelectOption(label="Rideau du Gladiateur", value="Rideau du Gladiateur", emoji=emojis["rideau_du_gladiateur"]),
                            SelectOption(label="Roche ancienne", value="Roche ancienne", emoji=emojis["roche_ancienne"]),
                            SelectOption(label="Sorcière des flammes ardentes", value="Sorciere des flammes ardentes", emoji=emojis["sorciere_des_flammes_ardentes"]),
                            SelectOption(label="Souvenir de forêt", value="Souvenir de foret", emoji=emojis["souvenir_de_foret"]),
                            SelectOption(label="Ténacité du Millelithe", value="Tenacite du Millelithe", emoji=emojis["tenacite_du_millelithe"]),
                            SelectOption(label="Troupe dorée", value="Troupe doree", emoji=emojis["troupe_doree"])
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

    async def get_emoji_dict(self) -> dict[str, interactions.Emoji]:
        res = {}
        serv = await interactions.get(self.client, interactions.Guild, object_id=1142078973929603212)
        for emote in serv.emojis:
            res[emote.name] = emote
        print(res)
        return res


def setup(client):
    ShowArtifacts(client)
