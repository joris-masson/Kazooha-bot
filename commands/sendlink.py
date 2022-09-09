import discord

from discord.ext import commands
from utils.functions import log


class SendLink(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        log(f"'{__name__}' initialisé")

    @commands.command(name="sendLink")
    async def send_link(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
            title="Cliquez ici, c'est trop bien :o",
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        )
        embed.set_image(url="https://cdn.oneesports.gg/cdn-data/2022/03/GenshinImpact_YaeMikoFoxFormRaidenShogun4-1024x576.jpg")
        await ctx.send(embed=embed)
