import discord
import saucenao_api
import os

from saucenao_api import SauceNao
from saucenao_api.errors import LongLimitReachedError, ShortLimitReachedError
from utils.functions import get_link_from_message, get_all_images, compare_image, convert_discord_id_to_time, log
from dotenv import load_dotenv
from data.log_channels import log_channels
from discord.ext import commands


class Recherche:
    def __init__(self, msg: discord.Message, client: commands.Bot):
        if not isinstance(msg.channel, discord.channel.DMChannel) and msg.guild.id in log_channels:
            self.client = client

            load_dotenv()
            self.SAUCENAO_TOKEN = os.getenv("SAUCENAO_TOKEN")
            self.SAUCENAO_TOKEN2 = os.getenv("SAUCENAO_TOKEN2")

            self.msg = msg
            self.images_link = self.__get_images()
            self.sauces = []
            if self.images_link is not None and not self.__check_if_good_sauce_provided():
                log(f"[IMG] - Recherche d'image initialisée dans <#{msg.channel.id} sur {msg.guild.name}, image envoyée par <@{msg.author.id}>")
                self.sauces = self.__get_sauces()
        else:
            self.sauces = []

    def __get_images(self) -> list[discord.Attachment] or None:
        if not len(self.msg.attachments) == 0:
            images_link_list = []
            for att in self.msg.attachments:
                if att.content_type.startswith("image") and ".gif" not in att.filename.lower():
                    images_link_list.append(att.url)
            return images_link_list
        else:
            return None

    def __check_if_link(self) -> bool:
        return not [element for element in ["http://", "https://"] if (element in self.msg.content)]

    def __get_sauces(self) -> list[saucenao_api.BasicSauce]:
        res = []
        for link in self.images_link:
            try:
                results = SauceNao(self.SAUCENAO_TOKEN, numres=1).from_url(link)
            except LongLimitReachedError or ShortLimitReachedError:
                results = SauceNao(self.SAUCENAO_TOKEN2, numres=1).from_url(link)
            if results[0].similarity > 70.0:
                res.append(results[0])
        return res

    def __check_if_good_sauce_provided(self):
        if [element for element in ["http://", "https://"] if (element in self.msg.content)]:
            all_images = get_all_images(get_link_from_message(self.msg))
            for base_image in self.images_link:
                for image_link in all_images:
                    print(base_image, image_link)
                    if compare_image(base_image, image_link):
                        return True
            return False
        else:
            return False

    async def reply_with_sauce(self):
        if len(self.sauces) != 0:
            await self.msg.add_reaction(emoji="⚠️")
            reply = ""
            for sauce in self.sauces:
                reply += f"\nSource: Auteur: {sauce.author}\nSauce: <{sauce.urls[0]}>\nSimilarité: {sauce.similarity}%\n\n"

            response = discord.Embed(
                title=f"Image sans source dans #{self.msg.channel.name}, envoyé par {self.msg.author} le <t:{convert_discord_id_to_time(self.msg.id)}:F>",
                url=self.msg.jump_url,
                description=f"**Fautif: <@{self.msg.author.id}>**\n{reply}"
            )

            await self.client.get_channel(log_channels[self.msg.guild.id]).send(embed=response)
            log("[IMG] - Source envoyée")
