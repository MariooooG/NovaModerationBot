import datetime
import os

import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

import time

from enum import Enum
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('MODERATION_BOT_TOKEN')

LOGGING_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))


class NovaBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

        cogs = []

        for root, dirs, files in os.walk('cogs'):
            if '__pycache__' in root:
                continue

            folder_name = os.path.basename(root)

            for file_name in files:
                if file_name.endswith('.py'):
                    if folder_name == 'cogs':
                        cogs.append(f'cogs.{file_name[:-3]}')
                    else:
                        cogs.append(f'cogs.{folder_name}.{file_name[:-3]}')

        self.initial_extensions = cogs
        self.added = False

    async def setup_hook(self):
        self.session = aiohttp.ClientSession()

        for cogs in self.initial_extensions:
            await self.load_extension(cogs)

        guild = discord.Object(id=963100732477816872)

        await self.tree.sync(guild=guild)

    async def close(self):
        await super().close()
        await self.session.close()

    async def on_ready(self):
        print(f'Bot ready')

        """embed = discord.Embed(title='<:trophy1:1236763773063397476> | Rules',
                              description='__The following behavior will result in a kick / ban__\n\n'
                                                         '> <:bulletpoint:1237033867785932890> Pinging a role or member without reason\n'
                                                         '> <:bulletpoint:1237033867785932890> Racism.\n'
                                                         '> <:bulletpoint:1237033867785932890> Derogatory language towards LGBTQ+.\n'
                                                         '> <:bulletpoint:1237033867785932890> Derogatory language towards mental health.\n'
                                                         '> <:bulletpoint:1237033867785932890> Bullying.\n'
                                                         '> <:bulletpoint:1237033867785932890> Death Threats.\n'
                                                         '> <:bulletpoint:1237033867785932890> Poaching\n'
                                                         '> <:bulletpoint:1237033867785932890> Unsolicited DM\'s\n'
                                                         '> <:bulletpoint:1237033867785932890> Doxxing (Private information)\n'
                                                         '> <:bulletpoint:1237033867785932890> Breaking discord ToS\n'
                                                         '> <:bulletpoint:1237033867785932890> Posting private business advertisements',
                              color=discord.Color.green())

        embed.set_footer(text='Created by Nova6 Team', icon_url=self.get_guild(963100732477816872).icon)
        embed.timestamp = datetime.datetime.now()
        
        channel = self.get_channel(1198588906757685308)

        if channel:
            await channel.send(embed=embed)
            await channel.send(file=discord.File('divider.gif'))"""

        await self.change_presence(activity=discord.Game(name='Clash of Clans'), status=discord.Status.dnd)


bot = NovaBot()
bot.remove_command('help')

bot.run(TOKEN)
