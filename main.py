import discord
from discord.ext import commands

from scrapy_contests import alert_new_contest
from camroom_automod import move_users

TOKEN = 'BOT_TOKEN_DISCORD'
GUILD_ID = int('GUILD_ID')
INTENTS = discord.Intents.default()
BOT = commands.Bot(command_prefix='!e', intents=INTENTS)

@BOT.event
async def on_ready():
    print(f'Logged in as {BOT.user}')
    alert_new_contest.start(BOT, GUILD_ID)  
    move_users.start(BOT, GUILD_ID)

if __name__ == '__main__':
    BOT.run(TOKEN)
