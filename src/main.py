import json
import os

import discord
from discord import app_commands
from discord.app_commands import Choice

from key import token

token = token.get("TOKEN")
server_id = "1131463549961633862"
intents = discord.Intents.default()


async def registerPerfil(user_id: int, so2_id: int):
    filename = "data.json"

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            if os.stat(filename).st_size == 0:
                data = []
            else:
                data = json.load(file)

    for item in data:
        if item[0] == user_id:
            return False

    data.append([user_id, ["SO2", so2_id]])

    with open(filename, "w") as f:
        json.dump(data, f)

    return True


async def getPerfil(user_id: int):
    filename = "data.json"

    with open(filename, 'r') as file:
        data = json.load(file)

    for item in data:
        if item[0] == user_id:
            return item[1]

    return None


class RegisterModal(discord.ui.Modal, title="Registro"):
    id_so2 = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="ID do SO2",
        required=True,
        max_length=30,
        placeholder="Digite seu ID do SO2"
    )

    async def on_submit(self, interaction: discord.Interaction):

        so2_id = self.id_so2.value

        if not so2_id.isnumeric():
            await interaction.response.send_message("O id deve ser um número!", ephemeral=True)
            return

        with open("data.json", 'r') as file:
            data = file.read()

        if so2_id in data:
            await interaction.response.send_message("Esse ID já está registrado!", ephemeral=True)
            return

        await registerPerfil(interaction.user.id, int(so2_id))
        await interaction.user.add_roles(aclient.role)
        await interaction.response.send_message("Registrado com sucesso!", ephemeral=True)


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Registrar", style=discord.ButtonStyle.green, custom_id="persistent_view:verify")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(aclient.role) is not discord.Role:
            aclient.role = interaction.guild.get_role(aclient.role)
        if aclient.role not in interaction.user.roles:
            await interaction.response.send_modal(RegisterModal())
        else:
            await interaction.response.send_message("Você já está registrado!", ephemeral=True)


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
        self.role = 1148716021205704764
        self.added = False

    if not os.path.exists("data.json"):
        with open("data.json", 'w') as file:
            file.write('{}')

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=server_id))
            self.synced = True
        if not self.added:
            self.add_view(PersistentView())
            self.added = True
        print(f'{self.user} has connected to Discord!')


aclient = Client()
tree = app_commands.CommandTree(aclient)


@tree.command(guild=discord.Object(id=server_id), name="register", description="configurar o canal de registro")
async def register(interaction: discord.Interaction, channel: discord.TextChannel):
    if interaction.user.guild_permissions.administrator < 1:
        await interaction.response.send_message("Você não tem permissão para usar esse comando!", ephemeral=True)
        return

    description = "Se registre no servidor! Você receberá acesso a todos os canais e poderá participar de eventos!"
    title = "Registrar"
    embed = discord.Embed(title=title, description=description, color=0x00ff00)
    await channel.send(embed=embed, view=PersistentView())
    await interaction.response.send_message("Canal de registro configurado com sucesso!", ephemeral=True)


@tree.command(guild=discord.Object(id=server_id), name="perfil", description="Perfil")
async def perfil(interaction: discord.Interaction, user: discord.User = None):
    global perfil_from

    if user is None:
        if interaction.user.id == aclient.user.id:
            return
        perfil_from = interaction.user.id
    else:
        perfil_from = user.id

    user_perfil = await getLinkPerfil(perfil_from)

    if user_perfil is None:
        if perfil_from == interaction.user.id:
            embed = discord.Embed(title="Perfil", description="Você não está registrado!", color=0xff0000)
        else:
            embed = discord.Embed(title="Perfil", description="Esse usuário não está registrado!", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = discord.Embed(title="Perfil", description=f"Perfil de <@{perfil_from}>", color=0x00ff00)
    button = discord.ui.Button(label="Perfil", url=user_perfil, style=discord.ButtonStyle.link)
    view = discord.ui.View()
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def getLinkPerfil(user_id: int):
    perfil = await getPerfil(user_id)

    if perfil is None:
        return None
    else:
        return f"https://link.standoff2.com/pt/profile/view/{perfil[1]}"


aclient.run(token)
