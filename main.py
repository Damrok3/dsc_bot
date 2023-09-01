import discord
from discord.ext import commands
from apikeys import *
from jokeapi import Jokes

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = commands.Bot(command_prefix='!', intents=intents)  # initializing instance of a bot and letting it know that its
                                                            # commands start with "!"                                       

@client.event
async def on_ready():   # when bot is ready to start receiving commands it executes this function
    print("Initialization complete")
    print("-----------------------")

# @client.event
# async def on_message(message):
#     if message.author.id != author id here:
#         channel = client.get_channel(channel id here)
#         await channel.send("test")

@client.command()
async def hello(ctx):   # ctx allows to communicate with discord server, like send and get messages as well as
                        # see other properties like about users and channels
    await ctx.send("Hello, I am damrok's bot")

@client.command()
async def joke(ctx):
    jokeObj = await Jokes()
    joke = await jokeObj.get_joke(category=["dark"])
    if joke["type"] == "single": # Print the joke
        await ctx.send(joke["joke"])
    else:
        await ctx.send(joke["setup"])
        await ctx.send(joke["delivery"])

@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):                           # if user is in a voice channel, it will get this chanel id     
        channel = ctx.message.author.voice.channel  # and join it
        await channel.connect()
    else:
        await ctx.send("You need to be in a voice channel to run this command!")
     
@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):                           # if the bot is in a voice channel
        await ctx.guild.voice_client.disconnect()   # guild is basically a server, voice client is the voice chat that the bot is in
        await ctx.send("Leaving the voice")
    else:
        await ctx.send("I am not in a voice channel")

client.run(BOTTOKEN)

