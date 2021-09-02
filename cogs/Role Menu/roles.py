import discord
from discord.ext import commands
from modules import menus#, lists
from modules.json import json

class RoleReactions(commands.Cog):
    """Sends the role menu to the chat"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rolemenu(self,ctx):
        # creates the embed
        embed = menus.get_embed(1)
        menu = await ctx.send(embed=embed)
        # add the reactions
        await menus.add_emojis(menu, 1)
        # change the role menu id
        menus.change_id(menu.id)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        # Gets the information from reaction
        information = menus.get(payload)
        user = information['user']
        emoji= information['emoji']
        message_id = information['message_id']

        # checks if input is from bot
        if user.bot:
            pass
        else:
            # checks if its from the correct message id
            if menus.check_message_id(message_id):
                #check if reaction is ◀ or ▶
                if emoji.name == '▶':
                    await menus.flip_right(self.client, payload)

                else:
                    # get the current menu number
                    msg = await menus.get_msg(self.client, payload)
                    menu_num = msg.embeds[0].title[0]
                    # find the matching role
                    role_id = menus.get_role_id(menu_num, emoji)
                    role = msg.guild.get_role(role_id)
                    if role in user.roles:
                        await user.remove_roles(role)
                    else:
                        await user.add_roles(role)
                        
def setup(client):
    client.add_cog(RoleReactions(client))