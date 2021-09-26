import discord
from discord.ext import commands
from modules.admins import check_channel,get_role

class RoleReactions(commands.Cog):
    """Sends the role menu to the chat"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rolemenu(self,ctx):
        menu = await ctx.send('If you would like to be an active member please react with ✅')
        await menu.add_reaction('✅')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        emoji = payload.emoji.name
        channel_id = payload.channel_id

        if emoji == "✅" and check_channel("welcome",channel_id):
            output = await get_role("Active Members",self,payload)
            user,role = output["User"],output["Role"]
            await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        channel_id = payload.channel_id

        if emoji == "✅" and check_channel("welcome",channel_id):
            output = await get_role("Active Members",self,payload)
            user,role = output["User"],output["Role"]
            await user.remove_roles(role)
                        
            
def setup(client):
    client.add_cog(RoleReactions(client))