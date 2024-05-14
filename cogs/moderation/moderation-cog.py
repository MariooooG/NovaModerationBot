import asyncio
import datetime

import discord
from discord import app_commands
from discord.ext import commands

LOGGING_CHANNEL_ID = 1236419814046568589
MUTED_ROLE_ID = 1236423377628037246


class ModerationCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('BanCommands are ready')

    @app_commands.command(name='announceembed', description='Announce some message in embed format')
    @app_commands.describe(channel='Channel you want to send in', title='Optional title', description='Optional description', footer='Optional footer')
    @app_commands.checks.has_permissions(administrator=True)
    async def announce_embed(self, interaction: discord.Interaction, channel: discord.TextChannel, title: str = None, description: str = None, footer: str = 'Created by Nova6 Team'):
        embed = discord.Embed(color=discord.Color.blurple())

        if title:
            embed.title = title

        if description:
            embed.description = description

        embed.set_footer(text=footer, icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        if channel:
            await channel.send(embed=embed)

        await interaction.response.send_message(f'Announcement sent!', ephemeral=True)

    @app_commands.command(name='announcetext', description='Announce some message in text format')
    @app_commands.describe(channel='Channel you want to send in', text='Text you want to announce')
    @app_commands.checks.has_permissions(administrator=True)
    async def announce_text(self, interaction: discord.Interaction, channel: discord.TextChannel, text: str):
        if channel and text:
            await channel.send(text)

        await interaction.response.send_message(f'Announcement sent!', ephemeral=True)

    @app_commands.command(name='ban', description='Ban a user')
    @app_commands.describe(member='The member you want to ban', reason='Optional with a reason')
    @app_commands.checks.has_permissions(administrator=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f'You need a higher role than {member.mention}',
                                                           ephemeral=True)

        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f'This bot needs a higher role than {member.mention}',
                                                           ephemeral=True)

        await member.ban(reason=reason)

        if reason:
            reason = f'\nReason: {reason}'
        else:
            reason = f'\nReason: n/a'

        embed = discord.Embed(title='Banned user | 🚫',
                              description=f'{interaction.user.mention} has banned {member.mention}! {reason}',
                              color=discord.Color.red())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

        await interaction.response.send_message(f'Successfully banned {member.mention}', ephemeral=True)

    @app_commands.command(name='unban', description='Unban a user')
    @app_commands.describe(id='The members id you want to unban')
    @app_commands.checks.has_permissions(administrator=True)
    async def unban(self, interaction: discord.Interaction, id: str):
        try:
            member = await self.bot.fetch_user(int(id))

            try:
                await interaction.guild.unban(member)
            except:
                return await interaction.response.send_message(f'{member.mention} is not banned', ephemeral=True)
        except:
            return await interaction.response.send_message(f'This is not a valid members id.', ephemeral=True)

        embed = discord.Embed(title='Unbanned user | 🚫',
                              description=f'{interaction.user.mention} has unbanned {member.mention}!',
                              color=discord.Color.green())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

        await interaction.response.send_message(f'Successfully unbanned {member.mention}', ephemeral=True)

    @app_commands.command(name='kick', description='Kick a user')
    @app_commands.describe(member='The member you want to kick', reason='Optional with a reason')
    @app_commands.checks.has_permissions(administrator=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f'You need a higher role than {member.mention}',
                                                           ephemeral=True)

        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f'This bot needs a higher role than {member.mention}',
                                                           ephemeral=True)

        await member.kick(reason=reason)

        if reason:
            reason = f'\nReason: {reason}'
        else:
            reason = f'\nReason: n/a'

        embed = discord.Embed(title='Kicked user | 🚫',
                              description=f'{interaction.user.mention} has kicked {member.mention}! {reason}',
                              color=discord.Color.red())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

        await interaction.response.send_message(f'Successfully kicked {member.mention}', ephemeral=True)

    @app_commands.command(name='mute', description='Mutes a user')
    @app_commands.describe(member='The member you want to mute', time='Time until the mute expires',
                           reason='Optional with a reason')
    @app_commands.checks.has_permissions(administrator=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, time: str = None,
                   reason: str = None):
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f'You need a higher role than {member.mention}',
                                                           ephemeral=True)

        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f'This bot needs a higher role than {member.mention}',
                                                           ephemeral=True)

        mute_role = interaction.guild.get_role(MUTED_ROLE_ID)

        if not mute_role:
            return await interaction.response.send_message(f'You have to setup a muted role, contact Mario',
                                                           ephemeral=True)

        if reason:
            reason = f'\nReason: {reason}'
        else:
            reason = f'\nReason: n/a'

        if not time:
            time_str = '\nTime: n/a'
        else:
            time_str = f'\nTime: {time}'

            time_converter = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24, 'w': 60 * 60 * 24 * 7,
                              'mo': 60 * 60 * 24 * 7 * 30, 'y': 60 * 60 * 24 * 365}

            convert = time[-1]
            seconds = time_converter.get(convert)

            actual_time = time[:-1]

            try:
                int(actual_time)
            except:
                return await interaction.response.send_message(f'You have to set <time> and unit <s|m|h|d|w|mo|y>',
                                                               ephemeral=True)

            try:
                expire = int(seconds) * int(actual_time)
            except:
                return await interaction.response.send_message(f'You have to set <time> and unit <s|m|h|d|w|mo|y>',
                                                               ephemeral=True)

        await member.add_roles(mute_role)

        embed = discord.Embed(title='Muted user | 🚫',
                              description=f'{interaction.user.mention} has muted {member.mention}! {reason} {time_str}',
                              color=discord.Color.red())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

        await interaction.response.send_message(f'Successfully muted {member.mention}', ephemeral=True)

        if time:
            await asyncio.sleep(expire)
            await member.remove_roles(mute_role)

            await member.send(f'You have been unmuted from **{interaction.guild.name}**')

            embed = discord.Embed(title='Expired user mute | 🚫',
                                  description=f"{member.mention}'s mute is expired",
                                  color=discord.Color.green())

            embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
            embed.timestamp = datetime.datetime.now()

            logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

            if logging_channel:
                await logging_channel.send(embed=embed)

    @app_commands.command(name='unmute', description='Unmutes a user')
    @app_commands.describe(member='The member you want to unmute')
    @app_commands.checks.has_permissions(administrator=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        mute_role = interaction.guild.get_role(MUTED_ROLE_ID)

        if not mute_role:
            return await interaction.response.send_message(f'You have to setup a muted role, contact Mario',
                                                           ephemeral=True)

        if not mute_role in member.roles:
            return await interaction.response.send_message(f'This user is not muted', ephemeral=True)

        if interaction.user == member:
            return await interaction.response.send_message(f'You can not unmute yourself', ephemeral=True)

        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f'You need a higher role than {member.mention}',
                                                           ephemeral=True)

        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f'This bot needs a higher role than {member.mention}',
                                                           ephemeral=True)

        await member.remove_roles(mute_role)

        if not member.bot:
            await member.send(f'You have been unmuted from **{interaction.guild.name}**')

        embed = discord.Embed(title='Unmuted user | 🚫',
                              description=f"{member.mention} got unmuted by {interaction.user.mention}",
                              color=discord.Color.green())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

    @app_commands.command(name='purge', description='Clear chat messages')
    @app_commands.describe(amount='Number of messages to delete')
    @app_commands.checks.has_permissions(administrator=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.response.send_message(f'Deleted {amount} messages from this channel', ephemeral=True)

        await interaction.channel.purge(limit=amount)

        embed = discord.Embed(title='Purged messages | 🚫',
                              description=f"{interaction.user.mention} did clear **{amount}** message(s) in {interaction.channel.mention}",
                              color=discord.Color.red())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

    @app_commands.command(name='timeout', description='Timeouts a user')
    @app_commands.describe(member='The member you want to timeout', time='Time until the timeout expires',
                           reason='Optional with a reason')
    @app_commands.checks.has_permissions(administrator=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, time: str,
                      reason: str = None):
        if interaction.user.top_role <= member.top_role:
            return await interaction.response.send_message(f'You need a higher role than {member.mention}',
                                                           ephemeral=True)

        if interaction.guild.me.top_role <= member.top_role:
            return await interaction.response.send_message(f'This bot needs a higher role than {member.mention}',
                                                           ephemeral=True)

        if reason:
            reason = f'\nReason: {reason}'
        else:
            reason = f'\nReason: n/a'

        if not time:
            time_str = '\nTime: n/a'
        else:
            time_str = f'\nTime: {time}'

            time_converter = {'s': 1, 'm': 60, 'h': 60 * 60, 'd': 60 * 60 * 24, 'w': 60 * 60 * 24 * 7,
                              'mo': 60 * 60 * 24 * 7 * 30, 'y': 60 * 60 * 24 * 365}

            convert = time[-1]
            seconds = time_converter.get(convert)

            actual_time = time[:-1]

            try:
                int(actual_time)
            except:
                return await interaction.response.send_message(f'You have to set <time> and unit <s|m|h|d|w|mo|y>',
                                                               ephemeral=True)

            try:
                expire = int(seconds) * int(actual_time)
            except:
                return await interaction.response.send_message(f'You have to set <time> and unit <s|m|h|d|w|mo|y>',
                                                               ephemeral=True)

        await member.timeout(datetime.timedelta(seconds=expire), reason=reason)

        embed = discord.Embed(title='Timeouted user | 🚫',
                              description=f'{interaction.user.mention} has timeouted {member.mention}! {reason} {time_str}',
                              color=discord.Color.red())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)

        await interaction.response.send_message(f'Successfully timeouted {member.mention}', ephemeral=True)

        await asyncio.sleep(expire)

        embed = discord.Embed(title='Expired user timeout | 🚫',
                              description=f"{member.mention}'s timeout is expired",
                              color=discord.Color.green())

        embed.set_footer(text='Created by Nova6 Team', icon_url=interaction.guild.icon)
        embed.timestamp = datetime.datetime.now()

        logging_channel = interaction.guild.get_channel(LOGGING_CHANNEL_ID)

        if logging_channel:
            await logging_channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ModerationCommands(bot))
