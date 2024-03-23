from interactions import Extension, StringSelectMenu, Embed, File, SlashContext, ComponentContext, slash_command, component_callback


class Dossiers(Extension):
    @slash_command(
        name="dossiers_confidentiels",
        description="Affiche une image contenant des informations sur un personnage du lore de Genshin Impact"
    )
    async def command(self, ctx: SlashContext):
        select = StringSelectMenu(
            "Alice", "Asmoday", "Columbina", "Dainsleif", "Istaroth", "Nabu Malikata", "Night Mother",
            "Paimon", "Phanes", "Pierro", "Pushpavatika", "Rhinedottir", "Le Sibling", "Le Traveler",
            placeholder="De quel personnage voulez-vous voir le dossier confidentiel?",
            min_values=1,
            max_values=1,
            custom_id="dossiers_select_id"
        )

        await ctx.send(components=select, ephemeral=True)

    @component_callback("dossiers_select_id")
    async def callback(self, ctx: ComponentContext):
        match ctx.values[0]:
            case "Nabu Malikata":
                selected_dossier = "Nabu_malikata"
            case "Night Mother":
                selected_dossier = "Night_mother"
            case "Le Sibling":
                selected_dossier = "Traveler_sibling"
            case "Le Traveler":
                selected_dossier = "Travelerp"
            case other:
                selected_dossier = ctx.values[0]
        file = File(f"data/dossiers/{selected_dossier}.png")
        embed = Embed(title=f"Dossier confidentiel: {selected_dossier}")
        embed.set_image(url=f"attachment://{selected_dossier}.png")
        await ctx.send(embeds=embed, files=file, ephemeral=True)
