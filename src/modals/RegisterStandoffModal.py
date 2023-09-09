import discord

from src.user.UserManager import UserManager


class RegisterStandoffModal(discord.ui.Modal, title="Registre seu perfil do SO2", color=0x00ff00):
    id_so2 = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="ID do SO2",
        required=True,
        max_length=30,
        placeholder="Coloque o ID do seu perfil do SO2 aqui!"
    )

    async def on_submit(self, interaction: discord.Interaction):
        if not UserManager().exists(interaction.user.id):
            await interaction.response.send_message("Você não está registrado!", ephemeral=True)
            return

        if not self.id_so2.value.isnumeric():
            await interaction.response.send_message("O ID do SO2 precisa ser um número!", ephemeral=True)
            return

        user = UserManager().get_user(interaction.user.id)
        user.set_so2_id(self.id_so2.value)