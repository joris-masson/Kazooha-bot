# prog par Dr.Emma(retire ça et jte pete les genoux)
import interactions


class GenshinGeoguessr(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.extension_command(name="genshin_geoguessr", options=[interactions.Option(name="submit", description="Soumettre une photo d un lieu", type=interactions.OptionType.SUB_COMMAND), interactions.Option(name="guess", description="Soumettre votre idee de lieu present dans la photo", type=interactions.OptionType.SUB_COMMAND)])
    async def genshin_geoguessr(self, ctx: interactions.CommandContext, sub_command: str):
        if sub_command == "submit":
            await self.soumettre(ctx)
        elif sub_command == "guess":
            pass

    async def soumettre(self, ctx: interactions.CommandContext):
        """
        si image, envoie dans salon/fil dédie un message
        message: contient image et deux boutons(yes, no)
        bouton oui: enregistre dans un rep commun l image et des infos autour(auteur)
        //     non: envoie un dm à l auteur(ou ailleurs) pour annoncer refus
        """
        pass

    async def guess(self, ctx: interactions.CommandContext):
        """
        ctx doit contenir image de carte
        envoie dans salon/fil dedie l image et ping la personne l ayant proposee
        demerdez vous pour comparer les res de tout le monde
        """
        pass


def setup(client):
    GenshinGeoguessr(client)
