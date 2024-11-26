from interactions import Extension, slash_command, slash_option, SlashContext, OptionType
from utils.util import prepare_message, log


class Send(Extension):
    @slash_command(
        name="send",
        description="Envoie un message préparé à l'avance"
    )
    @slash_option(
        name="nom_message",
        description="Le nom du message à envoyer",
        required=True,
        opt_type=OptionType.STRING
    )
    async def command(self, ctx: SlashContext, nom_message: str):
        log("SLASH", f"Commande slash `/send nom_message:{nom_message}` utilisée par {ctx.author.username}({ctx.author.id}) dans #{ctx.channel.name}({ctx.channel.id}) sur {ctx.guild.name}({ctx.guild.id})")
        message = prepare_message(nom_message)
        await ctx.send(message.get_content(), embeds=message.get_embeds())
