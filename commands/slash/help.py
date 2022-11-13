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
        log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        help_embed = interactions.Embed(title="__Aide pour Kazooha__", description="Voici un petit recap des commandes du bot")

        help_embed.add_field(name="__**Préfix**__", value="Le bot utilise maintenant les commandes slashs!\ncommencez votre commande par `/` et vous devriez être guidés!")

        help_embed.add_field(name="__**Afficher les artéfacts**__", value="""
                Nom de la commande: `/afficher_les_artefacts`
                Paramètre: `page`
                Valeurs possibles pour `page`: `1` ou `2`

                Exemples: `/afficher_les_artefacts 1` | `/afficher_les_artefacts 2`
                """, inline=False)

        help_embed.add_field(name="__**Afficher les livres des archives**__", value="""
                Nom de la commande: `/afficher_les_livres_des_archives`
                Paramètre: `page`
                Valeurs possibles pour `page`: `1` ou `2`

                Exemples: `/afficher_les_livres_des_archives 1` | `/afficher_les_livres_des_archives 2`
                """, inline=False)

        help_embed.add_field(name="__**Afficher les livres de quêtes**__", value="""
                Nom de la commande: `/afficher_les_livres_de_quete`

                Exemple: `/afficher_les_livres_de_quete`
                """, inline=False)

        help_embed.add_field(name="__**Afficher un dossier confidentiel**__", value="""
                Nom de la commande: `/dossiers_confidentiels`

                Exemple: `/dossiers_confidentiels`
                """, inline=False)

        print(self.client.me.icon_url)
        help_embed.set_thumbnail(url=self.client.me.icon_url)

        await ctx.send(embeds=help_embed, ephemeral=True)


def setup(client):
    Help(client)
