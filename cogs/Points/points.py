import discord
from discord.ext import commands
from modules import json

class Points(commands.Cog):
    """View the Leaders of the Group"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == '✅' or payload.emoji.name == '❌':
            if payload.channel_id == 885317697515188264:

                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)

                user = payload.member
                role = msg.guild.get_role(887140579253817374)
                await user.add_roles(role)

    @commands.command()
    async def clearrole(self,ctx):
        if ctx.message.author.name == 'CalebP':
            roles = ctx.message.role_mentions
            for x in range(len(roles)):
                while len(roles[x].members) > 0:
                    role = roles[x]
                    user = roles[x].members[0]
                    await user.remove_roles(role)
                
                    #print(f'{user.name}-{role.name}')
                    

    
    @commands.command()
    async def gc(self,ctx,*request):

        def loadGC(user):
            data = json.load('points')
            try:
                points = data[f"{user}"]
            except:
                points = 0
            return points

        def giveGC(user):
            data = json.load('points')
            try:
                points = data[f"{user}"]
            except:
                points = 0

            data[f"{user}"] = points+1
            json.write('points', data)


        user = ctx.message.author.name
        targets = ctx.message.mentions
        roles = ctx.message.role_mentions

        # Show your number of GCs
        if not request:
            balance = loadGC(user)
            await ctx.send(f'{user} has {balance} GCs')

        
        if len(request) > 1:
            if request[0] == 'balance':
                balance = loadGC(targets[0].name)
                await ctx.send(f'{targets[0]} has {balance} GCs')

        elif user == 'CalebP':
            if len(targets) > 0:
                for x in range(len(targets)):
                    giveGC(targets[x].name)
                    await ctx.send(f'Giving 1 GC to {targets[x].name}')

            if len(roles) > 0:
                for x in range(len(roles)):
                    for n in range(len(roles[x].members)):
                        giveGC(roles[x].members[n].name)
                    await ctx.send(f'Giving 1 GC to {roles[x].mention}')
        else:
            await ctx.send('You dont have permission to do this')

def setup(client):
    client.add_cog(Points(client))