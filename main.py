import discord
import random
from discord.ext import commands
import os
import discord.utils
from webserver import keep_alive
import asyncio
import datetime
import aiohttp
import math

global ver
ver = '`v1.6.2`'

intents = discord.Intents().all()

client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')


#bot ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game('.help'))
    print(f'Init Completed! ✅\nLogged in as: Kryptic #1648\nVersion: {ver} 🤖')


member = ()


@client.command(pass_context=True)
async def news(ctx):
    embed = discord.Embed(title="", description="")
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/news/new.json') as r:
            res = await r.json()
            embed = discord.Embed(
                color=0xff006a,
                title='Reddit: `r/news`',
                description=res['data']['children'][random.randint(
                    0, 25)]['data']['url'])
            embed.set_footer(text='The news is sourced from `r/news`')
            embed.set_author(
                name='reddit.com',
                url='https://reddit.com',
                icon_url='https://i.postimg.cc/fRNx315y/pngwing-com.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')


@client.command()
async def truth(ctx):

    truthResponses = [
        'When was the last time you lied?',
        'When was the last time you cried?', 'What is your biggest fear?',
        'What is something you are glad your mum does not know about you?',
        'Have you ever cheated on someone?',
        'What is the worst thing you have ever done?'
    ]

    truthem = discord.Embed(
        title=f'Truth',
        description=f'Truth: {random.choice(truthResponses)}',
        color=0xff006a,
        timestamp=ctx.message.created_at)
    truthem.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=truthem)


@client.command()
async def dare(ctx):

    dareResponses = [
        'Show the most embarrassing photo on your phone',
        'Show the last five people you texted and what the messages said',
        'Do 100 squats', 'Say something dirty to a person',
        'Twerk for a minute', 'Try to lick your elbow'
    ]

    darem = discord.Embed(title=f'Dare',
                          description=f'Dare: {random.choice(dareResponses)}',
                          color=0xff006a,
                          timestamp=ctx.message.created_at)
    darem.set_footer(text=f'Requested by {ctx.author}')

    await ctx.send(embed=darem)


@commands.has_permissions(administrator=True)
@client.command()
async def servers(ctx):
    for guild in client.guilds:
        em = discord.Embed(title='📑 | Bot Servers',
                           description=f'{guild.name}',
                           color=0xff006a)
        await ctx.send(embed=em)
        print(guild.name)


@client.command(aliases=['scount'])
async def servercount(ctx):
    em = discord.Embed(title='Server Count',
                       description=f"I'm in " + str(len(client.guilds)) +
                       " servers!",
                       color=0xff006a)
    await ctx.send(embed=em)


