import discord
from discord.ext import commands

class help_cog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.help_message = """
```
this is a help message
```

"""

        self.text_channel_list = []
    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.client.guilds:
            for channel in guild.text_channels:
                self.text_channel_list.append(channel)
        await self.send_to_all(self.help_message)

    @commands.command(name="help", help="Displays the help message")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
