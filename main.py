# https://youtu.be/M_6_GbDc39Q?si=ihgI3TTnVG529EZV

import discord
from apikeys import *
from discord.ext import commands

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=discord.Intents.all())
       
    async def setup_hook(self):
        await self.load_extension(f"cogs.bot_cog")                                                                  
        await client.tree.sync()
    
    async def on_ready(self):   # when bot is ready to start receiving commands it executes this function  
        await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity("Chinchilling"))
        print("Initialization complete")
        print("-----------------------")                                                                                                                                                                                        

client = MyBot()
client.run(BOTTOKEN)


