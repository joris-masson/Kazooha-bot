import ollama
from interactions import Extension, SlashContext, OptionType, slash_command, slash_option


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
    async def test(self, ctx: SlashContext, phrase: str):
        client = ollama.AsyncClient(host="http://192.168.1.241:11434/api/generate")
        original_message = await ctx.send("*Je réfléchis...*")

        response = await client.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': phrase,
            },
        ])

        await original_message.edit(content=response["message"]["content"])