import discord
from discord import embeds
from discord import channel
from discord import message
from discord.ext import commands,tasks
from modules import json
from modules.admins import check_admin

def get_embed(self):
        data = json.load('points')
        sorted_points = sorted(data.items(), key = lambda kv: kv[1]) # sort the data
        num_people = 10  # the number of members to display (n)
        top_members = sorted_points[-1*num_people:] # get the top n people
        top_members = top_members[::-1] # reverse the list
        scoreBoard_embed = discord.Embed(title = "GC LEADERBOARD", colour = 0xFFB900) # create discord embed
        i = 1
        for user in top_members:
            if i == 1:
                # Get the profile picture of the user that is in the lead
                a = self.client.guilds
                b = [(i.id == 881633300697985045) for i in a]
                server = [x for x, y in zip(a,b) if y == True][0]
                a = server.members
                b = [(i.name == user[0]) for i in a]
                winner_pic = [x for x, y in zip(a,b) if y == True][0].avatar_url

                scoreBoard_embed.set_author(name = f'{i}. {user[0]} - {user[1]}', icon_url= winner_pic)
            else:
                scoreBoard_embed.add_field(name=f'{i}. {user[0]}',value=user[1],inline=True)
            i+=1
        return scoreBoard_embed

class Points(commands.Cog):
    """View the Leaders of the Group"""

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()
    
    @commands.command()
    async def export(self,ctx):
        roles = ctx.message.role_mentions # The Roles mentioned in the command
        mystring = ''
        if len(roles) > 0:
                for x in range(len(roles)):
                    name = roles[x].name
                    mystring = mystring + f'{name}\n'
                    for i in range(len(roles[x].members)):
                        name = roles[x].members[i].name
                        mystring = mystring + f'{i+1}) {name}\n'
                await ctx.send(mystring)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channels = {
            "announcements":885317697515188264,
            "voting":887342368293003374
        }
        for x in channels:
            if payload.channel_id == channels[x]:

                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)
                user = payload.member

                role = msg.guild.get_role(887140579253817374) # get gentleman role
                await user.add_roles(role) # add gentleman role

    @commands.command()
    async def clearrole(self,ctx):
        if await check_admin(ctx):
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
        elif await check_admin(ctx): # Only admins can do this
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

    @commands.command(aliases=['lb'])
    async def leaderboard(self,ctx):
        await ctx.message.delete()
        embed = get_embed(self)
        board = await ctx.send(embed= embed)
        await ctx.send(board.id)
        
    
    @tasks.loop(seconds= 30)
    async def check(self):
        a = self.client.guilds
        b = [(i.id == 881633300697985045) for i in a]
        server = [x for x, y in zip(a,b) if y == True][0]
        data = json.load("config")
        channel_id = data["Channels"]["about-us"]
        channel = server.get_channel(channel_id)
        board_id = data["Messages"]["leaderboard"]
        board = await channel.fetch_message(board_id)
        score_board = get_embed(self)
        await board.edit(embed = score_board)

def setup(client):
    client.add_cog(Points(client))