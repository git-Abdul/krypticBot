import discord
import random
from discord.ext import commands
import os
import discord.utils
import requests
from bs4 import BeautifulSoup
from webserver import keep_alive
import asyncio
import datetime
import aiohttp
import math

global ver
ver = "`v1.7.0 Beta`"

global embedColor
embedColor = 0xfe9479

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

max_paragraphs = 2

intents = discord.Intents.default()
intents.messages = True
intents.members = True

intents = discord.Intents().all()

client = commands.Bot(command_prefix=".", intents=intents)
client.remove_command("help")


welcome_channels = {}
member = ()

# bot ready
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online, activity=discord.Game(".help")
    )
    print(f"Init Completed! ✅\nLogged in as: Kryptic #1648\nVersion: {ver} 🤖")
    
def fetch_answer(question):
    formatted_question = question.replace(' ', '_')
    search_url = f"https://en.wikipedia.org/wiki/{formatted_question}"

    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content = soup.find(id='content')
        paragraphs = content.find_all('p')

        answer = ''
        for p in paragraphs[:max_paragraphs]:
            answer += p.get_text() + ' '

        return answer
    else:
        return "Sorry, I couldn't find an answer to that question."

@client.command(aliases=["pt"])
async def prompt(ctx, *, question):
    answer = fetch_answer(question)
    em = discord.Embed(
        title="Here's your answer: ",
        description=f'{answer}',
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.set_footer(text=f"Requested by {ctx.author.name}")
    em.set_thumbnail(url="https://i.postimg.cc/3W5Bhfr6/ai.png")
    await ctx.send(embed=em)
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.news'):
        try:
            response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}')
            news_data = response.json()

            if news_data['status'] == 'ok':
                random.shuffle(news_data['articles'])
                for article in news_data['articles'][:2]:
                    await message.channel.send(f"**{article['title']}**\n{article['description']}\n{article['url']}")
            else:
                await message.channel.send("Error fetching news data.")
        except Exception as e:
            await message.channel.send("An error occurred while fetching news.")


@client.command()
async def truth(ctx):

    truthResponses = [
        "When was the last time you lied?",
        "When was the last time you cried?",
        "What is your biggest fear?",
        "What is something you are glad your mum does not know about you?",
        "Have you ever cheated on someone?",
        "What is the worst thing you have ever done?",
    ]

    truthem = discord.Embed(
        title=f"Truth",
        description=f"Truth: {random.choice(truthResponses)}",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    truthem.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=truthem)


@client.command()
async def dare(ctx):

    dareResponses = [
        "Show the most embarrassing photo on your phone",
        "Show the last five people you texted and what the messages said",
        "Do 100 squats",
        "Say something dirty to a person",
        "Twerk for a minute",
        "Try to lick your elbow",
    ]

    darem = discord.Embed(
        title=f"Dare",
        description=f"Dare: {random.choice(dareResponses)}",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    darem.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=darem)


@commands.has_permissions(administrator=True)
@client.command()
async def servers(ctx):
    for guild in client.guilds:
        em = discord.Embed(
            title="📑 | Bot Servers", description=f"{guild.name}", color=embedColor
        )
        await ctx.send(embed=em)
        print(guild.name)

@client.command(aliases=["scount"])
async def servercount(ctx):
    em = discord.Embed(
        title="Server Count",
        description=f"I'm in " + str(len(client.guilds)) + " servers!",
        color=embedColor,
    )
    await ctx.send(embed=em)


@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/dankmemes/new.json") as r:
            res = await r.json()
            embed = discord.Embed(color=embedColor, title="Reddit: `r/dankmemes`")
            embed.set_image(
                url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
            )
            embed.set_footer(
                text="We are not responsible for the memes posted (visit reddit.com for help)"
            )
            embed.set_author(
                name="reddit.com",
                url="https://reddit.com",
                icon_url="https://i.postimg.cc/cC75jRmZ/reddit.png",
            )
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("⬆️")
            await msg.add_reaction("⬇️")


