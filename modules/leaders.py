import discord
#from modules import lists
from modules.json import json

def load():
    # loads in the data
    location = f'./modules/files/leaders.json'
    a_file = open(location, "r")
    data = json.load(a_file)
    a_file.close()
    return data

def write(filename, data):
    location = f'./modules/files/{filename}.json'
    a_file = open(f'{location}', "w")
    json.dump(data, a_file)
    a_file.close()


def get_embed(number:int):
    # loads in the data
    data = load()
    # define the embed
    name = data["menu"][f"{number}"]["Name"]
    position = data["menu"][f"{number}"]["Positions"]
    description = data["menu"][f"{number}"]["Statement"]
    image = data["menu"][f"{number}"]["Image"]

    embed = discord.Embed(title=f'{number}.{name}',description = description,color=discord.Color.red())
    embed.set_image(url=image)
    embed.set_author(name = position)
    
    """
    for role in data["menu"][f"{number}"]["roles"]:
        emoji = data["menu"][f"{number}"]["roles"][role]["emoji"]
        embed.add_field(name=f'{emoji}',value = f'{role}', inline=True)
    """

    return embed

async def add_emojis(menu, number:int):
    data = load()
    for role in data["menu"][f"{number}"]["roles"]:
        emoji = data["menu"][f"{number}"]["roles"][role]["emoji"]
        await menu.add_reaction(emoji)

    await menu.add_reaction('▶')

def change_id(message_id):
    data = load()
    data["message_id"] = message_id
    write('rolemenu',data)

async def get_msg(bot,payload):
    # get menu number
    channel = bot.get_channel(payload.channel_id)
    msg = await channel.fetch_message(payload.message_id)
    return msg

async def flip_right(bot,payload):
    # get menu number
    msg = await get_msg(bot, payload)
    embed = msg.embeds[0]
    current = int(embed.title[0])
    try:
        embed2 = get_embed(current + 1)
        current = current + 1
    except:
        embed2 = get_embed(1)
        current = 1
    await msg.clear_reactions()
    await msg.edit(embed = embed2)
    await add_emojis(msg, current)

def get(payload):
    user = payload.member
    message_id = payload.message_id
    emoji = payload.emoji
    return {'user': user,'message_id': message_id, 'emoji': emoji}

def check_message_id(message_id):
# checks if the reaction was added to the role menu
    # loads in the data
    data = load()
    correct_message_id = data["message_id"]
    if message_id == correct_message_id:
        return True
    else:
        return False

def get_role_id(menu_num, reaction):
# returns the role id for the given reaction
    data = load()
    for role in data["menu"][f"{menu_num}"]["roles"]:
        if reaction.name in data["menu"][f"{menu_num}"]["roles"][f"{role}"]["emoji"]:
            return data["menu"][f"{menu_num}"]["roles"][f"{role}"]["id"]
