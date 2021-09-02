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
    async def t(self, ctx, *, command):
        """Run Terminal Commands"""
        output = str(subprocess.check_output(command, shell=True))
        output = output.replace("b\'","").replace("\\n\'","").replace("\\n","\n")[0:2000]
        if 'cat' in command:
            output = output.replace('\\r','')
            output = (f"```python\n{output}\n```").replace('\\','')
        await ctx.channel.send(f'{output}')

    @commands.command()
    async def github(self, ctx, *, message):
        """Pushes all the files to github repo"""
        command = f'cd /home/pi/Desktop/Discord; git add --all; git commit -a -m "{message}";git push'
        output = str(subprocess.check_output(command, shell=True))
        output = output.replace("b\'","").replace("\\n\'","").replace("\\n","\n")[0:2000]
        await ctx.channel.send(f'{output}')

    """
    @commands.command()
    async def timeout(self, ctx, *max_time):
        #Deletes all messages for a given period of time can pass in the amount of time as a variable `$timeout <time>`
        import time

        if not max_time:
            max_time = 600
        else:
            max_time = max_time[0]

        await ctx.channel.send(f'**Due to conflict:** Chat is disabled for {max_time} seconds')

        start_time = time.time()  # remember when we started
        while (time.time() - start_time) < int(max_time):
            thing = await self.client.wait_for('message')
            await thing.delete()

        await ctx.channel.send(f'Chat is enabled. Please be friends.')
    """
    
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