@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json') as r:
            res = await r.json()
            embed = discord.Embed(color=0xff006a,
                                  title='Reddit: `r/dankmemes`')
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                            ['data']['url'])
            embed.set_footer(
                text=
                'We are not responsible for the memes posted (visit reddit.com for help)'
            )
            embed.set_author(
                name='reddit.com',
                url='https://reddit.com',
                icon_url='https://i.postimg.cc/fRNx315y/pngwing-com.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('⬆️')
            await msg.add_reaction('⬇️')


@client.command(pass_context=True)
async def tits(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/tits/new.json') as r:
            res = await r.json()
            embed = discord.Embed(color=0xff006a,
                                  title='Reddit: `r/dankmemes`')
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                            ['data']['url'])
            embed.set_footer(
                text=
                'We are not responsible for the memes posted (visit reddit.com for help)'
            )
            embed.set_author(
                name='reddit.com',
                url='https://www.reddit.com/r/tits/',
                icon_url='https://i.postimg.cc/fRNx315y/pngwing-com.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('⬆️')
            await msg.add_reaction('⬇️')


#wrongcommand
@client.event
async def on_command_error(context, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        em = discord.Embed(
            title='❌ Wrong Command!',
            description=
            'Oh no! Looks like you have entered a wrong command, use `.help` to get to know all of my commands!',
            color=0xff006a)
        await context.send(embed=em)


intents = discord.Intents.default()
intents.members = True


@client.command()
async def afk(ctx, reason):
    em = discord.Embed(
        title='🛏️ | AFK',
        description=
        f'Status: {ctx.author.mention} is now AFK\nReason: \'{reason}\'',
        color=0xff006a)
    await ctx.send(embed=em)
    await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")


@client.command(aliases=['rafk'])
async def removeafk(ctx):
    em = discord.Embed(title='🛏️ | AFK Removed',
                       description=f'Your afk was removed 👋',
                       color=0xff006a)
    await ctx.send(embed=em)
    await ctx.author.edit(nick=f"{ctx.author.name}")


@client.command()
async def gayrate(ctx, user: discord.Member = None):
    if not user:
        user = ctx.message.author
    em = discord.Embed(
        title='Gayrate Machine 🏳️‍🌈',
        description=f"{user.mention} is {random.randint(0,100)}% gay",
        color=0xff006a)
    em.set_footer(text=f'Requested by: {ctx.author}')
    await ctx.send(embed=em)


@client.command()
async def ppsize(ctx, user: discord.Member = None):

    pp_sizes = [
        '8D', '8=D', '8==D', '8===D', '8====D', '8=====D', '8=========D',
        '8==========D', '8===========D', '8=================D',
        '8=============================================================D'
    ]
    if not user:
        user = ctx.message.author

    em = discord.Embed(
        title='pp Rate 🖊️',
        description=f"{user.mention}'s pp size is `{random.choice(pp_sizes)}`",
        color=0xff006a)
    await ctx.send(embed=em)


@client.command(pass_context=True)
async def ticket(ctx):
    guild = ctx.guild
    embed = discord.Embed(title='Ticket system',
                          description='React 📩 to make a ticket.',
                          color=0xff006a)

    embed.set_footer(text=f"Requested by {ctx.author.name}")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")

    await client.wait_for("reaction_add")
    await client.wait_for("reaction_add")

    await guild.create_text_channel(name=f'ticket-{ctx.author.name}')


#removechannel
@client.command(aliases=['rch'])
@commands.has_permissions(administrator=True)
async def removechannel(ctx, channel: discord.TextChannel):
    await channel.delete()


@client.command(aliases=['al'])
async def alerts(ctx):
    embed = discord.Embed(
        title='Alerts',
        description=
        '⚠️ Slash Commands have been removed in version `1.4.5` because of server incompatiblility.\n⚠️ Buttons functionality removed in version `1.5.1` because of server incompatiblility.\n⚠️ Winter break has started. Ends at 2nd Jan 2023 (`Done`)',
        color=0xff006a,
        timestamp=ctx.message.created_at)
    embed.set_thumbnail(url='https://i.postimg.cc/fRYS19w0/alert.png')
    embed.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)


@client.command()
async def dice(ctx):

    diceR = ['1', '2', '3', '4', '5', '6']

    dicem = discord.Embed(title=f'🎲 | Dice is Rolling....',
                          description=f'Rolled: {random.choice(diceR)}',
                          color=0xff006a,
                          timestamp=ctx.message.created_at)
    dicem.set_thumbnail(url='https://i.postimg.cc/28wNbLtQ/dice.png')
    dicem.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=dicem)


@client.command()
async def flip(ctx):

    flipR = ['Heads', 'Tails']

    flipem = discord.Embed(title=f'🪙 | Flipping coin....',
                           description=f'Flipped as: {random.choice(flipR)}',
                           color=0xff006a,
                           timestamp=ctx.message.created_at)
    flipem.set_thumbnail(url='https://i.postimg.cc/WbQgZtJ4/coin.png')
    flipem.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=flipem)


@client.command(pass_context=True, aliases=['tclose'])
@commands.has_permissions(administrator=True)
@commands.has_any_role('📩| Ticket Issue')
async def ticketclose(ctx):
    embed = discord.Embed(title='Ticket system',
                          description='React 📩 close this ticket',
                          color=0xff006a)

    embed.set_footer(text=f"Requested by {ctx.author.name}")

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")

    await client.wait_for("reaction_add")
    await client.wait_for("reaction_add")

    if ctx.channel.name == 'ticket':
        await ctx.channel.delete()


@client.command(aliases=['lc'])
@commands.has_permissions(administrator=True)
async def listcmds(ctx):
    helptext = "```"
    for command in client.commands:
        helptext += f"{command}\n"
    helptext += "```"
    em = discord.Embed(title='Listing all commands',
                       description=f'{helptext}',
                       color=0xff006a)
    await ctx.send(embed=em)


@client.command()
@commands.has_permissions(administrator=True)
async def cmds(ctx):
    userEm = discord.Embed(
        title='Commands',
        description='Here are the available commands! Do have a look.',
        color=0xff006a)

    userEm.add_field(
        name='Fun',
        value=
        "`8ball`, `say`, `kill`, `poll`, `giveaway`, `meme`, `truth` , `dare`, `flip`, `dice`, `gayrate`, `ppsize`, `afk`, `removeafk` |     "
    )
    userEm.add_field(
        name='Moderation',
        value=
        "`kick`, `ban`, `clear`, `removerole`, `removechannel`, `mute`, `unmute`, `lock`, `unlock` |      "
    )
    userEm.add_field(
        name='Bot Info',
        value=
        "`commands`, `ping`, `invite`, `about`, `copyright`, `version`, `credits`, `license`, `vote`, `links`, `socials`, `updatelist` |"
    )
    userEm.add_field(name='Memes', value="`heheboi`, `baka`, `sus`, `wide` |")
    userEm.add_field(name='Calculating',
                     value="`multi`, `div`, `add`, `sub`, `root`, `pow` |")
    userEm.add_field(
        name='Util',
        value=
        '`boostcount`, `avatar`, `shortforms`, `changelog`, `membercount`, `whois`, `serverinfo`, `alerts`, `news` |'
    )

    await ctx.send(embed=userEm)


