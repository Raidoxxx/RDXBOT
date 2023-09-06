import discord

class EventHandler:
    def __init__(self, client):
        self.client = client


    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')