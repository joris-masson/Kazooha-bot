import interactions
import os

from utils.func import save_attachment


class DemandChannelConcours:
    def __init__(self, client: interactions.Client, ctx: interactions.CommandContext, channel: interactions.Channel):
        self.ID = ctx.author.id
        self.client = client
        self.ctx = ctx
        self.channel = channel
        self.demand_message = interactions.Message

    def __str__(self):
        return f"{self.ID}"

    async def send_demand_msg(self):
        embed = interactions.Embed(
            title="Nouvelle participation!",
            description=f"Bienvenue dans le fil pour soumettre votre participation!\nPour soumettre votre participation, veuillez envoyer votre image **dans le même message** que votre titre/description\nVotre **titre** __doit être à la première ligne__, et votre **description**... __surtout pas sur la première ligne__\nEnsuite appuyez sur le bouton __**Envoyer**__(vous pouvez aussi annuler en appuyant sur le bouton **Annuler**)"
        )

        button_accept = interactions.Button(
            label="Envoyer",
            custom_id="but_accept",
            style=3
        )
        button_refuse = interactions.Button(
            label="Annuler",
            custom_id="but_refuse",
            style=4
        )
        self.demand_message = await self.channel.send(f"<@{self.ctx.author.id}>", embeds=embed, components=interactions.spread_to_rows(button_accept, button_refuse))
        await self.demand_message.pin()
        await self.ctx.send(f"Un fil a été créé: <#{self.channel.id}>", ephemeral=True)

    async def delete(self):
        await self.channel.delete()
