from discord.ext import commands
from discord_components import Button


class Magie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="magie")
    async def magic_access(self, ctx):
        if ctx.guild.id == 950118071425724466:
            warning_message1 = await ctx.send("https://c.tenor.com/sLgNruA4tsgAAAAS/warning-lights.gif")
            message_with_button = await ctx.send(
                """Bonjour, ce message est la première étape vers l'utilisation de la magie noire!

    __**Veuillez lire attentivement ce qui va suivre, et ne pas directement appuyer sur le bouton en bas pour dire que vous êtes OK, s'il vous plaît**__
    Vous devez comprendre une chose, c'est que la magie noire(serveur privé plus sérieusement), est quelque chose de potentiellement dangereux. Vous pouriez perdre votre compte si vous l'utilisez mal.
    C'est pourquoi je vous recommande très fortement de n'utiliser la magie noire que sur un PC sur lequel vous ne jouez pas à un certain jeu animé d'habitude.
    Sinon vous vous exposez à des risques.

        Voilà, cliquez sur le bouton pour avoir accès à la magie noire maintenant, ou ne cliquez pas, si vous n'avez pas spécialement envie que MhY fasse sauter votre compte principal.
                """,
                components=[
                    Button(label="Je suis OK")
                ],
            )
            warning_message2 = await ctx.send("https://c.tenor.com/sLgNruA4tsgAAAAS/warning-lights.gif")
            res = await self.bot.wait_for("button_click")
            if res.channel == ctx.channel:
                role = self.bot.utils.get(ctx.guild.roles, id=997525574727778365)
                await res.author.add_roles(role)
                await res.respond(
                    type=4,
                    content=f"Okay, vous avez maintenant le rôle pour accéder aux salon <#966115950535524392> et <#966117908252082227>!"
                )

            await ctx.message.delete()
            await warning_message1.delete()
            await message_with_button.delete()
            await warning_message2.delete()
        else:
            await ctx.message.delete()
