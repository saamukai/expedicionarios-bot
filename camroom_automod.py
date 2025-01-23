from discord.ext import tasks

from utils import msg_time

MOVE_USER_SOURCE_CHANNEL_ID = int('MOVE_USER_SOURCE_CHANNEL_ID')
MOVE_USER_TARGET_CHANNEL_ID = int('MOVE_USER_TARGET_CHANNEL_ID')
MOVE_USER_LOOP_INTERVAL = 2


@tasks.loop(minutes=MOVE_USER_LOOP_INTERVAL)
async def move_users(BOT, GUILD_ID):
    guild = BOT.get_guild(GUILD_ID)
    source_channel = guild.get_channel(MOVE_USER_SOURCE_CHANNEL_ID)
    target_channel = guild.get_channel(MOVE_USER_TARGET_CHANNEL_ID)

    if source_channel and target_channel:
        for member in source_channel.members:
            if not member.bot:
                if not member.voice.self_video and not member.voice.self_stream:
                    await member.move_to(target_channel)
                    print(f'{msg_time()} MOVE_USER: Membro {member.name} movido para {target_channel.name}')
                    try:
                        message = (
                                f'**[MODERAÇÃO EXPEDICIONÁRIOS]** Olá **{member.name}**,'
                                'o canal **"WEBCAM/TELA ON"** é apenas para câmeras ou'
                                'streams ligadas. Portanto, você foi movido para sala'
                                '**"GERAL"**.'
                        )
                        await member.send(message)
    
                    except Exception as e:
                        print(f'{msg_time()} MOVE_USER: ERRO AO ENVIAR MENSAGEM: {member.name}\n ERRO: {e}')
    
    else:
        print(f'{msg_time()} MOVE_USER: SOURCE_CHANNEL OU TARGET_CHANNEL INVÁLIDO.')

    

 
            
        

