import discord
from discord.ext import commands
import pandas as pd

class RollCall(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if isinstance(message.channel, discord.channel.DMChannel):            
            # Check if the password is correct
            location = "/home/pi/Desktop/CSC-Club/modules/files"
            p = open(f"{location}/password.txt","r")
            password = p.readline()

            if message.content == password:

                # Create DM with sender
                sender_channel = await message.author.create_dm()
                

                # Load all the information about the user
                try:
                    members = pd.read_csv(f"{location}/members.csv")
                    user = members[members["Discord"]==message.author.id]
                    fn = user["First Name"].iloc[0]
                    ln = user["Last Name"].iloc[0]
                    e = user["E-mail"].iloc[0]
                    user_info = f"{fn} {ln}, {e}"
                    await sender_channel.send("Attendence Confirmed, Welcome.")
                except:
                    await sender_channel.send("**ERROR:** ``Please register with the CSC Club to use this command.``")


                # Send the data
                leaders = {
                    "Caleb":487323172492935189,
                    "Fardin":736981053209575454,
                    "Ajay": 882009234114482196,
                    "Owen":517118478117896192
                }
                
                for x in leaders:
                    leader = self.client.get_user(leaders[x])
                    dm_channel = await leader.create_dm()
                    await dm_channel.send(user_info)           

     
def setup(client):
    client.add_cog(RollCall(client))
