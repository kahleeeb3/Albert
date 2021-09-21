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
    async def gc(self,ctx,*options):
        """
        Handles the Currency of the CSC Club
        """

        def loadGC(user):
            data = json.load('points')
            try:
                points = data[f"{user}"]
            except:
                points = 0
            return points

        def giveGC(user,add):
            data = json.load('points')
            try:
                points = data[f"{user}"]
            except:
                points = 0

            data[f"{user}"] = points+add
            json.write('points', data)

        user = ctx.message.author.name # The Person running the command
        targets = ctx.message.mentions # The person(s) mentioned in the command
        roles = ctx.message.role_mentions # The Roles mentioned in the command

        """
        $gc                     Gives user their balance
        $gc balance <user(s)>
        $gc <user(s)>           Gives <user(s)> 1 GC
        $gc <value> <user(s)>   Gives <user(s)> <value> GC's
        """
    # Checking Gentleman Coins
        # for yourself
        if not options:
            curr = loadGC(user)
            await ctx.send(f'{user} has {curr} GC(s)')
        # for another user
        elif options[0].lower() == 'balance':

            if len(targets) > 0:
                for i in range(len(targets)):
                    n = targets[i].name
                    curr = loadGC(n)
                    await ctx.send(f'{n} has {curr} GC(s)')

            if len(roles) > 0:
                for x in range(len(roles)):
                    for n in range(len(roles[x].members)):
                        curr = loadGC(roles[x].members[n].name)
                        await ctx.send(f'{roles[x].members[n].name} has {curr} GC(s)')

    # Giving Gentleman Coins
        elif user == 'CalebP': # Only CalebP can do this
            try:
                value = int(options[0]) # See if quantity is given
            except:
                value = 1 # if not given, say it's 1

            # For Users
            if len(targets) > 0:
                for i in range(len(targets)):
                    n = targets[i].name
                    giveGC(n,value)
                    curr = loadGC(n)
                    await ctx.send(f'Giving {value} GC to {n}. New Total: {curr}')
            
            # For Roles
            if len(roles) > 0:
                for x in range(len(roles)):
                    for n in range(len(roles[x].members)):
                        giveGC(roles[x].members[n].name,value)
                    await ctx.send(f'Giving 1 GC to {roles[x].mention}')

def setup(client):
    client.add_cog(Points(client))