import interactions
from utils.functions import log


class Uid(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="uid",
        description="Commande qui gère les UID",
        options=[
            interactions.Option(
                name="ajouter",
                description="Ajoute un UID au bot.",
                type=interactions.OptionType.SUB_COMMAND,
                options=[
                    interactions.Option(
                        name="uid",
                        description="L'UID à ajouter",
                        type=interactions.OptionType.STRING,
                        required=True
                    ),
                    interactions.Option(
                        name="jeu",
                        description="Le jeu",
                        type=interactions.OptionType.STRING,
                        required=True
                    )
                ]
            ),
            interactions.Option(
                name="liste",
                description="Liste tous les UIDs actuellement enregistrés pour un jeu donné.",
                type=interactions.OptionType.SUB_COMMAND,
                options=[
                    interactions.Option(
                        name="jeu",
                        description="Le jeu",
                        type=interactions.OptionType.STRING,
                        required=True
                    )
                ]
            ),
            interactions.Option(
                name="retirer",
                description="Retirer un UID enregistré.",
                type=interactions.OptionType.SUB_COMMAND,
                options=[
                    interactions.Option(
                        name="jeu",
                        description="Le jeu",
                        type=interactions.OptionType.STRING,
                        required=True
                    ),
                    interactions.Option(
                        name="uid",
                        description="L'UID à retirer",
                        type=interactions.OptionType.STRING,
                        required=True
                    )
                ]
            ),
            interactions.Option(
                name="modifier",
                description="Modifier un UID donné.",
                type=interactions.OptionType.SUB_COMMAND,
                options=[
                    interactions.Option(
                        name="jeu",
                        description="Le jeu",
                        type=interactions.OptionType.STRING,
                        required=True
                    ),
                    interactions.Option(
                        name="uid",
                        description="L'UID qui remplacera l'ancien",
                        type=interactions.OptionType.STRING,
                        required=True
                    )
                ]
            )
        ]
    )
    async def uid(self, ctx: interactions.CommandContext, sub_command: str, uid: str, jeu: str):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")

        if sub_command == "ajouter":
            self.ajouter(ctx, uid, jeu)
        elif sub_command == "liste":
            self.liste(ctx)
        elif sub_command == "retirer":
            self.retirer(ctx, uid, jeu)
        elif sub_command == "modifier":
            self.modifier(ctx, uid, jeu)

    def ajouter(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        pass

    def liste(self, ctx):
        pass

    def retirer(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        pass

    def modifier(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        pass


def setup(client):
    Uid(client)
