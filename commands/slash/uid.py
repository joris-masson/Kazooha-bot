import os
import interactions
import genshin

from utils.functions import log
from utils.database import open_connection
from dotenv import load_dotenv


class Uid(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client
        self.game_names = {
            "genshin": ["genshin", "gi", "genshinimpact"],
            "honkai": ["honkai", "honkaiimpact", "hi3", "hi", "3rd", "honkaiimpact3rd"],
            "star_rail": ["honkaistarrail", "star", "rail", "hsr", "starrail"]
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
                        name="uid",
                        description="L'ancien UID",
                        type=interactions.OptionType.STRING,
                        required=True
                    ),
                    interactions.Option(
                        name="nouvel_uid",
                        description="L'UID qui remplacera l'ancien",
                        type=interactions.OptionType.STRING,
                        required=True
                    )
                ]
            )
        ]
    )
    async def uid(self, ctx: interactions.CommandContext, sub_command: str, uid="", jeu="", nouvel_uid=""):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")

        if jeu is not None:
            if sub_command == "ajouter" and await self.is_uid_good(ctx, uid):
                jeu = await self.get_game(ctx, jeu)
                await self.ajouter(ctx, uid, jeu)
            elif sub_command == "liste":
                jeu = await self.get_game(ctx, jeu)
                await self.liste(ctx, jeu)
            elif sub_command == "retirer" and await self.is_uid_good(ctx, uid):
                await self.retirer(ctx, uid)
            elif sub_command == "modifier" and await self.is_uid_good(ctx, uid) and await self.is_uid_good(ctx, nouvel_uid):
                await self.modifier(ctx, uid, nouvel_uid)

    async def ajouter(self, ctx: interactions.CommandContext, uid: str, jeu: str):
        db = open_connection()
        cursor = db.cursor()
        if jeu == "genshin":
            user_info = await self.get_genshin_user_info(uid)
            if user_info is not None:
                cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid, nickname, level) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}', '{user_info.info.nickname}', '{user_info.info.level}')")
            else:
                cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}')")
        elif jeu == "honkai":
            user_info = await self.get_honkai_user_info(uid)
            if user_info is not None:
                cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid, nickname, level) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}', '{user_info.info.nickname}', '{user_info.info.level}')")
            else:
                cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}')")
        else:
            cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}')")
        db.commit()
        cursor.close()
        db.close()
        await ctx.send("UID ajouté!", ephemeral=True)

    async def liste(self, ctx: interactions.CommandContext, jeu: str):
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM Kazooha.GameUid WHERE game='{jeu}' ORDER BY discordId")
        uids = cursor.fetchall()
        cursor.close()
        db.close()

        desc = ""
        for uid in uids:
            discord_id = uid[0]

            server = uid[2]
            user_id = uid[3]
            nickname = uid[4]
            level = uid[5]

            if nickname is not None and level is not None:
                desc += f"({server})<@{discord_id}>({nickname} Lv.{level}) -> {user_id}\n"
            else:
                desc += f"({server})<@{discord_id}> -> {user_id}\n"

        embed = interactions.Embed(
            title=f"Joueurs pour {jeu}",
            description=desc
        )
        await ctx.send(embeds=embed, ephemeral=True)

    async def retirer(self, ctx: interactions.CommandContext, uid: str):
        if await self.is_author_good(ctx, uid):
            db = open_connection()
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM Kazooha.GameUid WHERE uid='{uid}'")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("UID supprimé!", ephemeral=True)

    async def modifier(self, ctx: interactions.CommandContext, uid: str, new_uid: str):
        if await self.is_author_good(ctx, uid):
            db = open_connection()
            cursor = db.cursor()
            cursor.execute(f"UPDATE Kazooha.GameUid SET uid='{new_uid}' WHERE uid='{uid}'")
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("UID mis à jour!", ephemeral=True)

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

    async def is_author_good(self, ctx: interactions.CommandContext, uid: str) -> bool:
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT discordId FROM Kazooha.GameUid WHERE uid='{uid}'")
        discord_id = cursor.fetchall()[0]
        cursor.close()
        db.close()
        if ctx.author.id == discord_id:
            return True
        else:
            await ctx.send("Vous n'avez pas l'autorisation de modifier ou de supprimer un UID qui ne vous appartient pas.", ephemeral=True)
            return False

    async def get_genshin_user_info(self, uid: str) -> genshin.models.PartialGenshinUserStats or None:
        load_dotenv()
        client = genshin.Client(game=genshin.Game.GENSHIN)
        client.set_cookies(ltuid=os.getenv("LAB_LTUID"), ltoken=os.getenv("LAB_LTOKEN"))
        try:
            res = await client.get_partial_genshin_user(int(uid))
            return res
        except genshin.errors.DataNotPublic:
            return None

    async def get_honkai_user_info(self, uid: str) -> genshin.models.HonkaiUserStats or None:
        load_dotenv()
        client = genshin.Client(game=genshin.Game.HONKAI)
        client.set_cookies(ltuid=os.getenv("LAB_LTUID"), ltoken=os.getenv("LAB_LTOKEN"))
        try:
            res = await client.get_honkai_user(int(uid))
            return res
        except genshin.errors.DataNotPublic:
            return None


def setup(client):
    Uid(client)
