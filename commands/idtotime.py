from discord.ext import commands
from utils.functions import log


class IdToTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="idToTime")
    async def id_to_time(self, ctx, discord_id: int):
        log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
        converted_id = int((int(bin(discord_id)[:-22], 2) + 1420070400000) / 1000)

        print(f"<t:{converted_id}>")
        await ctx.message.reply(f"L'objet a été créé le: <t:{converted_id}>\nTimestamp discord: `<t:{converted_id}>`")


