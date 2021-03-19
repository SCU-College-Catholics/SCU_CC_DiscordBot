# bot.py
import os


import discord
import requests
import json
import time
from dotenv import load_dotenv
from datetime import date
from urllib.parse import quote 
from urllib.request import urlopen
import re
from lxml import html

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

    if '-commands' in message.content.lower():
        commandsStr = '**SCU College Catholics Bot Commands:**\n'
        commandsStr += '**-sod**: Sends information on today\'s liturgical celebration as well as feast days, etc.\n'
        commandsStr += '**-gospel**: Sends today\'s gospel\n'
        commandsStr += '**-joke**: Sends a hillarious pun or joke\n'
        commandsStr += '**-yoda** & **-jarjar**: Translates the sentence after "-yoda " (or "-jarjar") into yoda (or gungan) speak. (limited to about 5x per hour)\n' 
        commandsStr += '**keywords**: There are some (secret?) keywords the bot looks for and it may respond with a message accordingly.\n'
        commandsStr += 'LMK if there are any new features you\'d like to see! View my source at Github: https://github.com/SCU-College-Catholics/SCU_CC_DiscordBot'
        await message.channel.send(commandsStr)

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
        nm = message.content[11:] # Get the user name parameter if it exists
        own = message.guild.get_member_named(nm)
        if own == None or own.name == 'kfenole' or own.name == 'The Mexican One':
            own = message.author
            # Reduntant, but we don't want to send this message if the victim isn't connected to voice
            if (own.voice.channel):
                await message.channel.send('I can\'t send that person to purgatory, but I can send you!')
        # If target isn't connected to voice, exit
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
        # if for some reason an insensitive joke is received,exit before sending
        if (data["safe"] == False):
            return
        # Either send the 1 line or 2 line joke
        if (data["type"] == "single"):
            await message.channel.send(data["joke"])
        else:
            await message.channel.send(data["setup"])
            time.sleep(2)
            await message.channel.send(data["delivery"])

    if '-yoda' in message.content.lower():
        strn = message.content[6:] #trim the string to just include the message
        url = 'https://api.funtranslations.com/translate/yoda.json?text='
        # https://api.funtranslations.com/translate/yoda.json?text=Master%20Obiwan%20has%20lost%20a%20planet.
        qstr = quote(strn)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url + qstr, timeout=2, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.headers)
            await message.channel.last_message.delete()
            return
        
        data = response.json()
        
        await message.channel.send(data["contents"]["translated"])
    if '-gungan' in message.content.lower() or '-jarjar' in message.content.lower():
        strn = message.content[8:] # trim to just inlcude message
        url = 'https://api.funtranslations.com/translate/gungan.json?text='
        # https://api.funtranslations.com/translate/yoda.json?text=Master%20Obiwan%20has%20lost%20a%20planet.
        qstr = quote(strn)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url + qstr, timeout=2, headers=headers)
        if response.status_code != 200:
            print(response.status_code)
            print(response.headers)
            await message.channel.last_message.delete()
            return
        
        data = response.json()
        
        await message.channel.send(data["contents"]["translated"])

    if 'depress' in message.content.lower() or 'affirmation' in message.content.lower() or 'sad' in message.content.lower():
        response = requests.get('https://www.affirmations.dev')
        if response.status_code != 200:
            print(response.status_code)
            print(response.headers)
            return
        
        data = response.json()
        await message.channel.send('Here\'s an affirmation to lift your spirits: **' + data["affirmation"] + '**')
    
    if 'tragedy' in message.content.lower() or 'sith' in message.content.lower() or 'plageuis' in message.content.lower() or 'darth' in message.content.lower():
        await message.channel.send('Did you ever hear the Tragedy of Darth Plagueis the wise? I thought not. It\'s not a story the Jedi would tell you. It\'s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. It\'s ironic he could save others from death, but not himself.')

    if '-gospel' in message.content.lower():
        #TODO: Clean this code up
        today = date.today()
        d = today.strftime("%m%d%y")
        isSunday = False

        # If today is sunday, we need to specift the year cycle in the url
        if (today.strftime("%A") == 'Sunday'):
            isSunday = True
            d += '-YearB'
        url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'
        print(url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        pageContent=requests.get(url, timeout=2, headers=headers)
        tree = html.fromstring(pageContent.content)

        secondReading = False # if there is a 2nd reading we need to adjust the xpath (index 9 instead of 8 in the 2nd div)
        if tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[8]/div/div/div/div/div[1]/div/a/text()'):
            gospelVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[8]/div/div/div/div/div[1]/div/a/text()')[0]
        else:
            # In case there are more readings
            gospelVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[9]/div/div/div/div/div[1]/div/a/text()')[0]
            secondReading = True

        # When there is a second reading the normal place for the gospel holds the psalm
        if gospelVerse[:2] == 'Ps':
            # In case there are more readings
            gospelVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[9]/div/div/div/div/div[1]/div/a/text()')[0]
            secondReading = True
        elif isSunday:
            #//*[@id="block-usccb-readings-content"]/div/div[10]/div/div/div/div/div[1]/div/a
            gospelVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[10]/div/div/div/div/div[1]/div/a/text()')[0]
            
        gospelString = ''
        i = 1
        while i:
            if secondReading == False and not isSunday:
                gospelPar = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[8]/div/div/div/div/div[2]/p[' + str(i) + ']/text()')
            elif secondReading == True:
                gospelPar = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[9]/div/div/div/div/div[2]/p[' + str(i) + ']/text()')
            else:
                gospelPar = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[10]/div/div/div/div/div[2]/p[' + str(i) + ']/text()')

            if (gospelPar == False or gospelPar == []):
                i = 0
                break
            for g in gospelPar:
                if g == 'OR:':
                    break
                gospelString += g
            gospelString += "\n\n"
            i += 1

        await message.channel.send('**' + today.strftime("%A %B %-d, %Y") + ' | ' + gospelVerse + '**\n' + gospelString)


client.run(TOKEN)
