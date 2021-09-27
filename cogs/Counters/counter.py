import discord
from discord.ext import commands
from modules.counters import counter

class Counter(commands.Cog):
    """Keeps count of the number of times a thing occurs"""

    def __init__(self, client):
        self.client = client
        
    @commands.command()
    async def miss(self, ctx, user, *option):
        """$<counter> <user> <list/reset/retract/null>"""
        await counter("Miss",option,self, ctx)

    @commands.command()
    async def late(self, ctx, user, *option):
        """$<counter> <user> <list/reset/retract/null>"""
        await counter("Late",option,self, ctx)
     
def setup(client):
    client.add_cog(Counter(client))
