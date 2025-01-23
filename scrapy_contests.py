from datetime import datetime

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import tasks
from utils import msg_time

CON_BR_CHANNEL_ID = int('CHANNEL_ID')
CON_BR_URL = 'https://concursosnobrasil.com/'
ROLE_NEWS_ID = int('ROLE_ID')
CON_BR_LOOP_INTERVAL_MIN = 10
last_request_time = ''

async def get_recents_contests():
    response = requests.get(CON_BR_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    recents_contests = soup.select_one('.recentes-container')
    return recents_contests.children

def filter_contests(contests):
    global last_request_time
    contests_to_publish = []  
    
    if not last_request_time:
        last_request_time = datetime.now()

    for article in contests:
        article_time = article.select_one('time').text.strip()
        article_time_formated = datetime.strptime(article_time, "%d/%m/%Y às %Hh%M")
        
        if article_time_formated < last_request_time: #artigo antigo/já publicado
            continue

        title_article = article.select_one('.post-title').text.strip()

        if ('seletivo' in title_article.lower() or 
            'prefeitura' in title_article.lower() or
            'seleção' in title_article.lower() or
            'simplificado' in title_article.lower()):
            print(f'{msg_time()} NOTÍCIAS CONCURSOS: Concurso de setivo/prefeitura não publicado')
            continue

        link = article.select_one('a')['href']
        location = article.select_one('.sigla').text.strip()
        author = article.select_one('span > span').text.strip()
        
        new_contest = f'## [{location} - {title_article}]({link})\n {article_time} por {author}'
        contests_to_publish.append(new_contest)
    
    last_request_time = datetime.now()
    return contests_to_publish

def make_embed_contest(contest):
    global last_request_time
    embed = discord.Embed(
        title=f'📢 Concursos Brasil - Notícias Recentes [{last_request_time.strftime('%d/%m/%Y %H:%M')}]',
        url=CON_BR_URL,
        color=discord.Color.yellow(),
        description="".join(contest)
    )

    embed.set_footer(text="[MENSAGEM AUTOMÁTICA] pelo @Bot Expedicionário")
    embed.set_thumbnail(
        url='https://i.ibb.co/KyTkq14/concursos-brasil.jpg' 
    )
    return embed

@tasks.loop(minutes=CON_BR_LOOP_INTERVAL_MIN)
async def alert_new_contest(BOT, GUILD_ID):
    recents_contests = await get_recents_contests()
    contests_to_publish = filter_contests(recents_contests)

    if len(contests_to_publish) == 0:
        print(f'{msg_time()} NOTICIAS CONCURSOS: Sem notícias recentes.')
        return
    else:
        guild = BOT.get_guild(GUILD_ID)
        channel = guild.get_channel(CON_BR_CHANNEL_ID)
        role_noticias = guild.get_role(ROLE_NEWS_ID)
        
        for contest in contests_to_publish:
            embed_to_publish = make_embed_contest(contest)
            await channel.send(f'{role_noticias.mention}', embed=embed_to_publish)
            print(f'{msg_time()} NOTICIAS CONCURSOS: Nova notícia publicada')
        return 
