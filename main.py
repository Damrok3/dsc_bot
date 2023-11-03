# https://youtu.be/M_6_GbDc39Q?si=ihgI3TTnVG529EZV

import discord
from apikeys import *
from discord.ext import commands
from discord import app_commands

from bot_cog import bot_cog
# from help_cog import help_cog

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(command_prefix='/', intents=intents)    # initializing instance of a bot and letting it know that its
                                                                    # commands start with "!"        
tree = app_commands.CommandTree(client)                                                                    
@client.event
async def on_ready():   # when bot is ready to start receiving commands it executes this function    
    await tree.sync()  
    print("Initialization complete")
    print("-----------------------")         

@tree.command(name="hello", description="this is a hello command")
async def hello(interaction: discord.Integration):   # ctx allows to communicate with discord server, like send and get messages as well as
    await interaction.response.send_message("Hello, I am damrok's bot")       # see other properties like about users and channels
                                                      
                                                                                                                                                                                    
#client.add_cog(bot_cog(client))
#client.add_cog(help_cog(client))

client.run(BOTTOKEN)