#help response
@client.command()
async def help(ctx):
    em = discord.Embed(
        title='✅ React to get help!',
        description=
        'React to the following embed to get a DM on the bot\'s commands',
        color=0x2f3136)
    em.set_thumbnail(url='https://i.postimg.cc/K8M4hNjG/tick.png')

    msg = await ctx.send(embed=em)

    await msg.add_reaction('✅')

    await client.wait_for("reaction_add")

    userEm = discord.Embed(
        title='Commands',
        description='Here are the available commands! Do have a look.',
        color=0x2f3136)

    userEm.add_field(
        name='Fun',
        value=
        "`8ball`, `say`, `roll`, `kill`, `poll`, `giveaway`, `meme`, `truth`, `dare`, `flip`, `dice` |     "
    )
    userEm.add_field(name='Moderation', value="`kick`, `ban`, `clear` |      ")
    userEm.add_field(
        name='Bot Info',
        value=
        "`commands`, `ping`, `invite`, `about`, `copyright`, `version`, `credits`, `license`, `vote`, `links`, `socials`, `updatelist` |"
    )
    userEm.add_field(name='Memes', value="`heheboi`, `baka`, `sus`, `wide` |")
    userEm.add_field(name='Calculating',
                     value="`multi`, `div`, `add`, `sub`, `root`, `pow` |")
    userEm.add_field(
        name='Util',
        value=
        '`boostcount`, `avatar`, `shortforms`, `changelog`, `membercount`, `whois`, `serverinfo`, `alerts`, `news` |'
    )

    user = ctx.author
    await user.send(embed=userEm)


#prefix
@client.command()
async def prefix(ctx):
    em = discord.Embed(title='⚡Server Prefix',
                       description='My prefix here is, `.`',
                       color=0x2f3136)
    await ctx.send(embed=em)


@client.command()
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=False)
    em = discord.Embed(title='🔒Locked',
                       description=ctx.channel.mention +
                       " ***is now in lockdown.***",
                       color=0xff006a)
    await ctx.send(embed=em)


@client.command()
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,
                                      send_messages=True)
    em = discord.Embed(title='🔓Unlocked',
                       description=ctx.channel.mention +
                       " ***is now unlocked.***",
                       color=0xff006a)
    await ctx.send(embed=em)


#servericon
@client.command(aliases=['sicon'])
async def servericon(ctx):
    serverName = ctx.guild.name
    serverIcon = ctx.guild.icon.url
    em = discord.Embed(title=serverName + "'s Icon:",
                       description='',
                       color=0xff006a)
    em.set_image(url=serverIcon)
    em.set_footer(text=f'Requested by {ctx.author}')

    await ctx.send(embed=em)


#listroles
@client.command(aliases=['sr'])
async def listroles(ctx):
    rlist = []
    for role in ctx.guild.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)
    server = ctx.guild.name

    em = discord.Embed(title=server + "'s Roles:",
                       description=", ".join([b]),
                       color=0xff006a)
    await ctx.send(embed=em)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, user: discord.Member):
    guild = ctx.guild
    role = discord.utils.get(ctx.guild.roles, name="🔇|Muted")

    if not role:
        perms = discord.Permissions(send_messages=False, read_messages=True)
        role = await guild.create_role(name="🔇|Muted",
                                       colour=discord.Colour(0xff006a),
                                       permissions=perms)

    for channel in guild.text_channels:
        await channel.set_permissions(role, send_messages=False)

    em = discord.Embed(
        title='🔇 Member muted',
        description=f'{user.mention} has been muted | {role.mention}',
        color=0xff006a)
    await user.add_roles(role)
    await ctx.send(embed=em)


#unmute
@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="🔇|Muted")
    em = discord.Embed(
        title='🔈Member unmuted',
        description=f'{user.mention} has been unmuted | {role.mention}',
        color=0xff006a)
    await user.remove_roles(role)
    await ctx.send(embed=em)


@client.command(aliases=['arole'])
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member, *, role: discord.Role = None):
    em = discord.Embed(
        title='Role Added!',
        description=f'{user.mention} has been assigned the role {role.mention}',
        color=0xff006a)
    await user.add_roles(role)
    await ctx.send(embed=em)


