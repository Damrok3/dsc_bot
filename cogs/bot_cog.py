from yt_dlp import YoutubeDL
from discord.ext import commands
from discord import app_commands
from jokeapi import Jokes
from discord import FFmpegPCMAudio
from discord.utils import get
import discord

class bot_cog(commands.Cog):
    
    def __init__(self, client:commands.Bot) -> None:
        self.client = client
        self.music_queue = []
        self.is_playing = False
        self.is_paused = False
        self.client = client
        self.vc = None

        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True',}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        @client.command()
        async def super_secret_command(ctx) -> None:
            if ctx.author.id == 274556257174552577:
                await ctx.send("Bokdan and Kuro are gay")
            else:
                await ctx.send("You're not worthy")

    @app_commands.command(name="hello", description="this is a hello command")
    async def hello(self, interaction: discord.Interaction) -> None:                          
        await interaction.response.send_message("Hello, I am damrok's bot")    
         

    @app_commands.command(name="play", description="turn the music on!")
    async def play(self,interaction: discord.Interaction, url: str) -> None:
        try:
            voice_channel = interaction.user.voice.channel
            if self.is_paused:
                self.vc.resume()
            else:
                song = self.search_yt(url)
                if type(song) == type(True):
                    Exception
                    await interaction.response.send_message("Error has occured while downloading the song")
                else:
                    await interaction.response.send_message("song added to the queue")
                    self.music_queue.append([song, voice_channel])

                    if self.is_playing == False:
                        await self.play_music(interaction)
        except AttributeError:
            await interaction.response.send_message("You need to be in a voice channel in order to use this command!")
        
    @app_commands.command(name = "check_play", description="check if the player is on")
    async def check_play(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(f"is playing = {self.is_playing}, is paused = {self.is_paused}")

    @app_commands.command(name = "pause", description= "pause the song")
    async def pause(self, interaction: discord.Interaction) -> None:
        if self.vc != None:
            if self.vc.is_playing():
                self.vc.pause()
                self.is_playing = False
                self.is_paused = True
                await interaction.response.send_message("song paused")

 


    @app_commands.command(name="resume", description="resume the song")
    async def resume(self, interaction: discord.Interaction) -> None:
        if self.vc != None:
            if self.is_paused:
                self.is_playing = True
                self.is_paused = False
                self.vc.resume()
                await interaction.response.send_message("song resumed")

    @app_commands.command(name="skip", description="skip the song")
    async def skip(self, interaction: discord.Interaction) -> None:
        if self.vc != None and self.vc:
            self.vc.stop()
            await interaction.response.send_message("song skipped")
            await self.play_music(interaction)

    @app_commands.command(name="queue", description="show how long the current song queue is")
    async def queue(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"current queue: {len(self.music_queue)} songs")

    @app_commands.command(name="clear", description="stop the music and clear the queue")
    async def clear(self, interaction: discord.Interaction) -> None:
        if self.vc != None and self.is_playing:
            self.vc.stop()
            self.is_playing = False
        self.music_queue = []
        await interaction.response.send_message("Music queue cleared")

    @app_commands.command(name="disconnect", description="tell me to go away")
    async def disconnect(self, interaction: discord.Interaction) -> None:
        self.is_playing = False
        self.is_paused = False
        await interaction.response.send_message("cya")
        await self.vc.disconnect()

    @app_commands.command(name="joke", description="ask me to send you a joke that definitelly won't get damrok cancelled")
    async def joke(self, interaction: discord.Interaction) -> None:
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
            await interaction.response.send_message(joke["joke"])
        else:
            await interaction.response.send_message(f"{joke['setup']}\n{joke['delivery']}")
                
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(item, download=False)
                URL = info['url']
            except Exception:
                return False
        return URL
    
    def play_next(self):
        print("entered play_next")
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda x = None: self.play_next())
        else:
            print("play_next sets playing to false")
            self.is_playing = False

    async def play_music(self, interaction):
        print("entered play_music")
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await interaction.response.send_message("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda x = None: self.play_next())

        else:
            print("play_music sets playing to false")
            self.is_playing = False

async def setup(client: commands.Bot) -> None:
    await client.add_cog(bot_cog(client))