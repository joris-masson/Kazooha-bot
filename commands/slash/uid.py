from interactions import Extension, SlashContext, SlashCommandChoice, OptionType, Embed, slash_command, slash_option

from utils.util import open_db_connection, log


class Uid(Extension):
    @slash_command(
        name="uid",
        sub_cmd_name="ajouter",
        sub_cmd_description="Ajouter un UID."
    )
    @slash_option(
        name="jeu",
        description="Le jeu à gérer.",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="Honkai Impact 3rd", value="honkai"),
            SlashCommandChoice(name="Genshin Impact", value="genshin"),
            SlashCommandChoice(name="Honkai: Star Rail", value="star rail"),
            SlashCommandChoice(name="Zenless Zone Zero", value="zzz")
        ]
    )
    @slash_option(
        name="uid",
        description="l'UID à ajouter.",
        required=True,
        opt_type=OptionType.STRING,
    )
    async def ajouter(self, ctx: SlashContext, jeu: str, uid: str) -> None:
        log("SLASH", log("SLASH", f"Commande slash `/uid ajouter jeu:{jeu} uid:{uid}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})"))

        db = open_db_connection()
        cursor = db.cursor()

        cursor.execute(f"INSERT INTO Kazooha.GameUid(discordId, game, server, uid) VALUE ('{int(ctx.author.id)}', '{jeu}', '{self.get_server(jeu, uid)}', '{int(uid)}')")

        db.commit()
        log("DB", f"Ajout d'un nouvel UID dans Kazooha.GameUid -> ({ctx.author.id}, {jeu}, {self.get_server(jeu, uid)}, {uid})")
        cursor.close()
        db.close()
        await ctx.send("UID ajouté !", ephemeral=True)

    @slash_command(
        name="uid",
        sub_cmd_name="liste",
        sub_cmd_description="Lister les UIDs pour un jeu donné.",
    )
    @slash_option(
        name="jeu",
        description="Le jeu.",
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="Honkai Impact 3rd", value="honkai"),
            SlashCommandChoice(name="Genshin Impact", value="genshin"),
            SlashCommandChoice(name="Honkai: Star Rail", value="star rail"),
            SlashCommandChoice(name="Zenless Zone Zero", value="zzz")
        ]
    )
    async def liste(self, ctx: SlashContext, jeu: str) -> None:
        log("SLASH", log("SLASH", f"Commande slash `/uid liste jeu:{jeu}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})"))

        db = open_db_connection()
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM Kazooha.GameUid WHERE game='{jeu}' ORDER BY discordId")
        uids = cursor.fetchall()
        cursor.close()
        db.close()

        desc = ""
        for uid in uids:
            discord_id = uid[0]

            game = uid[1]

            server = uid[2]
            user_id = uid[3]
            nickname = uid[4]
            level = uid[5]

            if nickname is not None and level is not None:
                desc += f"({server})<@{discord_id}>({nickname} Lv.{level}) -> `{user_id}`\n"
            else:
                desc += f"({server})<@{discord_id}> -> `{user_id}`\n"

        embed = Embed(
            title=f"Joueurs pour {jeu}",
            description=desc
        )
        await ctx.send(embeds=embed, ephemeral=True)

    @slash_command(
        name="uid",
        sub_cmd_name="retirer",
        sub_cmd_description="Retirer un UID d'un jeu donné"
    )
    @slash_option(
        name="uid",
        description="L'UID à retirer",
        required=True,
        opt_type=OptionType.STRING
    )
    async def retirer(self, ctx: SlashContext, uid: str):
        log("SLASH", log("SLASH", f"Commande slash `/uid retirer uid:{uid}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})"))

        if await self.is_author_good(ctx, uid):
            db = open_db_connection()
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM Kazooha.GameUid WHERE uid='{uid}'")
            db.commit()
            log("DB", f"Suppression de '{uid}' de Kazooha.GameUid")
            cursor.close()
            db.close()
            await ctx.send("UID supprimé !", ephemeral=True)
        else:
            await ctx.send("Vous n'avez pas l'autorisation de supprimer un UID qui ne vous appartient pas.", ephemeral=True)

    @slash_command(
        name="uid",
        sub_cmd_name="modifier",
        sub_cmd_description="Modifier un UID déjà enregistré."
    )
    @slash_option(
        name="uid",
        description="L'UID à modifier",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="new_uid",
        description="Le nouvel UID",
        required=True,
        opt_type=OptionType.STRING
    )
    async def modifier(self, ctx: SlashContext, uid: str, new_uid: str):
        log("SLASH", log("SLASH", f"Commande slash `/uid modifier uid:{uid} new_uid:{new_uid}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})"))

        if await self.is_author_good(ctx, uid):
            db = open_db_connection()
            cursor = db.cursor()
            cursor.execute(f"UPDATE Kazooha.GameUid SET uid='{new_uid}' WHERE uid='{uid}'")
            db.commit()
            log("DB", f"Modification de l'UID {uid} vers {new_uid} dans Kazooha.GameUid")
            cursor.close()
            db.close()
            await ctx.send("UID mis à jour !", ephemeral=True)
        else:
            await ctx.send("Vous n'avez pas l'autorisation de modifier un UID qui ne vous appartient pas.", ephemeral=True)

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
        else:
            return "Unknown"

    async def is_author_good(self, ctx: SlashContext, uid: str) -> bool:
        db = open_db_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT discordId FROM Kazooha.GameUid WHERE uid='{uid}'")
        discord_id = cursor.fetchall()[0]
        cursor.close()
        db.close()
        return ctx.author.id == discord_id[0]
