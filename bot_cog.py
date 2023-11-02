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
            try:
                voice_channel = ctx.author.voice.channel
                if self.is_paused:
                    self.vc.resume()
                else:
                    song = self.search_yt(url)
                    if type(song) == type(True):
                        await ctx.send("Couldn't download the song, incorrect format, you have to use the URL")
                    else:
                        await ctx.send("song added to the queue")
                        await ctx.send(f"current queue: {len(self.music_queue)} songs")
                        self.music_queue.append([song, voice_channel])

                        if self.is_playing == False:
                            await self.play_music(ctx)
            except AttributeError:
                await ctx.send("You need to be in a voice channel in order to use this command!")
        
        @client.command()
        async def check_play(ctx):
            await ctx.send(f"is playing = {self.is_playing}, is paused = {self.is_paused}")

        @client.command()
        async def pause(ctx):
            if self.vc != None:
                if self.vc.is_playing():
                    self.vc.pause()
                    self.is_playing = False
                    #HERE
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
                self.is_playing = False
            self.music_queue = []
            await ctx.send("Music queue cleared")

        @client.command()
        async def disconnect(ctx):
            self.is_playing = False
            self.is_paused = False
            await self.vc.disconnect()

        @client.command()
        async def joke(ctx):
            jokeObj = await Jokes()
            joke = await jokeObj.get_joke(  blacklist=[ "racist", 
                                                        "sexist",
                                                        "nsfw", 
                                                        "explicit", 
                                                        "religious"], 
                                            category=[  "Misc",
                                                        "Dark",
                                                        "Pun",
                                                        "Spooky",
                                                        "Christmas"])
                
            
            if joke["type"] == "single": # Print the joke
                await ctx.send(joke["joke"])
            else:
                await ctx.send(joke["setup"])
                await ctx.send(joke["delivery"])
                
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item, download=False)
                URL = info['url']
            except Exception:
                return False
        return URL
    
    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
            self.music_queue.pop(0)
            self.vc.play(FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False
            #HERE

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
        else:
            self.is_playing = False
