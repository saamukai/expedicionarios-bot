import datetime
import random

import discord
from discord.ext import tasks
from utils import msg_time

LOCK_CHANNEL_ID = int('LOCK_CHANNEL_ID')
ROLE_ID = int('ROLE_ID')

OFFSET = datetime.timedelta(hours=-3)
TZ = datetime.timezone(OFFSET)

TIME_TO_OPEN = datetime.time(hour=5, minute=00, tzinfo=TZ)
TIME_TO_CLOSE = datetime.time(hour=23, minute=39, tzinfo=TZ)


@tasks.loop(time=[TIME_TO_OPEN, TIME_TO_CLOSE])
async def lock_unlock_vip(BOT, GUILD_ID):
    guild = BOT.get_guild(GUILD_ID)
    channel = guild.get_channel(int(LOCK_CHANNEL_ID))

    vip_role = guild.get_role(ROLE_ID)

    overwrite = channel.overwrites_for(vip_role)
    color = discord.Color.blue()
    message = ''

    if overwrite.send_messages:
        overwrite.send_messages = False
        color = discord.Color.purple()

        message = (
            'Canal bloqueado. Boa noite! '
            '**Bora de dormes,** amanhã é outro dia 💤'
        )

    else:
        overwrite.send_messages = True
        color = discord.Color.yellow()

        message = (
            'Canal liberado. Bom dia! '
            '**Foco no papiro!!** 🎯'
        )

    embed = discord.Embed(
        title=message,
        color=color,
    )

    embed.set_footer(text="[MENSAGEM AUTOMÁTICA] pelo @Bot Expedicionário")
    await channel.send(embed=embed)
    await channel.set_permissions(vip_role, overwrite=overwrite)
    print(f'{msg_time()}: LOCK/UNLOCK CHAT: Canal geral bloqueado/desbloqueado')
