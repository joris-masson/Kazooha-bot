import discord
import os


class Archive:
    def __init__(self, channel: discord.TextChannel):
        self.channel = channel
        self.dir = rf"data/out/archives/{self.channel.guild.name}/{self.channel.name}/"

        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

        self.file = open(rf"{self.dir}archive.html", 'w', encoding="utf-8")

    async def make_archive(self):
        self.file.write("<!DOCTYPE html>")
        self.file.write("<html lang=\"fr\">")

        self.head()
        await self.body()
        self.file.write("</html>")
        self.file.close()

    def head(self):
        self.file.write("<head>")
        self.file.write(f"<title>{self.channel.guild.name} - {self.channel.name}</title>")
        self.file.write("<meta charset=utf-8>")
        self.file.write("<meta name=viewport content=\"width=device-width\">")

        with open(rf"utils/archive_bot/style/style.html", 'r') as style_file:
            for line in style_file:
                self.file.write(line)

        self.file.write("</head>")

    async def body(self):
        self.file.write("<body id=\"content\">")
        self.file.write(
            f"""<header id="infos"> <img class="guild_icon"
            src="{self.channel.guild.icon_url}"
            alt="Icone du serveur">
        <h3 class="text">{self.channel.guild.name}</h3>
        <div class="divider"></div> <svg width="24" height="24" viewBox="0 0 24 24" class="channel_icon">
            <path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd"
                d="M5.88657 21C5.57547 21 5.3399 20.7189 5.39427 20.4126L6.00001 17H2.59511C2.28449 17 2.04905 16.7198 2.10259 16.4138L2.27759 15.4138C2.31946 15.1746 2.52722 15 2.77011 15H6.35001L7.41001 9H4.00511C3.69449 9 3.45905 8.71977 3.51259 8.41381L3.68759 7.41381C3.72946 7.17456 3.93722 7 4.18011 7H7.76001L8.39677 3.41262C8.43914 3.17391 8.64664 3 8.88907 3H9.87344C10.1845 3 10.4201 3.28107 10.3657 3.58738L9.76001 7H15.76L16.3968 3.41262C16.4391 3.17391 16.6466 3 16.8891 3H17.8734C18.1845 3 18.4201 3.28107 18.3657 3.58738L17.76 7H21.1649C21.4755 7 21.711 7.28023 21.6574 7.58619L21.4824 8.58619C21.4406 8.82544 21.2328 9 20.9899 9H17.41L16.35 15H19.7549C20.0655 15 20.301 15.2802 20.2474 15.5862L20.0724 16.5862C20.0306 16.8254 19.8228 17 19.5799 17H16L15.3632 20.5874C15.3209 20.8261 15.1134 21 14.8709 21H13.8866C13.5755 21 13.3399 20.7189 13.3943 20.4126L14 17H8.00001L7.36325 20.5874C7.32088 20.8261 7.11337 21 6.87094 21H5.88657ZM9.41045 9L8.35045 15H14.3504L15.4104 9H9.41045Z">
            </path>
        </svg>
        <h3 class="text">{self.channel.name}</h3>
        <div class="divider"></div>
    </header>
            """
        )

        self.file.write("<main id=\"channel\">")

        messages = await self.channel.history(limit=None, oldest_first=True).flatten()
        for message in messages:
            self.file.write(await self.write_message(message))

        self.file.write("</main>")
        # self.file.write("<script>document.getElementById(\"content\").childNodes[0].remove()</script>")
        self.file.write("</body>")

    async def write_message(self, message: discord.Message) -> str:
        res = ""
        res += "<div class=\"message group_start\"\n>"
        res += f"""<div class="contents"> <img
                    src="{message.author.avatar_url}"
                    class="avatar">
                <h2 class="header"> <span class="username" style="color: #f8f8f9">{message.author.name}</span> <span
                        class="timestamp_header">{message.created_at.strftime("envoyé le %d/%m/%Y à %H:%M:%S")}</span> </h2>
                <div class="messageContent">{message.content}</div>
        """
        if len(message.attachments) != 0:
            if not os.path.exists(rf"{self.dir}attachments/"):
                os.makedirs(rf"{self.dir}attachments/")
            for att in message.attachments:
                filename = rf"{self.dir}attachments/{att.filename}"
                if not os.path.exists(filename):
                    await att.save(filename)
                    res += f"<a href=\"attachments/{att.filename}\">{att.filename}</a>"
                else:
                    ze_filename = list(filename)
                    del ze_filename[-4:]
                    extension = filename[-4:]
                    for i in range(1, 101):
                        if not os.path.exists(f"{''.join(ze_filename)}_{i}{extension}"):
                            await att.save(f"{''.join(ze_filename)}_{i}{extension}")
                            res += f"<a href=\"attachments/{att.filename[:-4]}_{i}{extension}\">{att.filename}</a>"
                            break

        res += "</div></div>"
        return res
