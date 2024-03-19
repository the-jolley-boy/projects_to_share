import discord
import os
import time
import logging
import asyncio
from discord.ui import Button, View
import datetime
from datetime import date
import io
from discord import app_commands
from dotenv import load_dotenv

from database import dbaccess
from utils import survey_utils
from embeds import embeds

log_file_path = os.path.join('logs', 'jarvis.log')
logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"), filename=log_file_path, filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')

#Bot Token
load_dotenv()
token = os.environ.get('JARVIS_TOKEN')
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

KIANROLE = int(os.environ.get('KIANROLE'))
MICHAELROLE = int(os.environ.get('MICHAELROLE'))
DOOLEYROLE = int(os.environ.get('DOOLEYROLE'))

ALERT = os.environ.get('ALERT')
ADMIN = os.environ.get('ADMIN')

TICKETBOTID = int(os.environ.get('TICKETBOTID'))
LOYALMEMBERUSCATID = int(os.environ.get('LOYALMEMBERUSCATID'))
LOYALMEMBEREUCATID = int(os.environ.get('LOYALMEMBEREUCATID'))

TICKETCATEGORYID = int(os.environ.get('TICKETCATEGORYID'))
NEWMEMBERCATLIST = [int(os.environ.get('NEWMEMBERCATID1')),int(os.environ.get('NEWMEMBERCATID2')),int(os.environ.get('NEWMEMBERCATID3'))]

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

        await survey_utils.set_vars(Client)

        print(f'{self.user} has connected to Discord!')

Client = Client()
client = app_commands.CommandTree(Client)

# Buttons for Topup US
fourtyButton = Button(label = "40", style = discord.ButtonStyle.grey)
fourtyNineButton = Button(label = "49", style = discord.ButtonStyle.blurple)
fourty_threeButton = Button(label = "3 Months", style = discord.ButtonStyle.grey)
fourty_sixButton = Button(label = "6 Months", style = discord.ButtonStyle.blurple)
fourty_yearButton = Button(label = "12 Months", style = discord.ButtonStyle.blurple)
fourtyNine_threeButton = Button(label = "3 Months", style = discord.ButtonStyle.link, url = "https://notify.org/3m-top-up")
fourtyNine_sixButton = Button(label = "6 Months", style = discord.ButtonStyle.link, url = "https://notify.org/6m-top-up")
fourtyNine_yearButton = Button(label = "12 Months", style = discord.ButtonStyle.link, url = "https://notify.org/12m-top-up")

####################################################################################################
# 
# Commands for Survey Stuff
#
####################################################################################################
@client.command(name="surveyreport")
async def survey_report_all(interaction: discord.Interaction):
    if interaction.user.id in [KIANROLE, MICHAELROLE]:
        await survey_utils.generate_survey_report(
            interaction,
            "select q1, q2, q3, q4, q5, q6, timefinished from ticketsurvey where q2 != 0",
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Time"],
            "surveyreport.csv",
            "Q6: Is there anything you feel we can improve on regarding support?"
        )
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name="surveyreportwelcomes")
async def survey_report_welcomes(interaction: discord.Interaction):
    if interaction.user.id in [KIANROLE, MICHAELROLE, DOOLEYROLE]:
        await survey_utils.generate_survey_report(
            interaction,
            "select q1, q2, q3, q4, q5, timefinished from ticketsurveywelcomes where q2 != 0",
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Time"],
            "surveyreportwelcomes.csv"
        )
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "surveyreport1w")
async def surveyreport1w(interaction: discord.Interaction):

    if interaction.user.id in [KIANROLE, MICHAELROLE]:
        await survey_utils.generate_survey_report(
            interaction,
            "select q1, q2, q3, q4, q5, q6, timefinished from ticketsurvey where q2 != 0 AND TO_TIMESTAMP(timefinished, 'YYYY-MM-DD HH24:MI:SS.US') >= NOW() - INTERVAL '{604800} seconds'",
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Time"],
            "surveyreport.csv",
            "Q6: Is there anything you feel we can improve on regarding support?",
        )
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "surveyreport1m")
async def surveyreport1m(interaction: discord.Interaction):

    if interaction.user.id in [KIANROLE, MICHAELROLE]:
        await survey_utils.generate_survey_report(
            interaction,
            "select q1, q2, q3, q4, q5, q6, timefinished from ticketsurvey where q2 != 0 AND TO_TIMESTAMP(timefinished, 'YYYY-MM-DD HH24:MI:SS.US') >= NOW() - INTERVAL '{2630000} seconds'",
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Time"],
            "surveyreport.csv",
            "Q6: Is there anything you feel we can improve on regarding support?",
        )
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "surveyreport3m")
async def surveyreport3m(interaction: discord.Interaction):

    if interaction.user.id in [KIANROLE, MICHAELROLE]:
        await survey_utils.generate_survey_report(
            interaction,
            "select q1, q2, q3, q4, q5, q6, timefinished from ticketsurvey where q2 != 0 AND TO_TIMESTAMP(timefinished, 'YYYY-MM-DD HH24:MI:SS.US') >= NOW() - INTERVAL '{7890000} seconds'",
            ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Time"],
            "surveyreport.csv",
            "Q6: Is there anything you feel we can improve on regarding support?",
        )
    else:
        await interaction.response.send_message("You don't have access to this command.")

