import discord
from discord.ext import commands
from datetime import datetime


WELCOME_CHANNEL_ID = 1236422259586109461
RULES_CHANNEL_ID = 1198588906757685308
APPLY_CHANNEL_ID = 1234562064442458172


class NovaEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('NovaEvents ready')

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        rules_channel = member.guild.get_channel(RULES_CHANNEL_ID)
        apply_channel = member.guild.get_channel(APPLY_CHANNEL_ID)

        embed = discord.Embed(title='Welcome!',
                              description=f'Welcome {member.mention} to the **Nova Family** discord!\n\n'
                                          f'Please make sure to read our {rules_channel.mention}\n\n'
                                          f'If you are looking to join one of our clans, '
                                          f'make sure to use {apply_channel.mention}',
                              color=discord.Color.blurple())

        if member.display_icon:
            embed.set_thumbnail(url=member.display_icon)

        if member.banner:
            embed.set_image(url=member.banner)

        embed.set_footer(text='Created by Nova6 Team', icon_url=member.guild.icon)
        embed.timestamp = datetime.now()

        await welcome_channel.send(embed=embed, view=RedirectView())


class RedirectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        button = discord.ui.Button(label='Apply', style=discord.ButtonStyle.url, url='https://discord.com/channels/963100732477816872/1234562064442458172/1237042178900103280')
        self.add_item(button)


async def setup(bot: commands.Bot):
    await bot.add_cog(NovaEvents(bot))
    bot.add_view(RedirectView())

