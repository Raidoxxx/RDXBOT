import discord

from src.main import aclient


class RegistrarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Registrar", style=discord.ButtonStyle.green, custom_id="persistent_view:verify")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(aclient.role) is not discord.Role:
            aclient.role = interaction.guild.get_role(aclient.role)
        if aclient.role not in interaction.user.roles:
            await interaction.user.add_roles(aclient.role)
            await interaction.response.send_message("Registrado com sucesso!", ephemeral=True)
        else:
            await interaction.response.send_message("Você já está registrado!", ephemeral=True)
