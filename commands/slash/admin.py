import os
import interactions
import re

from utils.functions import log
from random import shuffle


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
                name="give_marqueurs",
                description="Donne les marqueurs, mélangés",
                type=interactions.OptionType.SUB_COMMAND
            )
        ]
    )
    async def admin(self, ctx: interactions.CommandContext, sub_command: str):
        try:
            log(f"{__name__} utilisé par @{ctx.author.name}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur le serveur {ctx.guild.name}({ctx.guild.id})")
        except AttributeError:
            log(f"{__name__} utilisé")
        if ctx.author.id != 171028477682647040:
            await ctx.send("Vous n'avez pas l'autorisation de lancer cette commande", ephemeral=True)
        else:
            if sub_command == "count_emotes":
                await self.count_emotes(ctx)
            elif sub_command == "give_marqueurs":
                await self.give_marqueurs(ctx)

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

    async def give_marqueurs(self, ctx):
        img_list = os.listdir("data/commands/admin/give_marqueurs/img")
        dict_attributions = self.attribute_all(img_list)
        for participant in dict_attributions:
            embed = interactions.Embed(description=f"Marqueur de <@{dict_attributions[participant]}>.")
            marqueur_image = interactions.File(f"data/commands/admin/give_marqueurs/img/{dict_attributions[participant]}.png")
            embed.set_image(f"attachment://{dict_attributions[participant]}.png")
            await ctx.send(f"<@{participant}>", embeds=embed, files=marqueur_image)

    def attribute_all(self, img_list: list[str]) -> dict[int, int]:
        res = {}
        while len(res) != len(img_list):
            ze_list = img_list.copy()
            shuffle(ze_list)
            for participant in [int(img_name[:-4]) for img_name in img_list]:
                for img_name in ze_list:
                    act_img = int(img_name[:-4])
                    if participant != act_img and self.check_if_inversion(participant, act_img, res):
                        res[participant] = act_img
                        ze_list.remove(img_name)
                        break
        return res

    def check_if_inversion(self, participant: int, img_name: int, res_dict: dict[int, int]) -> bool:
        for id_participant in res_dict:
            if img_name == id_participant and res_dict[id_participant] == participant:
                return False
        return True


def setup(client):
    Admin(client)