####################################################################################################
# 
# on_message used to start many different functions of the bot
#
####################################################################################################
@Client.event
async def on_message(message):

    # Used 3x, so set to a variable for cleanliness
    is_ticket_bot = str(message.author) == str(Client.get_user(TICKETBOTID))

    # Initiates Jarvis For Topups US
    if ('thanks for being a loyal member!' in message.content) and message.channel.category_id == LOYALMEMBERUSCATID and is_ticket_bot:

        embedVar = await embeds.loyalMemberUS()

        view = View(timeout = None)
        view.add_item(fourtyButton)
        view.add_item(fourtyNineButton)

        fourtyButton.callback = fourty_callback
        fourtyNineButton.callback = fourtyNine_callback

        await message.channel.send(embed=embedVar, view=view)

    # Initiates Jarvis For Topups EU
    if ('thanks for being a loyal member.' in message.content) and message.channel.category_id == LOYALMEMBEREUCATID and is_ticket_bot:

        embedVar = await embeds.loyalMemberEU()

        view = View(timeout = None)
        view.add_item(Button(label = "3 Months", style = discord.ButtonStyle.link, url = "https://notify.org/eu-3m-top-up"))
        view.add_item(Button(label = "6 Months", style = discord.ButtonStyle.link, url = "https://notify.org/eu-6m-top-up"))

        await message.channel.send( embed=embedVar, view = view)

    # Initiates Jarvis
    if ('Initiating Jarvis...' in message.content) and is_ticket_bot:

        #Sets db vars.
        chid = message.channel.id
        mention = str(message.mentions[0])
        mentionID = str(message.mentions[0].id)

        t = str(datetime.datetime.now())

        query = """INSERT INTO ticketsurvey (id, name, q1, q2, q3, q4, q5, q6, timefinished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE set (name, q1, timefinished) = (EXCLUDED.name, EXCLUDED.q1, EXCLUDED.timefinished)"""
        data = (chid, mentionID, mention, 0, 0, 0, "Nothing", "Nothing", t)

        await dbaccess.write_data(query, data)

        for embed in message.embeds:

            content = str(embed.title).split("Support Topic:")[1]
            user_question = f"**{content}**"

            packagekw = ["package","shoes","item","stolen","missing","lost"]
            acckw = ["nike accounts", "nike"]
            cardkw = ["privacy","amex","slash","eno","mastercard","tradeshift","stripe","visa","citi","vcc"]
            memkw = ["cancel","break","vacation","pause","og role","membership"]
            otherkw = ["notify app","notify anywhere","emerging","notify tools","notify helper","aycd","aws","ebay","notify toolbox","automations","autos","aycd ai"]
            botkw = ["balko","cyber","prism","hayha","kylinbot","mekaio","ksr","valor","mek","chegg","cheggaio","refract"]
            sitekw = ["finishline","finish line","fnl","jd","footsites","foots","ftl","champs","hibbett","shopify","shop","supreme"," ys","yeezy supply","target","bestbuy","amazon","walmart","amd","gamestop","microsoft"]
            proxkw = ["proxies","proxy","resi","residential","isp","isps","subnet"]

            category_keywords = {
                "Bot": botkw,
                "Site": sitekw,
                "Membership": memkw,
                "Proxies": proxkw,
                "Package": packagekw,
                "Accounts": acckw,
                "Cards": cardkw,
                "Other": otherkw
            }

            # Main embeds to send in each ticket.
            embedVarFirst = await embeds.talkToSupport()
            embedVarLast = await embeds.ticketInfo(user_question)

            embeds_to_send = []
            addend = 0

            # Collects any extra needed embeds
            for category, keywords in category_keywords.items():
                if any(keyword in content.lower() for keyword in keywords):
                    if category == "Package":
                        if any(keyword in content.lower() for keyword in packagekw[:3]) and any(keyword in content.lower() for keyword in packagekw[3:]):
                            embedVar = await embeds.shipping()
                            embeds_to_send.append(embedVar)
                    if category == "Accounts":
                        embedVar = await embeds.nike()
                        embeds_to_send.append(embedVar)
                    if category == "Cards":
                        embedVar = await embeds.creditCards()
                        embeds_to_send.append(embedVar)
                    if category == "Membership":
                        embedVar = await embeds.membership()
                        embeds_to_send.append(embedVar)
                    if category == "Proxies":
                        embedVar = await embeds.proxy()
                        embeds_to_send.append(embedVar)
                    if category == "Other":
                        embedVar = await embeds.other(content, otherkw)
                        embeds_to_send.append(embedVar)
                    if category == "Bot":
                        embedVar = await embeds.bots(content, botkw)
                        embeds_to_send.append(embedVar)
                    if category == "Site":
                        embedVar = await embeds.sites(content, sitekw)
                        embeds_to_send.append(embedVar)

            # Sends initial embed to ping staff, then relevant embeds to the kws, then the final embed.
            # Initial
            await message.channel.send(embed=embedVarFirst)
            await message.channel.send(ALERT)

            # Relevant content
            for emb in embeds_to_send:
                await message.channel.send(embed=emb)

            # Final embed with FAQ and user question
            await message.channel.send(embed=embedVarLast)     

    if "Woohoo! You're now a part of the Notify community" in message.content and message.channel.category_id in NEWMEMBERCATLIST:

        chid = message.channel.id
        mention = message.mentions[0]
        mentionID = message.mentions[0].id

        t = str(datetime.datetime.now())

        query = """INSERT INTO ticketsurveywelcomes (id, name, q1, q2, q3, q4, q5, timefinished) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE set (name, q1, timefinished) = (EXCLUDED.name, EXCLUDED.q1, EXCLUDED.timefinished)"""
        data = (chid, str(mentionID), str(mention), 0, 0, 0, "Nothing", t)

        await dbaccess.write_data(query, data)

