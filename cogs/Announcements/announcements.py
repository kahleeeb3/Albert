import discord
from discord.ext import commands, tasks
from modules import canvas, json, time

class Canvas(commands.Cog):
    """Pulls Physics Department Announcements Feed from Canvas"""
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()

    @commands.command()
    async def canvas(self, ctx):
       embed = canvas.get_embed()
       await ctx.send(embed=embed)
    
    @tasks.loop(seconds= 60)
    async def check(self):

        channel_id = 812754306712600607
        channel = self.client.get_channel(channel_id)

        info = canvas.get_info()
        date = time.convert_datetime_to_text(info[0])[2]
        title = info[2]
        
        new = {
            "Date":date,
            "Title": title
            }

        old = json.load('events')
        if new != old:
            json.write('events',new)
            embed = canvas.get_embed()
            await channel.send(embed = embed)
        

def setup(client):
    client.add_cog(Canvas(client))