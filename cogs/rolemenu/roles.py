import discord
from discord.ext import commands
from modules import menus
from modules.json import json

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

        # Gets the information from reaction
        user = payload.member
        channel_id = payload.channel_id
        emoji = payload.emoji.name

        # checks if input is from bot
        if user.bot:
            pass
        elif emoji == '✅' and channel_id == 885318831688548363:
            # checks if its from the correct message id
                channel = self.client.get_channel(payload.channel_id)
                msg = await channel.fetch_message(payload.message_id)

                role = msg.guild.get_role(890279940090626098)
                await user.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Gets the information from reaction
        channel = self.client.get_channel(payload.channel_id)
        msg = await channel.fetch_message(payload.message_id)
        user = await msg.guild.fetch_member(payload.user_id)

        channel_id = payload.channel_id
        emoji = payload.emoji.name

        # checks if input is from bot
        if user.bot:
            pass
        elif emoji == '✅' and channel_id == 885318831688548363:
            # checks if its from the correct message id
            role = msg.guild.get_role(890279940090626098)
            await user.remove_roles(role)
                

                
                        
            
def setup(client):
    client.add_cog(RoleReactions(client))