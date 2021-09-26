from .json import *
import discord

async def check_admin(ctx):
    user = ctx.message.author
    config = load('config')
    admins = config["Admins"]
    admin_ids = []
    for x in admins:
        admin_ids.append(admins[x])
    if user.id in admin_ids:
        return True
    else:
        await ctx.send(f"You dont have the authority for that {user.mention}")
        return False

def check_channel(correct_channel_name,channel_id):
    config = load('config')
    channels = config["Channels"]
    correct_channel_id = channels[correct_channel_name]
    if correct_channel_id == channel_id:
        return True
    else:
        return False

async def get_role(rolename,self,payload):
    config = load('config')
    roles = config["Roles"]
    role_id = roles[rolename]

    # Gets the information from reaction
    channel = self.client.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    user = await msg.guild.fetch_member(payload.user_id)

    # checks if input is from bot
    if user.bot:
        pass
    else:
        # checks if its from the correct message id
        role = msg.guild.get_role(role_id)
        return {"Role":role,"User":user}

