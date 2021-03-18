# bot.py
import os


import discord
import requests
import json
import time
from dotenv import load_dotenv
from datetime import date
from urllib.parse import quote 

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    # print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        if guild.name == GUILD:
            print(guild.name)

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
        # YYYY/MM/DD
        d = today.strftime("%Y/%m/%d")
        # Send an api request to get the SOD
        url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/default/' + d
        # url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/default/2021/03/16'

        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url, timeout = 1, headers=headers)

        print(response.status_code)
        print(response.text)

        data = response.json()
        celebrations = data["celebrations"]
        print(celebrations)
        for c in celebrations:
            await message.channel.send(c['rank'] + ': **' + c["title"] + '** with liturgical color ' + c["colour"])

    if '-purgatory' in message.content.lower():
        vcs = message.guild.voice_channels
        nm = message.content[11:]
        own = message.guild.get_member_named(nm)
        if own == None or own.name == 'kfenole' or own.name == 'The Mexican One':
            own = message.author
            if (own.voice.channel):
                await message.channel.send('I can\'t send that person to purgatory, but I can send you!')
        if (own.voice.channel == False):
            return
        for vc in vcs:
            if vc.name == 'Purgatory':
                await own.move_to(vc)
                if own in vc.members:
                    msg = 'Sent ' + own.name + ' to purgatory. Purgatory go brr!'
                    await message.channel.send(msg)
    

    if '-joke' in message.content.lower():
        url = 'https://v2.jokeapi.dev/joke/Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&safe-mode'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url, timeout = 2, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            await message.channel.last_message.delete()
            return
        data = response.json()
        print(data["safe"])
        if (data["safe"] == False):
            return
        if (data["type"] == "single"):
            await message.channel.send(data["joke"])
        else:
            await message.channel.send(data["setup"])
            time.sleep(2)
            await message.channel.send(data["delivery"])

    if '-yoda' in message.content.lower():
        strn = message.content[6:]
        url = 'https://api.funtranslations.com/translate/yoda.json?text='
        # https://api.funtranslations.com/translate/yoda.json?text=Master%20Obiwan%20has%20lost%20a%20planet.
        qstr = quote(strn)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url + qstr, timeout=2, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.headers)
            # await message.channel.last_message.delete()
            return
        
        data = response.json()
        
        await message.channel.send(data["contents"]["translated"])
    if '-gungan' in message.content.lower() or '-jarjar' in message.content.lower():
        strn = message.content[8:]
        url = 'https://api.funtranslations.com/translate/gungan.json?text='
        # https://api.funtranslations.com/translate/yoda.json?text=Master%20Obiwan%20has%20lost%20a%20planet.
        qstr = quote(strn)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url + qstr, timeout=2, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.headers)
            # await message.channel.last_message.delete()
            return
        
        data = response.json()
        
        await message.channel.send(data["contents"]["translated"])


        


client.run(TOKEN)