@Client.event
async def on_guild_channel_delete(ch):

    GUILD = Client.get_guild(int(os.environ.get('NOTIFYGUILDID')))
    category_id = ch.category_id
    chid = ch.id

    # Gets the uid related to the channel id of the ticket, then attempts a dm, if successful it will send the survey to the user to complete.
    if category_id == TICKETCATEGORYID:

        uid = ""
        query = "select * from ticketsurvey where id = %s"

        ticketsurvey = await dbaccess.get_data(query, (chid,))
        
        for row in ticketsurvey:
            uid = row[1]

        print("Member: " + uid)

        await survey_utils.send_survey(uid, GUILD, 0)

    # Gets the uid related to the channel id of the welcome ticket, then attempts a dm, if successful it will send the survey to the user to complete.
    if category_id in NEWMEMBERCATLIST:

        uid = ""
        query = "select * from ticketsurveywelcomes where id = %s"

        ticketsurvey = await dbaccess.get_data(query, (chid,))
        
        for row in ticketsurvey:
            uid = row[1]

        print("Member (Welcomes): " + uid)

        await survey_utils.send_survey(uid, GUILD, 1)

# Creates channel with welcome ticket for member that just joined.
@Client.event
async def on_member_join(member):

    GUILD = Client.get_guild(int(os.environ.get('NOTIFYGUILDID')))

    dooley = await Client.fetch_user(str(DOOLEYROLE))
    endless = await Client.fetch_user(str(517856488652275714))
    kian = await Client.fetch_user(str(KIANROLE))

    overwrites={
                    GUILD.default_role: discord.PermissionOverwrite(read_messages=False),
                    GUILD.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    dooley: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                    endless: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                    kian: discord.PermissionOverwrite(read_messages=True, manage_channels=True),
                }

    try:
        ch = await GUILD.create_text_channel("welcome-" + str(member), overwrites=overwrites, category=discord.utils.get(GUILD.categories, id=1084368328673476608))
    except Exception as e:
        logging.info("Error, exception 1: " + str(e))
        if "Maximum number of channels in category reached (50)" in str(e):
            try:
                ch = await GUILD.create_text_channel("welcome-" + str(member), overwrites=overwrites, category=discord.utils.get(GUILD.categories, id=1086427580166590514))
            except Exception as e:
                logging.info("Error, exception 2: " + str(e))
                if "Maximum number of channels in category reached (50)" in str(e):
                    try:
                        ch = await GUILD.create_text_channel("welcome-" + str(member), overwrites=overwrites, category=discord.utils.get(GUILD.categories, id=1087054788300124311))
                    except Exception as e:
                        logging.info("Error, exception 3: " + str(e))
                        print("Error, final exception: " + str(e))

    embedVar = await embeds.welcome_ticket(member)

    view = View(timeout=None)
    view.add_item(Button(label="Customize Channels", style=discord.ButtonStyle.grey, emoji="⭐", url="https://discord.com/channels/570142274902818816/1091086648734916758"))
    view.add_item(Button(label="Personalized Support", style=discord.ButtonStyle.grey, emoji="🧠", url="https://discord.com/channels/570142274902818816/915302513127874611"))
    view.add_item(Button(label="Getting Started", style=discord.ButtonStyle.grey, url="https://discord.com/channels/570142274902818816/598105432103583744"))

    await ch.send("**Woohoo! You're now a part of the Notify community** <@!" + str(member.id) + ">!")
    await ch.send(embed=embedVar, view=view)

