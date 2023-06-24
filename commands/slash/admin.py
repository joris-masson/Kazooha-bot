import interactions
import re

from utils.functions import log


class Admin(interactions.Extension):
    def __init__(self, client):
        log(f"'{__name__}' initialisé")
        self.client: interactions.Client = client

    @interactions.extension_command(
        name="admin",
        options=[
            interactions.Option(
                name="count_emotes",
                description="fais un petit compte des emotes les plus utilisées sur un serveur",
                type=interactions.OptionType.SUB_COMMAND
            ),
            interactions.Option(
                name="test",
                description="test",
                type=interactions.OptionType.SUB_COMMAND
            )
        ]
    )
    async def admin(self, ctx: interactions.CommandContext, sub_command: str):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        if sub_command == "count_emotes":
            await self.count_emotes(ctx)
        elif sub_command == "test":
            await self.test(ctx)

    async def count_emotes(self, ctx):
        the_serv = await ctx.get_guild()
        res = {}
        serv_emotes = []
        for emote in the_serv.emojis:
            serv_emotes.append(f"<:{emote.name}:{emote.id}>")
        for channel in await the_serv.get_all_channels():
            print(f"Je compte dans {channel.name}\n{str(res)}")
            if channel.type == interactions.ChannelType.GUILD_TEXT or channel.type == interactions.ChannelType.PRIVATE_THREAD or channel.type == interactions.ChannelType.PUBLIC_THREAD:
                try:
                    for message in await channel.history(maximum=1000).flatten():
                        if not message.author.bot:
                            custom_emojis = re.findall(r'<:\w*:\d*>', message.content)
                            if len(custom_emojis) >= 1:
                                for emoji in custom_emojis:
                                    if emoji in serv_emotes:
                                        try:
                                            res[emoji] += 1
                                        except KeyError:
                                            res[emoji] = 1
                except IndexError:
                    pass
        print(f"Jéfini")
        for emote in sorted(res, key=res.get, reverse=True):
            print(f"{emote}: {res[emote]}")

    async def test(self, ctx):
        await ctx.send("aaaaaaaaaaa")


def setup(client):
    Admin(client)
