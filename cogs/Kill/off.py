import discord
from discord.ext import commands
import os
import subprocess
from modules.admins import check_admin

class Kill(commands.Cog):
    """Commands for Controlling the Pi"""

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def clear(self,ctx, amount:int):
        """deletes a set number of messages"""
        if await check_admin(ctx):
            #clears the messages + the command message
            deleted= await ctx.channel.purge(limit = amount+1)
            #returns the number of messages deleted minus the command message
            cleanMessage = await ctx.send(f'Cleared {len(deleted)-1} messages')
            # deletes the message
            await cleanMessage.delete(delay = 3)

    @commands.command()
    async def github(self, ctx, *, message):
        """Pushes all the files to github repo"""
        if await check_admin(ctx):
            command = f'cd /home/pi/Desktop/CSC-Club; git add --all; git commit -a -m "{message}";git push'
            output = str(subprocess.check_output(command, shell=True))
            output = output.replace("b\'","").replace("\\n\'","").replace("\\n","\n")[0:2000]
            await ctx.channel.send(f'{output}')

    @commands.command()
    async def off(self, ctx):
        """Turns the Bot off"""
        if await check_admin(ctx):
            await ctx.channel.send(f'Powering Off')
            exit()

    @commands.command()
    async def restart(self, ctx):
        """Restarts the Bot"""
        if await check_admin(ctx):
            await self.client.change_presence(activity=discord.Activity(type = discord.ActivityType.streaming, name = f'Rebooting...') )
            import os
            os.system("sudo reboot")
            exit()
        
def setup(client):
    client.add_cog(Kill(client))
