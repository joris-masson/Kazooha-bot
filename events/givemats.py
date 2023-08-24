import os
import interactions

from utils.functions import log
from utils.classes.matsimagemaker import MatsImageMaker
from interactions.ext.tasks import IntervalTrigger, create_task
from datetime import datetime
from dotenv import load_dotenv


class GiveMats(interactions.Extension):
    def __init__(self, client):
        load_dotenv()
        self.client = client

        self.start_hour = 5
        self.dico_day = {
            0: ["Lundi"],
            1: ["Mardi"],
            2: ["Mercredi"],
            3: ["Lundi"],
            4: ["Mardi"],
            5: ["Mercredi"],
            6: ["Lundi", "Mardi", "Mercredi"]
        }

        self.send_channel = None

        self.method = create_task(IntervalTrigger(300))(self.method)
        self.method.start()

    async def method(self):
        if ((self.start_hour <= datetime.now().hour < self.start_hour + 1) and not self.is_same_day()) or not self.message_exists() or not self.is_same_day():
            if self.send_channel is None:
                self.send_channel = await interactions.get(self.client, interactions.Channel, object_id=int(os.getenv("MATS_CHANNEL_ID")))
            a = MatsImageMaker(self.dico_day[datetime.now().weekday()])
            a.make()
            embed_chars = interactions.Embed(
                title="Les personnages pouvant être farmés aujourd'hui"
            )
            mats_chars_image = interactions.File("data/out/mats_chars.png")
            embed_chars.set_image(url="attachment://mats_chars.png")

            embed_weapons = interactions.Embed(
                title="Les armes pouvant être farmées aujourd'hui"
            )
            mats_weapons_image = interactions.File("data/out/mats_weapons.png")
            embed_weapons.set_image(url="attachment://mats_weapons.png")
            if not self.message_exists():
                message = await self.send_channel.send(embeds=[embed_chars, embed_weapons], files=[mats_chars_image, mats_weapons_image])
            with open(rf"data/events/givemats/last_day.txt", 'r') as last_day_file:
                try:
                    message = await self.send_channel.get_message(message_id=int(last_day_file.readlines()[1]))
                    await message.edit(embeds=[embed_chars, embed_weapons], files=[mats_chars_image, mats_weapons_image])
                except IndexError:
                    pass
            with open(rf"data/events/givemats/last_day.txt", 'w') as last_day_file:
                last_day_file.write(f"{str(datetime.now().day)}\n{str(message.id)}")

    def is_same_day(self):
        with open(rf"data/events/givemats/last_day.txt", 'r') as last_day_file:
            try:
                return datetime.now().day == int(last_day_file.readlines()[0])
            except IndexError:
                return False

    def message_exists(self):
        with open(rf"data/events/givemats/last_day.txt", 'r') as last_day_file:
            try:
                a = last_day_file.readlines()[1]
                return True
            except IndexError:
                return False


def setup(client):
    GiveMats(client)
