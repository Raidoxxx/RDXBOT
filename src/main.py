import json
import os

import discord
from discord import app_commands
from discord.app_commands import Choice

from src.user.UserManager import UserManager
from src.views.RegistrarView import RegistrarView

if not os.path.exists("config.yml"):
    with open("config.yml", 'w') as file:
        file.write('{}')
with open("config.yml", 'r') as file:
    config = json.load(file)

if not os.path.exists("key.json"):
    with open("key.json", 'w') as file:
        file.write('{}')

with open("key.json", 'r') as file:
    key = json.load(file)

token = key["TOKEN"]

server_id = config["server_id"]
intents = discord.Intents.default()


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False
        self.role = 1148716021205704764
        self.added = False
        UserManager().__init__()

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=server_id))
            self.synced = True
        if not self.added:
            self.add_view(RegistrarView())
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
