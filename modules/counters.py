import discord
from .json import *
from modules.time import *
from modules.admins import check_admin
import asyncio

async def send_count(ctx, person, counter_name):
    # Step 1: load in the data
    data = load(counter_name)

    # Step 2: Send the data
    try:
        data = data["member"][f'{person.name}']
        embed = discord.Embed(title=f'{counter_name} Count: {data["count"]}',color=discord.Color.red())
        embed.set_author(name=f"{person}", icon_url=f"{person.avatar_url}")
        for case in data["cases"]:

            details = data["cases"][case]
            day = details["day"]
            date = details["date"]
            time = details["time"]

            embed.add_field(name=f'{case}. {date}',value = f'{day} at {time}', inline=False)

        await ctx.send(embed=embed)
    except:
        await ctx.channel.send(f"This person's {counter_name} is zero")

async def send_new_count(ctx, person,counter_name):
    # Step 1: load in the data
    data = load(counter_name)

    # Step 2: Send the data
    data = data["member"][f'{person.name}']
    embed = discord.Embed(title=f'{counter_name} Count: {data["count"]}',color=discord.Color.red())
    embed.set_author(name=f"{person}", icon_url=f"{person.avatar_url}")
    numCases = len(data["cases"])

    details = data["cases"][str(numCases)]
    day = details["day"]
    date = details["date"]
    time = details["time"]

    embed.add_field(name=f'{date}',value = f'{day} at {time}', inline=False)

    await ctx.send(embed=embed)

async def confirm(ctx, self, user,counter_name):
    counter = await ctx.send(f'Please vote to retract last {counter_name} count from {user}')
    await counter.add_reaction('✅')
    await counter.add_reaction('❌')

    def check(reaction, user):
        votes_to_pass = 4
        for reaction in reaction.message.reactions:
                if (reaction.count >= votes_to_pass):
                    if str(reaction.emoji) == '✅':
                        return True

    try:
        reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send('Vote did not pass. Counter Remains.👎')
        return False
    else:
        await ctx.send('Vote passed. Last count removed. 👍')
        return True

async def counter(counter_name,option,self,ctx):
    # Step 1: load in the data or create the file
    data = load(counter_name)
    try:
        data["member"]
    except:
        data= {"member":{}}
        write(counter_name,data)

    # Step 2: Determine which person to target

    person = ctx.message.mentions[0].name

    if not option:
        # Step 3: add 1 to their counter 
        try:
            data["member"][f'{person}']['count'] = data["member"][f'{person}']['count'] + 1
            caseNum = len(data["member"][f'{person}']['cases']) + 1
        except:
            data["member"][f'{person}'] = {"count": 1,"cases":{}}
            caseNum = 1

        
        # Step 3: get new data
        
        cases = data["member"][f'{person}']['cases']
        now = curr_time()
        day = now[0]
        time = now[1]
        date = now[2]
        newCase = {
                "day": f"{day}",
                "date": f"{date}",
                "time": f"{time}"
                }
        cases[f'{caseNum}'] = newCase

        # Step 4: Add the data
        write(counter_name,data)
        person = ctx.message.mentions[0]
        await send_new_count(ctx, person,counter_name)

    else:
        if option[0]=='list':
            person = ctx.message.mentions[0]
            await send_count(ctx, person, counter_name)
        elif option[0] == 'retract':
            if await confirm(ctx,self,person,counter_name):
                data["member"][f'{person}']['count'] = data["member"][f'{person}']['count'] - 1
                caseNum = len(data["member"][f'{person}']['cases'])
                cases = data["member"][f'{person}']['cases']

                del cases[f"{caseNum}"]
                write(counter_name,data)

        elif option[0]== 'reset':
            if await check_admin(ctx): 
                data["member"][f"{person}"] = {}
                write(counter_name,data)
                await ctx.channel.send(f'Reset {person}\'s counter to 0')
        
