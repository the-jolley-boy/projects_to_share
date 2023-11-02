import discord
import os
import time
import logging
import asyncio
import psycopg as psycopg2
from psycopg import sql
from discord.ui import Button, View
import datetime
from datetime import date
import string
import io
import csv
from operator import itemgetter
from discord import app_commands

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"), filename='main.log', filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')

#Bot Token
token = ''
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

DBTable = ""
DBHost = ""
DBUsr = ""
DBPass = ""
DBPort = ""

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await client.sync()
            self.synced = True
        print(f'{self.user} has connected to Discord!')

Client = Client()
client = app_commands.CommandTree(Client)

@client.command(name = "surveyreport")
async def surveyreportall(interaction: discord.Interaction):

    if interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED":

        q1 = []
        q2 = []
        q3 = []
        q4 = []
        q5 = []
        q6 = []
        t = []

        rowcount = 0

        # Grab data from the db
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    postgreSQL_select_Query = "select * from REDACTED"
                    await curr.execute(postgreSQL_select_Query)
                    ticketsurvey = await curr.fetchall()

                    for row in ticketsurvey:
                        if row[3] != 0:
                            q1.append(row[2])
                            q2.append(row[3])
                            q3.append(row[4])
                            q4.append(row[5])
                            q5.append(row[6])
                            q6.append(row[7])
                            t.append(row[8])
                        rowcount = rowcount + 1

                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

        q2avg = round(sum(q2) / len(q2), 2)
        q3avg = round(sum(q3) / len(q3), 2)
        q4avg = round(sum(q4) / len(q4), 2)

        fulllist = []

        countq1 = 0
        countq5 = 0
        countq6 = 0

        for i in range(len(q1)):
            newlist = []
            newlist.append(str(q1[i]))
            newlist.append(str(q2[i]))
            newlist.append(str(q3[i]))
            newlist.append(str(q4[i]))
            newlist.append(str(q5[i]))
            newlist.append(str(q6[i]))
            newlist.append(str(t[i]))
            fulllist.append(newlist)
            fulllistsorted = sorted(fulllist, key = itemgetter(6))

            if str(q1[i]) != "Redacted":
                countq1 = countq1 + 1

            if "na" != str(q5[i]).lower() and "nothing" != str(q5[i]).lower():
                countq5 = countq5 + 1

            if "na" != str(q6[i]).lower() and "nothing" != str(q6[i]).lower():
                countq6 = countq6 + 1

        header = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Time']

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(header)
        writer.writerows(fulllistsorted)
        buffer.seek(0)

        rat = 100 * len(q1) / rowcount
        ratio = round(rat, 2)

        embed = discord.Embed(title="Suvey Summary" , description="See below for a brief summary." , color=0xDB0B23)
        embed.add_field(name="REDACTED", value="`" + str(len(q1)) + "/" + str(rowcount) + "` Totalling " + str(ratio) + "%" + " of tickets.", inline=False)
        embed.add_field(name="REDACTED", value="`" + str(countq1) + "/" + str(len(q1)) + "`" + " Gave their name.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(q2avg) + "`" + " Was the average score of " + str(len(q2)) + " responses." ,inline=False)
        embed.add_field(name="REDACTED", value="`" + str(q3avg) + "`" + " Was the average score of " + str(len(q3)) + " responses.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(q4avg) + "`" + " Was the average score of " + str(len(q4)) + " responses.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(countq5) + "/" + str(len(q5)) + "`" + " Gave staff commendations.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(countq6) + "/" + str(len(q6)) + "`" + " Suggested Improvements.",inline=False)

        await interaction.response.send_message(embed=embed)
        await interaction.channel.send(file=discord.File(buffer, 'surveyreport.csv'))

    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "surveyreportwelcomes")
async def surveyreportwelcomes(interaction: discord.Interaction):

    if interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED":

        q1 = []
        q2 = []
        q3 = []
        q4 = []
        q5 = []
        t = []

        rowcount = 0

        # Grab data from the db
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    postgreSQL_select_Query = "select * from REDACTED"
                    await curr.execute(postgreSQL_select_Query)
                    ticketsurvey = await curr.fetchall()

                    for row in ticketsurvey:
                        if row[3] != 0:
                            q1.append(row[2])
                            q2.append(row[3])
                            q3.append(row[4])
                            q4.append(row[5])
                            q5.append(row[6])
                            t.append(row[7])
                        rowcount = rowcount + 1

                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

        q2avg = round(sum(q2) / len(q2), 2)
        q3avg = round(sum(q3) / len(q3), 2)
        q4avg = round(sum(q4) / len(q4), 2)

        fulllist = []

        countq1 = 0
        countq5 = 0
        countq6 = 0

        for i in range(len(q1)):
            newlist = []
            newlist.append(str(q1[i]))
            newlist.append(str(q2[i]))
            newlist.append(str(q3[i]))
            newlist.append(str(q4[i]))
            newlist.append(str(q5[i]))
            newlist.append(str(t[i]))
            fulllist.append(newlist)
            fulllistsorted = sorted(fulllist, key = itemgetter(5))

            if str(q1[i]) != "Redacted":
                countq1 = countq1 + 1

            if "na" != str(q5[i]).lower() and "nothing" != str(q5[i]).lower():
                countq5 = countq5 + 1

        header = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Time']

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(header)
        writer.writerows(fulllistsorted)
        buffer.seek(0)

        rat = 100 * len(q1) / rowcount
        ratio = round(rat, 2)

        embed = discord.Embed(title="Suvey Summary" , description="See below for a brief summary." , color=0xDB0B23)
        embed.add_field(name="REDACTED", value="`" + str(len(q1)) + "/" + str(rowcount) + "` Totalling " + str(ratio) + "%" + " of tickets.", inline=False)
        embed.add_field(name="REDACTED", value="`" + str(countq1) + "/" + str(len(q1)) + "`" + " Gave their name.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(q2avg) + "`" + " Was the average score of " + str(len(q2)) + " responses." ,inline=False)
        embed.add_field(name="REDACTED", value="`" + str(q3avg) + "`" + " Was the average score of " + str(len(q3)) + " responses.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(q4avg) + "`" + " Was the average score of " + str(len(q4)) + " responses.",inline=False)
        embed.add_field(name="REDACTED", value="`" + str(countq5) + "/" + str(len(q5)) + "`" + " Suggested Improvements.",inline=False)

        await interaction.response.send_message(embed=embed)
        await interaction.channel.send(file=discord.File(buffer, 'surveyreportwelcomes.csv'))

    else:
        await interaction.response.send_message("You don't have access to this command.")

####################################################################################################
# 
# Generates the reports
#
####################################################################################################
async def report(interaction, timeframe):

    q1 = []
    q2 = []
    q3 = []
    q4 = []
    q5 = []
    q6 = []
    t = []

    rowcount = 0

    # Grab data from the db
    async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:

                postgreSQL_select_Query = "select * from REDACTED"
                await curr.execute(postgreSQL_select_Query)
                ticketsurvey = await curr.fetchall()

                for row in ticketsurvey:

                    endtime = datetime.datetime.now()
                    timestr = row[8]
                    timeobj = datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
                    timediff = endtime - timeobj

                    if row[3] != 0:

                        if timediff.total_seconds() < timeframe:
                            q1.append(row[2])
                            q2.append(row[3])
                            q3.append(row[4])
                            q4.append(row[5])
                            q5.append(row[6])
                            q6.append(row[7])
                            t.append(row[8])
                    
                    if timediff.total_seconds() < timeframe:
                        rowcount = rowcount + 1

                logging.info("Pulled values and closed")
                await conn.close()

        except Exception as e:
            logging.error(e)
            await conn.close()

    q2avg = round(sum(q2) / len(q2), 2)
    q3avg = round(sum(q3) / len(q3), 2)
    q4avg = round(sum(q4) / len(q4), 2)

    fulllist = []

    countq1 = 0
    countq5 = 0
    countq6 = 0

    for i in range(len(q1)):
        newlist = []
        newlist.append(str(q1[i]))
        newlist.append(str(q2[i]))
        newlist.append(str(q3[i]))
        newlist.append(str(q4[i]))
        newlist.append(str(q5[i]))
        newlist.append(str(q6[i]))
        newlist.append(str(t[i]))
        fulllist.append(newlist)
        fulllistsorted = sorted(fulllist, key = itemgetter(6))

        if str(q1[i]) != "Redacted":
            countq1 = countq1 + 1

        if "na" != str(q5[i]).lower() and "nothing" != str(q5[i]).lower():
            countq5 = countq5 + 1

        if "na" != str(q6[i]).lower() and "nothing" != str(q6[i]).lower():
            countq6 = countq6 + 1

    header = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Time']

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(header)
    writer.writerows(fulllistsorted)
    buffer.seek(0)

    rat = 100 * len(q1) / rowcount
    ratio = round(rat, 2)

    embed = discord.Embed(title="Suvey Summary" , description="See below for a brief summary." , color=0xDB0B23)
    embed.add_field(name="REDACTED", value="`" + str(len(q1)) + "/" + str(rowcount) + "` Totalling " + str(ratio) + "%" + " of tickets.", inline=False)
    embed.add_field(name="REDACTED", value="`" + str(countq1) + "/" + str(len(q1)) + "`" + " Gave their name.",inline=False)
    embed.add_field(name="REDACTED", value="`" + str(q2avg) + "`" + " Was the average score of " + str(len(q2)) + " responses." ,inline=False)
    embed.add_field(name="REDACTED", value="`" + str(q3avg) + "`" + " Was the average score of " + str(len(q3)) + " responses.",inline=False)
    embed.add_field(name="REDACTED", value="`" + str(q4avg) + "`" + " Was the average score of " + str(len(q4)) + " responses.",inline=False)
    embed.add_field(name="REDACTED", value="`" + str(countq5) + "/" + str(len(q5)) + "`" + " Gave staff commendations.",inline=False)
    embed.add_field(name="REDACTED", value="`" + str(countq6) + "/" + str(len(q6)) + "`" + " Suggested Improvements.",inline=False)

    await interaction.response.send_message(embed=embed)
    await interaction.channel.send(file=discord.File(buffer, 'surveyreport.csv'))

@client.command(name = "surveyreport1w")
async def surveyreport1w(interaction: discord.Interaction):

    if interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED":
        await report(interaction, 604800)
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "surveyreport1m")
async def surveyreport1m(interaction: discord.Interaction):

    if interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED":
        await report(interaction, 2630000)
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "surveyreport3m")
async def surveyreport3m(interaction: discord.Interaction):

    if interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED":
        await report(interaction, 7890000)
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "kwfrequency")
async def kwfrequency(interaction: discord.Interaction):

    if interaction.user.id == "REDACTED" or interaction.user.id == "REDACTED":
        with open("kwlist.txt", "r") as ch:
            mk = open("kwfrequency.csv", "w")
            content = ch.read()
            content = content.lower()
            content = content.translate(str.maketrans('', '', string.punctuation))
            content = content.split()
            content2 = []
            removeitems = ["i", "help", "a", "for", "need", "on", "the", "to", 
                           "with", "do", "in", "if", "you", "my", "was", "and", 
                           "can", "get", "of", "w", "some", "up", "good", "has", 
                           "or", "are", "just", "got", "an", "as", "have", "so", 
                           "me", "how", "know", "that", "it", "from", "please", 
                           "make", "sure", "who", "better", "sup", "ago", "asked", 
                           "he", "at", "same", "time", "your", "had", "about", 
                           "not", "like", "could", "also", "is", "hey", "ty", "when",
                           "im", "i'm", "what", "but", "be", "this", "want", "would",
                           "any", "1", "there", "hi"]
            for i in content:
                if i not in content2 and i not in removeitems:
                    content2.append(i)
            for i in range(0, len(content2)):
                mk.write(content2[i] + "," + str(content.count(content2[i])) + "\n")
            mk.close()
            await interaction.response.send_message("CSV", file=discord.File("kwfrequency.csv"))
        ch.close()
    else:
        await interaction.response.send_message("You don't have access to this command.")

# Bot and Site Emojis and Buttons
cybersole = '<:cybersole:732423220577173566>'
mekpreme = '<:mekpreme:614273873956831232>'
wrath = '<:wrath:619333000072790016>'
prism = '<:prism:753691950502117528>'
hayha = '<:hayha:862469783394975815>'
kylinbot = '<:kylinbot:862469783478992946>'
mekaio = '<:mekaio:862469783701028904>'
valor = '<:valoraio:862469783273734185>'
ksr = '<:ksr:862469783391961148>'

# Buttons for Topup US
fourtyButton = Button(label = "40", style = discord.ButtonStyle.grey)
fourtyNineButton = Button(label = "49", style = discord.ButtonStyle.blurple)
fourty_threeButton = Button(label = "3 Months", style = discord.ButtonStyle.grey)
fourty_sixButton = Button(label = "6 Months", style = discord.ButtonStyle.blurple)
fourty_yearButton = Button(label = "12 Months", style = discord.ButtonStyle.blurple)
fourtyNine_threeButton = Button(label = "3 Months", style = discord.ButtonStyle.link, url = "REDACTED")
fourtyNine_sixButton = Button(label = "6 Months", style = discord.ButtonStyle.link, url = "REDACTED")
fourtyNine_yearButton = Button(label = "12 Months", style = discord.ButtonStyle.link, url = "REDACTED")

# Buttons for Topup US
three_monthButton = Button(label = "3 Months", style = discord.ButtonStyle.link, url = "REDACTED")
six_monthButton = Button(label = "6 Months", style = discord.ButtonStyle.link, url = "REDACTED")

finishJd = '<:finishline:872706006092754945>'
footsites = '<:footlocker:872706006315061279>'
hibbet = '<:hibbett:872706006336024606>'
shopify = '<:shopify:872706006377984020>'
supreme = '<:supreme:872706006327656488>'
yzy = '<:yeezy:872706006461870100>'
target = '<:target:872706006474432532>'
bestbuy = '<:bestbuy:872706006243754045>'
amazon = '<:amazon:872706006457659442>'
notiLogo = '<:notifylogo:833564290225012766>'
walmart = '<:walmart:874529769000144947>'
amd = '<:AMD:909132674688491520>'
gamestop = '<:gamestop:909132708456845323>'
microsoft = '<:microsoft:909132738253164554>'

YesButton = Button(label = "Yes", style = discord.ButtonStyle.green)
NoButton = Button(label = "No", style = discord.ButtonStyle.red)
OneButton = Button(label = "1", style = discord.ButtonStyle.grey)
TwoButton = Button(label = "2", style = discord.ButtonStyle.grey)
ThreeButton = Button(label = "3", style = discord.ButtonStyle.grey)
FourButton = Button(label = "4", style = discord.ButtonStyle.grey)
FiveButton = Button(label = "5", style = discord.ButtonStyle.grey)
q2OneButton = Button(label = "1", style = discord.ButtonStyle.grey)
q2TwoButton = Button(label = "2", style = discord.ButtonStyle.grey)
q2ThreeButton = Button(label = "3", style = discord.ButtonStyle.grey)
q2FourButton = Button(label = "4", style = discord.ButtonStyle.grey)
q2FiveButton = Button(label = "5", style = discord.ButtonStyle.grey)
q3OneButton = Button(label = "1", style = discord.ButtonStyle.grey)
q3TwoButton = Button(label = "2", style = discord.ButtonStyle.grey)
q3ThreeButton = Button(label = "3", style = discord.ButtonStyle.grey)
q3FourButton = Button(label = "4", style = discord.ButtonStyle.grey)
q3FiveButton = Button(label = "5", style = discord.ButtonStyle.grey)

####################################################################################################
# Purpose: Sets the footer to all the embeds
#
#
#
# Inputs: Discord ember object
#
# Outputs: embed of the footer
#
# Future:
#
####################################################################################################
async def setFooter(embedVar):
    embedVar.set_footer(text = "Jarvis", icon_url = "https://cdn.discordapp.com/avatars/730136171983667280/7804ea245de12dd9a124e761b55eb97a.webp")
    embedVar.set_thumbnail(url = 'https://notify.org/notify.png')
    return embedVar

async def setFooterEU(embedVar):
    embedVar.set_footer(text = "Jarvis", icon_url = "https://cdn.discordapp.com/avatars/730136171983667280/7804ea245de12dd9a124e761b55eb97a.webp")
    embedVar.set_thumbnail(url = 'https://media.discordapp.net/attachments/719312417200537670/909442302366339142/NEU_NBG.png')
    return embedVar

########################################################
#CALLBACKS FOR TOPUP US
########################################################

async def fourty_callback(interaction):

    await interaction.response.edit_message(view = None)

    embedVar = discord.Embed(title="REDACTED", description='''Please react with the option that you would like to go with.
                                                                    \n\n `-` REDACTED
                                                                    \n `-` REDACTED
                                                                    ''', color=0xDB0B23)

    view = View(timeout = None)
    view.add_item(fourty_threeButton)
    view.add_item(fourty_sixButton)

    fourty_threeButton.callback = fourty_three_callback
    fourty_sixButton.callback = fourty_six_callback

    await interaction.channel.send( embed=embedVar, view = view)

async def fourty_three_callback(interaction):

    await interaction.response.edit_message(view = None)
    embedVar = discord.Embed(title="REDACTED", description="An Admin will be with you shortly, please wait.", color=0xDB0B23)

    await interaction.channel.send( embed=embedVar)
    await interaction.channel.send( "<@&1064073195533119488>")

async def fourty_six_callback(interaction):

    await interaction.response.edit_message(view = None)
    embedVar = discord.Embed(title="REDACTED", description="An Admin will be with you shortly, please wait.", color=0xDB0B23)

    await interaction.channel.send( embed=embedVar)
    await interaction.channel.send( "<@&1064073195533119488>")

async def fourtyNine_callback(interaction):

    await interaction.response.edit_message(view = None)

    embedVar = discord.Embed(title="REDACTED", description='''Please react with the option that you would like to go with.
                                                                    \n\n `-` REDACTED
                                                                    \n `-` REDACTED
                                                                    \n\n**Once you're done, please let us know your purchase email.**''', color=0xDB0B23)

    view = View(timeout = None)
    view.add_item(fourtyNine_threeButton)
    view.add_item(fourtyNine_sixButton)

    fourtyNine_threeButton.callback = fourtyNine_three_callback
    fourtyNine_sixButton.callback = fourtyNine_six_callback

    await interaction.channel.send( embed=embedVar, view = view)

async def fourtyNine_three_callback(interaction):

    await interaction.response.edit_message(view = None)
    embedVar = discord.Embed(title="REDACTED", description="Please use this link: REDACTED\n\nOnce you're done, please let us know your purchase email.", color=0xDB0B23)

    await interaction.channel.send( embed=embedVar)

async def fourtyNine_six_callback(interaction):

    await interaction.response.edit_message(view = None)
    embedVar = discord.Embed(title="REDACTED", description="Please use this link: REDACTED\n\nOnce you're done, please let us know your purchase email.", color=0xDB0B23)

    await interaction.channel.send( embed=embedVar)

####################################################################################################
# Purpose: Trigger Jarvis on messages sent by the Notify ticket bot looking for Initiating Jarvis...
#           for user opened tickets to support them
#
#
# Inputs: Discord message object
#
# Outputs: None
#
# Future:
#
####################################################################################################
@Client.event
async def on_message(message):
    guild = Client.get_guild(570142274902818816)

    #Discord Emote Id's
    alert = '<@&575144399013543977>'
    admin = '<@&1064073195533119488>'  

########################################################
# Initiates Jarvis For Topups US
########################################################
    if ('thanks for being a loyal member!' in message.content) and message.channel.category_id == 1052768590144733194 and str(message.author) == str(Client.get_user("REDACTED")):

        embedVar = discord.Embed(title="Do you pay $40 or $49 a month for your renewal?", color=0xDB0B23)

        view = View(timeout = None)
        view.add_item(fourtyButton)
        view.add_item(fourtyNineButton)

        fourtyButton.callback = fourty_callback
        fourtyNineButton.callback = fourtyNine_callback

        await message.channel.send( embed=embedVar, view = view)

########################################################
# Initiates Jarvis For Topups EU
########################################################
    if ('thanks for being a loyal member.' in message.content) and message.channel.category_id == 790097994712088576 and str(message.author) == str(Client.get_user("REDACTED")):

        embedVar = discord.Embed(title="Click The Buttons Below If You Would Like A 3 Or 6 Month Renewal.", description='''Please react with the option that you would like to go with.
                                                                        \n\n `-` REDACTED
                                                                        \n `-` REDACTED
                                                                        \n\n `-` **Once you're done, please let us know your purchase email and tag Michael. If you have questions please let us know.**
                                                                        ''', color=0x563ef0)
        await setFooterEU(embedVar)

        view = View(timeout = None)
        view.add_item(three_monthButton)
        view.add_item(six_monthButton)

        await message.channel.send( embed=embedVar, view = view)

########################################################
# Initiates Jarvis
########################################################

    if ('Initiating Jarvis...' in message.content) and str(message.author) ==  str(Client.get_user("REDACTED")):

        channelId = str(message.channel.id)

        embeds = message.embeds

        for embed in embeds:

            contentStringDesc = str(embed.description)
            contentStringLess = contentStringDesc.split(":")[1].split("⏰")[0]
            contentStringDescTrim = contentStringLess.replace('"', '').replace('**','').replace('<','').replace('\n','')

            channelId = str(message.channel.id)

            userQuestion = "**" + contentStringDescTrim + "**"

            packagekw = ["REDACTED"]
            acckw = ["REDACTED"]
            cardkw = ["REDACTED"]
            memkw = ["REDACTED"]
            otherkw = ["REDACTED"]
            botkw = ["REDACTED"]
            sitekw = ["REDACTED"]
            proxkw = ["REDACTED"]

            addend = 0

            if any(x in contentStringDesc.lower() for x in botkw) or any(x in contentStringDesc.lower() for x in sitekw) or any(x in contentStringDesc.lower() for x in memkw) or any(x in contentStringDesc.lower() for x in proxkw) or any(x in contentStringDesc.lower() for x in packagekw) or any(x in contentStringDesc.lower() for x in acckw) or any(x in contentStringDesc.lower() for x in cardkw) or any(x in contentStringDesc.lower() for x in otherkw):
                
                embedVar1 = discord.Embed(title="Talk To Support", description="A staff member will be with you shortly.\n\nPlease refer to any of the guides below to help answer your question.", color=0xDB0B23)
                await setFooter(embedVar1)

                addend = 1

                await message.channel.send( embed=embedVar1)
                await message.channel.send( alert)

            if not any(x in contentStringDesc.lower() for x in botkw) and not any(x in contentStringDesc.lower() for x in sitekw) and not any(x in contentStringDesc.lower() for x in memkw) and not any(x in contentStringDesc.lower() for x in proxkw) and not any(x in contentStringDesc.lower() for x in packagekw) and not any(x in contentStringDesc.lower() for x in acckw) and not any(x in contentStringDesc.lower() for x in cardkw) and not any(x in contentStringDesc.lower() for x in otherkw):

                embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                await setFooter(embedVar)

                embedVar1 = discord.Embed(title="Ticket Info", description="Please also check out our [FAQ](REDACTED) to see if you can get your question answered there.\n\nMember asked: " + userQuestion, color=0xDB0B23)
                await setFooter(embedVar1)

                await message.channel.send( embed=embedVar)
                await message.channel.send( alert)
                await message.channel.send( embed=embedVar1)

            # Used for Postal issues.
            if (packagekw[0] in contentStringDesc.lower() and packagekw[1] in contentStringDesc.lower()) or (packagekw[0] in contentStringDesc.lower() and packagekw[2] in contentStringDesc.lower()) or (packagekw[0] in contentStringDesc.lower() and packagekw[3] in contentStringDesc.lower()):

                embedVar = discord.Embed(title="Package issues?", description="Unfortunately we can't easily assist with package issues.\nBest plan of action is to make a claim with links below.\n\n", color=0xDB0B23)
                await setFooter(embedVar)

                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                await message.channel.send( embed=embedVar)

            # Used for Nike Accounts.
            if any(x in contentStringDesc.lower() for x in acckw):

                embedVar = discord.Embed(title="Nike Information", color=0xDB0B23)
                await setFooter(embedVar)

                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                embedVar.add_field(name = 'REDACTED', value = 'REDACTED')

                await message.channel.send( embed=embedVar)

            # Used for Card Related Questions
            if any(x in contentStringDesc.lower() for x in cardkw):

                embedVar = discord.Embed(title="Card Related Questions?", color=0xDB0B23)
                await setFooter(embedVar)

                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=False)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=False)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=False)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=False)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=False)

                await message.channel.send( embed=embedVar)

            # Used for membership stuff
            if any(x in contentStringDesc.lower() for x in memkw) and not any(x in contentStringDesc.lower() for x in botkw) and not any(x in contentStringDesc.lower() for x in sitekw) and not any(x in contentStringDesc.lower() for x in otherkw) and not any(x in contentStringDesc.lower() for x in proxkw):

                embedVar = discord.Embed(title="REDACTED", description="REDACTED", color=0xDB0B23)
                await setFooter(embedVar)

                await message.channel.send( embed=embedVar)

            # Used for other kws
            if any(x in contentStringDesc.lower() for x in otherkw):

                embedVar = discord.Embed(title="REDACTED", color=0xDB0B23)
                await setFooter(embedVar)

                if otherkw[0] in contentStringDesc.lower() or otherkw[1] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[3] in contentStringDesc.lower() or otherkw[8] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[4] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[5] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[6] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[7] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[9] in contentStringDesc.lower() or otherkw[10] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if otherkw[11] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                await message.channel.send( embed=embedVar)

            # Bots
            if any(x in contentStringDesc.lower() for x in botkw):

                embedVar = discord.Embed(title="Bot Guides", color=0xDB0B23)
                await setFooter(embedVar)

                if botkw[1] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[2] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[3] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[5] in contentStringDesc.lower() or botkw[9] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[6] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[12] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[7] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[8] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if botkw[10] in contentStringDesc.lower() or botkw[11] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                await message.channel.send( embed=embedVar)

            # Sites
            if any(x in contentStringDesc.lower() for x in sitekw):

                embedVar = discord.Embed(title="Site Guides", color=0xDB0B23)
                await setFooter(embedVar)

                if sitekw[0] in contentStringDesc.lower() or sitekw[1] in contentStringDesc.lower() or sitekw[2] in contentStringDesc.lower() or sitekw[3] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[4] in contentStringDesc.lower() or sitekw[5] in contentStringDesc.lower() or sitekw[6] in contentStringDesc.lower() or sitekw[7] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[8] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[9] in contentStringDesc.lower() or sitekw[10] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[11] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[14] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[15] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[16] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[17] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[18] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[19] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                if sitekw[20] in contentStringDesc.lower():
                    embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                await message.channel.send( embed=embedVar)

            # Proxies
            if any(x in contentStringDesc.lower() for x in proxkw):

                embedVar = discord.Embed(title="Proxies", color=0xDB0B23)
                await setFooter(embedVar)

                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)
                embedVar.add_field(name = 'REDACTED', value = 'REDACTED', inline=True)

                await message.channel.send( embed=embedVar)

            if addend == 1:
                embedVar = discord.Embed(title="REDACTED", description="REDACTED" + userQuestion, color=0xDB0B23)
                await setFooter(embedVar)

                await message.channel.send(embed=embedVar)  

    ####################################################################################################
    # 
    # Used to trigger the bot to update the DB with user info for end of ticket survey
    #
    ####################################################################################################
    if "our Staff team will be with you shortly." in message.content and message.channel.category_id == 570248275374899200:

        chid = message.channel.id
        mention = message.mentions[0]
        mentionID = message.mentions[0].id

        t = str(datetime.datetime.now())

        # Push to DB
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    #insert into the db unless already in the db in that case update
                    sql = """INSERT INTO REDACTED (id, name, q1, q2, q3, q4, q5, q6, timefinished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE set (name, q1, timefinished) = (EXCLUDED.name, EXCLUDED.q1, EXCLUDED.timefinished)"""

                    #data for the %s value
                    data = (chid, str(mentionID), str(mention), 0, 0, 0, "Nothing", "Nothing", t)
                    await curr.execute(sql, data)
                    await conn.commit()
                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

    if "Woohoo! You're now a part of the Notify community" in message.content and (message.channel.category_id == 1084368328673476608 or message.channel.category_id == 1086427580166590514 or message.channel.category_id == 1087054788300124311):

        chid = message.channel.id
        mention = message.mentions[0]
        mentionID = message.mentions[0].id

        t = str(datetime.datetime.now())

        # Push to DB
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    #insert into the db unless already in the db in that case update
                    sql = """INSERT INTO REDACTED (id, name, q1, q2, q3, q4, q5, timefinished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE set (name, q1, timefinished) = (EXCLUDED.name, EXCLUDED.q1, EXCLUDED.timefinished)"""

                    #data for the %s value
                    data = (chid, str(mentionID), str(mention), 0, 0, 0, "Nothing", t)
                    await curr.execute(sql, data)
                    await conn.commit()
                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

####################################################################################################
# 
# Initially writes survey stuff to the DB
#
####################################################################################################
@Client.event
async def on_guild_channel_create(ch):

    if ch.category_id == 570248275374899200:

        t = str(datetime.datetime.now())

        # Push to DB
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    #insert into the db unless already in the db in that case update
                    sql = """INSERT INTO REDACTED (id, name, q1, q2, q3, q4, q5, q6, timefinished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

                    #data for the %s value
                    data = (ch.id, "Nothing", "Nothing", 0, 0, 0, "Nothing", "Nothing", t)
                    await curr.execute(sql, data)
                    await conn.commit()
                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

    if ch.category_id == 1084368328673476608 or ch.category_id == 1086427580166590514 or ch.category_id == 1087054788300124311:

        t = str(datetime.datetime.now())

        # Push to DB
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    #insert into the db unless already in the db in that case update
                    sql = """INSERT INTO REDACTED (id, name, q1, q2, q3, q4, q5, timefinished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

                    #data for the %s value
                    data = (ch.id, "Nothing", "Nothing", 0, 0, 0, "Nothing", t)
                    await curr.execute(sql, data)
                    await conn.commit()
                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

####################################################################################################
# 
# Survey callbacks
#
####################################################################################################
async def write_to_db(question, payload, user):

    # Push to DB
    async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:

                postgreSQL_select_Query = "select * from REDACTED"
                await curr.execute(postgreSQL_select_Query)
                ticketsurvey = await curr.fetchall()

                for row in ticketsurvey:
                    if row[1] == user:
                        chid = row[0]

                postgreSQL_upload_Query = sql.SQL("INSERT INTO ticketsurvey (id, name, {question}) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set {question} = EXCLUDED.{question}").format(
                question = sql.Identifier(question))

                #data for the %s value
                data = (chid, user, payload)
                await curr.execute(postgreSQL_upload_Query, data)
                await conn.commit()
                logging.info("Pulled values and closed")
                await conn.close()

        except Exception as e:
            logging.error(e)
            await conn.close()

async def remove_after_complete(user):

    async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:

                postgreSQL_upload_Query = "UPDATE REDACTED SET name = %s WHERE name = %s"

                #data for the %s value
                data = ("Survey Completed", user)
                await curr.execute(postgreSQL_upload_Query, data)
                await conn.commit()
                logging.info("Pulled values and closed")
                await conn.close()

        except Exception as e:
            logging.error(e)
            await conn.close()

async def initial_func(user):

    view = View(timeout = 86400)
    view.add_item(YesButton)
    view.add_item(NoButton)

    YesButton.callback = yes_callback
    NoButton.callback = no_callback

    await user.send("REDACTED", view = view)

async def yes_callback(interaction):

    user = interaction.user

    await interaction.response.edit_message(view = None)

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = one_callback
    TwoButton.callback = two_callback
    ThreeButton.callback = three_callback
    FourButton.callback = four_callback
    FiveButton.callback = five_callback

    await user.send("REDACTED", view = view)

async def no_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q1", "Redacted", str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = one_callback
    TwoButton.callback = two_callback
    ThreeButton.callback = three_callback
    FourButton.callback = four_callback
    FiveButton.callback = five_callback

    await user.send("REDACTED", view = view)

async def one_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q2", 1, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback
    TwoButton.callback = q2two_callback
    ThreeButton.callback = q2three_callback
    FourButton.callback = q2four_callback
    FiveButton.callback = q2five_callback

    await user.send("REDACTED", view = view)

async def two_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q2", 2, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback
    TwoButton.callback = q2two_callback
    ThreeButton.callback = q2three_callback
    FourButton.callback = q2four_callback
    FiveButton.callback = q2five_callback

    await user.send("REDACTED", view = view)

async def three_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q2", 3, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback
    TwoButton.callback = q2two_callback
    ThreeButton.callback = q2three_callback
    FourButton.callback = q2four_callback
    FiveButton.callback = q2five_callback

    await user.send("REDACTED", view = view)

async def four_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q2", 4, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback
    TwoButton.callback = q2two_callback
    ThreeButton.callback = q2three_callback
    FourButton.callback = q2four_callback
    FiveButton.callback = q2five_callback

    await user.send("REDACTED", view = view)

async def five_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q2", 5, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback
    TwoButton.callback = q2two_callback
    ThreeButton.callback = q2three_callback
    FourButton.callback = q2four_callback
    FiveButton.callback = q2five_callback

    await user.send("REDACTED", view = view)

async def q2one_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q3", 1, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback
    TwoButton.callback = q3two_callback
    ThreeButton.callback = q3three_callback
    FourButton.callback = q3four_callback
    FiveButton.callback = q3five_callback

    await user.send("REDACTED", view = view)

async def q2two_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q3", 2, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback
    TwoButton.callback = q3two_callback
    ThreeButton.callback = q3three_callback
    FourButton.callback = q3four_callback
    FiveButton.callback = q3five_callback

    await user.send("REDACTED", view = view)

async def q2three_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q3", 3, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback
    TwoButton.callback = q3two_callback
    ThreeButton.callback = q3three_callback
    FourButton.callback = q3four_callback
    FiveButton.callback = q3five_callback

    await user.send("REDACTED", view = view)

async def q2four_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q3", 4, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback
    TwoButton.callback = q3two_callback
    ThreeButton.callback = q3three_callback
    FourButton.callback = q3four_callback
    FiveButton.callback = q3five_callback

    await user.send("REDACTED", view = view)

async def q2five_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q3", 5, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback
    TwoButton.callback = q3two_callback
    ThreeButton.callback = q3three_callback
    FourButton.callback = q3four_callback
    FiveButton.callback = q3five_callback

    await user.send("REDACTED", view = view)

async def q3one_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q4", 1, str(userID))

    await question5_6(user, userID)

async def q3two_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q4", 2, str(userID))

    await question5_6(user, userID)

async def q3three_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q4", 3, str(userID))

    await question5_6(user, userID)

async def q3four_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q4", 4, str(userID))

    await question5_6(user, userID)

async def q3five_callback(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db("q4", 5, str(userID))

    await question5_6(user, userID)

async def question5_6(user, userID):

    def check(m):
        return user == m.author and isinstance(m.channel, discord.DMChannel)

    await user.send("REDACTED")
    try:
        q5 = await Client.wait_for("message", timeout = 300, check = check)
    except asyncio.TimeoutError:
        await write_to_db("q5", "NA", str(userID))
        await user.send("Didn't get an input, so moving to the last question.")
    else:
        await write_to_db("q5", q5.content, str(userID))

    await user.send("REDACTED")
    try:
        q6 = await Client.wait_for("message", timeout = 300, check = check)
    except asyncio.TimeoutError:
        await write_to_db("q6", "NA", str(userID))
        await user.send("Didn't get an input.")
        t = str(datetime.datetime.now())
        await write_to_db("timefinished", t, str(userID))
        await remove_after_complete(str(userID))
        await user.send("Thanks for taking part in the feedback form!")
    else:
        await write_to_db("q6", q6.content, str(userID))
        t = str(datetime.datetime.now())
        await write_to_db("timefinished", t, str(userID))
        await remove_after_complete(str(userID))
        await user.send("Thanks for taking part in the feedback form!")

async def write_to_db_welcomes(question, payload, user):

    # Push to DB
    async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:

                postgreSQL_select_Query = "select * from REDACTED"
                await curr.execute(postgreSQL_select_Query)
                ticketsurvey = await curr.fetchall()

                for row in ticketsurvey:
                    if row[1] == user:
                        chid = row[0]

                postgreSQL_upload_Query = sql.SQL("INSERT INTO REDACTED (id, name, {question}) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set {question} = EXCLUDED.{question}").format(
                question = sql.Identifier(question))

                #data for the %s value
                data = (chid, user, payload)
                await curr.execute(postgreSQL_upload_Query, data)
                await conn.commit()
                logging.info("Pulled values and closed")
                await conn.close()

        except Exception as e:
            logging.error(e)
            await conn.close()

async def remove_after_complete_welcomes(user):

    async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
        try:
            logging.info("Opened database successfully")
            async with conn.cursor() as curr:

                postgreSQL_upload_Query = "UPDATE REDACTED SET name = %s WHERE name = %s"

                #data for the %s value
                data = ("Survey Completed", user)
                await curr.execute(postgreSQL_upload_Query, data)
                await conn.commit()
                logging.info("Pulled values and closed")
                await conn.close()
        except Exception as e:
            logging.error(e)
            await conn.close()

async def initial_func_welcomes(user):

    view = View(timeout = 86400)
    view.add_item(YesButton)
    view.add_item(NoButton)

    YesButton.callback = yes_callback_welcomes
    NoButton.callback = no_callback_welcomes

    await user.send("REDACTED", view = view)

async def yes_callback_welcomes(interaction):
    user = interaction.user

    await interaction.response.edit_message(view = None)

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = one_callback_welcomes
    TwoButton.callback = two_callback_welcomes
    ThreeButton.callback = three_callback_welcomes
    FourButton.callback = four_callback_welcomes
    FiveButton.callback = five_callback_welcomes

    await user.send("REDACTED", view = view)

async def no_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q1", "Redacted", str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = one_callback_welcomes
    TwoButton.callback = two_callback_welcomes
    ThreeButton.callback = three_callback_welcomes
    FourButton.callback = four_callback_welcomes
    FiveButton.callback = five_callback_welcomes

    await user.send("REDACTED", view = view)

async def one_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q2", 1, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback_welcomes
    TwoButton.callback = q2two_callback_welcomes
    ThreeButton.callback = q2three_callback_welcomes
    FourButton.callback = q2four_callback_welcomes
    FiveButton.callback = q2five_callback_welcomes

    await user.send("REDACTED", view = view)

async def two_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q2", 2, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback_welcomes
    TwoButton.callback = q2two_callback_welcomes
    ThreeButton.callback = q2three_callback_welcomes
    FourButton.callback = q2four_callback_welcomes
    FiveButton.callback = q2five_callback_welcomes

    await user.send("REDACTED", view = view)

async def three_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q2", 3, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback_welcomes
    TwoButton.callback = q2two_callback_welcomes
    ThreeButton.callback = q2three_callback_welcomes
    FourButton.callback = q2four_callback_welcomes
    FiveButton.callback = q2five_callback_welcomes

    await user.send("REDACTED", view = view)

async def four_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q2", 4, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback_welcomes
    TwoButton.callback = q2two_callback_welcomes
    ThreeButton.callback = q2three_callback_welcomes
    FourButton.callback = q2four_callback_welcomes
    FiveButton.callback = q2five_callback_welcomes

    await user.send("REDACTED", view = view)

async def five_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q2", 5, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q2one_callback_welcomes
    TwoButton.callback = q2two_callback_welcomes
    ThreeButton.callback = q2three_callback_welcomes
    FourButton.callback = q2four_callback_welcomes
    FiveButton.callback = q2five_callback_welcomes

    await user.send("REDACTED", view = view)

async def q2one_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q3", 1, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback_welcomes
    TwoButton.callback = q3two_callback_welcomes
    ThreeButton.callback = q3three_callback_welcomes
    FourButton.callback = q3four_callback_welcomes
    FiveButton.callback = q3five_callback_welcomes

    await user.send("REDACTED", view = view)

async def q2two_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q3", 2, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback_welcomes
    TwoButton.callback = q3two_callback_welcomes
    ThreeButton.callback = q3three_callback_welcomes
    FourButton.callback = q3four_callback_welcomes
    FiveButton.callback = q3five_callback_welcomes

    await user.send("REDACTED", view = view)

async def q2three_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q3", 3, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback_welcomes
    TwoButton.callback = q3two_callback_welcomes
    ThreeButton.callback = q3three_callback_welcomes
    FourButton.callback = q3four_callback_welcomes
    FiveButton.callback = q3five_callback_welcomes

    await user.send("REDACTED", view = view)

async def q2four_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q3", 4, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback_welcomes
    TwoButton.callback = q3two_callback_welcomes
    ThreeButton.callback = q3three_callback_welcomes
    FourButton.callback = q3four_callback_welcomes
    FiveButton.callback = q3five_callback_welcomes

    await user.send("REDACTED", view = view)

async def q2five_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q3", 5, str(userID))

    view = View(timeout = 86400)
    view.add_item(OneButton)
    view.add_item(TwoButton)
    view.add_item(ThreeButton)
    view.add_item(FourButton)
    view.add_item(FiveButton)

    OneButton.callback = q3one_callback_welcomes
    TwoButton.callback = q3two_callback_welcomes
    ThreeButton.callback = q3three_callback_welcomes
    FourButton.callback = q3four_callback_welcomes
    FiveButton.callback = q3five_callback_welcomes

    await user.send("REDACTED", view = view)

async def q3one_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q4", 1, str(userID))

    await question5_welcomes(user, userID)

async def q3two_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q4", 2, str(userID))

    await question5_welcomes(user, userID)

async def q3three_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q4", 3, str(userID))

    await question5_welcomes(user, userID)

async def q3four_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q4", 4, str(userID))

    await question5_welcomes(user, userID)

async def q3five_callback_welcomes(interaction):
    user = interaction.user
    userID = interaction.user.id

    await interaction.response.edit_message(view = None)

    await write_to_db_welcomes("q4", 5, str(userID))

    await question5_welcomes(user, userID)

async def question5_welcomes(user, userID):

    def check(m):
        return user == m.author and isinstance(m.channel, discord.DMChannel)

    await user.send("REDACTED")
    try:
        q6 = await Client.wait_for("message", timeout = 300, check = check)
    except asyncio.TimeoutError:
        await write_to_db_welcomes("q5", "NA", str(userID))
        await user.send("Didn't get an input.")
        t = str(datetime.datetime.now())
        await write_to_db_welcomes("timefinished", t, str(userID))
        await remove_after_complete_welcomes(str(userID))
        await user.send("Thanks for taking part in the feedback form!")
    else:
        await write_to_db_welcomes("q5", q6.content, str(userID))
        t = str(datetime.datetime.now())
        await write_to_db_welcomes("timefinished", t, str(userID))
        await remove_after_complete_welcomes(str(userID))
        await user.send("Thanks for taking part in the feedback form!")

####################################################################################################
# 
# Send the end of ticket survey and all the questions, also writes all the answers to the DB
#
####################################################################################################
@Client.event
async def on_guild_channel_delete(ch):

    guild = Client.get_guild(REDACTED)

    if ch.category_id == REDACTED:

        chid = ch.id
        uid = ""
        
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    postgreSQL_select_Query = "select * from REDACTED"
                    await curr.execute(postgreSQL_select_Query)
                    ticketsurvey = await curr.fetchall()

                    for row in ticketsurvey:
                        if row[0] == chid:
                            uid = row[1]

                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

        print("Member: " + uid)

        if uid != "Nothing":
            u = int(uid)
            if guild.get_member(u) is not None:
                user = guild.get_member(u)

                print("Member element: " + str(user) + ", DM attempt")

                try:
                    await user.send("**Please help us improve our support by giving feedback.** \nIt will take just 30 seconds. Survey expires after 24 hours.")
                    print("DM sent")
                except Exception as e:
                    print("User cannot be DM'd. (Support Tickets)")
                    print(e)
                    return

                await initial_func(user)
            else:
                print("member is not in Notify anymore.")
        else:
            print("ticket made when bot/survey was not setup. (Support Tickets)")

    if ch.category_id == REDACTED or ch.category_id == REDACTED or ch.category_id == REDACTED:

        chid = ch.id
        uid = ""
        
        async with await psycopg2.AsyncConnection.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort) as conn:
            try:
                logging.info("Opened database successfully")
                async with conn.cursor() as curr:

                    postgreSQL_select_Query = "select * from REDACTED"
                    await curr.execute(postgreSQL_select_Query)
                    ticketsurvey = await curr.fetchall()

                    for row in ticketsurvey:
                        if row[0] == chid:
                            uid = row[1]

                    logging.info("Pulled values and closed")
                    await conn.close()

            except Exception as e:
                logging.error(e)
                await conn.close()

        print("Member (Welcomes): " + uid)

        if uid != "Nothing":
            u = int(uid)
            if guild.get_member(u) is not None:
                user = guild.get_member(u)

                print("Member element: " + str(user) + ", DM attempt")

                try:
                    await user.send("**Please help us improve our support by giving feedback.** \nIt will take just 30 seconds. Survey expires after 24 hours.")
                    print("DM sent")
                except Exception as e:
                    print("User cannot be DM'd. (Support Tickets)")
                    print(e)
                    return

                await initial_func_welcomes(user)
            else:
                print("member is not in Notify anymore.")
        else:
            print("Ticket made when bot/survey was not setup. (Welcome Tickets)")

####################################################################################################
# 
# Callbacks for new members
#
####################################################################################################
async def brandNew_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = discord.Embed(title="Newbie", description="""How exciting! Just getting into reselling is an awesome feeling. I know joining a reselling group can be slightly overwhelming with all the channels but rest assured, we are here to help. Our goal is to have you leaving after the 48 hours fully confident navigating our servers and understanding what we offer.""", color=0xDB0B23)
    await setFooter(embedVar)

    await interaction.channel.send( embed=embedVar)

async def beginner_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = discord.Embed(title="Beginner", description="""We're glad you joined Notify to continue your craft! Although you're not completely new to reselling and your knowledge may be limited,  we want to get you on the right path to accel your reselling career. Our goal is to have you leaving after the 48 hours fully confident navigating our servers and understanding what we offer.""", color=0xDB0B23)
    await setFooter(embedVar)

    await interaction.channel.send( embed=embedVar)

async def intermediate_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = discord.Embed(title="Intermediate", description="""Notify is happy to have you and excited to help your business take off! With your prior knowledge, you might know your way around most group and channels. However, we know the layout differs from group to group. We want to take this 48 hours to make sure you fully understand what we have and where channels are located.""", color=0xDB0B23)
    await setFooter(embedVar)

    await interaction.channel.send( embed=embedVar)

async def advanced_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = discord.Embed(title="Advanced", description="""You've joined the best! Were happy you chose to bring your talents to Notify! If you want a quick run down of the channels, we're more than happy to do that for you. We dont want to bore you with the small talk since you already have most the knowledge. But if there is anything we can help you with to make your transition to Notify easier, please let us know.""", color=0xDB0B23)
    await setFooter(embedVar)

    await interaction.channel.send( embed=embedVar)

####################################################################################################
# 
# Creates channel with member that just joined.
#
####################################################################################################

customizeButton = Button(label = "Customize Channels", style = discord.ButtonStyle.grey, emoji = "⭐", url = "REDACTED")
supportButton = Button(label = "Personalized Support", style = discord.ButtonStyle.grey, emoji = "🧠", url = "REDACTED")
jumpstartButton = Button(label = "Getting Started", style = discord.ButtonStyle.grey, url = "REDACTED")

@Client.event
async def on_member_join(member):

    guild = Client.get_guild(REDACTED)
    user = member
    dooleyId = str(REDACTED)
    endlessID = str(REDACTED)
    dooley = await Client.fetch_user(dooleyId)
    endless = await Client.fetch_user(endlessID)
    kianId = str(REDACTED)
    kian = await Client.fetch_user(kianId)
    cat = discord.utils.get(guild.categories, id = REDACTED)
    cat2 = discord.utils.get(guild.categories, id = REDACTED)
    cat3 = discord.utils.get(guild.categories, id = REDACTED)

    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                        dooley: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                        endless: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                        kian: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                    }

    try:
        ch = await guild.create_text_channel("welcome-" + str(user), overwrites = overwrites, category = cat)
    except Exception as e:
        logging.info("Error, exception 1: " + str(e))
        if "Maximum number of channels in category reached (50)" in str(e):
            try:
                ch = await guild.create_text_channel("welcome-" + str(user), overwrites = overwrites, category = cat2)
            except Exception as e:
                logging.info("Error, exception 2: " + str(e))
                if "Maximum number of channels in category reached (50)" in str(e):
                    try:
                        ch = await guild.create_text_channel("welcome-" + str(user), overwrites = overwrites, category = cat3)
                    except Exception as e:
                        logging.info("Error, exception 3: " + str(e))
                        print("Error, final exception: " + str(e))

    # \n**To help us better understand your level of experience, please select the button below that corresponds to your reselling expertise:**
    # \n> 🆕**Newbie:** Welcome to your first reselling group! You're starting with a clean slate and have no prior knowledge of what these groups offer. Don't worry, we'll teach you everything from the basics.
    # \n> 🚶**Beginner:** You've dabbled in reselling before but want to take things a little more seriously. You understand the basics of what reselling groups offer and are ready to learn more.
    # \n> 🏃**Intermediate:** You have a fair amount of reselling experience and are knowledgeable of what reselling groups offer. You're ready to take your business to the next level and we're here to help you get there.
    # \n> 🏆**Advanced:** You're a reselling pro with extensive knowledge of what reselling groups offer. You've gained immense experience through various avenues and don't need much guidance. You're just looking to enjoy the most elite reselling group around."""

    sendEmbed = discord.Embed(title="Welcome " + str(user.name) + " 👋", description="""
                                \nOur <@&570142915326771218> is always here:\n`•` Customize the channels you see <#1091086648734916758>\n`•` Need 24/7 support? <#712154540576866354>\n`•` Get personalized support: <#915302513127874611>\n`•` Introduce yourself: <#992842655346196490>\n`•` Download our Mobile App: <#991577591158947921>\n`•` Jumpstart your journey: <#598105432103583744> \n\n **Note:** You **must** respond in this welcome ticket to receive chat access.""", color=0xDB0B23)
    await setFooter(sendEmbed)

    view = View(timeout = None)
    view.add_item(customizeButton)
    view.add_item(supportButton)
    view.add_item(jumpstartButton)

    # customizeButton.callback = brandNew_callback
    # supportButton.callback = beginner_callback
    # jumpstartButton.callback = intermediate_callback

    await ch.send("**Woohoo! You're now a part of the Notify community** <@!" + str(user.id) + ">!")
    await ch.send( embed=sendEmbed, view = view)

Client.run(token)
