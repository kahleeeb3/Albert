import discord
from discord.ext import commands
from modules.admins import check_channel,get_role,check_admin, check_message
from modules import json

class RoleReactions(commands.Cog):
    """Sends the role menu to the chat"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rolemenu(self,ctx):
        if await check_admin(ctx): # check the the user is an admin
            menu = await ctx.send('If you would like to participate in the main chat as an active member please react with ✅')
            await menu.add_reaction('✅')

            # assign the new menu id
            data = json.load('config')
            data["Messages"]["rolemenu"] = menu.id
            json.write('config', data)

    @commands.command()
    async def classmenu(self,ctx,*input):
        """
        Gives the Class role selection menu
        Run the command the following way:

        $classmenu 
        "Class 1 name" @class1role
        "Class 2 name" @class2role 
        """
        if await check_admin(ctx): # check the the user is an admin

            numbers = ['1️⃣',"2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            choices = ""
            input = [x for x in input if (input.index(x) %2 == 0)] # select only the class names
            rolenames = [x.name for x in ctx.message.role_mentions]
            print(rolenames)

            # create the message to send in the chat
            for i, x in enumerate(input):
                choices += f"{numbers[i]} {x}\n"

            menu = await ctx.send(f'Which classes are you in?\n{choices}') # send the message

            # add the reactions
            for i, x in enumerate(input):
                await menu.add_reaction(numbers[i])

            # assign the new menu id
            data = json.load('config')
            data["Messages"]["classmenu"] = menu.id
            json.write('config', data)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        
        emoji = payload.emoji.name
        channel_id = payload.channel_id
        message_id = payload.message_id

        if emoji == "✅" and check_message("rolemenu",message_id):
            output = await get_role("Active Members",self,payload)
            user,role = output["User"],output["Role"]
            await user.add_roles(role)
        if check_message("classmenu",message_id):
            numbers = ['1️⃣',"2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            names = ['111','211','235','242','243','271-01','271-02']
            if emoji in numbers: # if the reaction is one of the numbers
                index = numbers.index(emoji) # get the index of the number
                output = await get_role(names[index],self,payload) #get the role and user
                user,role = output["User"],output["Role"] # assign variables
                await user.add_roles(role) #give the role

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji.name
        channel_id = payload.channel_id
        message_id = payload.message_id

        if emoji == "✅" and check_message("rolemenu",message_id):
            output = await get_role("Active Members",self,payload)
            user,role = output["User"],output["Role"]
            await user.remove_roles(role)

        if check_message("classmenu",message_id):
            numbers = ['1️⃣',"2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
            names = ['111','211','235','242','243','271-01','271-02']
            if emoji in numbers: # if the reaction is one of the numbers
                index = numbers.index(emoji) # get the index of the number
                output = await get_role(names[index],self,payload) #get the role and user
                user,role = output["User"],output["Role"] # assign variables
                await user.remove_roles(role) #give the role
                        
            
def setup(client):
    client.add_cog(RoleReactions(client))