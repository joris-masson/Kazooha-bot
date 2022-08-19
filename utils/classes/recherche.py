import discord
import saucenao_api
import os

from saucenao_api import SauceNao
from saucenao_api.errors import LongLimitReachedError, ShortLimitReachedError
from utils.functions import get_link_from_message, get_all_images, compare_image
from dotenv import load_dotenv

# TODO les logs
class Recherche:
    def __init__(self, msg: discord.Message):
        load_dotenv()
        self.SAUCENAO_TOKEN = os.getenv("SAUCENAO_TOKEN")
        self.SAUCENAO_TOKEN2 = os.getenv("SAUCENAO_TOKEN2")

        self.msg = msg
        self.images_link = self.__get_images()
        self.sauces = []
        if self.images_link is not None and not self.__check_if_good_sauce_provided():
            self.sauces = self.__get_sauces()

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
                    if not compare_image(base_image, image_link):
                        return False
            return True

    async def reply_with_sauce(self):
        if len(self.sauces) != 0:
            reply = ""
            for sauce in self.sauces:
                reply += f"Merci d'indiquer la source dans le même message que votre image, sinon les modos vont vous tomber dessus :eyes:\nAuteur: {sauce.author}\nSauce: <{sauce.urls[0]}>\nSimilarité: {sauce.similarity}%\n\n"
            await self.msg.reply(reply)
