import discord
from discord.ext import commands
from modules import leaders, json, menus

class Leaders(commands.Cog):
    """View the Leaders of the Group"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def leadermenu(self,ctx):
        # creates the embed
        embed = leaders.get_embed(1)
        # upload file to embed
        
        # Add Image File
        menu = await ctx.send(embed=embed)
        # add the reactions
        await menu.add_reaction('▶')
        # change the role menu id
        data = json.load('leaders')
        data["message_id"] = menu.id
        json.write('leaders',data)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        async def flip_right(bot,payload):
            # get menu number
            channel = bot.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            embed = msg.embeds[0]
            current = int(embed.title[0])
            try:
                embed2 = leaders.get_embed(current + 1)
                current = current + 1
            except:
                embed2 = leaders.get_embed(1)
                current = 1
            await msg.clear_reactions()
            await msg.edit(embed=embed2)
            # add the reactions
            await msg.add_reaction('▶')


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
            data = json.load('leaders')
            correct_message_id = data["message_id"]
            if message_id == correct_message_id:
                #check if reaction is ◀ or ▶
                if emoji.name == '▶':
                    await flip_right(self.client, payload)
                        
def setup(client):
    client.add_cog(Leaders(client))