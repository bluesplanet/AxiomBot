import discord
from data.config import get_config,set_config



def language_embed(ctx):

    config = get_config(ctx.guild.id)
    
    embed = discord.Embed(
        title=f"Langue actuelle : `{config['language']}`\n\n",
    )

    return embed


class LanguageSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Français",
                value="français",
                emoji="🇫🇷"
            )
        ]

        super().__init__(
            placeholder="Sélectionnez la nouvelle langue d'AxiomBot....",
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        language = self.values[0]

        
        guild_id = interaction.guild.id
        config = {
            "guild_id" : guild_id,
            "language" : language
        }
        verif = set_config(config)

        if verif is True:
            message = f"🌐 Langue configurée avec succès : `{language}`"
        else:
            message = "❌ Échec de la configuration de la langue."

        await interaction.response.send_message(
            message,
            ephemeral=True,
            delete_after=3
        )


class LanguageView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=60)

        self.add_item(LanguageSelect())