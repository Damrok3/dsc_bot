from yt_dlp import YoutubeDL
from discord.ext import commands
from jokeapi import Jokes
from discord import FFmpegPCMAudio
from discord.utils import get

class bot_cog(commands.Cog):

    def __init__(self, client):
        self.music_queue = []
        self.is_playing = False
        self.is_paused = False
        self.client = client
        self.vc = None

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True',}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
        @client.event
        async def on_ready():   # when bot is ready to start receiving commands it executes this function    
            print("Initialization complete")
            print("-----------------------")
        
        @client.command()
        async def hello(ctx):   # ctx allows to communicate with discord server, like send and get messages as well as
                                # see other properties like about users and channels
            await ctx.send("Hello, I am damrok's bot")

        @client.command()
        async def play(ctx, url):
            
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send("You need to be in a voice channel to run this command")
            elif self.is_paused:
                self.vc.resume()
            else:
                song = self.search_yt(url)
                if type(song) == type(True):
                    await ctx.send("Couldn't download the song, incorrect format, try different keyword")
                else:
                    await ctx.send("song added to the queue")
                    self.music_queue.append([song, voice_channel])

                    if self.is_playing == False:
                        await self.play_music(ctx)
        
        @client.command()
        async def pause(ctx):
            if self.vc != None:
                if self.vc.is_playing():
                    self.vc.pause()
                    self.is_playing = False
                    self.is_paused = True

        @client.command()
        async def resume(ctx):
            if self.vc != None:
                if self.is_paused:
                    self.is_playing = True
                    self.is_paused = False
                    self.vc.resume()

        @client.command()
        async def isplaying(ctx):
            await ctx.send(self.is_playing)

        @client.command()
        async def skip(ctx):
            if self.vc != None and self.vc:
                self.vc.stop()
                await self.play_music(ctx)

        @client.command()
        async def clear(ctx):
            if self.vc != None and self.is_playing:
                self.vc.stop()
            self.music_queue = []
            await ctx.send("Music queue cleared")

        @client.command()
        async def disconnect(ctx):
            self.is_playing = False
            self.is_paused = False
            await self.vc.disconnect()
                
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item, download=False)
                URL = info['url']
            except Exception:
                return False
        return URL
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
            self.music_queue.pop(0)
            self.vc.play(FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)
            self.vc.play(FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
    
    


        
        

        # @client.command()
        # async def joke(ctx):
        #     jokeObj = await Jokes()
        #     joke = await jokeObj.get_joke(category=["dark"])
        #     if joke["type"] == "single": # Print the joke
        #         await ctx.send(joke["joke"])
        #     else:
        #         await ctx.send(joke["setup"])
        #         await ctx.send(joke["delivery"])

        # @client.command()
        # async def join(ctx):
        #     if(ctx.author.voice):                           # if user is in a voice channel, it will get this chanel id     
        #         channel = ctx.message.author.voice.channel  # and join it
        #         # voice = await channel.connect()
        #         # source = FFmpegPCMAudio("maestro.mp3")
        #         # player = voice.play(source)
        #         await channel.connect()
        #         print(channel)
        #         print(ctx.voice_client.channel)
        #     else:
        #         await ctx.send("You need to be in a voice channel to run this command!")

        # # @client.command()
        # # async def play(ctx, url):
        # #     if(ctx.author.voice):
        # #         channel = ctx.message.author.voice.channel
        # #         if(ctx.voice_client):
        # #             if(ctx.voice_client.channel == channel):
                        
        # #                 voice = get(client.voice_clients, guild=ctx.guild)
        # #                 try:
        # #                     with YoutubeDL(YDL_OPTIONS) as ydl:
        # #                         info = ydl.extract_info(url, download=False)
        # #                         URL = info['url']
        # #                 except Exception as e:
        # #                     await ctx.send(e)
        # #                     return
                        
        # #                 voice.play(FFmpegPCMAudio(queue.pop(0), **FFMPEG_OPTIONS), after = lambda e: self.play_next())
                        
        # #                 # if not voice.is_playing():
        # #                 # else:
        # #                 #     await ctx.send("Already playing song")
        # #                 #     return
        # #             else:
        # #                 await ctx.send("You need to be in the same voice channel as me to run this command!")
        # #                 return
        # #         else:
        # #             await ctx.send("First i need to connect to the voice channel to run this command!")
        # #             return
        # #     else:
        # #         await ctx.send("You need to be in a voice channel to run this command!")
        # #         return

        # @client.command()
        # async def stop(ctx):
        #     if(ctx.author.voice):
        #         channel = ctx.message.author.voice.channel
        #         if(ctx.voice_client):
        #             if(ctx.voice_client.channel == channel):
        #                 voice = get(client.voice_clients, guild=ctx.guild)
        #                 if voice.is_playing():
        #                     voice.stop()                   
        #                 else:
        #                     await ctx.send("Not playing anything currently.")
        #                     return
        #             else:
        #                 await ctx.send("You need to be in the same voice channel as me to run this command!")
        #                 return
        #         else:
        #             await ctx.send("First i need to connect to the voice channel to run this command!")
        #             return
        #     else:
        #         await ctx.send("You need to be in a voice channel to run this command!")
        #         return
            
        # @client.command()
        # async def resume(ctx):
        #     if(ctx.author.voice):
        #         channel = ctx.message.author.voice.channel
        #         if(ctx.voice_client):
        #             if(ctx.voice_client.channel == channel):
        #                 voice = get(client.voice_clients, guild=ctx.guild)
        #                 if not voice.is_playing():
        #                     voice.resume()                   
        #                 else:
        #                     await ctx.send("Not playing anything currently.")
        #                     return
        #             else:
        #                 await ctx.send("You need to be in the same voice channel as me to run this command!")
        #                 return
        #         else:
        #             await ctx.send("First i need to connect to the voice channel to run this command!")
        #             return
        #     else:
        #         await ctx.send("You need to be in a voice channel to run this command!")
        #         return
            
        # @client.command()
        # async def leave(ctx):
        #     if(ctx.voice_client):                           # if the bot is in a voice channel
        #         await ctx.guild.voice_client.disconnect()   # guild is basically a server, voice client is the voice chat that the bot is in
        #         await ctx.send("Leaving the voice")
        #     else:
        #         await ctx.send("I am not in a voice channel")
