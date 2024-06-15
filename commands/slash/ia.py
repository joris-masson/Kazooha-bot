import os

import mysql.connector
import ollama

from dotenv import load_dotenv
from interactions import Extension, SlashContext, OptionType, slash_command, slash_option

from utils.util import open_db_connection


class Test(Extension):
    @slash_command(
        name="ia",
        description="Pour discuter avec l'IA !"
    )
    @slash_option(
        name="phrase",
        description="La phrase à communiquer à l'IA",
        required=True,
        opt_type=OptionType.STRING
    )
    async def command(self, ctx: SlashContext, phrase: str):
        load_dotenv()
        host = os.getenv("OLLAMA_HOST")

        # "http://192.168.1.241:11434/api/generate"
        client = ollama.AsyncClient(host=host)
        await ctx.defer()

        db = open_db_connection()

        response = await client.chat(model='llama3', messages=self.reconstruct_chat(int(ctx.author.id), db, phrase))

        message_content = response["message"]["content"]

        await ctx.send(content=message_content)

        cursor = db.cursor()

        query = "INSERT INTO Kazooha.MessageIa (discordUserId, messageNumber, userContent, botContent) VALUES (%s, %s, %s, %s)"
        val = [
            int(ctx.author.id),
            self.get_last_chat_id(int(ctx.author.id), db),
            phrase,
            message_content
        ]

        cursor.execute(query, val)
        db.commit()

        cursor.close()
        db.close()

    def get_last_chat_id(self, discord_user_id: int, db: mysql.connector.MySQLConnection) -> int:
        query = "SELECT messageNumber FROM Kazooha.MessageIa WHERE discordUserId=%s"

        cursor = db.cursor()

        cursor.execute(query, [discord_user_id])

        res = cursor.fetchall()
        cursor.close()

        if len(res) >= 1:
            id_list = []
            for last_chat_id in res:
                id_list.append(last_chat_id[0])
            return max(id_list) + 1
        else:
            return 0

    def reconstruct_chat(self, discord_user_id: int, db: mysql.connector.MySQLConnection, actual_phrase: str) -> list[dict]:
        res = []

        cursor = db.cursor()

        query = "SELECT userContent, botContent FROM Kazooha.MessageIa WHERE discordUserId=%s"
        cursor.execute(query, [discord_user_id])

        query_result = cursor.fetchall()

        if len(query_result) >= 1:
            for conv in query_result:
                res.append({
                    'role': 'user',
                    'content': conv[0],
                })

                res.append({
                    'role': 'assistant',
                    'content': conv[1],
                })

        res.append({
            'role': 'user',
            'content': actual_phrase,
        })

        return res