@client.command(aliases=['rrole'])
@commands.has_permissions(administrator=True)
async def removerole(ctx, user: discord.Member, *, role: discord.Role = None):
    em = discord.Embed(
        title='Role Removed!',
        description=
        f'{user.mention} has been dismissed the role {role.mention}',
        color=0xff006a)
    await user.remove_roles(role)
    await ctx.send(embed=em)


#giveaway
@client.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly

    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = [
        'Which channel will I host the giveaway in?',
        'What is the prize?',
        'How long should the giveaway run for (in seconds)?',
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
            message = await client.wait_for('message',
                                            timeout=30.0,
                                            check=check)
        except asyncio.TimeoutError:
            await ctx.send(
                'You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.'
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
            f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}'
        )
        return

    # Storing the variables needed to run the rest of the commands
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(
        f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.'
    )

    # Giveaway embed message
    give = discord.Embed(color=0xff006a)
    give.set_author(name=f'🥳 GIVEAWAY TIME!')
    give.add_field(
        name=f'{ctx.author.name} is giving away: {prize}!',
        value=f'React with 🎉 to enter!\n Ends in {round(time/60, 2)} minutes!',
        inline=False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
    give.set_footer(text=f'Giveaway ends at {end} UTC!')
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
    winning_announcement = discord.Embed(color=0xff006a)
    winning_announcement.set_author(name=f'THE GIVEAWAY HAS ENDED!',
                                    icon_url='https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(
        name=f'🎉 Prize: {prize}',
        value=
        f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}',
        inline=False)
    winning_announcement.set_footer(text='Thanks for entering!')
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
    reroll_announcement = discord.Embed(color=0xff006a)
    reroll_announcement.set_author(
        name=f'The giveaway was re-rolled by the host!',
        icon_url='https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name=f'🥳 New Winner:',
                                  value=f'{winner.mention}',
                                  inline=False)
    await channel.send(embed=reroll_announcement)


#boostcount
@client.command(aliases=['bc'])
async def boostcount(ctx):
    embed = discord.Embed(
        title=f'{ctx.guild.name}\'s Boost Count',
        description=f'{str(ctx.guild.premium_subscription_count)} boosts',
        color=0xff006a)
    await ctx.send(embed=embed)


#ping
@client.command()
async def ping(ctx):
    em = discord.Embed(title='Ping',
                       description=f'Pong! {round(client.latency * 1000)}ms',
                       color=0xff006a)
    await ctx.send(embed=em)


#version
@client.command(aliases=['ver'])
async def version(ctx):
    em = discord.Embed(title='Version', description=f'`{ver}`', color=0xff006a)
    em.set_thumbnail(url='https://i.postimg.cc/SRhJgzkS/logo-modified.png')

    await ctx.send(embed=em)


#license
@client.command(aliases=['li'])
async def license(ctx):
    em = discord.Embed(
        title='MIT license',
        description=
        f'MIT License \n\n Copyright 2023 AR ©️ \n\n Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files, to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. \n \n THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
        color=0xff006a)
    await ctx.send(embed=em)


#membercount
@client.command(aliases=['mc'])
async def membercount(ctx):
    memberCount = str(ctx.guild.member_count)
    name = str(ctx.guild.name)
    em = discord.Embed(color=0xff006a,
                       timestamp=ctx.message.created_at,
                       title=name + "'s Members",
                       description=f'{memberCount}')
    em.set_footer(text=f'Requested by {ctx.author}')

    await ctx.send(embed=em)


#serverinfo
@client.command(aliases=['si'])
async def serverinfo(ctx):

    role_count = len(ctx.guild.roles)

    embed2 = discord.Embed(timestamp=ctx.message.created_at, color=0xff006a)
    embed2.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
    embed2.add_field(name='Owner', value=f"ar im.", inline=False)
    embed2.add_field(name='Verification Level',
                     value=str(ctx.guild.verification_level),
                     inline=False)
    embed2.add_field(name='Highest role',
                     value=ctx.guild.roles[-1],
                     inline=False)
    embed2.add_field(name='Contributers:', value="None")

    embed2.add_field(name='Number of roles',
                     value=str(role_count),
                     inline=False)
    embed2.add_field(name='Number Of Members',
                     value=ctx.guild.member_count,
                     inline=False)
    embed2.add_field(
        name='Created At',
        value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'),
        inline=False)
    embed2.set_thumbnail(url=ctx.guild.icon.url)
    embed2.set_author(name=ctx.author.name)
    embed2.set_footer(text=f'Requested by - {ctx.author}',
                      icon_url=ctx.guild.icon.url)

    await ctx.send(embed=embed2)