@client.command(pass_context=True)
async def nsfw(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://www.reddit.com/r/tits/new.json") as r:
            res = await r.json()
            embed = discord.Embed(color=embedColor, title="Reddit: `r/dankmemes`")
            embed.set_image(
                url=res["data"]["children"][random.randint(0, 25)]["data"]["url"]
            )
            embed.set_footer(
                text="We are not responsible for the memes posted (visit reddit.com for help)"
            )
            embed.set_author(
                name="reddit.com",
                url="https://www.reddit.com/r/tits/",
                icon_url="https://i.postimg.cc/cC75jRmZ/reddit.png",
            )
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("⬆️")
            await msg.add_reaction("⬇️")


#wrongcommand
@client.event
async def on_command_error(context, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        em = discord.Embed(
            title="❌ Wrong Command!",
            description="Oh no! Looks like you have entered a wrong command, use `.help` to get to know all of my commands!",
            color=embedColor,
        )
        em.set_thumbnail(url="https://i.postimg.cc/3RsPzJQj/kick.png")
        await context.send(embed=em)

@client.command()
async def afk(ctx, reason):
    em = discord.Embed(
        title="🛏️ | AFK",
        description=f"Status: {ctx.author.mention} is now AFK\nReason: '{reason}'",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/dtKbB1Bw/afk.png")
    await ctx.send(embed=em)
    await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")


@client.command(aliases=["rafk"])
async def removeafk(ctx):
    em = discord.Embed(
        title="🛏️ | AFK Removed", description=f"Your afk was removed 👋", color=embedColor
    )
    em.set_thumbnail(url="https://i.postimg.cc/dtKbB1Bw/afk.png")
    await ctx.send(embed=em)
    await ctx.author.edit(nick=f"{ctx.author.name}")


@client.command()
async def gayrate(ctx, user: discord.Member = None):
    if not user:
        user = ctx.message.author
    em = discord.Embed(
        title="Gayrate Machine 🏳️‍🌈",
        description=f"{user.mention} is {random.randint(0,100)}% gay",
        color=embedColor,
    )
    em.set_footer(text=f"Requested by: {ctx.author}")
    await ctx.send(embed=em)


@client.command()
async def ppsize(ctx, user: discord.Member = None):

    pp_sizes = [
        "8D",
        "8=D",
        "8==D",
        "8===D",
        "8====D",
        "8=====D",
        "8=========D",
        "8==========D",
        "8===========D",
        "8=================D",
        "8=============================================================D",
    ]
    if not user:
        user = ctx.message.author

    em = discord.Embed(
        title="pp Rate 🖊️",
        description=f"{user.mention}'s pp size is `{random.choice(pp_sizes)}`",
        color=embedColor,
    )
    await ctx.send(embed=em)


@client.command(pass_context=True)
async def ticket(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title="Ticket system", description="React 📩 to make a ticket.", color=embedColor
    )
    embed.set_footer(text=f"Requested by {ctx.author.name}")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")

    await client.wait_for("reaction_add")
    await client.wait_for("reaction_add")

    await guild.create_text_channel(name=f"ticket-{ctx.author.name}")


# removechannel
@client.command(aliases=["rch"])
@commands.has_permissions(administrator=True)
async def removechannel(ctx, channel: discord.TextChannel):
    await channel.delete()


@client.command(aliases=["al"])
async def alerts(ctx):
    embed = discord.Embed(
        title="Alerts",
        description="⚠️ Slash Commands have been removed in version `1.4.5` because of server incompatiblility.\n⚠️ Buttons functionality removed in version `1.5.1` because of server incompatiblility.\n⚠️ Winter break has started. Ends at 2nd Jan 2023 (`Done`)",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    embed.set_thumbnail(url="https://i.postimg.cc/YqfJyHng/alert.png")
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@client.command()
async def dice(ctx):

    diceR = ["1", "2", "3", "4", "5", "6"]

    dicem = discord.Embed(
        title=f"🎲 | Dice is Rolling....",
        description=f"Rolled: {random.choice(diceR)}",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    dicem.set_thumbnail(url="https://i.postimg.cc/kMWZBCdZ/dice.png")
    dicem.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=dicem)


@client.command()
async def flip(ctx):

    flipR = ["Heads", "Tails"]

    flipem = discord.Embed(
        title=f"🪙 | Flipping coin....",
        description=f"Flipped as: {random.choice(flipR)}",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    flipem.set_thumbnail(url="https://i.postimg.cc/vZ0CbvdZ/flip.png")
    flipem.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=flipem)


@client.command(pass_context=True, aliases=["tclose"])
@commands.has_permissions(administrator=True)
@commands.has_any_role("📩| Ticket Issue")
async def ticketclose(ctx):
    embed = discord.Embed(
        title="Ticket system", description="React 📩 close this ticket", color=embedColor
    )

    embed.set_footer(text=f"Requested by {ctx.author.name}")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")

    await client.wait_for("reaction_add")
    await client.wait_for("reaction_add")

    if ctx.channel.name == "ticket":
        await ctx.channel.delete()


@client.command(aliases=["lc"])
@commands.has_permissions(administrator=True)
async def listcmds(ctx):
    helptext = "```"
    for command in client.commands:
        helptext += f"{command}\n"
    helptext += "```"
    em = discord.Embed(
        title="Listing all commands", description=f"{helptext}", color=embedColor
    )
    await ctx.send(embed=em)


@client.command()
@commands.has_permissions(administrator=True)
async def cmds(ctx):
    userEm = discord.Embed(
        title="**Commands**",
        description="Here are the available commands! Do have a look.",
        color=embedColor,
    )

    userEm.add_field(
        name="Fun",
        value="`8ball`, `say`, `kill`, `poll`, `giveaway`, `meme`, `truth` , `dare`, `flip`, `dice`, `gayrate`, `ppsize`, `afk`, `removeafk` |     ",
    )
    userEm.add_field(
        name="Moderation",
        value="`kick`, `ban`, `clear`, `removerole`, `removechannel`, `mute`, `unmute`, `lock`, `unlock`, `set_welcome` |      ",
    )
    userEm.add_field(
        name="Bot Info",
        value="`commands`, `ping`, `invite`, `about`, `copyright`, `version`, `credits`, `license`, `vote`, `links`, `socials`, `updatelist` |",
    )
    userEm.add_field(name="API's", value="`meme`, `news`, `prompt` |")
    userEm.add_field(
        name="Calculating", value="`multi`, `div`, `add`, `sub`, `root`, `pow` |"
    )
    userEm.add_field(
        name="Util",
        value="`prompt`, `boostcount`, `avatar`, `shortforms`, `changelog`, `membercount`, `whois`, `serverinfo`, `alerts`, `news` |",
    )

    await ctx.send(embed=userEm)


# help response
@client.command()
async def help(ctx):
    em = discord.Embed(
        title="✅ React to get help!",
        description="React to the following embed to get a DM on the bot's commands",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/x1yCxVyN/tick.png")

    msg = await ctx.send(embed=em)

    await msg.add_reaction("✅")

    await client.wait_for("reaction_add")

    userEm = discord.Embed(
        title="**Commands**",
        description="Here are the available commands! Do have a look.",
        color=embedColor,
    )

    userEm.add_field(
        name="Fun",
        value="`8ball`, `say`, `roll`, `kill`, `poll`, `giveaway`, `meme`, `truth`, `dare`, `flip`, `dice` |     ",
    )
    userEm.add_field(
        name="Moderation",
        value="`kick`, `ban`, `clear`, `removerole`, `removechannel`, `mute`, `unmute`, `lock`, `unlock`, `set_welcome` |      ",
    )
    userEm.add_field(
        name="Bot Info",
        value="`commands`, `ping`, `invite`, `about`, `copyright`, `version`, `credits`, `license`, `vote`, `links`, `socials`, `updatelist` |",
    )
    userEm.add_field(name="API's", value="`meme`, `news`, `prompt` |")
    userEm.add_field(
        name="Calculating", value="`multi`, `div`, `add`, `sub`, `root`, `pow` |"
    )
    userEm.add_field(
        name="Util",
        value="`prompt`, `boostcount`, `avatar`, `shortforms`, `changelog`, `membercount`, `whois`, `serverinfo`, `alerts`, `news` |",
    )

    user = ctx.author
    await user.send(embed=userEm)


# prefix
@client.command()
async def prefix(ctx):
    em = discord.Embed(
        title="⚡Server Prefix", description="My prefix here is, `.`", color=embedColor
    )
    await ctx.send(embed=em)


@client.command()
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    em = discord.Embed(
        title="🔒Locked",
        description=ctx.channel.mention + " ***is now in lockdown.***",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/nzjyd9gc/lock.png")
    await ctx.send(embed=em)


@client.command()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    em = discord.Embed(
        title="🔓Unlocked",
        description=ctx.channel.mention + " ***is now unlocked.***",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/DzMVdPCM/unlock.png")
    await ctx.send(embed=em)


# servericon
@client.command(aliases=["sicon"])
async def servericon(ctx):
    serverName = ctx.guild.name
    serverIcon = ctx.guild.icon_url
    em = discord.Embed(title=serverName + "'s Icon:", description="", color=embedColor)
    em.set_image(url=serverIcon)
    em.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=em)


# listroles
@client.command(aliases=["sr"])
async def listroles(ctx):
    rlist = []
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)
    server = ctx.guild.name

    em = discord.Embed(
        title=server + "'s Roles:", description=", ".join([b]), color=embedColor
    )
    await ctx.send(embed=em)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
    guild = ctx.guild
    role = discord.utils.get(ctx.guild.roles, name="🔇|Muted")

    if not role:
        perms = discord.Permissions(send_messages=False, read_messages=True)
        role = await guild.create_role(
            name="🔇|Muted", colour=discord.Colour(0xFF006A), permissions=perms
        )

    for channel in guild.text_channels:
        await channel.set_permissions(role, send_messages=False)

    em = discord.Embed(
        title="🔇 Member muted",
        description=f"{user.mention} has been muted | {role.mention}",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/50FY7zRn/hammer.png")
    await user.add_roles(role)
    await ctx.send(embed=em)


# unmute
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="🔇|Muted")
    em = discord.Embed(
        title="🔈Member unmuted",
        description=f"{user.mention} has been unmuted | {role.mention}",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/50FY7zRn/hammer.png")
    await user.remove_roles(role)
    await ctx.send(embed=em)


@client.command(aliases=["arole"])
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member, *, role: discord.Role = None):
    em = discord.Embed(
        title="Role Added!",
        description=f"{user.mention} has been assigned the role {role.mention}",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/50FY7zRn/hammer.png")
    await user.add_roles(role)
    await ctx.send(embed=em)


@client.command(aliases=["rrole"])
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member, *, role: discord.Role = None):
    em = discord.Embed(
        title="Role Removed!",
        description=f"{user.mention} has been dismissed the role {role.mention}",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/50FY7zRn/hammer.png")
    await user.remove_roles(role)
    await ctx.send(embed=em)


# giveaway
@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = [
        "Which channel will I host the giveaway in?",
        "What is the prize?",
        "How long should the giveaway run for (in seconds)?",
    ]
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for("message", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                "You didn't answer in time.  Please try again and be sure to send your answer within 30 seconds of the question."
            )
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(
            f"You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}"
        )
        return

    # Storing the variables needed to run the rest of the commands
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(
        f"The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds."
    )

    # Giveaway embed message
    give = discord.Embed(color=embedColor)
    give.set_author(name=f"🥳 GIVEAWAY TIME!")
    give.add_field(
        name=f"{ctx.author.name} is giving away: {prize}!",
        value=f"React with 🎉 to enter!\n Ends in {round(time/60, 2)} minutes!",
        inline=False,
    )
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
    give.set_footer(text=f"Giveaway ends at {end} UTC!")
    my_message = await channel.send(embed=give)

    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = discord.Embed(color=embedColor)
    winning_announcement.set_author(
        name=f"THE GIVEAWAY HAS ENDED!", icon_url="https://i.imgur.com/DDric14.png"
    )
    winning_announcement.add_field(
        name=f"🎉 Prize: {prize}",
        value=f"🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}",
        inline=False,
    )
    winning_announcement.set_footer(text="Thanks for entering!")
    await channel.send(embed=winning_announcement)


@client.command()
# @commands.has_role("Giveaway Host")
async def reroll(ctx, channel: discord.TextChannel, id_: int):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly
    try:
        new_message = await channel.fetch_message(id_)
    except:
        await ctx.send("Incorrect id.")
        return

    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the new winner to the server
    reroll_announcement = discord.Embed(color=embedColor)
    reroll_announcement.set_author(
        name=f"The giveaway was re-rolled by the host!",
        icon_url="https://i.imgur.com/DDric14.png",
    )
    reroll_announcement.add_field(
        name=f"🥳 New Winner:", value=f"{winner.mention}", inline=False
    )
    await channel.send(embed=reroll_announcement)


# boostcount
@client.command(aliases=["bc"])
async def boostcount(ctx):
    embed = discord.Embed(
        title=f"{ctx.guild.name}'s Boost Count",
        description=f"{str(ctx.guild.premium_subscription_count)} boosts",
        color=embedColor,
    )
    await ctx.send(embed=embed)


# ping
@client.command()
async def ping(ctx):
    em = discord.Embed(
        title="Ping",
        description=f"Pong! {round(client.latency * 1000)}ms",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/YSn7DHS8/version.png")
    await ctx.send(embed=em)


# version
@client.command(aliases=["ver"])
async def version(ctx):
    em = discord.Embed(title="Version", description=f"`{ver}`", color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/YSn7DHS8/version.png")

    await ctx.send(embed=em)


# license
@client.command(aliases=["li"])
async def license(ctx):
    em = discord.Embed(
        title="MIT license",
        description=f"MIT License \n\n Copyright 2023 AR ©️ \n\n Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. \n \n THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
        color=embedColor,
    )
    await ctx.send(embed=em)


# membercount
@client.command(aliases=["mc"])
async def membercount(ctx):
    memberCount = str(ctx.guild.member_count)
    name = str(ctx.guild.name)
    em = discord.Embed(
        color=embedColor,
        timestamp=ctx.message.created_at,
        title=name + "'s Members",
        description=f"{memberCount}",
    )
    em.set_thumbnail(url="https://i.postimg.cc/YSjZ9mpf/user.png")
    em.set_footer(text=f"Requested by {ctx.author}")

    await ctx.send(embed=em)


# serverinfo
@client.command(aliases=["si"])
async def serverinfo(ctx):

    role_count = len(ctx.guild.roles)

    embed2 = discord.Embed(timestamp=ctx.message.created_at, color=embedColor)
    embed2.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
    embed2.add_field(name="Owner", value=f"ar im.", inline=False)
    embed2.add_field(
        name="Verification Level", value=str(ctx.guild.verification_level), inline=False
    )
    embed2.add_field(name="Highest role", value=ctx.guild.roles[-1], inline=False)
    embed2.add_field(name="Contributers:", value="None")

    embed2.add_field(name="Number of roles", value=str(role_count), inline=False)
    embed2.add_field(
        name="Number Of Members", value=ctx.guild.member_count, inline=False
    )
    embed2.add_field(
        name="Created At",
        value=ctx.guild.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
        inline=False,
    )
    embed2.set_thumbnail(url=ctx.guild.icon_url)
    embed2.set_author(name=ctx.author.name)
    embed2.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.guild.icon_url)

    await ctx.send(embed=embed2)


# whois
@client.command(name="whois")
async def whois(ctx, user: discord.Member = None):

    if not user:
        user = ctx.author

    rlist = []
    for role in user.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = discord.Embed(colour=embedColor, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar_url),
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=user.id, inline=False)
    embed.add_field(name="Name:", value=user.display_name, inline=False)

    embed.add_field(name="Account Created at:", value=user.created_at, inline=False)
    embed.add_field(name="Server Joined at:", value=user.joined_at, inline=False)

    embed.add_field(name="Bot:", value=user.bot, inline=False)

    embed.add_field(name=f"Roles:({len(rlist)})", value="".join([b]), inline=False)
    embed.add_field(name="Top Role:", value=user.top_role.mention, inline=False)

    await ctx.send(embed=embed)


@client.command(aliases=["ul"])
async def updatelist(ctx):
    em = discord.Embed(
        title=f"Update list from `v1.4.0` to {ver}",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.add_field(
        name=f"Changes: `1.4.0`",
        value="\n1. Added random api for `sus` and `wide` `meme` commands.",
    )
    em.add_field(
        name=f"Changes: 1.4.1",
        value="\n1. Added `say` command to slash! 2. Added `listcmds` for devs and server admins!",
    )
    em.add_field(
        name=f"Changes: 1.5.0",
        value="\nAdded: `gayrate`, `ppsize`, `afk` and `removeafk` commands and reworked them from `KrypticRG™️ v3.6.2`",
    )
    em.add_field(
        name=f"Changes: `1.5.1`",
        value="\n1. Added: Overhaul to `.help` menu, new embed color and new thumbnail, buttons to be added soon. (Delay due to server issues)",
    )
    em.add_field(
        name=f"Changes: `1.5.2`",
        value="\n1. Thumbnail Changes: Added permanent thumbnail links so that thumbnails wont dissappear over time)",
    )
    em.add_field(
        name=f"Changes: `1.5.3`",
        value="\n1. Fixed commands like `.whois`, `.avatar`, `.serverinfo` and `.servericon` to work again The new api version discord 2.0 made this commands unusable, from the previous versions, which i made a fix for.",
    )
    em.add_field(
        name=f"Changes: `1.5.4` (Alerts update)",
        value="\n⚠️ Slash Commands have been removed in version `1.4.5` because of server incompatiblility. ⚠️ Buttons functionality removed in version `1.5.1` because of server incompatiblility.",
    )
    em.add_field(
        name=f"Changes: `1.5.5`",
        value="\n1. Added: New Profile picture for the bot!, Added new `.socials` command!",
    )
    em.add_field(
        name=f"Changes: `1.5.6` (LWU)",
        value="\n1. Added: New news command! ⚠️ LWU: Last Winter Update",
    )
    em.add_field(
        name=f"Changes: `1.6.0` (Math update)",
        value="\n1. Added new images for math commands. Added new `root` and `pow` commands.",
    )
    em.add_field(
        name=f"Changes: `1.6.1`",
        value="\n1. Fixed the `.mute` command. Previously the mute command used to generate more than one `🔇|Muted` role and the mute functionality did not work. Both these bugs have been fixed!",
    )
    em.add_field(
        name=f"Changes: `1.6.2`",
        value="\n1. Added `.updatelist` command or `.ul` that shows all updates to the bot",
    )
    em.add_field(
        name=f"Changes: `1.6.3`",
        value="\n1. Added: `.set_welcome` for server owners, now an embed will be sent for every new member joining a server",
    )
    em.add_field(
        name=f"Changes: `1.7.0 Beta`",
        value="\nAdded: 1. `.prompt` command that gives you detailed info on a topic\n2. Added new 3d assets to kryptic, Added new embed color\n 3. Added embeds to news command and made it better\n4. UI improvements for kryptic done!",
    )
    em.set_thumbnail(url="https://i.postimg.cc/YSn7DHS8/version.png")
    em.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=em)


# changelog
@client.command(aliases=["chl"])
async def changelog(ctx):
    em = discord.Embed(
        title=f"Changelog of `{ver}`", color=embedColor, timestamp=ctx.message.created_at
    )
    em.add_field(
        name=f"Changes:",
        value="\n\n**Added: **\n\n1. `.prompt` command that gives you detailed info on a topic\n2. Added new 3d assets to kryptic, Added new embed color\n 3. Added embeds to news command and made it better\n4. UI improvements for kryptic done!",
    )
    em.add_field(
        name=f"Planned updates:",
        value="\n\n**Going to add: **\n\n1. New ai system\n2. Buttons and slash commands.",
    )
    em.set_thumbnail(url="https://i.postimg.cc/YSn7DHS8/version.png")
    em.set_image(url="https://i.postimg.cc/rFx8V3hF/thumbnail.png")
    em.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=em)


# about
@client.command(aliases=["abt"])
async def about(ctx):
    em = discord.Embed(
        title="About me!",
        description="Nice to see you wanted to hear more, lets look at my stats!",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )

    em.add_field(name="Version", value=f"`{ver}`")
    em.add_field(name="Main Server", value="[Support:](https://discord.gg/jA34s8Zwtr)")
    em.add_field(name="Invite Link", value="[Click here:](https://dsc.gg/krypticgg)")
    em.add_field(
        name="Copyright",
        value="[Click here:](https://www.copyrighted.com/work/b5LQCsHu5EcxDDZc)",
    )
    em.add_field(
        name="Upvote",
        value="[Top.gg](https://top.gg/bot/822074775483711488)\n[DBL](https://discordbotlist.com/bots/kryptic)",
    )
    em.add_field(name="Ping", value=f"{round(client.latency * 1000)}ms")
    em.set_author(
        name="Owner: ar im.",
        url="https://www.instagram.com/abdul.__.r",
        icon_url="https://i.postimg.cc/LXCqNbzt/pfp.jpg",
    )
    em.set_image(url="https://i.postimg.cc/rFx8V3hF/thumbnail.png")
    em.set_thumbnail(url="https://i.postimg.cc/YSn7DHS8/version.png")
    user = ctx.author
    em.set_footer(text=f"Reqested by {ctx.author}", icon_url=user.avatar_url)

    await ctx.send(embed=em)

# cp-info
@client.command(aliases=["cp", "cpr"])
async def copyright(ctx):
    await ctx.send("https://www.copyrighted.com/work/b5LQCsHu5EcxDDZc")


@client.command(pass_context=True)
async def vote(ctx):
    em = discord.Embed(
        title="⬆️ | Upvote!",
        description="[Discord Bot List](https://discordbotlist.com/bots/kryptic)\n[Top.gg](https://top.gg/bot/822074775483711488)",
        color=embedColor,
    )
    em.set_footer(text=f"Requested by: {ctx.author}")
    await ctx.send(embed=em)


# avatar
@client.command(aliases=["av"])
async def avatar(ctx, *, avamember: discord.Member = None):
    if not avamember:
        avamember = ctx.author
    userAvatarUrl = avamember.avatar_url
    em = discord.Embed(
        title=f"Avatar of {avamember}",
        description="",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.set_image(url=userAvatarUrl)
    em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=em)


@client.event
async def on_guild_join(guild):
    welcome_channels[guild.id] = None


@client.command()
async def set_welcome(ctx, channel: discord.TextChannel):
    if ctx.author.guild_permissions.manage_channels and ctx.author == ctx.guild.owner:
        welcome_channels[ctx.guild.id] = channel.id
        await ctx.send(f"Welcome channel set to {channel.mention}")
    else:
        await ctx.send("You don't have permission to set the welcome channel.")


@client.event
async def on_member_join(member):
    welcome_channel_id = welcome_channels.get(member.guild.id)
    if welcome_channel_id:
        welcome_channel = client.get_channel(welcome_channel_id)
        welcome_message = discord.Embed(
            title="👤 | New server member: ",
            description=f"{member.mention} Has joined the server",
            color=embedColor,
        )
        welcome_message.set_thumbnail(url="https://i.postimg.cc/YSjZ9mpf/user.png")
        await welcome_channel.send(embed=welcome_message)


@client.command()
async def poll(ctx, question, option1=None, option2=None):
    if option1 == None and option2 == None:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title="New poll:",
            description=f"{question} \n \n**✅ = {option1}**\n**❎ = {option2}**",
            color=embedColor,
            timestamp=ctx.message.created_at,
        )
        em.set_footer(text=f"Requested by {ctx.author}")
        message = await ctx.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❎")
    elif option1 == None:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title="New poll:",
            description=f"{question} \n \n**✅ = {option1}**\n**❎ = {option2}**",
            color=embedColor,
            timestamp=ctx.message.created_at,
        )
        em.set_footer(text=f"Requested by {ctx.author}")
        message = await ctx.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❎")
    elif option2 == None:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title="New poll:",
            description=f"{question} \n \n**✅ = {option1}**\n**❎ = {option2}**",
            color=embedColor,
            timestamp=ctx.message.created_at,
        )
        em.set_footer(text=f"Requested by {ctx.author}")
        message = await ctx.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❎")
    else:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title="New poll:",
            description=f"{question} \n \n**✅ = {option1}**\n**❎ = {option2}**",
            color=embedColor,
            timestamp=ctx.message.created_at,
        )
        em.set_footer(text=f"Requested by {ctx.author}")
        message = await ctx.send(embed=em)
        await message.add_reaction("✅")
        await message.add_reaction("❎")


# kill
@client.command()
async def kill(ctx, *, member: discord.Member = None):

    responses = [
        "got burnt to a crisp 🔥",
        "got stabbed about 69 times 😳",
        "was too soft to handle this command 😔",
        "dies with constipation 💩",
        "dies with a sus face",
        "got squashed by the rock 🪨",
        "never existed, lol",
        "got farted to death 😮‍💨" "died. yea he just died 😀",
        "got ||kissed|| to death 💋",
        "had ||sex|| with a dragon 🐲",
        "started to be vegan, and died because of it 🌱",
    ]

    em = discord.Embed(
        title=f"You killed {member}",
        description=f"{member.mention} {random.choice(responses)}",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.set_footer(text=f"Requested by {ctx.author}")
    em.set_thumbnail(url="https://i.postimg.cc/QdjrXt90/kill.png")
    await ctx.send(embed=em)

# 8ball
@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):

    responses = [
        "It is certain",
        "Outlook good",
        "You may rely on it",
        "Ask again later",
        "Concentrate and ask again",
        "Reply hazy, try again",
        "My reply is no",
        "My sources say no",
        "Without a doubt",
        "Very doubtful",
        "Cannot predict now",
        "Go ask someone else :)",
        "U basically suck for asking me this question lol!",
        "amang as ඞ",
    ]

    em = discord.Embed(
        title="8ball",
        description=(f"🎱 Question: {question}  |  Answer: {random.choice(responses)}"),
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/sxCNw65w/8ball.png")
    await ctx.send(embed=em)


# clear
@client.command(aliases=["clr"])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    em = discord.Embed(
        title="❌ | Permissions Error",
        description="You must be an **Administrator** to use this command",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/3RsPzJQj/kick.png")
    if commands.has_permissions(administrator=True):
        pass
    else:
        await ctx.send(embed=em)


# kick
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    em = discord.Embed(
        title="Member Kicked",
        description=f"{member} has been kicked from the server \n for reason: {reason}",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/3RsPzJQj/kick.png")
    await ctx.send(embed=em)


# ban
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    em = discord.Embed(
        title="Member Banned",
        description=f"{member} has been banned from the server",
        color=embedColor,
    )
    em.set_thumbnail(url="https://i.postimg.cc/50FY7zRn/hammer.png")
    await ctx.send(embed=em)


# say
@client.command()
async def say(ctx, *, text):
    em = discord.Embed(title="", description=text, color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/fbTZvLMJ/logo.png")
    await ctx.send(embed=em)


# Hi
@client.command()
async def hi(ctx):
    em = discord.Embed(
        title="Hi there!",
        description="Hi there, always ready to help! TYPE: `.help` for usage.",
        color=embedColor,
    )
    await ctx.send(embed=em)


# ShortForms
@client.command(aliases=["short", "shorts", "shrt", "sh"])
async def shortforms(ctx):
    em = discord.Embed(
        title="Shortforms:",
        description=f"Here are all the short forms of the bot as per update `{ver}`",
        color=embedColor,
    )
    em.add_field(
        name="Util",
        value="Avatar = `av`, BoostCount = `bc`, ShortForms = `sh`, Changelog = `chl`, Membercount = `mc`, ServerInfo = `si`, Server Icon = `sicon`, Server Roles = `sr`, removeafk = `rafk`",
    )
    em.add_field(
        name="Bot Info",
        value="Commands = `cmds`, Invite = `invi`, Copyright = `cp`, About = `abt`, Version = `ver`, Credits = `cre`, updatelist = `ul`",
    )
    em.add_field(
        name="Moderation",
        value="Clear = `clr`, RemoveChannel = rch, addrole = `arole`, removerole = `rrole`",
    )

    em.set_thumbnail(url="https://i.postimg.cc/YSn7DHS8/version.png")
    await ctx.send(embed=em)


# Credits
@client.command(aliases=["cre"])
async def credits(ctx):
    em = discord.Embed(title="Credits - Kryptic ™️", description="", color=embedColor)
    em.add_field(name="Owner", value="ar im.#3865")
    em.add_field(name="Server", value="RapidG™️")
    em.add_field(name="Copyright", value="https://copyrighted.com")
    em.add_field(name="Inspiration", value="Eternos Bot, made by Phantomヅ#3132")
    em.add_field(name="Coding Section", value="VS Code, Python V3.10, Discord Module")
    em.add_field(name="Links", value="discord.com, dsc.gg, bit.ly")

    em.add_field(name="Invite link for Kryptic", value="https://dsc.gg/krypticgg")
    em.add_field(name="Invite link for Eternos", value="https://dsc.gg/eternosguild")

    await ctx.send(embed=em)


# Adding
@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    em = discord.Embed(title="Addition", description=left + right, color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/K8GC6HwW/math.png")
    await ctx.send(embed=em)


# Subtracting
@client.command()
async def sub(ctx, left: int, right: int):
    """Subs two numbers together."""
    em = discord.Embed(title="Subtraction", description=left - right, color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/K8GC6HwW/math.png")
    await ctx.send(embed=em)


# Multi
@client.command()
async def multi(ctx, left: int, right: int):
    """multi two numbers together."""
    em = discord.Embed(title="Multiplication", description=left * right, color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/K8GC6HwW/math.png")
    await ctx.send(embed=em)


# Div
@client.command()
async def div(ctx, left: int, right: int):
    """multi two numbers together."""
    em = discord.Embed(title="Division", description=left / right, color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/K8GC6HwW/math.png")
    await ctx.send(embed=em)


# Root
@client.command()
async def root(ctx, num: int):
    em = discord.Embed(title="Square root", description=math.sqrt(num), color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/K8GC6HwW/math.png")
    await ctx.send(embed=em)


# Pow
@client.command()
async def pow(ctx, num: int, pow: int):
    em = discord.Embed(title="Power", description=math.pow(num, pow), color=embedColor)
    em.set_thumbnail(url="https://i.postimg.cc/K8GC6HwW/math.png")
    await ctx.send(embed=em)


# Invite
@client.command()
async def invite(
    ctx,
):
    em = discord.Embed(
        title="🔗 | Invite",
        description="[Invite](https://dsc.gg/krypticgg)",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.set_thumbnail(url="https://i.postimg.cc/rFx8V3hF/thumbnail.png")
    em.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=em)


@client.command()
async def links(
    ctx,
):
    em = discord.Embed(
        title="🔗 | Useful Links",
        description="[Invite](https://dsc.gg/krypticgg)\n[Support](https://discord.gg/jA34s8Zwtr)",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.set_footer(text=f"Requested by {ctx.author.name}")
    em.set_thumbnail(url="https://i.postimg.cc/rFx8V3hF/thumbnail.png")
    await ctx.send(embed=em)


@client.command()
async def socials(
    ctx,
):
    em = discord.Embed(
        title="🔗 | Socials",
        description="[Invite](https://dsc.gg/krypticgg)\n[Support](https://discord.gg/jA34s8Zwtr)\n[Instagram](https://www.instagram.com/abdul.__.r/)\n[Twitter](https://twitter.com/AR_tveeter)\n[All Links](https://linktr.ee/ar.im)",
        color=embedColor,
        timestamp=ctx.message.created_at,
    )
    em.set_footer(text=f"Requested by {ctx.author.name}")
    em.set_thumbnail(url="https://i.postimg.cc/rFx8V3hF/thumbnail.png")
    await ctx.send(embed=em)

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
