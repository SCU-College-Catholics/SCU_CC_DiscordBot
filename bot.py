# bot.py
import os


import discord
import requests
import json
from dotenv import load_dotenv
from datetime import date

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    # print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')

    if '-sod' in message.content.lower():
        await message.channel.send('🙏Today\'s celebrations are: ')
        today = date.today()

    # dd/mm/YY  YYYY/MM/DD
    d = today.strftime("%Y/%m/%d")
    # Send an api request to get the SOD
    # url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/default/' + d
    url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/default/2021/03/16'
    # url = 'https://apple.com'
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    # HEADERS = {
    #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    # }
    response = requests.get(url, timeout = 1, headers=headers)
    # response = requests.get('http://calapi.inadiutorium.cz/api/v0/en/calendars/default/2021/03/16')
    print(response.status_code)
    print(response.text)

    # print(response.json)
    # json.dumps(response)

    data = response.json()
    celebrations = data["celebrations"]
    print(celebrations)
    for c in celebrations:
        await message.channel.send(c['rank'] + ': **' + c["title"] + '** with liturgical color ' + c["colour"])
        


client.run(TOKEN)
