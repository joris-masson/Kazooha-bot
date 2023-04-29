import interactions
from utils.functions import log
from utils.database import open_connection


class Uid(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        type=interactions.ApplicationCommandType.USER,
        name="Donne moi son UID!",
    )
    async def info(self, ctx: interactions.CommandContext):
        log(f"Les UIDs de {ctx.target.user.username} ont été demandés par {ctx.user.username}")
        db = open_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM Kazooha.GameUid WHERE discordId='{ctx.target.user.id}' ORDER BY game")
        uids = cursor.fetchall()
        cursor.close()
        db.close()

        if len(uids) != 0:
            desc = ""
            for uid in uids:
                game = uid[1]
                server = uid[2]
                user_id = uid[3]
                nickname = uid[4]
                level = uid[5]

                if nickname is not None and level is not None:
                    desc += f"**[{game}]**({server}) - {nickname} Lv.{level} -> {user_id}\n"
                else:
                    desc += f"**[{game}]**({server}) -> {user_id}\n"

            embed = interactions.Embed(title=f"UIDs de {ctx.target.user.username}", description=desc)
            await ctx.send(embeds=embed, ephemeral=True)
        else:
            await ctx.send(f"{ctx.target.user.username} n'a renseigné aucun UID.", ephemeral=True)


def setup(client):
    Uid(client)
