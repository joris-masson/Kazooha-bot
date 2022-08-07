from discord.ext import commands


class IdToTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="idToTime")
    async def id_to_time(self, ctx, discord_id: int):
        converted_id = int((int(bin(discord_id)[:-22], 2) + 1420070400000) / 1000)

        print(f"<t:{converted_id}>")
        await ctx.message.reply(f"L'objet a été créé le: <t:{converted_id}>\nTimestamp discord: `<t:{converted_id}>`")


