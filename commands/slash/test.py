from interactions import Extension, slash_command, SlashContext


class Test(Extension):
    @slash_command()
    async def test(self, ctx: SlashContext):
        await ctx.send("Hello world!", ephemeral=True)
