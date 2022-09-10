import discord
import base64

from discord.ext import commands
from utils.functions import log
from os import listdir
from datetime import datetime


class Vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.la_personne_qui_s_occupe_du_vote = 689082007124574273
        log(f"'{__name__}' initialisé")

    @commands.command(name="endVote")
    async def end_vote(self, ctx) -> None:
        if datetime.now() > datetime(2022, 9, 10, 23, 59, 59) and ctx.author.id == self.la_personne_qui_s_occupe_du_vote:
            res = {"A_Ludovic": 0, "Amalia": 0, "Anastassya": 0, "Kazoohigh": 0, "Kurkigal": 0, "Lia": 0, "Nemesis": 0, "Teddy": 0, "Yoshika": 0}
            numb = 0
            all_vote_file = listdir("vote_results/")
            for vote_file in all_vote_file:
                with open(rf"vote_results/{vote_file}", 'r') as vote:
                    values = base64.b64decode(vote.readline().encode("ascii")).decode("ascii")
                    for person in res:
                        res[person] += int(values[numb])
                        numb += 1
                numb = 0

            message = "Voici les résultats par participant:\n"
            for person in sorted(res, key=res.get, reverse=True):
                message += f"{person}: {res[person]}\n"
            await self.bot.get_user(self.la_personne_qui_s_occupe_du_vote).send(message)
        else:
            self.bot.get_user(self.la_personne_qui_s_occupe_du_vote).send("Le vote n'est pas encore terminé, impossible d'y mettre fin\nLe vote se termine <t:1662847140:R>.")

    @commands.command(name="vote")
    async def vote(self, ctx, *args: str) -> None:
        if datetime.now() > datetime(2022, 9, 10, 23, 59, 59):
            await ctx.send("Désolé, le vote est terminé.\nLes résultats arriveront bientôt!")
        elif not isinstance(ctx.channel, discord.channel.DMChannel):
            log(f"{__name__} utilisé par @{ctx.message.author.name}({ctx.message.author.id}) dans #{ctx.message.channel.name}({ctx.message.channel.id}) sur le serveur {ctx.message.guild.name}({ctx.message.guild.id})")
            await ctx.message.delete()
            embed = discord.Embed(
                title="__Explications de la procédure de vote pour le concours photo__",
                description="""Hello!
Pour que le vote soit anonyme, et gardé secret, nous allons passer par les MP!
Je vais vous expliquer comment ça fonctionne tout ça:

Pour commencer, allez voir la liste des candidatures dans <#1010861164219072613>

Ensuite, vous allez voter dans cet ordre: __**A_Ludovic -> Amalia -> Anastassya -> Kazoohigh -> Kurkigal -> Lia -> Nemesis -> Teddy -> Yoshika**__(ordre alphabétique)

Vous devrez tapez la commande `;vote` ici, et rajouter vos votes à la suite, comme ceci:
`;vote 1 2 3 4 5 1 2 3 4`
Avec bien un numéro pour chaque personne, le premier numéro correspond à A_Ludovic, le second à Amalia, etc...

Chaque numéro représente une note, plus le numéro est élevé, plus sa note est élevée
Vous pouvez noter **de 1 à 5 seulement**

Si le vote est valide, vous devriez recevoir un message pour vous le confirmer!"""
            )
            await ctx.author.send(embed=embed)
        elif self.__check_validity(args):
            res = ''
            for elem in args:
                res += elem
            with open(rf"vote_results/{self.__encode_b64(ctx.author.id)}.txt", 'w') as res_file:
                res_file.write(self.__encode_b64(res))
            await ctx.reply("Vote enregistré!\nVous pouvez toujours le changer en retapant la commande")
        else:
            await ctx.reply("Désolé, le format de réponse n'est pas correct, il faut qu'il y ait 9 notes, et que ces notes soient toutes entre 1 et 5.")

    def __check_validity(self, votes) -> bool:
        vote_len = len(votes) == 9
        vote_num = True
        for vote in votes:
            if int(vote) > 5 or int(vote) < 1:
                vote_num = False
                break
        return vote_len and vote_num

    def __encode_b64(self, val: str) -> str:
        return base64.b64encode(val.encode("ascii")).decode("ascii")