#whois
@client.command(name="whois")
async def whois(ctx, user: discord.Member = None):

    if not user:
        user = ctx.author

    rlist = []
    for role in user.roles:
        if role.name != "@everyone":
            rlist.append(role.mention)

    b = ", ".join(rlist)

    embed = discord.Embed(colour=0xff006a, timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {user}"),
    embed.set_thumbnail(url=user.avatar.url),
    embed.set_footer(text=f'Requested by {ctx.author}')

    embed.add_field(name='ID:', value=user.id, inline=False)
    embed.add_field(name='Name:', value=user.display_name, inline=False)

    embed.add_field(name='Account Created at:',
                    value=user.created_at,
                    inline=False)
    embed.add_field(name='Server Joined at:',
                    value=user.joined_at,
                    inline=False)

    embed.add_field(name='Bot:', value=user.bot, inline=False)

    embed.add_field(name=f'Roles:({len(rlist)})',
                    value=''.join([b]),
                    inline=False)
    embed.add_field(name='Top Role:',
                    value=user.top_role.mention,
                    inline=False)

    await ctx.send(embed=embed)


@client.command(aliases=['ul'])
async def updatelist(ctx):
    em = discord.Embed(title=f'Update list from `v1.4.0` to {ver}',
                       color=0xff006a,
                       timestamp=ctx.message.created_at)
    em.add_field(
        name=f'Changes: `1.4.0`',
        value='\n1. Added random api for `sus` and `wide` `meme` commands.')
    em.add_field(
        name=f'Changes: 1.4.1',
        value=
        '\n1. Added `say` command to slash! 2. Added `listcmds` for devs and server admins!'
    )
    em.add_field(
        name=f'Changes: 1.5.0',
        value=
        '\nAdded: `gayrate`, `ppsize`, `afk` and `removeafk` commands and reworked them from `KrypticRG™️ v3.6.2`'
    )
    em.add_field(
        name=f'Changes: `1.5.1`',
        value=
        '\n1. Added: Overhaul to `.help` menu, new embed color and new thumbnail, buttons to be added soon. (Delay due to server issues)'
    )
    em.add_field(
        name=f'Changes: `1.5.2`',
        value=
        '\n1. Thumbnail Changes: Added permanent thumbnail links so that thumbnails wont dissappear over time)'
    )
    em.add_field(
        name=f'Changes: `1.5.3`',
        value=
        '\n1. Fixed commands like `.whois`, `.avatar`, `.serverinfo` and `.servericon` to work again The new api version discord 2.0 made this commands unusable, from the previous versions, which i made a fix for.'
    )
    em.add_field(
        name=f'Changes: `1.5.4` (Alerts update)',
        value=
        '\n⚠️ Slash Commands have been removed in version `1.4.5` because of server incompatiblility. ⚠️ Buttons functionality removed in version `1.5.1` because of server incompatiblility.'
    )
    em.add_field(
        name=f'Changes: `1.5.5`',
        value=
        '\n1. Added: New Profile picture for the bot!, Added new `.socials` command!'
    )
    em.add_field(
        name=f'Changes: `1.5.6` (LWU)',
        value='\n1. Added: New news command! ⚠️ LWU: Last Winter Update')
    em.add_field(
        name=f'Changes: `1.6.0` (Math update)',
        value=
        '\n1. Added new images for math commands. Added new `root` and `pow` commands.'
    )
    em.add_field(
        name=f'Changes: `1.6.1`',
        value=
        '\n1. Fixed the `.mute` command. Previously the mute command used to generate more than one `🔇|Muted` role and the mute functionality did not work. Both these bugs have been fixed!'
    )
    em.add_field(
        name=f'Changes: `1.6.2`',
        value=
        '\n1. Added `.updatelist` command or `.ul` that shows all updates to the bot'
    )
    em.set_thumbnail(url='https://i.postimg.cc/SRhJgzkS/logo-modified.png')
    em.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=em)


#changelog
@client.command(aliases=['chl'])
async def changelog(ctx):
    em = discord.Embed(title=f'Changelog of `{ver}`',
                       color=0xff006a,
                       timestamp=ctx.message.created_at)
    em.add_field(
        name=f'Changes:',
        value=
        '\n\n**Added: **\n\n1. `.updatelist` command or `.ul` that shows all updates to the bot'
    )
    em.set_thumbnail(url='https://i.postimg.cc/SRhJgzkS/logo-modified.png')
    em.set_image(url='https://i.postimg.cc/wv8KbfYt/pfp.png')
    em.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=em)


