import genshin.errors
from interactions import Extension, slash_command, slash_option, SlashContext, OptionType, Embed, File
from utils.genshin_util import get_genshin_client, get_genshin_player_info, prepare_player_characters_image
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
        await ctx.defer(ephemeral=True)
        try:
            client = get_genshin_client()
            user_data = await client.get_genshin_user(int(uid))
            detailed_infos = await get_genshin_player_info(uid)

            nickname = detailed_infos["nickname"]
            ar = detailed_infos["adventure_rank"]
            icon = detailed_infos["icon"]

            embed = Embed(
                title=f"{nickname} (AR {ar})",
                thumbnail=icon
            ).add_field(
                name="Personnages possédés",
                value=user_data.stats.characters,
                inline=False
            ).add_field(
                name="Succès",
                value=user_data.stats.achievements,
                inline=True
            ).add_field(
                name="Jours d'activité",
                value=user_data.stats.days_active,
                inline=True,
            )
            img_name = prepare_player_characters_image(uid, detailed_infos["characters"])
            image = File(img_name[0])
            embed.set_image(f"attachment://{img_name[1]}")
            await ctx.send(embeds=embed, files=image, ephemeral=True)
        except ValueError:
            await ctx.send("UID incorrect.", ephemeral=True)
        except genshin.errors.DataNotPublic:
            await ctx.send("Les données de cet utilisateur ne sont pas publiques.", ephemeral=True)
