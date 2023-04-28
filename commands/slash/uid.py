import interactions
from utils.functions import log
from utils.database import open_connection


class Uid(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client
        self.game_names = {
            "genshin": ["genshin", "gi"],
            "honkai": ["honkai", "honkaiimpact", "hi3", "hi", "3rd"],
            "star_rail": ["star", "rail", "hsr"]
        }

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
    async def uid(self, ctx: interactions.CommandContext, sub_command: str, uid="", jeu=""):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")

        jeu = await self.get_game(ctx, jeu)
        if jeu is not None and await self.is_uid_good(ctx, uid):
            if sub_command == "ajouter":
                await self.ajouter(ctx, uid, jeu)
            elif sub_command == "liste":
                await self.liste(ctx, jeu)
            elif sub_command == "retirer":
                await self.retirer(ctx, uid, jeu)
            elif sub_command == "modifier":
                await self.modifier(ctx, uid, jeu)

    async def ajouter(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}')")
        db.commit()
        cursor.close()
        db.close()
        await ctx.send("UID ajouté!", ephemeral=True)

    async def liste(self, ctx: interactions.CommandContext, jeu: str):
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM Kazooha.GameUid WHERE game='{jeu}'")
        uids = cursor.fetchall()
        cursor.close()
        db.close()

        desc = ""
        for uid in uids:
            discord_id = uid[0]

            server = uid[2]
            user_id = uid[3]

            desc += f"({server})<@{discord_id}> -> {user_id}\n"

        embed = interactions.Embed(
            title=f"Joueurs pour {jeu}",
            description=desc
        )
        await ctx.send(embeds=embed, ephemeral=True)

    async def retirer(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        await ctx.send("Commande non implémentée pour le moment")

    async def modifier(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        await ctx.send("Commande non implémentée pour le moment")

    async def get_game(self, ctx: interactions.CommandContext, jeu: str) -> str or None:
        jeu = jeu.lower().replace(' ', '')
        for game in self.game_names:
            if jeu in self.game_names[game]:
                return game
        await ctx.send("Jeu non trouvé", ephemeral=True)
        return None

    def get_server(self, jeu: str, uid: str) -> str:
        if jeu == "genshin" or jeu == "star_rail":
            if uid.startswith("6"):
                return "America"
            if uid.startswith("7"):
                return "Europe"
            if uid.startswith("8"):
                return "Asia"
            if uid.startswith("9"):
                return "TW, HK, MO"
        if jeu == "honkai":
            if uid.startswith("2"):
                return "Europe"

    async def is_uid_good(self, ctx: interactions.CommandContext, uid: str) -> bool:
        if len(uid) == 9:
            return True
        else:
            await ctx.send("Format de l'UID invalide", ephemeral=True)
            return False


def setup(client):
    Uid(client)