#about
@client.command(aliases=['abt'])
async def about(ctx):
    em = discord.Embed(
        title='About me!',
        description=
        'Nice to see you wanted to hear more, lets look at my stats!',
        color=0xff006a,
        timestamp=ctx.message.created_at)

    em.add_field(name='Version', value=f'`{ver}`')
    em.add_field(name='Main Server',
                 value="[Support:](https://discord.gg/jA34s8Zwtr)")
    em.add_field(name='Invite Link',
                 value="[Click here:](https://dsc.gg/krypticgg)")
    em.add_field(
        name='Copyright',
        value="[Click here:](https://www.copyrighted.com/work/b5LQCsHu5EcxDDZc)"
    )
    em.add_field(
        name='Upvote',
        value=
        '[Top.gg](https://top.gg/bot/822074775483711488)\n[DBL](https://discordbotlist.com/bots/kryptic)'
    )
    em.add_field(name='Ping', value=f'{round(client.latency * 1000)}ms')
    em.set_author(name="Owner: ar im.",
                  url="https://www.instagram.com/abdul.__.r",
                  icon_url="https://i.postimg.cc/LXCqNbzt/pfp.jpg")
    em.set_image(url="https://i.postimg.cc/wv8KbfYt/pfp.png")
    em.set_thumbnail(url='https://i.postimg.cc/SRhJgzkS/logo-modified.png')
    user = ctx.author
    em.set_footer(text=f'Reqested by {ctx.author.name}',
                  icon_url=user.avatar.url)

    await ctx.send(embed=em)


@client.command(pass_context=True)
async def nsfw(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/Miakhalifa/new.json') as r:
            res = await r.json()
            embed = discord.Embed(color=0xff006a,
                                  title='Reddit: `r/Miakhalifa`')
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]
                            ['data']['url'])
            embed.set_footer(
                text=
                'We are not responsible for the memes posted (visit reddit.com for help)'
            )
            embed.set_author(
                name='reddit.com',
                url='https://reddit.com',
                icon_url='https://i.postimg.cc/fRNx315y/pngwing-com.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('⬆️')
            await msg.add_reaction('⬇️')


#cp-info
@client.command(aliases=['cp', 'cpr'])
async def copyright(ctx):
    await ctx.send('https://www.copyrighted.com/work/b5LQCsHu5EcxDDZc')


@client.command(pass_context=True)
async def vote(ctx):
    em = discord.Embed(
        title='⬆️ | Upvote!',
        description=
        '[Discord Bot List](https://discordbotlist.com/bots/kryptic)\n[Top.gg](https://top.gg/bot/822074775483711488)',
        color=0xff006a)
    em.set_footer(text=f'Requested by: {ctx.author}')
    await ctx.send(embed=em)


#avatar
@client.command(aliases=['av'])
async def avatar(ctx, *, avamember: discord.Member = None):
    if not avamember:
        avamember = ctx.author
    userAvatarUrl = avamember.avatar.url
    em = discord.Embed(title=f'Avatar of {avamember}',
                       description='',
                       color=0xff006a,
                       timestamp=ctx.message.created_at)
    em.set_image(url=userAvatarUrl)
    em.set_footer(text=f'Requested by {ctx.author}',
                  icon_url=ctx.author.avatar.url)
    await ctx.send(embed=em)


@client.command()
async def poll(ctx, question, option1=None, option2=None):
    if option1 == None and option2 == None:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title='New poll:',
            description=f'{question} \n \n**✅ = {option1}**\n**❎ = {option2}**',
            color=0xff006a,
            timestamp=ctx.message.created_at)
        em.set_footer(text=f'Requested by {ctx.author}')
        message = await ctx.send(embed=em)
        await message.add_reaction('✅')
        await message.add_reaction('❎')
    elif option1 == None:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title='New poll:',
            description=f'{question} \n \n**✅ = {option1}**\n**❎ = {option2}**',
            color=0xff006a,
            timestamp=ctx.message.created_at)
        em.set_footer(text=f'Requested by {ctx.author}')
        message = await ctx.send(embed=em)
        await message.add_reaction('✅')
        await message.add_reaction('❎')
    elif option2 == None:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title='New poll:',
            description=f'{question} \n \n**✅ = {option1}**\n**❎ = {option2}**',
            color=0xff006a,
            timestamp=ctx.message.created_at)
        em.set_footer(text=f'Requested by {ctx.author}')
        message = await ctx.send(embed=em)
        await message.add_reaction('✅')
        await message.add_reaction('❎')
    else:
        await ctx.channel.purge(limit=1)
        em = discord.Embed(
            title='New poll:',
            description=f'{question} \n \n**✅ = {option1}**\n**❎ = {option2}**',
            color=0xff006a,
            timestamp=ctx.message.created_at)
        em.set_footer(text=f'Requested by {ctx.author}')
        message = await ctx.send(embed=em)
        await message.add_reaction('✅')
        await message.add_reaction('❎')


