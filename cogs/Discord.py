from discord.ext import commands as cmd
from discord.utils import get
import util.Modular as mod
import youtube_dl as yt
import discord
import os

class Discord(cmd.Cog):
    
    #--------Construction--------
    def __init__(self, panda):
        self.panda=panda

    @cmd.Cog.listener()
    async def on_ready(self):
        print('Discord-based tools have been initialized')
    
    #-------Message Cleanup------ *includes the command itself
    @cmd.command(help='Deletes the previous message')
    async def cleanup(self, bot):
        await bot.channel.purge(limit=2)

    @cmd.command(help='Deletes the last 30 messages')
    async def wipe(self, bot):
        await bot.channel.purge(limit=31)

    #----YouTube Music Player----
    @cmd.command(help='Play Audio from YouTube')
    async def play(self, bot, link):
        channel = bot.message.author.voice.channel
        try:
            audio = get(self.panda.voice_clients, guild=bot.guild)
            #Bot VC
            if audio and audio.is_connected(): #move to channel if already connected
                await audio.move_to(channel)
            else: #connect if not connected
                audio = await channel.connect()
            #Play audio
            audio = get(self.panda.voice_clients, guild=bot.guild)
            if not audio.is_playing():
                    info = yt.YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}).extract_info(link, download=False)
                    audio.play(discord.FFmpegPCMAudio(info['formats'][0]['url'], **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}))
                    title = mod.border('Panda™ Music')
                    await bot.channel.send(f'{title} \n**Now Playing:** "{link}" as requested by {bot.author.mention}')
            else:
                await bot.channel.send(f'{bot.author.mention}, music is already playing. {link} Please wait until this audio has completed playing.*')
        except Exception as err: #notifies and disconnects upon error
            await bot.channel.send(f'{bot.author.mention}, unfortunately, an error occured ({err}). Either try again or give me a different link.')
            if audio and audio.is_connected():
                await audio.disconnect()

    @cmd.command(help='Stop Audio and Leave Voice Channel')
    async def stop(self, bot):
        audio = get(self.panda.voice_clients, guild=bot.guild)
        if audio and audio.is_connected():
            await audio.disconnect()
        else:
            await bot.channel.send(f'{bot.author.mention}, there is no audio playing.')

def setup(panda):
    panda.add_cog(Discord(panda))