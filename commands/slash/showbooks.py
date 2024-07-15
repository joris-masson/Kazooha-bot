import json

from interactions import Extension, SlashContext, OptionType, Embed, AutocompleteContext, slash_command, slash_option
from interactions.ext.paginators import Paginator
from fast_autocomplete import AutoComplete
from utils.util import open_db_connection, log


class ShowBooks(Extension):
    @slash_command(
        name="afficher_livre",
        description="Afficher un livre, t'as juste à taper son nom (il y a une autocomplétion) !"
    )
    @slash_option(
        name="livre",
        description="Le livre à afficher (il y a une autocomplétion).",
        required=True,
        opt_type=OptionType.STRING,
        autocomplete=True
    )
    async def command(self, ctx: SlashContext, livre: str):
        log("SLASH", log("SLASH", f"Commande slash `/afficher_livre livre:{livre}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})"))

        paginator = Paginator.create_from_embeds(self.bot, *self.prepare_pages(livre))
        await paginator.send(ctx, ephemeral=True)

    @command.autocomplete("livre")
    async def livre_autocomplete(self, ctx: AutocompleteContext) -> None:
        user_input = ctx.input_text
        autocomplete = AutoComplete(words=self.get_books_names(True))

        names = []
        for name in autocomplete.search(word=user_input, size=25):
            names.append(name[0])

        await ctx.send(choices=names)

    def get_books_names(self, archives: bool) -> dict[str:dict]:
        res = {}

        db = open_db_connection()
        cursor = db.cursor()

        if archives:
            query = "SELECT name FROM Kazooha.Book WHERE type='archive'"
        else:
            query = "SELECT name FROM Kazooha.Book WHERE type='quest'"

        cursor.execute(query)
        for book_name in cursor.fetchall():
            res[book_name[0]] = {}

        cursor.close()
        db.close()

        return res

    def get_all_book_info(self, livre: str) -> dict[str:str]:
        db = open_db_connection()
        cursor = db.cursor()

        cursor.execute(f"SELECT name, descriptions, pages FROM Kazooha.Book WHERE name='{livre}'")
        raw_book_info = cursor.fetchall()[0]

        cursor.close()
        db.close()

        return {
            "name": raw_book_info[0],
            "descriptions": raw_book_info[1],
            "pages": raw_book_info[2]
        }

    def prepare_pages(self, livre: str) -> list[Embed]:
        book_info = self.get_all_book_info(livre)
        res = []

        descriptions = json.loads(book_info["descriptions"])
        pages = json.loads(book_info["pages"])

        for page_nb in range(1, len(descriptions) + 1):
            embed_desc = f"*{descriptions[str(page_nb)]}*\n\n{pages[str(page_nb)]}"

            new_page = Embed(
                title=book_info["name"],
                description=embed_desc
            )

            res.append(new_page)

        return res
