import discord
import aiohttp
from discord import app_commands
from discord.ext import commands
from config import *
from cogs.ticket import opzionistaff, menustaff, ticket_bott

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), case_insensitive=True)
        self.script_necessari = ['cogs.ticket']
        self.message_event = ['events.on_message']
        self.bottoni_dacaricare = [opzionistaff, menustaff, ticket_bott]
        self.startato = False

    async def setup_hook(self):
        self.sessione = aiohttp.ClientSession()
        for file in self.script_necessari: 
            await self.load_extension(file)
        for file in self.message_event:
            await self.load_extension(file)
        await self.tree.sync()

    async def close(self):
        await super().close()
        await self.sessione.close()

    async def on_ready(self):
        print(f'{self.user} Online!')
        if not self.startato:
            for bottone in self.bottoni_dacaricare: 
                self.add_view(bottone())
            self.startato = True
            await bot.change_presence(activity=discord.Game(name=f"Qupr Digital"))

bot = Bot()

@bot.tree.command()
async def channel(ctx, channel: discord.TextChannel):
    '''Set the channel to monitor for tickets'''
    channel_id = channel.id
    if any(role.id in ALLOWED_ROLE_IDS for role in ctx.author.roles):
        global TICKET_CHANNEL_ID
        TICKET_CHANNEL_ID = channel_id
        await ctx.send(f'Ticket channel set to {channel.mention}')
     
bot.remove_command('help')
bot.run(token)
