from interactions import Extension, slash_command, slash_option, SlashContext, OptionType
from utils.util import convert_discord_id_to_time, log


class IdToTime(Extension):
    @slash_command(
        name="id_to_time",
        description="Conversion d'un ID discord en un timestamp."
    )
    @slash_option(
        name="discord_id",
        description="L'ID à convertir",
        required=True,
        opt_type=OptionType.STRING
    )
    async def command(self, ctx: SlashContext, discord_id: str):
        log("SLASH", f"Commande slash `/id_to_time discord_id:{discord_id}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})")

        timestamp = convert_discord_id_to_time(int(discord_id))
        await ctx.send(f"<t:{timestamp}>", ephemeral=True)
