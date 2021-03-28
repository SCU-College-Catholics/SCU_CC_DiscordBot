# bot.py
import os


import discord
import requests
import json
import time
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from urllib.parse import quote 
from urllib.request import urlopen
import re
from lxml import html
import random
import math

load_dotenv('.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# Returns the first image result from Bing
def getFirstImageResultFor(name, i):
    if i > 3:
        return
    if i == 2:
        name = name[0] + name[2:]
    elif i == 3:
        name = name + ' pictures'
    # Get the image
    url = 'https://www.bing.com/images/search?q=' + name.lower().replace(' ', '_') + '&form=HDRSC2&first=1&tsc=ImageBasicHover'
    print('Getting image from: ' + url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    pageContent=requests.get(url, timeout=2, headers=headers)
    tree = html.fromstring(pageContent.content)
    p = tree.xpath('//*[@id="mmComponent_images_2"]/ul[1]/li[1]/div/div/a/div/img/@src')
    if (p):
        if ('data:' in p[0]):
            return getFirstImageResultFor(name, i+1)
        else:
            return p[0]

    else:
        print('error getting image')


client = discord.Client()

@client.event
async def on_ready():
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
        print('Sending Commands List')
        commandsStr = '**SCU College Catholics Bot Commands:** (Last Updated: 3/26/21)\n'
        commandsStr += '**-sod**: Sends information on today\'s liturgical celebration as well as feast days, etc.\n'
        commandsStr += '**-first**: Sends today\'s first reading\n'
        commandsStr += '**-second**: Sends today\'s second reading (if there is one)\n'
        commandsStr += '**-gospel**: Sends today\'s gospel\n'
        commandsStr += '**-rosary**: Sends today\'s rosary mysteries. Include \'prayers\' with the command to get all the prayers for the rosary.\n'
        commandsStr += '**-joke**: Sends a hillarious pun or joke\n'
        commandsStr += '**-yoda** & **-jarjar**: Translates the sentence after "-yoda " (or "-jarjar") into yoda (or gungan) speak. (limited to about 5x per hour)\n' 
        commandsStr += '**-final fantasy** & **-pokemon** & **-star wars**: Sends a random ff, pokemon, or star wars character respectively. Shorthand -ff, -poke, -sw.\n' 
        commandsStr += '**keywords**: There are some (secret?) keywords the bot looks for and it may respond with a message accordingly.\n'
        commandsStr += 'LMK if there are any new features you\'d like to see! View my source at Github: https://github.com/SCU-College-Catholics/SCU_CC_DiscordBot'
        await message.channel.send(commandsStr)

    if 'happy birthday' in message.content.lower():
        print('Sending birthay wishes!')
        await message.channel.send('Happy Birthday! 🎈🎉')

    if '-sod' in message.content.lower():
        await message.channel.send('🙏Today\'s celebrations are: ')
        today = date.today()
        # YYYY/MM/DD
        d = today.strftime("%Y/%m/%d")
        # Send an api request to get the SOD
        url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/default/' + d
        # url = 'http://calapi.inadiutorium.cz/api/v0/en/calendars/default/2021/03/16'

        print('Getting Today\'s celebrations from: ' + url)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response = requests.get(url, timeout = 1, headers=headers)

        # print('Got response' + response.status_code)
        # print(response.text)

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
        print('Sending ' + own.name + ' to Purgatory')
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
        # if for some reason an insensitive joke is received,exit before sending
        if (data["safe"] == False):
            return

        print('Sending a joke')

        # Either send the 1 line or 2 line joke
        if (data["type"] == "single"):
            await message.channel.send(data["joke"])
        else:
            await message.channel.send(data["setup"])
            time.sleep(2)
            await message.channel.send(data["delivery"])

    if '-yoda' in message.content.lower():
        print('Doing yoda translation')
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
        print('Doing jar jar translation')
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
        print('Sending an affirmation')
        response = requests.get('https://www.affirmations.dev')
        if response.status_code != 200:
            print(response.status_code)
            print(response.headers)
            return
        
        data = response.json()
        await message.channel.send('Here\'s an affirmation to lift your spirits: **' + data["affirmation"] + '**')
    
    if 'tragedy' in message.content.lower() or 'sith' in message.content.lower() or 'plageuis' in message.content.lower() or 'darth' in message.content.lower():
        print('Sending the tragedy')
        await message.channel.send('Did you ever hear the Tragedy of Darth Plagueis the wise? I thought not. It\'s not a story the Jedi would tell you. It\'s a Sith legend. Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life... He had such a knowledge of the dark side that he could even keep the ones he cared about from dying. The dark side of the Force is a pathway to many abilities some consider to be unnatural. He became so powerful... the only thing he was afraid of was losing his power, which eventually, of course, he did. Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep. It\'s ironic he could save others from death, but not himself.')

    if 'minecraft' in message.content.lower() or '-ip' in message.content.lower():
        print('Sending the minecraft info')
        await message.channel.send('Our Minecraft Server (Java, MC 1.15.2): **142.44.222.25:25726**')

    if '-final fantasy' in message.content.lower() or '-ff' in message.content.lower():
        url = "https://www.moogleapi.com/api/v1/characters/random"

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response=requests.get(url, timeout=2, headers=headers)
        data = response.json()
        print('Sending an ff character')
        strng = '**' + data['name'] + '**\n'
        strng += 'Age: ' + data['age'] + ' | job: ' + data['job'] + ' | game: ' + data['origin'] + '\n'
        if (data['description']):
            strng += data['description']
        if (data['pictures']):
            await message.channel.send(data['pictures'][0]['url'])
        # await message.channel.send("https://mooglestorage.blob.core.windows.net/images/7230498b-51b2-4eff-8040-74911933c342.jpg")
        await message.channel.send(strng)

    if '-star wars' in message.content.lower() or '-sw' in message.content.lower():
        random.seed(datetime.now())
        r = random.randint(1, 82)
        url = "https://swapi.dev/api/people/" + str(r) + "/"
        print('Sending a SW char:' + url)
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response=requests.get(url, timeout=2)
        data = response.json()
        # print(data)
        # Get the home planet
        url = data['homeworld']
        response=requests.get(url, timeout=2)
        data2 = response.json()
        # Get the first film
        url = data['films'][0]
        response=requests.get(url, timeout=2)
        data3 = response.json()
        # Get the image
        name = data['name']
        
        await message.channel.send(getFirstImageResultFor(name + ' star wars', 1))


        strng = '**' + name + '**\n'
        strng += 'Birth Year: ' + data['birth_year'] + ' | homeworld: ' + data2['name'] + ' | 1st movie: ' + data3['title'] + '\n'
        # if (data['description']):
        #     strng += data['description']
        
        # await message.channel.send("https://mooglestorage.blob.core.windows.net/images/7230498b-51b2-4eff-8040-74911933c342.jpg")
        await message.channel.send(strng)

    if '-pokemon' in message.content.lower() or '-poke' in message.content.lower():
        random.seed(datetime.now())
        r = random.randint(1, 893)
        url = 'https://pokeapi.co/api/v2/pokemon/' + str(r)
        print('Sending this pokemon: ' + url)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        response=requests.get(url, timeout=2, headers=headers)
        data = response.json()
        # print(data)

        strng = '**' + data['name'] + '**\n'
        strng += 'Type: '
        for t in data['types']:
            strng += t['type']['name'] + ' '
        await message.channel.send(data['sprites']['front_default'])
        await message.channel.send(strng)



    if '-gospel' in message.content.lower():
        today = date.today()
        d = today.strftime("%m%d%y")

        # If today is sunday, we need to specify the year cycle in the url
        print(today.strftime("%A"))
        if (today.strftime("%A") == 'Sunday'):
            d += '-YearB'
        url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'
        print("Request: Gospel Reading: " + url)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        pageContent=requests.get(url, timeout=2, headers=headers)
        if pageContent.status_code != 200:
            d = today.strftime("%m%d%y")
            url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'
            pageContent=requests.get(url, timeout=2, headers=headers)
        tree = html.fromstring(pageContent.content)

        for n in range(7, 12):
            path = '//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/h3/text()'

            # Make sure the data is valid and that this is the gospel section
            if tree.xpath(path):
                if 'Gospel' == tree.xpath(path)[0]:
                    break

        # Make sure that the data is valid
        if tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/div/a/text()'):
            gospelVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/div/a/text()')[0]
        
        # The actual Gospel passage
        gospelString = ''
        i = 1
        while i:
            gospelPar = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[2]/p[' + str(i) + ']/text()')
            if (gospelPar == False or gospelPar == []):
                i = 0
                break
            for g in gospelPar:
                if g == 'OR:':
                    break
                gospelString += g
            gospelString += "\n\n"
            i += 1

        # TODO: Optimize this so that it doesn't split in between words 
        msg = '**' + today.strftime("%A %B %-d, %Y") + ' | ' + gospelVerse + '**\n' + gospelString
        n = math.ceil(len(msg) / 2000)
        for i in range(0,n):
            await message.channel.send(msg[i*2000 : (i + 1) * 2000])


    if '-reading1' in message.content.lower() or '-1st' in message.content.lower() or '-first' in message.content.lower():
        today = date.today()
        d = today.strftime("%m%d%y")

        # If today is sunday, we need to specify the year cycle in the url
        print(today.strftime("%A"))
        if (today.strftime("%A") == 'Sunday'):
            d += '-YearB'
        url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'
        print("Request: 1st Reading: " + url)

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        pageContent=requests.get(url, timeout=2, headers=headers)
        if pageContent.status_code != 200:
            d = today.strftime("%m%d%y")
            url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'
            pageContent=requests.get(url, timeout=2, headers=headers)
        tree = html.fromstring(pageContent.content)

        for n in range(4, 8):
            path = '//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/h3/text()'

            # Make sure the data is valid and that this is the gospel section
            if tree.xpath(path):
                if 'Reading I' in tree.xpath(path)[0]:
                    break

        # Make sure that the data is valid
        if tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/div/a/text()'):
            firstVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/div/a/text()')[0]
        
        # The actual Gospel passage
        firstString = ''
        i = 1
        while i:
            firstPar = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[2]/p[' + str(i) + ']/text()')

            if (firstPar == False or firstPar == []):
                i = 0
                break
            for f in firstPar:
                if f == 'OR:':
                    break
                firstString += f
            firstString += "\n\n"
            i += 1


        # TODO: Optimize this so that it doesn't split in between words 
        msg = '**' + today.strftime("%A %B %-d, %Y") + ' | ' + firstVerse + '**\n' + firstString
        n = math.ceil(len(msg) / 2000)
        for i in range(0,n):
            await message.channel.send(msg[i*2000 : (i + 1) * 2000])

    if '-reading2' in message.content.lower() or '-2nd' in message.content.lower() or '-second' in message.content.lower():
            today = date.today()
            d = today.strftime("%m%d%y")

            # If today is sunday, we need to specify the year cycle in the url
            print(today.strftime("%A"))
            if (today.strftime("%A") == 'Sunday'):
                d += '-YearB'
            url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'

            print("Request: 2nd Reading: " + url)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
            pageContent=requests.get(url, timeout=2, headers=headers)
            if pageContent.status_code != 200:
                d = today.strftime("%m%d%y")
                url = 'https://bible.usccb.org/bible/readings/' + d + '.cfm'
                pageContent=requests.get(url, timeout=2, headers=headers)
            tree = html.fromstring(pageContent.content)

            for n in range(3, 11):
                path = '//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/h3/text()'

                # Make sure the data is valid and that this is the gospel section
                if tree.xpath(path):
                    if 'Reading II' in tree.xpath(path)[0]:
                        break

            # Make sure that the data is valid
            if tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/div/a/text()'):
                firstVerse = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[1]/div/a/text()')[0]
            else:
                await message.channel.send('No Reading II for today.')
                return

            # The actual Gospel passage
            firstString = ''
            i = 1
            while i:
                firstPar = tree.xpath('//*[@id="block-usccb-readings-content"]/div/div[' + str(n) + ']/div/div/div/div/div[2]/p[' + str(i) + ']/text()')

                if (firstPar == False or firstPar == []):
                    i = 0
                    break
                for f in firstPar:
                    if f == 'OR:':
                        break
                    firstString += f
                firstString += "\n\n"
                i += 1


            # TODO: Optimize this so that it doesn't split in between words 
            msg = '**' + today.strftime("%A %B %-d, %Y") + ' | ' + firstVerse + '**\n' + firstString
            n = math.ceil(len(msg) / 2000)
            for i in range(0,n):
                await message.channel.send(msg[i*2000 : (i + 1) * 2000])
    
    if '-rosary' in message.content.lower():
        print('Sending the rosary')
        today = date.today()
        d = today.strftime("%A")
        advent = False
        lent = True
        msg = ''
        if (d == 'Monday' or d == 'Saturday' or (advent and d == 'Sunday')):
            msg += '**The Joyful Mysteries** (' + d + ')\n'
            msg += '1. The Annunciation\n'
            msg += '2. The Visitation\n'
            msg += '3. The Nativity\n'
            msg += '4. The Presentation in the Temple\n'
            msg += '5. The Finding in the Temple'
        elif (d == 'Tuesday' or d == 'Friday' or (lent and d == 'Sunday')):
            msg += '**The Sorrowful Mysteries** (' + d + ')\n'
            msg += '1. The Agony in the Garden\n'
            msg += '2. The Scourging at the Pillar\n'
            msg += '3. The Crowning with Thorns\n'
            msg += '4. The Carrying of the Cross\n'
            msg += '5. The Crucifixion and Death'
        elif (d == 'Wednesday' or (not lent and not advent and d == 'Sunday')):
            msg += '**The Glorious Mysteries** (' + d + ')\n'
            msg += '1. The Resurrection\n'
            msg += '2. The Ascension\n'
            msg += '3. The Descent of the Holy Spirit\n'
            msg += '4. The Assumption\n'
            msg += '5. The Coronation of Mary'
        else:
            msg += '**The Luminous Mysteries** (' + d + ')\n'
            msg += '1. The Baptism of Christ in the Jordan\n'
            msg += '2. The Wedding Feast at Cana\n'
            msg += '3. Jesus\' Proclamation of the Coming of the Kingdom of God\n'
            msg += '4. The Transfiguration\n'
            msg += '5. The Institution of the Eucharist'
        
        await message.channel.send(msg)

        if 'prayer' in message.content.lower():
            p=''
            p+="**The Apostles Creed**\n"
            p+="I believe in God,\n"
            p+="the Father almighty,\n"
            p+="Creator of heaven and earth,\n"
            p+="and in Jesus Christ, his only Son, our Lord,\n"
            p+="who was conceived by the Holy Spirit,\n"
            p+="born of the Virgin Mary,\n"
            p+="suffered under Pontius Pilate,\n"
            p+="was crucified, died and was buried;\n"
            p+="he descended into hell;\n"
            p+="on the third day he rose again from the dead;\n"
            p+="he ascended into heaven,\n"
            p+="and is seated at the right hand of God the Father almighty;\n"
            p+="from there he will come to judge the living and the dead.\n"
            p+="I believe in the Holy Spirit,\n"
            p+="the holy catholic Church,\n"
            p+="the communion of saints,\n"
            p+="the forgiveness of sins,\n"
            p+="the resurrection of the body,\n"
            p+="and life everlasting.\n"
            p+="Amen."
            await message.channel.send(p)

            p = ''
            p+= '**The Our Father**\n'
            p+="Our Father, who art in heaven,\n"
            p+="hallowed be thy name;\n"
            p+="thy kingdom come;\n"
            p+="thy will be done on earth as it is in heaven.\n"
            p+="Give us this day our daily bread;\n"
            p+="and forgive us our trespasses\n"
            p+="as we forgive those who trespass\n"
            p+="against us;\n"
            p+="and lead us not into temptation,\n"
            p+="but deliver us from evil.\n"
            p+="Amen"
            await message.channel.send(p)

            p = ''
            p+= '**The Hail Mary**\n'
            p+="Hail Mary, full of grace, the Lord is with you;\n"
            p+="blessed are you among women,\n"
            p+="and blessed is the fruit of your womb, Jesus.\n"
            p+="Holy Mary, Mother of God,\n"
            p+="pray for us sinners\n"
            p+="now and at the hour of our death.\n"
            p+="Amen."
            await message.channel.send(p)

            p = ''
            p+= '**The Glory Be**\n'
            p+="Glory be to the Father, the Son, and the Holy Spirit;\n"
            p+="as it was in the beginning, is now, and ever shall be,\n"
            p+="world without end.\n"
            p+="Amen."
            await message.channel.send(p)

            p = ''
            p+= '**The Hail Holy Queen**\n'
            p+="Hail, holy Queen, mother of mercy,\n"
            p+="our life, our sweetness, and our hope.\n"
            p+="To you we cry, poor banished children of Eve;\n"
            p+="to you we send up our sighs,\n"
            p+="mourning and weeping in this valley of tears.\n"
            p+="Turn, then, most gracious advocate,\n"
            p+="your eyes of mercy toward us;\n"
            p+="and after this, our exile,\n"
            p+="show unto us the blessed fruit of your womb, Jesus.\n"
            p+="O clement, O loving, O sweet Virgin Mary."
            await message.channel.send(p)
              
client.run(TOKEN)
