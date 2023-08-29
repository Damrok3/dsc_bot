import discord
from discord.ext import commands
from apikeys import *

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents) # initializing instance of a bot and letting it know that its
                                            # commands start with "!"

@client.event
async def on_ready():   # when bot is ready to start receiving commands it executes this function
    print("Initialization complete")
    print("-----------------------")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am damrok's bot")

@client.command()
async def tell_joke(ctx):
    await ctx.send("joke")

client.run(BOTTOKEN)

