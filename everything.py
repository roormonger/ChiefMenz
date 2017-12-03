'''Here we go
Other functions or cogs for Craig, adding clips, playing clips, recording clips?'''
from discord.ext import commands
import discord
from discord.ext import commands
import asyncio
import random
import os
import aiohttp

from .utils import chat_formatting as cf

#class Craig:
#class RecordClip
#class Clip
#class AddDrop

#need to call something to make sure the bot is in the channel, or if not, bring it in the channel?  possibly call from redbot api or discord api

class DropSounds:
    """Read files (or folders?) from folder, json (or just a file), Read from a json/file into a list
    Randomly choose list item and play"""

    def __init__(self, bot):
        self.bot = bot
        self.droplistFile = "data/everything/droplist.txt" #define the relative path and name of the file
        self.dropfilesLocation = "data/audio/drop2"

    async def _join_voice_channel(self, channel):
        try:
            await self.bot.join_voice_channel()
        except asyncio.futures.TimeoutError as e:
            print(e)
            print("We timed out connecting to a voice channel")

    @commands.command(no_pm=True, pass_context=True)
    async def ping2(self): #test to see if the bot is working
        await self.bot.say("pong")

    @commands.command(no_pm=True, pass_context=True, aliases=['adddrops'])
    async def adddrop(self, ctx, link: str=None):
        """Adds a new sound.

        Either upload the file as a Discord attachment and make your comment
        "[p]addsfx", or use "[p]addsfx direct-URL-to-file".
        """

        await self.bot.type()

        server = ctx.message.server

        attach = ctx.message.attachments
        if len(attach) > 1 or (attach and link):
            await self.bot.say(
                cf.error("Please only add one sound at a time."))
            return

        url = ""
        filename = ""
        if attach:
            a = attach[0]
            url = a["url"]
            filename = a["filename"]
        elif link:
            url = "".join(link)
            filename = os.path.basename(
                "_".join(url.split()).replace("%20", "_"))
        else:
            await self.bot.say(
                cf.error("You must provide either a Discord attachment or a"
                         " direct link to a sound."))
            return

        filepath = os.path.join(self.dropfilesLocation, filename)

        async with aiohttp.get(url) as new_sound:
            f = open(filepath, "wb")
            f.write(await new_sound.read())
            f.close()

        await self.bot.say(
            cf.info("Sound {} added.".format(os.path.splitext(filename)[0])))


    @commands.command(no_pm=True, pass_context=True)
    async def dropsy(self, ctx): #this is the command
        #first create the droplist file from folder
        dropList = os.listdir("data/audio/drop2") #put the files from directory into a list
        print("\n\ndrops listed: ", dropList)
        song = random.choice(dropList) #this should be the file name hopefully
        print("\n\nrandom song:", song)

        channel = channel()
        voice = await self._join_voice_channel() #example from discordpy.readthedocs.io
        player = await voice.create_ffmpeg_player(song)
        player.start()
        """first I thought we would have to write to a file, but I think just storing the list in a... list variable will work fine with no benefit to making a file?
        	with open(droplistFile, mode="w", encoding="utf-8") as dList: for filename in dropfileslocation dList.write(droplist)"""
        await self.bot.say("Go fuck yourself!")

def setup(bot):#tells red all the things that need to be done before the plugin is loaded
    x = DropSounds(bot) #name of class
    bot.add_cog(x)
