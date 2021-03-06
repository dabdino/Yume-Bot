#  Copyright (c) 2019.
#  MIT License
#
#  Copyright (c) 2019 YumeNetwork
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
import random

import discord
from discord.ext import commands

from modules.utils import lists
from modules.utils.db import Settings
from modules.utils.guildy import GuildY


class Event(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """

        :param member: The member who joined the guild
        """

        guildy = GuildY(member.guild)
        await guildy.get()

        # glob = await Settings().get_glob_settings()
        if guildy.greet:
            channel = self.bot.get_channel(int(guildy.greet_channel))
            greet = random.choice(lists.greet)

            em = discord.Embed(timestamp=member.joined_at)
            em.set_author(name="Welcome", icon_url=member.avatar_url)
            em.set_footer(text=f'{member.name}')
            em.description = f"{greet}"
            await channel.send(embed=em)

        if guildy.members_count:
            category = discord.utils.get(
                member.guild.categories, id=int(guildy.count_category))
            for channel in category.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    return
                except discord.HTTPException:
                    return

            overwrite = {
                member.guild.default_role: discord.PermissionOverwrite(connect=False),
            }

            await member.guild.create_voice_channel(f'Users : {len(member.guild.members)}', overwrites=overwrite,
                                                    category=category)
            bots = []
            for user in member.guild.members:
                if user.bot is True:
                    bots.append(user)
            await member.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
            await member.guild.create_voice_channel(f'Members : {len(member.guild.members) - len(bots)}',
                                                    overwrites=overwrite, category=category)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """

        :param member: The member who has left
        """

        guildy = GuildY(member.guild)
        await guildy.get()

        if guildy.members_count:
            category = discord.utils.get(
                member.guild.categories, id=int(guildy.count_category))
            for channel in category.channels:
                try:
                    await channel.delete()
                except discord.Forbidden:
                    return
                except discord.HTTPException:
                    return

            overwrite = {
                member.guild.default_role: discord.PermissionOverwrite(connect=False),
            }

            await member.guild.create_voice_channel(f'Users : {len(member.guild.members)}', overwrites=overwrite,
                                                    category=category)
            bots = []
            for user in member.guild.members:
                if user.bot is True:
                    bots.append(user)
            await member.guild.create_voice_channel(f'Bots : {len(bots)}', overwrites=overwrite, category=category)
            await member.guild.create_voice_channel(f'Members : {len(member.guild.members) - len(bots)}',
                                                    overwrites=overwrite, category=category)

        if guildy.greet:
            channel = self.bot.get_channel(int(guildy.greet_channel))
            leave = random.choice(lists.leave)

            em = discord.Embed(timestamp=member.joined_at)
            em.set_author(name="Left", icon_url=member.avatar_url)
            em.set_footer(text=f'{member.name}')
            em.description = f"{leave}"
            await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        glob = await Settings().get_glob_settings()
        if 'AFK' in glob:
            if author.id in glob['AFK']:
                if message.content == '--afk':
                    return
                glob['AFK'].remove(author.id)
                await Settings().set_glob_settings(glob)
                await message.channel.send("{}, welcome back !".format(author.mention), delete_after=10)
            else:
                for user in message.mentions:
                    if user.id in glob['AFK']:
                        await message.channel.send("{}#{} is AFK".format(user.name, user.discriminator),
                                                   delete_after=10)
                        # await user.send(f"{author} has mentionned you in {message.guild} : \n`{message.content}`")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await Settings().del_reaction_settings(str(guild.id))
        await Settings().del_server_settings(str(guild.id))

def setup(bot):
    bot.add_cog(Event(bot))