#kill
@client.command()
async def kill(ctx, *, member: discord.Member = None):

    responses = [
        'got burnt to a crisp 🔥', 'got stabbed about 69 times 😳',
        'was too soft to handle this command 😔', 'dies with constipation 💩',
        'dies with a sus face', 'got squashed by the rock 🪨',
        'never existed, lol', 'got farted to death 😮‍💨'
        'died. yea he just died 😀', 'got ||kissed|| to death 💋',
        'had ||sex|| with a dragon 🐲',
        'started to be vegan, and died because of it 🌱'
    ]

    em = discord.Embed(
        title=f'You killed {member}',
        description=f'{member.mention} {random.choice(responses)}',
        color=0xff006a,
        timestamp=ctx.message.created_at)
    em.set_footer(text=f'Requested by {ctx.author}')
    await ctx.send(embed=em)


#sus
@client.command()
async def sus(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://meme-api.herokuapp.com/gimme/sus') as r:
            res = await r.json()
            embed = discord.Embed(color=0xff006a, title=res["title"])
            embed.set_image(url=res['url'])
            embed.set_footer(
                text=
                'We are not responsible for the memes posted (visit reddit.com for help)'
            )
            embed.set_author(
                name='reddit.com',
                url='https://reddit.com',
                icon_url='https://i.postimg.cc/fRNx315y/pngwing-com.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('⬆️')
            await msg.add_reaction('⬇️')


#wide
@client.command()
async def wide(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://meme-api.herokuapp.com/gimme/wide') as r:
            res = await r.json()
            embed = discord.Embed(color=0xff006a, title=res["title"])
            embed.set_image(url=res['url'])
            embed.set_footer(
                text=
                'We are not responsible for the memes posted (visit reddit.com for help)'
            )
            embed.set_author(
                name='reddit.com',
                url='https://reddit.com',
                icon_url='https://i.postimg.cc/fRNx315y/pngwing-com.png')
            msg = await ctx.send(embed=embed)
            await msg.add_reaction('⬆️')
            await msg.add_reaction('⬇️')


#baka
@client.command()
async def baka(ctx):
    em = discord.Embed(title='baka 😳', description='', color=0xff006a)
    em.set_image(url="https://i.ytimg.com/vi/WviwYLZubSw/maxresdefault.jpg")
    await ctx.send(embed=em)


#heheboi
@client.command()
async def heheboi(ctx):
    em = discord.Embed(title='hehe boyy', description='', color=0xff006a)
    em.set_image(
        url=
        "http://pm1.narvii.com/7073/e8531975a9a2f49caabe3dad4d12470c787f3cf5r1-720-759v2_uhq.jpg"
    )
    await ctx.send(embed=em)


#8ball
@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):

    responses = [
        'It is certain', 'Outlook good', 'You may rely on it',
        'Ask again later', 'Concentrate and ask again',
        'Reply hazy, try again', 'My reply is no', 'My sources say no',
        'Without a doubt', 'Very doubtful', 'Cannot predict now',
        'Go ask someone else :)',
        'U basically suck for asking me this question lol!', 'amang as ඞ'
    ]

    em = discord.Embed(
        title='8ball',
        description=(
            f'🎱 Question: {question}  |  Answer: {random.choice(responses)}'),
        color=0xff006a)
    em.set_thumbnail(url='https://i.postimg.cc/YSQ30Ynk/8ball.png')
    await ctx.send(embed=em)


#clear


@client.command(aliases=['clr'])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)
    em = discord.Embed(
        title='❌ | Permissions Error',
        description='You must be an **Administrator** to use this command',
        color=0xff006a)
    em.set_thumbnail(url='https://i.postimg.cc/YSQ30Ynk/8ball.png')
    if (commands.has_permissions(administrator=True)):
        pass
    else:
        await ctx.send(embed=em)


#kick
@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    em = discord.Embed(
        title='Member Kicked',
        description=
        f'{member} has been kicked from the server \n for reason: {reason}',
        color=0xff006a)
    await ctx.send(embed=em)


#ban
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    em = discord.Embed(title='Member Banned',
                       description=f'{member} has been Banned from the server',
                       color=0xff006a)
    await ctx.send(embed=em)


#say
@client.command()
async def say(ctx, *, text):
    em = discord.Embed(title='', description=text, color=0xff006a)
    await ctx.send(embed=em)


#Hi
@client.command()
async def hi(ctx):
    em = discord.Embed(
        title='Hi there!',
        description='Hi there, always ready to help! TYPE: `.help` for usage.',
        color=0xff006a)
    await ctx.send(embed=em)


#ShortForms
@client.command(aliases=['short', 'shorts', 'shrt', 'sh'])
async def shortforms(ctx):
    em = discord.Embed(
        title='Shortforms:',
        description=
        f'Here are all the short forms of the bot as per update `{ver}`',
        color=0xff006a)
    em.add_field(
        name='Util',
        value=
        'Avatar = `av`, BoostCount = `bc`, ShortForms = `sh`, Changelog = `chl`, Membercount = `mc`, ServerInfo = `si`, Server Icon = `sicon`, Server Roles = `sr`, removeafk = `rafk`'
    )
    em.add_field(
        name='Bot Info',
        value=
        'Commands = `cmds`, Invite = `invi`, Copyright = `cp`, About = `abt`, Version = `ver`, Credits = `cre`, updatelist = `ul`'
    )
    em.add_field(
        name='Moderation',
        value=
        'Clear = `clr`, RemoveChannel = rch, addrole = `arole`, removerole = `rrole`'
    )

    await ctx.send(embed=em)


#Credits
@client.command(aliases=['cre'])
async def credits(ctx):
    em = discord.Embed(title='Credits - Kryptic ™️',
                       description='',
                       color=0xff006a)
    em.add_field(name='Owner', value='ar im.#3865')
    em.add_field(name='Server', value='RapidG™️')
    em.add_field(name='Copyright', value='https://copyrighted.com')
    em.add_field(name='Inspiration',
                 value='Eternos Bot, made by Phantomヅ#3132')
    em.add_field(name='Coding Section',
                 value='VS Code, Python V3.10, Discord Module')
    em.add_field(name='Links', value='discord.com, dsc.gg, bit.ly')

    em.add_field(name='Invite link for Kryptic',
                 value='https://dsc.gg/krypticgg')
    em.add_field(name='Invite link for Eternos',
                 value='https://dsc.gg/eternosguild')

    await ctx.send(embed=em)


#Adding
@client.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    em = discord.Embed(title='Addition',
                       description=left + right,
                       color=0xff006a)
    em.set_thumbnail(url="https://i.postimg.cc/C5BYRshM/math.png")
    await ctx.send(embed=em)


#Subtracting
@client.command()
async def sub(ctx, left: int, right: int):
    """Subs two numbers together."""
    em = discord.Embed(title='Subtraction',
                       description=left - right,
                       color=0xff006a)
    em.set_thumbnail(url="https://i.postimg.cc/C5BYRshM/math.png")
    await ctx.send(embed=em)


#Multi
@client.command()
async def multi(ctx, left: int, right: int):
    """multi two numbers together."""
    em = discord.Embed(title='Multiplication',
                       description=left * right,
                       color=0xff006a)
    em.set_thumbnail(url="https://i.postimg.cc/C5BYRshM/math.png")
    await ctx.send(embed=em)


#Div
@client.command()
async def div(ctx, left: int, right: int):
    """multi two numbers together."""
    em = discord.Embed(title='Division',
                       description=left / right,
                       color=0xff006a)
    em.set_thumbnail(url="https://i.postimg.cc/C5BYRshM/math.png")
    await ctx.send(embed=em)


#Root
@client.command()
async def root(ctx, num: int):
    em = discord.Embed(title='Square root',
                       description=math.sqrt(num),
                       color=0xff006a)
    em.set_thumbnail(url="https://i.postimg.cc/C5BYRshM/math.png")
    await ctx.send(embed=em)


#Pow
@client.command()
async def pow(ctx, num: int, pow: int):
    em = discord.Embed(title='Power',
                       description=math.pow(num, pow),
                       color=0xff006a)
    em.set_thumbnail(url="https://i.postimg.cc/C5BYRshM/math.png")
    await ctx.send(embed=em)


#Invite
@client.command()
async def invite(ctx, ):
    em = discord.Embed(title='🔗 | Invite',
                       description='[Invite](https://dsc.gg/krypticgg)',
                       color=0xff006a,
                       timestamp=ctx.message.created_at)
    em.set_thumbnail(url='https://i.postimg.cc/wv8KbfYt/pfp.png')
    em.set_footer(text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=em)


@client.command()
async def links(ctx, ):
    em = discord.Embed(
        title='🔗 | Useful Links',
        description=
        '[Invite](https://dsc.gg/krypticgg)\n[Support](https://discord.gg/jA34s8Zwtr)',
        color=0xff006a,
        timestamp=ctx.message.created_at)
    em.set_footer(text=f"Requested by {ctx.author.name}")
    em.set_thumbnail(url='https://i.postimg.cc/wv8KbfYt/pfp.png')
    await ctx.send(embed=em)


@client.command()
async def socials(ctx, ):
    em = discord.Embed(
        title='🔗 | Socials',
        description=
        '[Invite](https://dsc.gg/krypticgg)\n[Support](https://discord.gg/jA34s8Zwtr)\n[Instagram](https://www.instagram.com/abdul.__.r/)\n[Twitter](https://twitter.com/AR_tveeter)\n[All Links](https://linktr.ee/ar.im)',
        color=0xff006a,
        timestamp=ctx.message.created_at)
    em.set_footer(text=f"Requested by {ctx.author.name}")
    em.set_thumbnail(url='https://i.postimg.cc/wv8KbfYt/pfp.png')
    await ctx.send(embed=em)


#token
keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)
