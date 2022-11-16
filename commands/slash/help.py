import interactions
from utils.functions import log


class Help(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="help",
        description="C'est la commande d'aide :D",
    )
    async def help(self, ctx: interactions.CommandContext):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        help_embed = interactions.Embed(title="__Aide pour Kazooha__", description="Voici un petit recap des commandes du bot")

        help_embed.add_field(name="__**Préfix**__", value="Le bot utilise maintenant les commandes slashs!\ncommencez votre commande par `/` et vous devriez être guidés!")

        help_embed.add_field(name="__**Afficher les artéfacts**__", value="""
                **Nom de la commande**: `/afficher_les_artefacts`
                **Paramètre**: `page`
                Valeurs possibles pour `page`: `1` ou `2`
                
                **Visibilité**: *cette commande est visible par les autres*

                **Exemples**: `/afficher_les_artefacts 1` | `/afficher_les_artefacts 2`
                """, inline=False)

        help_embed.add_field(name="__**Afficher les livres des archives**__", value="""
                **Nom de la commande**: `/afficher_les_livres_des_archives`
                **Paramètre**: `page`
                Valeurs possibles pour `page`: `1` ou `2`
                
                **Visibilité**: *cette commande est visible par les autres*

                **Exemples**: `/afficher_les_livres_des_archives 1` | `/afficher_les_livres_des_archives 2`
                """, inline=False)

        help_embed.add_field(name="__**Afficher les livres de quêtes**__", value="""                
                **Nom de la commande**: `/afficher_les_livres_de_quete`

                **Visibilité**: *cette commande est visible par les autres*

                **Exemple**: `/afficher_les_livres_de_quete`
                """, inline=False)

        help_embed.add_field(name="__**Afficher un dossier confidentiel**__", value="""
                **Nom de la commande**: `/dossiers_confidentiels`

                **Visibilité**: *cette commande n'est pas visible par les autres*

                **Exemple**: `/dossiers_confidentiels`
                """, inline=False)

        help_embed.add_field(name="__**Afficher les personnages dont les aptitudes sont farmables aujourd'hui**__", value="""
                        **Nom de la commande**: `/afficher_persos_farmables`

                        **Visibilité**: *cette commande n'est pas visible par les autres*

                        **Exemple**: `/afficher_persos_farmables`
                        """, inline=False)

        help_embed.add_field(name="__**Afficher les armes farmables aujourd'hui**__",
                             value="""
                                **Nom de la commande**: `/afficher_armes_farmables`

                                **Visibilité**: *cette commande n'est pas visible par les autres*

                                **Exemple**: `/afficher_armes_farmables`
                                """, inline=False)

        help_embed.set_thumbnail(url=self.client.me.icon_url)

        await ctx.send(embeds=help_embed, ephemeral=True)


def setup(client):
    Help(client)
