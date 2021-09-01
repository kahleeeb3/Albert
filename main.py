print('Starting Bot...')
# IMPORTS
import discord
from discord.ext import commands, tasks
import os

# defines the prefix for all commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '$', intents=intents)


# loads all folders within the cogs folder
for folder in os.listdir('/home/pi/Desktop/Albert/cogs'):
    # ignores the cache folder
    if folder == '__pycache__':
        pass
    else:
        # loads all files in folder
        for filename in os.listdir(f'/home/pi/Desktop/Albert/cogs/{folder}'):
            #if its a python folder:
            if filename.endswith('.py'):
                #create a cog with the files in that folder
                client.load_extension(f'cogs.{folder}.{filename[:-3]}')

@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence(activity=discord.Game(f'Epic Physics Stuff'))

 
# place token code in the following directory
client.run(open('/home/pi/Desktop/token-albert.txt', "r").read())