########################################################
#CALLBACKS FOR TOPUP US
########################################################
async def fourty_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = await embeds.topup_us_40()

    view = View(timeout = None)
    view.add_item(fourty_threeButton)
    view.add_item(fourty_sixButton)

    fourty_threeButton.callback = fourty_three_callback
    fourty_sixButton.callback = fourty_six_callback

    await interaction.channel.send( embed=embedVar, view = view)

async def fourty_three_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = await embeds.topup_us_40_final("3")

    await interaction.channel.send(embed=embedVar)
    await interaction.channel.send(ADMIN)

async def fourty_six_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = await embeds.topup_us_40_final("6")

    await interaction.channel.send(embed=embedVar)
    await interaction.channel.send(ADMIN)

async def fourtyNine_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = await embeds.topup_us_49()

    view = View(timeout = None)
    view.add_item(fourtyNine_threeButton)
    view.add_item(fourtyNine_sixButton)

    fourtyNine_threeButton.callback = fourtyNine_three_callback
    fourtyNine_sixButton.callback = fourtyNine_six_callback

    await interaction.channel.send( embed=embedVar, view = view)

async def fourtyNine_three_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = await embeds.topup_us_49_final("3", "https://notify.org/3m-top-up")

    await interaction.channel.send( embed=embedVar)

async def fourtyNine_six_callback(interaction):
    await interaction.response.edit_message(view = None)

    embedVar = await embeds.topup_us_49_final("6", "https://notify.org/6m-top-up")

    await interaction.channel.send( embed=embedVar)

Client.run(token)