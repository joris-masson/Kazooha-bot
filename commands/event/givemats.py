import os
from interactions import Extension, Task, IntervalTrigger, OptionType, Embed, SlashContext, slash_command, slash_option, listen
from datetime import datetime
from dotenv import load_dotenv
from utils.util import log
from utils.mats_util import generate_embeds


class GiveMats(Extension):
    @listen()
    async def on_startup(self):
        self.send_mats.start()

    """@slash_command(name="send")
    async def command(self, ctx: SlashContext):
        await ctx.defer(ephemeral=True)
        data = (generate_embeds(True), generate_embeds(False))
        await ctx.send("Personnages à farmer aujourd'hui", embeds=data[0][0], files=data[0][1], ephemeral=True)
        await ctx.send("Armes à farmer aujourd'hui", embeds=data[1][0], files=data[1][1], ephemeral=True)"""

    @Task.create(IntervalTrigger(minutes=30))
    async def send_mats(self):
        log("EVENT", "Démarrage de givemats")
        if self.check_can_be_sent():
            log("EVENT", "Préparation de l'envoi.")
            load_dotenv()
            channel = self.bot.get_channel(os.getenv("MATS_CHANNEL_ID"))
            data = (generate_embeds(True), generate_embeds(False))
            if not self.message_exists():
                log("EVENT", "Les messages n'existent pas, envoi programmé.")
                log("EVENT", "Envoi du message des personnages...")
                chars_message = await channel.send("Personnages à farmer aujourd'hui", embeds=data[0][0], files=data[0][1])
                log("EVENT", "Envoi du message des armes...")
                weaps_message = await channel.send("Armes à farmer aujourd'hui", embeds=data[1][0], files=data[1][1])
                with open(r"data/events/givemats/last_day.txt", 'w') as last_day_file:
                    log("EVENT", "Mise à jour de 'last_day.txt'.")
                    last_day_file.write(f"{str(datetime.now().day)}\n{str(chars_message.id)}\n{str(weaps_message.id)}")
            else:
                chars_message_id = 0
                weaps_message_id = 0
                with open(rf"data/events/givemats/last_day.txt", 'r') as last_day_file:
                    try:
                        lines = last_day_file.readlines()
                        chars_message_id = int(lines[1].replace('\n', ''))
                        weaps_message_id = int(lines[2].replace('\n', ''))
                        print(chars_message_id, weaps_message_id)
                        chars_message = await channel.fetch_message(message_id=chars_message_id)
                        weaps_message = await channel.fetch_message(message_id=weaps_message_id)
                        log("EVENT", "Edition du message des personnages.")
                        await chars_message.edit(embeds=data[0][0], files=data[0][1])
                        log("EVENT", "Edition du message des armes.")
                        await weaps_message.edit(embeds=data[1][0], files=data[1][1])
                        log("EVENT", "Mise à jour de 'last_day.txt'.")
                    except IndexError:
                        log("EVENT", "IndexError")
                        pass
                with open(rf"data/events/givemats/last_day.txt", 'w') as last_day_file:
                    last_day_file.write(f"{str(datetime.now().day)}\n{str(chars_message_id)}\n{str(weaps_message_id)}")
        else:
            log("EVENT", "Ce n'est pas l'heure de l'envoi.")

    def check_can_be_sent(self):
        start_hour = 5
        return ((start_hour <= datetime.now().hour < start_hour + 1) and not self.is_same_day()) or not self.message_exists()

    def is_same_day(self):
        with open(r"data/events/givemats/last_day.txt", 'r') as last_day_file:
            try:
                return datetime.now().day == int(last_day_file.readlines()[0])
            except IndexError:
                return False

    def message_exists(self):
        with open(r"data/events/givemats/last_day.txt", 'r') as last_day_file:
            try:
                lines = last_day_file.readlines()
                a = lines[1]
                b = lines[2]
                return True
            except IndexError:
                return False
