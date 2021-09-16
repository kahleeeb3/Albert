import discord
from discord.ext import commands

class Workshop(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 887342368293003374:
            user = payload.member
            channel = self.client.get_channel(payload.channel_id)
            msg = await channel.fetch_message(payload.message_id)
            if msg.id == 887831348142805013:

                role = None
                
                if payload.emoji.name == 'python':
                    role = msg.guild.get_role(887819292542894160)
                if payload.emoji.name == 'discord':
                    role = msg.guild.get_role(887819345240129546)
                if payload.emoji.name == 'cpp':
                    role = msg.guild.get_role(887819420209147974)

                await user.add_roles(role)

                      
def setup(client):
    client.add_cog(Workshop(client))