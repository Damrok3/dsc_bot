from yt_dlp import YoutubeDL
from discord.ext import commands
from jokeapi import Jokes
from discord import FFmpegPCMAudio
from discord.utils import get

class bot_cog(commands.Cog):
    def __init__(self, client):
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

            @client.command()
            async def join(ctx):
                if(ctx.author.voice):                           # if user is in a voice channel, it will get this chanel id     
                    channel = ctx.message.author.voice.channel  # and join it
                    # voice = await channel.connect()
                    # source = FFmpegPCMAudio("maestro.mp3")
                    # player = voice.play(source)
                    await channel.connect()
                    print(channel)
                    print(ctx.voice_client.channel)
                else:
                    await ctx.send("You need to be in a voice channel to run this command!")

            @client.command()
            async def play(ctx, url):
                if(ctx.author.voice):
                    channel = ctx.message.author.voice.channel
                    if(ctx.voice_client):
                        if(ctx.voice_client.channel == channel):
                            YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True',}
                            FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                            voice = get(client.voice_clients, guild=ctx.guild)
                            if not voice.is_playing():
                                try:
                                    with YoutubeDL(YDL_OPTIONS) as ydl:
                                        info = ydl.extract_info(url, download=False)
                                        URL = info['url']
                                        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                                except Exception as e:
                                    await ctx.send(e)
                                    return
                            else:
                                await ctx.send("Already playing song")
                                return
                        else:
                            await ctx.send("You need to be in the same voice channel as me to run this command!")
                            return
                    else:
                        await ctx.send("First i need to connect to the voice channel to run this command!")
                        return
                else:
                    await ctx.send("You need to be in a voice channel to run this command!")
                    return

            @client.command()
            async def stop(ctx):
                if(ctx.author.voice):
                    channel = ctx.message.author.voice.channel
                    if(ctx.voice_client):
                        if(ctx.voice_client.channel == channel):
                            voice = get(client.voice_clients, guild=ctx.guild)
                            if voice.is_playing():
                                voice.stop()                   
                            else:
                                await ctx.send("Not playing anything currently.")
                                return
                        else:
                            await ctx.send("You need to be in the same voice channel as me to run this command!")
                            return
                    else:
                        await ctx.send("First i need to connect to the voice channel to run this command!")
                        return
                else:
                    await ctx.send("You need to be in a voice channel to run this command!")
                    return
                
            @client.command()
            async def leave(ctx):
                if(ctx.voice_client):                           # if the bot is in a voice channel
                    await ctx.guild.voice_client.disconnect()   # guild is basically a server, voice client is the voice chat that the bot is in
                    await ctx.send("Leaving the voice")
                else:
                    await ctx.send("I am not in a voice channel")
