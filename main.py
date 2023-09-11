# https://youtu.be/M_6_GbDc39Q?si=ihgI3TTnVG529EZV

import discord
from apikeys import *
from bot_cog import bot_cog
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)  # initializing instance of a bot and letting it know that its
                                                            # commands start with "!"                                                                                          
client.add_cog(bot_cog(client))

client.run(BOTTOKEN)

