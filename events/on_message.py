import discord
from discord.ext import commands
from config import *

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.mentions:
            for member in message.mentions:
                if member == self.bot.user:
                    await message.channel.send('Hello! If you need any help. Please open ticket via <#1255046606869500009> channel!')

            for role in message.mentions[0].roles:
                if role.id in ALLOWED_ROLE_IDS:
                    if STAFF_ROLES in [role.id for role in message.author.roles]:
                        pass
                    elif ON_GOING_TICKET_ROLE in [role.id for role in message.author.roles]:
                        pass
                    else:
                        await message.channel.send(
                            message.author.mention,
                            embed=discord.Embed(
                                title="Anti-Ping Warning",
                                description=f"{message.author.mention} please do not ping users with the role {role.mention}.",
                                color=discord.Color.red()
                            ).set_image(
                                url="https://media.tenor.com/aslruXgPKHEAAAAM/discord-ping.gif"
                            ),
                            delete_after=15
                        )

        if message.channel.id == 1258699643915604060:
            if TICKET_CHANNEL_ID is not None:
                control_channel = self.bot.get_channel(TICKET_CHANNEL_ID)
                await control_channel.send(message.content)
            else:
                await message.channel.send('No ticket channel set up')

async def setup(bot):
    await bot.add_cog(OnMessage(bot))
