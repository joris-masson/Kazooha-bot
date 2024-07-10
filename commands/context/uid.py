from interactions import Extension, user_context_menu, Embed, ContextMenuContext

from utils.util import open_db_connection


class Uid(Extension):
    @user_context_menu(
        name="uid_liste"
    )
    async def command(self, ctx: ContextMenuContext):
        db = open_db_connection()
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM Kazooha.GameUid WHERE discordId='{ctx.target.user.id}' ORDER BY game")
        uids = cursor.fetchall()
        cursor.close()
        db.close()

        if len(uids) > 0:
            desc = ""
            for uid in uids:
                discord_id = uid[0]

                server = uid[2]
                user_id = uid[3]
                nickname = uid[4]
                level = uid[5]

                if nickname is not None and level is not None:
                    desc += f"({server})<@{discord_id}>({nickname} Lv.{level}) -> `{user_id}`\n"
                else:
                    desc += f"({server})<@{discord_id}> -> `{user_id}`\n"

            embed = Embed(
                title=f"UIDs de {ctx.target.user.username}",
                description=desc
            )
            await ctx.send(embeds=embed, ephemeral=True)
        else:
            await ctx.send(f"<@{ctx.target.user.id}> n'a renseigné aucun UID.", ephemeral=True)
