import genshin.errors
from interactions import Extension, slash_command, slash_option, SlashContext, OptionType, Embed
from utils.genshin_util import get_genshin_client
from utils.util import log


class GenshinInfo(Extension):
    @slash_command(
        name="infos_joueur_genshin",
        description="Donne des informations sur un joueur Genshin Impact avec son UID."
    )
    @slash_option(
        name="uid",
        description="L'UID du joueur dont les infos seront récupérées.",
        required=True,
        opt_type=OptionType.STRING
    )
    async def command(self, ctx: SlashContext, uid: str):
        log("SLASH", f"Commande slash `/infos_joueur_genshin uid:{uid}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})")
        try:
            client = get_genshin_client()
            user_data = await client.get_full_genshin_user(int(uid))

            embed_general = Embed(
                title=f"{user_data.info.nickname} (AR {user_data.info.level})",
            ).add_field(
                name="Succès",
                value=user_data.stats.achievements,
                inline=True
            ).add_field(
                name="Personnages",
                value=user_data.stats.characters,
                inline=True
            ).add_field(
                name="Jours d'activité",
                value=user_data.stats.days_active,
                inline=True,

            ).add_field(
                name="Abysses",
                value=f"{user_data.abyss.current.max_floor} ({user_data.abyss.current.total_stars} étoiles)",
                inline=True
            )

            await ctx.send(embeds=[embed_general], ephemeral=True)
        except ValueError:
            await ctx.send("UID incorrect.", ephemeral=True)
        except genshin.errors.DataNotPublic:
            await ctx.send("Les données de cet utilisateur ne sont pas publiques.", ephemeral=True)
