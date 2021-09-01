import discord
from discord.ext import commands, tasks
from modules import canvas, time
from datetime import datetime as dt

class Canvas(commands.Cog):
    """Pulls Physics Department Announcements Feed from Canvas"""
    
    def __init__(self, client):
        self.client = client
    
    """
    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()
    """

    @commands.command()
    async def canvas(self, ctx):
       embed = canvas.get_embed()
       await ctx.send(embed=embed)
        
        
    
    @tasks.loop(seconds= 60)
    async def check(self):

        channel_id = 812754306712600607
        channel = self.client.get_channel(channel_id)

        curr_date = time.curr_time()[2]
        date_unformatted = canvas.get_info()[0]
        date = time.convert_datetime_to_text(date_unformatted)[2]

        a = dt.strptime(curr_date, "%m/%d/%y")
        b = dt.strptime(date, "%m/%d/%y")

        if a > b:
            embed = canvas.get_embed()
            await channel.send(embed = embed)

def setup(client):
    client.add_cog(Canvas(client))