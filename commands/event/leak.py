import os

from interactions import Task, IntervalTrigger, Extension, Embed, EmbedFooter, listen
from utils.util import open_db_connection, log
from dotenv import load_dotenv


class Leak(Extension):
    @listen()
    async def on_startup(self):
        self.send_new_leaks.start()

    @Task.create(IntervalTrigger(minutes=5))
    async def send_new_leaks(self):
        new_leaks = self.check_new_leaks()
        if new_leaks is not None:
            db = open_db_connection()
            cursor = db.cursor()
            load_dotenv()
            leak_channel = self.bot.get_channel(os.getenv("LEAK_CHANNEL_ID"))

            for leak in new_leaks:
                title = leak[2]
                footer = EmbedFooter(f"/u/{leak[4]}")

                embed = Embed(
                    title=title,
                    url=leak[3],
                    footer=footer
                )

                embed.set_image(url=leak[5])

                await leak_channel.send(embeds=embed)
                log("EVENT", f"Le leak \"{title}\" a été envoyé.")

                query = f"UPDATE Kazooha.Leak SET sent=1 WHERE id='{leak[0]}'"
                cursor.execute(query)
                log("DB", f"Le leak d'ID `{leak[0]}` a été update: `sent=0` -> `sent=1`")
            db.commit()
            cursor.close()
            db.close()

    def check_new_leaks(self):
        db = open_db_connection()
        cursor = db.cursor()

        query = "SELECT DISTINCT * FROM Kazooha.Leak WHERE sent=0"
        cursor.execute(query)

        all_leaks = cursor.fetchall()

        cursor.close()
        db.close()

        return all_leaks
