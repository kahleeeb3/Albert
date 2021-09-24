import discord
from discord.ext import commands
import os
import subprocess
import json


class Kill(commands.Cog):
    """Commands For Caleb's Use"""

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def clean(self,ctx, amount:int):
        """deletes a set number of messages"""
        deleted= await ctx.channel.purge(limit = amount+1) #clears the messages + the command message
        cleanMessage = await ctx.send(f'Cleared {len(deleted)-1} messages') #returns the number of messages deleted minus the command message
        await cleanMessage.delete(delay = 3)

    @commands.command()
    async def github(self, ctx, *, message):
        """Pushes all the files to github repo"""
        command = f'cd /home/pi/Desktop/CSC-Club; git add --all; git commit -a -m "{message}";git push'
        output = str(subprocess.check_output(command, shell=True))
        output = output.replace("b\'","").replace("\\n\'","").replace("\\n","\n")[0:2000]
        await ctx.channel.send(f'{output}')

    @commands.command()
    async def off(self, ctx):
        """Turns the Bot off"""
        if ctx.message.author.name == 'CalebP':
            await ctx.channel.send(f'https://tenor.com/view/cry-sad-toy-story-woody-so-long-partner-gif-9797730')
            exit()
        else:
            await ctx.channel.send(f'Shut the fuck up {ctx.message.author.name}, you dont have the authority for that.')

    @commands.command()
    async def restart(self, ctx):
        """Restarts the Bot"""
        if ctx.message.author.name == 'CalebP':
            await self.client.change_presence(activity=discord.Activity(type = discord.ActivityType.streaming, name = f'Rebooting...') )
            import os
            os.system("sudo reboot")
            exit()
        else:
            await ctx.channel.send(f'Shut the fuck up {ctx.message.author.name}, you dont have the authority for that.')
        


def setup(client):
    client.add_cog(Kill(client))
