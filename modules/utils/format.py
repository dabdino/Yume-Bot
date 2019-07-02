import random

import discord

from modules.utils import lists


class Mod():

    @staticmethod
    async def check_embed(member, guild, sanctions, time):

        em = discord.Embed(
            title="{}".format(member.name),
            description="A new user has joined",
            color=discord.Colour.magenta()
        )
        em.set_author(name=f"{guild.name}")
        em.set_thumbnail(url=member.avatar_url)
        em.add_field(name="User", value = f"Name : {member.mention} \nID : {member.id}")
        em.add_field(name ="Informations", value = f"Sanctions : {sanctions} \nAge : {time}days")

        return em


class Embeds():

    @staticmethod
    async def format_mod_embed(ctx, user, command, sanction=None, duration=None):

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name=f"{command}", icon_url=user.avatar_url)
        if sanction is not None:    
            em.set_footer(text=f'Sanction ID: {sanction}')
        if command == 'ban' or command == 'hackban':
            em.description = f'**{user}** was just {command}ned...'
        elif command == 'mute':
            em.description = f'**{user}** was just muted for {duration}...'
        elif command == 'unmute':
            em.description = f'**{user}** was just unmuted...'
        elif command == 'kick':
            em.description = f'**{user}** was just kicked...'
        elif command == 'unban':
            em.description = f'**{user}** was just unbanned...'
        elif command == 'strike':
            em.description = f'**{user}** was just {command}d...'

        return em

    @staticmethod
    async def format_feedback_embed(ctx, auth, guild, success, message):
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name="Feedback", icon_url=auth.avatar_url)
        if success:
            em.add_field(
                name="Author", value=f"Name : {auth} \n ID : {auth.id}", inline=False)
            em.add_field(
                name="Guild", value=f"Name : {guild.name} \n ID : {guild.id}", inline=False)
            em.add_field(name="Content",
                         value=f"{message.content}", inline=False)
            em.set_footer(text=tip)

        return em

    @staticmethod
    async def format_get_set_embed(ctx, greet, greetchannel, blacklist, logging, logchannel, automod, stats, vip):
        tip = random.choice(lists.tip)
        greetchan = discord.utils.get(ctx.guild.text_channels, id=int(greetchannel))

        logchan = discord.utils.get(ctx.guild.text_channels, id=int(logchannel))

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Settings')
        em.set_footer(text=f'Tip: {tip}')

        em.add_field(name="Greet", value=greet)

        em.add_field(name="Greet Channel", value=greetchan.mention)
        em.add_field(name="Blacklist", value=blacklist)
        em.add_field(name="Logging", value=logging)
        em.add_field(name="Log Channel", value=logchan.mention)
        em.add_field(name='Automod', value=automod)
        em.add_field(name='Stats', value=stats)
        em.add_field(name='Vip', value=vip)

        return em

    @staticmethod
    async def format_commands_embed(ctx, icon):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Yume Bot', url="https://yumenetwork.gitbook.io/yumebot/", icon_url=icon)
        em.description = "**» Does anyone need any help?**\nYou can use **--h <category>** to view commands for that category."
        em.add_field(name="**Categories**", value="**--h general** | General Commands\n"
                                                  "**--h fun** | Fun Commands\n"
                                                  "**--h utils** | Utils Commands\n"
                                                  "**--h mods** | Mods Commands\n"
                                                  "**--h admin** | Admin Commands\n"
                                                  "**--h level** | Level Commands\n"
                                                  "**--h settings** | Settings Commands\n"
                                                  "**--h about** | About Commands")

        em.add_field(name="Links", value="[Documentation](https://yumenetwork.gitbook.io/yumebot/) | [Support]("
                                         "https://invite.gg/yumenetwork) | [Sources]("
                                         "https://github.com/yumenetwork/Yume-Bot) | "
                                         "[Invite]"
                                         "(https://discordapp.com/oauth2/authorize?client_id=456504213262827524&permissions=8&&scope=bot)",
                     inline=False)

        return em

    @staticmethod
    async def format_cat_embed(ctx, icon, category, liste):
        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(name='Yume Bot', url="https://yumenetwork.gitbook.io/yumebot/", icon_url=icon)
        em.description = f"**Category : {category}**\nYou can get more info about a command [here](https://yumenetwork.gitbook.io/yumebot/commands/{str.lower(category)})"
        em.add_field(name="**:pushpin: Commands**", value= f"{liste}")

        return em

