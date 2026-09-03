import discord
from data.config import get_config,set_config


class PrefixModal(discord.ui.Modal, title="Configuration du préfixe"):

    prefix = discord.ui.TextInput(
        label="Nouveau préfixe",
        placeholder="Exemple : !",
        min_length=1,
        max_length=5,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):

        prefix = self.prefix.value

        config = {
            "guild_id": interaction.guild.id,
            "prefix": prefix
        }

        verif = set_config(config)

        if verif is True:
            message = f"✅ Préfixe modifié avec succès : `{prefix}`"
        else:
            message = "❌ Impossible de modifier le préfixe."

        await interaction.response.send_message(
            message,
            ephemeral=True,
            delete_after=30
        )