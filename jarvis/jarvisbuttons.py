import discord
import os
import time
import logging
import asyncio
import psycopg2
from psycopg2 import sql
from discord.ui import Button, View
from datetime import timedelta, datetime
import string

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), filename='info.log', filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')

#Bot Token
token = ''
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

userQList = []

class DiscordBot(discord.Client):

    tixChannels = [0] * 10001
    notibot = 0
    category = "start"
    resolved = False
    tixCounter = [0] * 10
    botTimer = time.time()

    #Discord dev id's
    botEmoji = '<:bot_related:872705898919919666>'
    retailBotEmoji = '<:retail_bot_related:909132821824688138>'
    botSetupEmoji = '<:bot_setup_check:909132786919669842>'
    proxyEmoji = '<:proxy_related:872727550596632586>'
    siteEmoji = '<:site_related:872705898999599134>'
    retailSiteEmoji = '<:retail_site_related:909132846369738762>'
    memberEmoji = '<:membership_related:872705899494514758>'
    supportEmoji = '<:support_related:872705899477729310>'
    restartEmoji = '<:restart_prompts:872705977911234590>'

    botButton = Button(label = "Sneaker Bots", style = discord.ButtonStyle.grey, emoji = botEmoji)
    retailBotButton = Button(label = "Retail Bots", style = discord.ButtonStyle.grey, emoji = retailBotEmoji)
    botSetupButton = Button(label = "Bot Setup", style = discord.ButtonStyle.grey, emoji = botSetupEmoji)
    proxyButton = Button(label = "Proxy Related", style = discord.ButtonStyle.grey, emoji = proxyEmoji)
    siteButton = Button(label = "Sneaker Sites", style = discord.ButtonStyle.grey, emoji = siteEmoji)
    retailSiteButton = Button(label = "Retail Sites", style = discord.ButtonStyle.grey, emoji = retailSiteEmoji)
    memberButton = Button(label = "Membership Related", style = discord.ButtonStyle.grey, emoji = memberEmoji)
    supportButton = Button(label = "Talk to Support", style = discord.ButtonStyle.grey, emoji = supportEmoji)
    restartButton = Button(label = "At Any Time to Restart", style = discord.ButtonStyle.grey, emoji = restartEmoji)

    cancelButton = Button(label = "Cancellation", style = discord.ButtonStyle.grey, emoji = '⛔')
    questionButton = Button(label = "Other", style = discord.ButtonStyle.grey, emoji = '❓')

    redButton = Button(label = "Yes", style = discord.ButtonStyle.green)
    greenButton = Button(label = "No", style = discord.ButtonStyle.danger)

    # Bot setup check
    botSetupcheckButton = Button(label = "Finished", style = discord.ButtonStyle.green, emoji = '✔')

    # For all Bots Check button
    allBotcheckButton = Button(label = "Resolved", style = discord.ButtonStyle.green)
    
    # Retail Bots X
    akarixButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    dakozaxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    ksrxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    ominousxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    stellarxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)

    # Sneaker Bots X
    balkoxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    cyberxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    kodaixButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    mekpremexButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    whatbotxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    wrathxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    tohruxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    prismxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    ganeshxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    kylinxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    mekaioxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    hayhaxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    tricklexButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    valorxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)
    veloxxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)

    # Check and X for all other categories
    othercheckButton = Button(label = "Resolved", style = discord.ButtonStyle.green)
    otherxButton = Button(label = "Not Resolved", style = discord.ButtonStyle.danger)

    # Bot and Site Emojis and Buttons
    balko = '<:balkobot:862470852817059871>'
    cybersole = '<:cybersole:732423220577173566>'
    kodai = '<:kodai:732423220853997708>'
    mekpreme = '<:mekpreme:614273873956831232>'
    whatbot = '<:whatbot:732423221823012897>'
    wrath = '<:wrath:619333000072790016>'
    tohru = '<:tohru:729762487515480144>'
    nikeOther = '<:nike_bots:872705946248429589>'
    aioOther = '<:other_AIO_bots:872705946655285258>'
    prism = '<:prism:753691950502117528>'
    ganesh = '<:ganesh:862471436370182165>'
    hayha = '<:hayha:862469783394975815>'
    kylinbot = '<:kylinbot:862469783478992946>'
    mekaio = '<:mekaio:862469783701028904>'
    ominous = '<:ominous:864302805971632148>'
    stellar = '<:stellar:864302972476325908>'
    trickle = '<:trickle:952812471398301707>'
    valor = '<:valoraio:862469783273734185>'
    velox = '<:velox:729763753629057096>'
    dakoza = '<:dakoza:908218468858462248>'
    akari = '<:akari:908218430686113872>'
    ksr = '<:ksr:862469783391961148>'

    balkoButton = Button(label = "Balko", style = discord.ButtonStyle.grey, emoji = balko)
    cyberButton = Button(label = "Cyber", style = discord.ButtonStyle.grey, emoji = cybersole)
    kodaiButton = Button(label = "Kodai", style = discord.ButtonStyle.grey, emoji = kodai)
    mekpremeButton = Button(label = "Mekpreme", style = discord.ButtonStyle.grey, emoji = mekpreme)
    whatbotButton = Button(label = "Whatbot", style = discord.ButtonStyle.grey, emoji = whatbot)
    wrathButton = Button(label = "Wrath", style = discord.ButtonStyle.grey, emoji = wrath)
    tohruButton = Button(label = "Tohru", style = discord.ButtonStyle.grey, emoji = tohru)
    nikeOtherButton = Button(label = "Nike Bots", style = discord.ButtonStyle.grey, emoji = nikeOther)
    aioButton = Button(label = "AIO Bots", style = discord.ButtonStyle.grey, emoji = aioOther)
    prismButton = Button(label = "Prism", style = discord.ButtonStyle.grey, emoji = prism)
    ganeshButton = Button(label = "Ganesh", style = discord.ButtonStyle.grey, emoji = ganesh)
    hayhaButton = Button(label = "Hayha", style = discord.ButtonStyle.grey, emoji = hayha)
    kylinbotButton = Button(label = "Kylin", style = discord.ButtonStyle.grey, emoji = kylinbot)
    mekaioButton = Button(label = "Mekaio", style = discord.ButtonStyle.grey, emoji = mekaio)
    ominousButton = Button(label = "Ominous", style = discord.ButtonStyle.grey, emoji = ominous)
    stellarButton = Button(label = "Stellar", style = discord.ButtonStyle.grey, emoji = stellar)
    trickleButton = Button(label = "Trickle", style = discord.ButtonStyle.grey, emoji = trickle)
    valorButton = Button(label = "Valor", style = discord.ButtonStyle.grey, emoji = valor)
    veloxButton = Button(label = "Velox", style = discord.ButtonStyle.grey, emoji = velox)
    dakozaButton = Button(label = "Dakoza", style = discord.ButtonStyle.grey, emoji = dakoza)
    akariButton = Button(label = "Akari", style = discord.ButtonStyle.grey, emoji = akari)
    ksrButton = Button(label = "KSR", style = discord.ButtonStyle.grey, emoji = ksr)

    # Buttons for Topup US
    fourtyButton = Button(label = "40", style = discord.ButtonStyle.grey)
    fourtyNineButton = Button(label = "49", style = discord.ButtonStyle.blurple)
    fourty_threeButton = Button(label = "3 Months", style = discord.ButtonStyle.grey)
    fourty_sixButton = Button(label = "6 Months", style = discord.ButtonStyle.blurple)
    fourty_yearButton = Button(label = "12 Months", style = discord.ButtonStyle.blurple)
    fourtyNine_threeButton = Button(label = "3 Months", style = discord.ButtonStyle.link, url = "https://notify.org/3m-top-up")
    fourtyNine_sixButton = Button(label = "6 Months", style = discord.ButtonStyle.link, url = "https://notify.org/6m-top-up")
    fourtyNine_yearButton = Button(label = "12 Months", style = discord.ButtonStyle.link, url = "https://notify.org/12m-top-up")

    # Buttons for Topup US
    three_monthButton = Button(label = "3 Months", style = discord.ButtonStyle.link, url = "https://notify.org/eu-3m-top-up")
    six_monthButton = Button(label = "6 Months", style = discord.ButtonStyle.link, url = "https://notify.org/eu-6m-top-up")

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

    finishJdButton = Button(label = "Finishline & JD", style = discord.ButtonStyle.grey, emoji = finishJd)
    footsitesButton = Button(label = "Footsites", style = discord.ButtonStyle.grey, emoji = footsites)
    hibbetButton = Button(label = "Hibbett", style = discord.ButtonStyle.grey, emoji = hibbet)
    shopifyButton = Button(label = "Shopify", style = discord.ButtonStyle.grey, emoji = shopify)
    supremeButton = Button(label = "Supreme", style = discord.ButtonStyle.grey, emoji = supreme)
    yzyButton = Button(label = "Yeezy Supply", style = discord.ButtonStyle.grey, emoji = yzy)
    targetButton = Button(label = "Target", style = discord.ButtonStyle.grey, emoji = target)
    bestbuyButton = Button(label = "BestBuy", style = discord.ButtonStyle.grey, emoji = bestbuy)
    amazonButton = Button(label = "Amazon", style = discord.ButtonStyle.grey, emoji = amazon)
    notiLogoButton = Button(label = "Other Site", style = discord.ButtonStyle.grey, emoji = notiLogo)
    walmartButton = Button(label = "Walmart", style = discord.ButtonStyle.grey, emoji = walmart)
    amdButton = Button(label = "AMD", style = discord.ButtonStyle.grey, emoji = amd)
    gamestopButton = Button(label = "Gamestop", style = discord.ButtonStyle.grey, emoji = gamestop)
    microsoftButton = Button(label = "Microsoft", style = discord.ButtonStyle.grey, emoji = microsoft)

    DBTable = ""
    DBHost = ""
    DBUsr = ""
    DBPass = ""
    DBPort = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create the background task and run it in the background
        # self.bg_task = self.loop.create_task(self.reminder())

####################################################################################################
# Purpose: Used for testing, getting bot ID, and is initiated once the bot is online and ready
#
#
#
# Inputs: None
#
# Outputs: None
#
# Future:
#
####################################################################################################
    async def on_ready(self):

        self.notibot = bot.get_user(730136171983667280)#Bot Id
        self.notiTix = bot.get_user(722196398635745312)
        self.me = bot.get_user(94328613540724736)

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
    async def setFooter(self,embedVar):
        embedVar.set_footer(text = "Jarvis", icon_url = "https://cdn.discordapp.com/avatars/730136171983667280/7804ea245de12dd9a124e761b55eb97a.webp")
        embedVar.set_thumbnail(url = 'https://18pairsonkith.com/notify.png')
        return embedVar

    async def setFooterEU(self,embedVar):
        embedVar.set_footer(text = "Jarvis", icon_url = "https://cdn.discordapp.com/avatars/730136171983667280/7804ea245de12dd9a124e761b55eb97a.webp")
        embedVar.set_thumbnail(url = 'https://media.discordapp.net/attachments/719312417200537670/909442302366339142/NEU_NBG.png')
        return embedVar

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
    async def on_message(self, message):
        guild = bot.get_guild(570142274902818816)
        global userQList

        # try:
        #     self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
        #     logging.info("Opened database successfully")
        #     cur = self.conn.cursor()
        #     cur.execute("""SELECT * FROM PUBLIC.JARVIS WHERE "chId" = %s  """, (int(ch.id), ) )
        #     row = cur.fetchone()
        #     channel = discord.utils.get(guild.channels, id=int(row[10]))
        #     message = await channel.fetch_message(reaction.message_id)
        #     category = str(row[3])
        #     subCat = str(row[4])
        #     resolved = row[5]
        #     created = row[6]
        #     author = row[7]
        #     resolved = row[8]
        #     staff = row[9]
        #     chId = row[10]
        #     authId = row[11]
        #     self.conn.close()
        # except Exception as e:
        #     logging.error(e)
        #     self.conn.close()
        #     return

        #Discord Emote Id's
        start = '💌'
        self.alert = '<@&575144399013543977>'
        self.admin = '<@&570142914492235791>'

########################################################
#START OF RED/GREEN REACTION EMOTE
########################################################

        async def red_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("start", "None", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            
            embedVar = discord.Embed(title="Resolve issue", description='''Please react with the button that best fits your question.
                                                                        \n''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item(self.botButton)
            view.add_item(self.retailBotButton)
            view.add_item(self.botSetupButton)
            view.add_item(self.proxyButton)
            view.add_item(self.siteButton)
            view.add_item(self.retailSiteButton)
            view.add_item(self.memberButton)
            view.add_item(self.supportButton)
            view.add_item(self.restartButton)

            self.botButton.callback = bot_callback
            self.retailBotButton.callback = retailbot_callback
            self.botSetupButton.callback = botsetup_callback
            self.proxyButton.callback = proxy_callback
            self.siteButton.callback = site_callback
            self.retailSiteButton.callback = retailsite_callback
            self.memberButton.callback = member_callback
            self.supportButton.callback = support_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)

        async def green_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET "resolved" = %s WHERE "chId" = %s""",(True, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Resolved issue", description="Ticket will be closed by support.", color=0xDB0B23)
            await self.setFooter(embedVar)
            await interaction.channel.send( embed=embedVar)

########################################################
#END OF RED/GREEN REACTION EMOTE
########################################################

########################################################
#START OF CATEGORY SELECTION / SUPPORT TREE
########################################################
        #RETAIL BOT
        async def retailbot_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("retailbot", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Retail Bot Related", description="Please choose a bot you need assistance with below.\n", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.akariButton)
            view.add_item( self.dakozaButton)
            view.add_item( self.ksrButton)
            view.add_item( self.ominousButton)
            view.add_item( self.stellarButton)
            view.add_item( self.restartButton)

            self.akariButton.callback = akari_callback
            self.dakozaButton.callback = dakoza_callback
            self.ksrButton.callback = ksr_callback
            self.ominousButton.callback = ominous_callback
            self.stellarButton.callback = stellar_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #RETAIL BOT

        #BOT
        async def bot_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Bot Related", description="Please choose a bot you need assistance with below.\n\n", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.balkoButton)
            view.add_item( self.cyberButton)
            view.add_item( self.ganeshButton)
            view.add_item( self.hayhaButton)
            view.add_item( self.kodaiButton)
            view.add_item( self.kylinbotButton)
            view.add_item( self.mekpremeButton)
            view.add_item( self.mekaioButton)
            view.add_item( self.prismButton)
            view.add_item( self.tohruButton)
            view.add_item( self.trickleButton)
            view.add_item( self.veloxButton)
            view.add_item( self.valorButton)
            view.add_item( self.whatbotButton)
            view.add_item( self.wrathButton)
            view.add_item( self.nikeOtherButton)
            view.add_item( self.aioButton)
            view.add_item( self.restartButton)

            self.balkoButton.callback = balko_callback
            self.cyberButton.callback = cyber_callback
            self.ganeshButton.callback = ganesh_callback
            self.hayhaButton.callback = hayha_callback
            self.kodaiButton.callback = kodai_callback
            self.kylinbotButton.callback = kylin_callback
            self.mekpremeButton.callback = mekpreme_callback
            self.mekaioButton.callback = mekaio_callback
            self.prismButton.callback = prism_callback
            self.tohruButton.callback = tohru_callback
            self.trickleButton.callback = trickle_callback
            self.veloxButton.callback = velox_callback
            self.valorButton.callback = valor_callback
            self.whatbotButton.callback = whatbot_callback
            self.wrathButton.callback = wrath_callback
            self.nikeOtherButton.callback = nikeother_callback
            self.aioButton.callback = aio_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #BOT

        #BOT SETUP
        async def botsetup_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("botsetup", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Bot Setup Check Format", 
                description="**Copy the following and add your setup:**\n\n"
                "**Bot:**\n"
                "**Website:**\n"
                "**Server or Local:**\n"
                "**Specs (CPU/RAM):**\n"
                "**Task Mode (if applicable):**\n"
                "**Keywords (in the correct format for your bot):**\n"
                "**Number of Tasks (Resi/ISP):**\n"
                "**Number of Gmails:**\n"
                "**In-Bot or AYCD:**\n"
                "**3rd Party Solvers:**\n"
                "**When do you plan on starting tasks?:**\n"
                "**Delays (including delays changes):**\n"
                "**Additional Questions:**\n\n"
                + " Press ✔ once you have completed the above to ping support\n"
                + self.restartEmoji + " At any time to start over"
                , color=0xDB0B23)
            
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.botSetupcheckButton)
            view.add_item( self.restartButton)

            self.botSetupcheckButton.callback = botsetup_check_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #BOT SETUP

        #PROXY
        async def proxy_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("proxy", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Proxy Related", description = ''' Please slect the button that best suits your needs.
                                                                            \n''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.proxyButton)
            view.add_item( self.restartButton)

            self.proxyButton.callback = proxy_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #PROXY

        #SITE
        async def site_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("site", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Site Related", description= ''' Please slect the button of the site you need assistance with below.
                                                                            \n''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.finishJdButton)
            view.add_item( self.footsitesButton)
            view.add_item( self.hibbetButton)
            view.add_item( self.shopifyButton)
            view.add_item( self.supremeButton)
            view.add_item( self.yzyButton)
            view.add_item( self.notiLogoButton)
            view.add_item( self.restartButton)

            self.finishJdButton.callback = finishjd_callback
            self.footsitesButton.callback = footsites_callback
            self.hibbetButton.callback = hibbet_callback
            self.shopifyButton.callback = shopify_callback
            self.supremeButton.callback = supreme_callback
            self.yzyButton.callback = yzy_callback
            self.notiLogoButton.callback = notiLogo_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #SITE

        #RETAIL SITE
        async def retailsite_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("retailsite", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Site Related", description= ''' Please slect the button of the site you need assistance with below.
                                                                            \n''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.amazonButton)
            view.add_item( self.amdButton)
            view.add_item( self.bestbuyButton)
            view.add_item( self.gamestopButton)
            view.add_item( self.microsoftButton)
            view.add_item( self.targetButton)
            view.add_item( self.walmartButton)
            view.add_item( self.notiLogoButton)
            view.add_item( self.restartButton)

            self.amazonButton.callback = amazon_callback
            self.amdButton.callback = amd_callback
            self.bestbuyButton.callback = bestbuy_callback
            self.gamestopButton.callback = gamestop_callback
            self.microsoftButton.callback = microsoft_callback
            self.targetButton.callback = target_callback
            self.walmartButton.callback = walmart_callback
            self.notiLogoButton.callback = notiLogo_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #RETAIL SITE

        #MEMBER
        async def member_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("membership", "None", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Membership", description="Note: To cancel, go to [the dashboard](https://dash.notify.org/) and click `Disable auto-renewal`. You can also rejoin at any time if you fit the necessary criteria [here](https://notify.wiki/rejoin-policy)\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.cancelButton)
            view.add_item( self.questionButton)
            view.add_item( self.restartButton)

            self.cancelButton.callback = cancel_callback
            self.questionButton.callback = question_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #MEMBER

        #DIRECT SUPPORT
        async def support_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("support", "None", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            #DIRECT SUPPORT

        #Restart the process at any point to the start
        async def restart_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("start", "None", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Resolve issue", description='''Please react with the button that best fits your question.
                                                                        \n''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item(self.botButton)
            view.add_item(self.retailBotButton)
            view.add_item(self.botSetupButton)
            view.add_item(self.proxyButton)
            view.add_item(self.siteButton)
            view.add_item(self.retailSiteButton)
            view.add_item(self.memberButton)
            view.add_item(self.supportButton)
            view.add_item(self.restartButton)

            self.botButton.callback = bot_callback
            self.retailBotButton.callback = retailbot_callback
            self.botSetupButton.callback = botsetup_callback
            self.proxyButton.callback = proxy_callback
            self.siteButton.callback = site_callback
            self.retailSiteButton.callback = retailsite_callback
            self.memberButton.callback = member_callback
            self.supportButton.callback = support_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)

########################################################
#END OF CATEGORY SELECTION / SUPPORT TREE
########################################################


########################################################
#START OF RETAIL BOTS GUIDE REFERENCE
########################################################

        #AKARI
        async def akari_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "akari", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Akari", description="Refer to [the Akari guide](https://dash.notify.org/guides/akari)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.akarixButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.akarixButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #AKARI

        #DAKOZA
        async def dakoza_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "dakoza", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Dakoza", description="Refer to [the Dakoza guide](https://dash.notify.org/guides/dakoza-bmSv)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.dakozaxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.dakozaxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #DAKOZA

        #KSR
        async def ksr_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "ksr", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            
            embedVar = discord.Embed(title="KSR", description="Refer to [the KSR guide](https://dash.notify.org/guides/ksr-uTo8n)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.ksrxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.ksrxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #KSR

        #OMINOUS
        async def ominous_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "ominous", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            
            embedVar = discord.Embed(title="Ominous", description="Refer to [the Ominous guide](https://dash.notify.org/guides/ominous)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.ominousxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.ominousxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #OMINOUS

        #STELLAR
        async def stellar_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "stellar", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            
            embedVar = discord.Embed(title="Stellar", description="Refer to [the Stellar guide](https://dash.notify.org/guides/stellar)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.stellarxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.stellarxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #STELLAR

########################################################
#END OF RETAIL BOTS GUIDE REFERENCE
########################################################

# ########################################################
# #START OF RETAIL BOTS NOT RESOLVED
# ########################################################

#         #AKARI
#         async def akari_x_callback(interaction):
#             await interaction.response.send_message( "<@&908218571186913320> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "akari", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #AKARI

#         #DAKOZA
#         async def dakoza_x_callback(interaction):
#             await interaction.response.send_message( "<@&908218584923275284> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "dakoza", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #DAKOZA

#         #KSR
#         async def ksr_x_callback(interaction):
#             await interaction.response.send_message( self.alert)
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "ksr", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #KSR

#         #OMINOUS
#         async def ominous_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302633426354177> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "ominous", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #OMINOUS

#         #STELLAR
#         async def stellar_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302295738744872> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("retailbot", "stellar", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #STELLAR

# ########################################################
# #END OF RETAIL BOTS NOT RESOLVED
# ########################################################

########################################################
#START OF BOTS GUIDE REFERENCE
########################################################

        #BALKOBOT
        async def balko_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "balko", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Balkobot", description="Refer to [the Balko guide](https://dash.notify.org/guides/balko)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.balkoxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.balkoxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #BALKOBOT

        #CYBER
        async def cyber_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "cyber", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Cybersole", description="Refer to [the Cyber guide](https://dash.notify.org/guides/cyber)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.cyberxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.cyberxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #CYBER

        #KODAI
        async def kodai_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "kodai", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Kodai", description="Refer to [the Kodai guide](https://dash.notify.org/guides/kodai)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.kodaixButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.kodaixButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #KODAI

        #MEKPREME
        async def mekpreme_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "mekpreme", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Mekpreme", description="Refer to [the Mekpreme guide](https://dash.notify.org/guides/mekpreme)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.mekpremexButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.mekpremexButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #MEKPREME

        #WHATBOT
        async def whatbot_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "whatbot", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Whatbot", description="Refer to [the Whatbot guide](https://dash.notify.org/guides/whatbot)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.whatbotxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.whatbotxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #WHATBOT

        #WRATH
        async def wrath_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "wrath", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Wrath", description="Refer to [the Wrath guide](https://dash.notify.org/guides/wrath)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.wrathxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.wrathxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #WRATH

        #TOHRU
        async def tohru_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "tohru", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Tohru", description="Refer to [the Tohru guide](https://dash.notify.org/guides/tohru)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.tohruxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.tohruxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #TOHRU

        #PRISM
        async def prism_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "prism", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Prism", description="Refer to [the Prism guide](https://dash.notify.org/guides/prism)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.prismxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.prismxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #PRISM

        #GANESH
        async def ganesh_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "ganesh", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Ganesh", description="Refer to [the Ganesh guide](https://dash.notify.org/guides/ganesh)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.ganeshxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.ganeshxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #GANESH

        #KYLINBOT
        async def kylin_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "kylinbot", chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            await message.clear_reactions()
            embedVar = discord.Embed(title="Kylin Bot", description="Refer to [the Kylin guide](https://dash.notify.org/guides/kylin)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.kylinxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.kylinxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #KYLINBOT

        #MEKAIO
        async def mekaio_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "mekaio", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="MEKaio", description="Refer to [the Mekaio guide](https://dash.notify.org/guides/mekaio)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.mekaioxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.mekaioxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #MEKAIO

        #HAYHA
        async def hayha_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "hayha", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Hayha", description="Staff will be with you shortly", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            #HAYHA

        #TRICKLE
        async def trickle_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "trickle", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Trickle", description="Staff will be with you shortly", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            #TRICKLE

        #VALOR
        async def valor_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "valor", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Valor", description="Refer to [the Valor guide](https://dash.notify.org/guides/valor)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.valorxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.valorxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #VALOR

        #VELOX
        async def velox_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "velox", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            await message.clear_reactions()
            embedVar = discord.Embed(title="Velox", description="Refer to [the Velox guide](https://dash.notify.org/guides/velox)\n\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
           
            view = View(timeout = None)
            view.add_item( self.allBotcheckButton)
            view.add_item( self.veloxxButton)
            view.add_item( self.restartButton)

            self.allBotcheckButton.callback = other_check_callback
            self.veloxxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #VELOX

        #OTHER AIO
        async def aio_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Other AIO Bots", description="Staff will be with you shortly", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            #OTHER AIO

        #NIKE BOTS
        async def nikeother_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Nike Bots", description="Staff will be with you shortly", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            #NIKE BOTS

########################################################
#END OF BOTS GUIDE REFERENCE
########################################################

# ########################################################
# #START OF BOTS NOT RESOLVED
# ########################################################

#         #GANESH
#         async def ganesh_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302275299508224> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "ganesh", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #GANESH

#         #KYLINBOT
#         async def kylin_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302277506105366> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "kylinbot", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #KYLINBOT

#         #MEKAIO
#         async def mekaio_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302280731656192> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "mekaio", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #MEKAIO

#         #VALOR
#         async def valor_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302286943944724> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "valor", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #VALOR

#         #TRICKLE
#         async def trickle_x_callback(interaction):
#             await interaction.response.send_message( "<@&952782386943361104> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "trickle", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #TRICKLE

#         #VELOX
#         async def velox_x_callback(interaction):
#             await interaction.response.send_message( "<@&864302289186717728> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "velox", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #VELOX

#         #BALKO
#         async def balko_x_callback(interaction):
#             await interaction.response.send_message( "<@&572634780345040906> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "balko", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #BALKO

#         #CYBER
#         async def cyber_x_callback(interaction):
#             await interaction.response.send_message( "<@&570142934935142412> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "cyber", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #CYBER

#         #KODAI
#         async def kodai_x_callback(interaction):
#             await interaction.response.send_message( "<@&606319522374483978> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "kodai", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #KODAI

#         #MEKPREME
#         async def mekpreme_x_callback(interaction):
#             await interaction.response.send_message( "<@&732426610078384169> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "mekpreme", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #MEKPREME

#         #WHATBOT
#         async def whatbot_x_callback(interaction):
#             await interaction.response.send_message( "<@&570142941436313601> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "whatbot", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #WHATBOT

#         #WRATH
#         async def wrath_x_callback(interaction):
#             await interaction.response.send_message( "<@&641812933340430357> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "wrath", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #WRATH

#         #TOHRU
#         async def tohru_x_callback(interaction):
#             await interaction.response.send_message( "<@&732426890689904662> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "tohru", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #TOHRU

#         #PRISM
#         async def prism_x_callback(interaction):
#             await interaction.response.send_message( "<@&753692572576120862> Will be with you shortly.")
#             await interaction.response.send_message( "Please state your question now so staff can better help when they arrive, Thanks!")
#             try:
#                 self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
#                 logging.info("Opened database successfully")
#                 cur = self.conn.cursor()
#                 cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "prism", False, chId ))
#                 self.conn.commit()
#                 logging.info("Updated DB for resolved")
#                 self.conn.close()
#             except Exception as e:
#                 logging.error(e)
#                 self.conn.close()
#                 #PRISM

# ########################################################
# #END OF BOTS NOT RESOLVED
# ########################################################

########################################################
#START OF BOT SETUP
########################################################

        #FINISHED
        async def botsetup_check_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Finished", description="Staff will be with you shortly.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("botsetup", "None", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
                #FINISHED

########################################################
#END OF BOT SETUP
########################################################

########################################################
#START OF PROXY RELATED
########################################################

        #GENERAL PROXY
        async def proxy_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("proxy", "other", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="General Proxy Info", description="Refer to [the Proxies guide](https://dash.notify.org/guides/proxies)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #GENERAL PROXY

########################################################
#END OF PROXY RELATED
########################################################

########################################################
#START OF SITE RELATED
########################################################

        #FNLJD
        async def finishjd_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Finishline and JD Sports", description="Refer to [the FNL&JD guide](https://dash.notify.org/guides/fnl-jd)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #FNLJD

        #FOOTSITES
        async def footsites_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Footsites", description="For FCFS drops refer to [the Footsites guide](https://dash.notify.org/guides/footsites)\n For raffles refer to https://guides.notify.org/bBqEudL3rZBob2ils0U0S\n Did it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #FOOTSITES

        #HIBBETT
        async def hibbet_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Hibbett", description="Refer to [the Hibbett guide](https://dash.notify.org/guides/hibbett)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #HIBBETT

        #SHOPIFY
        async def shopify_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Shopify", description="Refer to [the Shopify botting guide](https://dash.notify.org/guides/shopify-botting-e_9K)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #SHOPIFY

        #SUPREME
        async def supreme_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Supreme", description="Refer to [the Supreme guide](https://dash.notify.org/guides/supreme)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #SUPREME

        #YEEZYSUPPLY
        async def yzy_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Yeezy Supply and Adidas", description="Refer to [the YS/Adidas guide](https://dash.notify.org/guides/ys-adidas)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #YEEZYSUPPLY

        #OTHER
        async def notiLogo_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("site", "support", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            #OTHER

########################################################
#END OF SITE RELATED
########################################################

########################################################
#START OF RETAIL SITE RELATED
########################################################

        #AMAZON
        async def amazon_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Amazon", description="Refer to [the Amazon guide](https://dash.notify.org/guides/amazon)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #AMAZON

        #AMD
        async def amd_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="AMD", description="Refer to [the AMD guide](https://dash.notify.org/guides/amd)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #AMD

        #BESTBUY
        async def bestbuy_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="BestBuy", description="Refer to [the Bestbuy guide](https://dash.notify.org/guides/bestbuy)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #BESTBUY

        #GAMESTOP
        async def gamestop_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Gamestop", description="Refer to [the Gamestop guide](https://dash.notify.org/guides/gamestop)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #GAMESTOP

        #MICROSOFT
        async def microsoft_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Microsoft", description="Refer to [the Microsoft guide](https://dash.notify.org/guides/microsoft)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #MICROSOFT

        #TARGET
        async def target_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Target", description="Refer to [the Target guide](https://dash.notify.org/guides/target)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #TARGET

        #WALMART
        async def walmart_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Walmart", description="Refer to [the Walmart guide](https://dash.notify.org/guides/walmart)\nDid it solve your issue?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.othercheckButton)
            view.add_item( self.otherxButton)
            view.add_item( self.restartButton)

            self.othercheckButton.callback = other_check_callback
            self.otherxButton.callback = other_x_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)
            #WALMART

########################################################
#END OF RETAIL SITE RELATED
########################################################

########################################################
#START OF MEMBERSHIP STUFF
########################################################

        #CANCELLATION
        async def cancel_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Cancellation", description="Please state the reason for your cancellation and staff will be with you shortly.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("membership", "cancel", True, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
                #CANCELLATION

        #OTHER
        async def question_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Other", description="A staff member will be with you shortly.\n", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("membership", "other", False, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
                #OTHER

########################################################
#END OF MEMBERSHIP STUFF
########################################################

########################################################
#START OF RESOLVED AND NOT RESOLVED FOR OTHER
########################################################

        #RESOLVED
        async def other_check_callback(interaction):
            await interaction.response.edit_message(view = None)
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET "resolved" = %s WHERE "chId" = %s""",( True, chId ))
                self.conn.commit()
                logging.info("Updated DB for resolved")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            resolved = True

            embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
            await self.setFooter(embedVar)
            
            view = View(timeout = None)
            view.add_item( self.greenButton)
            view.add_item( self.redButton)
            view.add_item( self.restartButton)

            self.greenButton.callback = green_callback
            self.redButton.callback = red_callback
            self.restartButton.callback = restart_callback

            await interaction.channel.send( embed=embedVar, view = view)

            # self.clear_items()
            # await message.channel.edit_message(view = self)
            #RESOLVED

        #NOT RESOLVED
        async def other_x_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="Not Resolved", description="Staff will be with you shortly.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.alert)
            index = userQList.index(str(interaction.channel.id))
            value = userQList[index + 1]
            userQList.pop(index)
            userQList.pop(index)
            await interaction.channel.send( "Member Asked: " + value)

########################################################
#END OF RESOLVED AND NOT RESOLVED FOR OTHER
########################################################   

########################################################
#CALLBACKS FOR TOPUP US
########################################################

        async def fourty_callback(interaction):
            await interaction.response.edit_message(view = None)

            embedVar = discord.Embed(title="$40/m License Top-Up", description='''Please react with the option that you would like to go with.
                                                                            \n\n `-` **Top-Up 3 months for $105 (13%) off**
                                                                            \n `-` **Top-Up 6 months for $199 (17%) off**
                                                                            \n `-` **Top-Up 12 months for $319 (33%) off**
                                                                            ''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item(self.fourty_threeButton)
            view.add_item(self.fourty_sixButton)
            view.add_item(self.fourty_yearButton)

            self.fourty_threeButton.callback = fourty_three_callback
            self.fourty_sixButton.callback = fourty_six_callback
            self.fourty_yearButton.callback = fourty_year_callback

            await interaction.channel.send( embed=embedVar, view = view)

        async def fourty_three_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="$40/m ddLicense 3 Month Top-Up", description="An Admin will be with you shortly, please wait.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.admin)

        async def fourty_six_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="$40/m License 6 Month Top-Up", description="An Admin will be with you shortly, please wait.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.admin)

        async def fourty_year_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="$40/m License 12 Month Top-Up", description="An Admin will be with you shortly, please wait.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)
            await interaction.channel.send( self.admin)

        async def fourtyNine_callback(interaction):
            await interaction.response.edit_message(view = None)

            embedVar = discord.Embed(title="$49/m License Top-Up", description='''Please react with the option that you would like to go with.
                                                                            \n\n `-` **Top-Up 3 months for $125 (15%) off**
                                                                            \n `-` **Top-Up 6 months for $239 (20%) off**
                                                                            \n `-` **Top-Up 12 months for $379 (35%) off**
                                                                            \n\n**Once you're done, please let us know your purchase email.**''', color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item(self.fourtyNine_threeButton)
            view.add_item(self.fourtyNine_sixButton)
            view.add_item(self.fourtyNine_yearButton)

            self.fourtyNine_threeButton.callback = fourtyNine_three_callback
            self.fourtyNine_sixButton.callback = fourtyNine_six_callback
            self.fourtyNine_yearButton.callback = fourtyNine_year_callback

            await interaction.channel.send( embed=embedVar, view = view)

        async def fourtyNine_three_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="$49/m License 3 Month Top-Up", description="Please use this link: https://notify.org/3m-top-up\n\nOnce you're done, please let us know your purchase email.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)

        async def fourtyNine_six_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="$49/m License 6 Month Top-Up", description="Please use this link: https://notify.org/6m-top-up\n\nOnce you're done, please let us know your purchase email.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)

        async def fourtyNine_year_callback(interaction):
            await interaction.response.edit_message(view = None)
            embedVar = discord.Embed(title="$49/m License 12 Month Top-Up", description="Please use this link: https://notify.org/12m-top-up\n\nOnce you're done, please let us know your purchase email.", color=0xDB0B23)
            await self.setFooter(embedVar)

            await interaction.channel.send( embed=embedVar)

########################################################
# Initiates Jarvis For Topups US
########################################################
        if ('thanks for being a loyal member!' in message.content) and message.channel.category_id == 1052768590144733194 and str(message.author) == str(self.notiTix):
            embedVar = discord.Embed(title="Do you pay $40 or $49 a month for your renewal?", color=0xDB0B23)
            await self.setFooter(embedVar)

            view = View(timeout = None)
            view.add_item(self.fourtyButton)
            view.add_item(self.fourtyNineButton)

            self.fourtyButton.callback = fourty_callback
            self.fourtyNineButton.callback = fourtyNine_callback

            await message.channel.send( embed=embedVar, view = view)

########################################################
# Initiates Jarvis For Topups EU
########################################################
        if ('thanks for being a loyal member.' in message.content) and message.channel.category_id == 790097994712088576 and str(message.author) == str(self.notiTix):
            embedVar = discord.Embed(title="Click The Buttons Below If You Would Like A 3 Or 6 Month Renewal.", description='''Please react with the option that you would like to go with.
                                                                            \n\n `-` **Top-Up 3 months for £89 instead of £105 (15%) off**
                                                                            \n `-` **Top-Up 6 months for £163 instead of £210 (22%) off**
                                                                            \n\n `-` **Once you're done, please let us know your purchase email and tag Michael. If you have questions please let us know.**
                                                                            ''', color=0x563ef0)
            await self.setFooterEU(embedVar)

            view = View(timeout = None)
            view.add_item(self.three_monthButton)
            view.add_item(self.six_monthButton)

            await message.channel.send( embed=embedVar, view = view)

########################################################
# Initiates Jarvis
########################################################

        if ('Initiating Jarvis...' in message.content) and ( str(message.author) ==  str(self.notiTix) ) :

            channelId = str(message.channel.id)

            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""INSERT INTO PUBLIC.JARVIS ("chNum", "message", "mainCat", "subCat", "resolved", "createdAt", "author", "chId", "authId", "reminder") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",(str(message.channel), int(message.id), "start", "None", False, time.ctime(), str(message.mentions[0]),int(message.channel.id),int(message.mentions[0].id), time.time()) )
                self.conn.commit()
                logging.info("Records created successfully")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()

            #23
            botkw = ["balko", "cyber", "kodai", "mekpreme", "whatbot", "tohru", "prism", "ganesh", "hayha", "kylinbot", "mekaio", "ominous", "stellar", "trickle", "valor", "noble", "velox", "dakoza", "akari", "ksr", "wrath", "mek", "chegg", "cheggaio"]
            #20
            sitekw = ["finishline", "finish line", "fnl", "jd", "footsites", "foots", "ftl", "champs", "hibbett", "shopify", "shop", "supreme", " ys", "yeezy supply", "target", "bestbuy", "amazon", "walmart", "amd", "gamestop", "microsoft"]
            memkw = ["cancel", "break", "vacation", "pause", "og role", "membership"]
            proxkw = ["proxies", "proxy", "resi", "residential", "isp", "isps", "subnet"]
            #setkw = ["setting", "setup"]
            otherkw = ["notify app", "notify anywhere", "emerging", "notify tools", "notify helper", "aycd", "aws", "ebay", "notify toolbox"]
            #othernikebotkw = ["tsb", "project enigma", "enigma", "nike", "nike accounts"]
            #otheraiobotkw = ["osiris"]
            negkw = []
            packagekw = ["package", "stolen", "missing", "lost"]
            acckw = ["nike accounts", "nike"]
            cardkw = ["privacy", "amex", "slash", "eno", "mastercard", "tradeshift", "stripe", "visa", "citi", "vcc"]

            embeds = message.embeds

            for embed in embeds:

                contentStringDesc = str(embed.description)
                contentStringDescTrim = contentStringDesc.replace('> **Topic:** ', '')

                channelId = str(message.channel.id)

                userQuestion = "**" + contentStringDescTrim + "**"

                userQList.append(channelId)
                userQList.append(userQuestion)

                embedVar = discord.Embed(title="Relevant Guides", description="Please reference the list of guides below:\n\n", color=0xDB0B23)

                if not any(x in contentStringDesc.lower() for x in botkw) and not any(x in contentStringDesc.lower() for x in sitekw) and not any(x in contentStringDesc.lower() for x in memkw) and not any(x in contentStringDesc.lower() for x in proxkw) and not any(x in contentStringDesc.lower() for x in packagekw) and not any(x in contentStringDesc.lower() for x in acckw) and not any(x in contentStringDesc.lower() for x in cardkw) and not any(x in contentStringDesc.lower() for x in otherkw):

                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Member Asked: " + userQuestion)

                f = open("kwlist.txt", "a")
                if "topic:" in contentStringDesc.lower():
                    f.write(contentStringDescTrim + "\n")
                f.close()

                # Used for bot setups
                # if any(x in contentStringDesc.lower() for x in setkw):

                #     embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                #     await self.setFooter(embedVar)

                #     await message.channel.send( embed=embedVar)
                #     await message.channel.send( self.alert)

                #     embedVar = discord.Embed(title="Bot Setup Check Format", 
                #         description="**Copy the following and add your setup:**\n\n"
                #         "**Bot:**\n"
                #         "**Website:**\n"
                #         "**Server or Local:**\n"
                #         "**Specs (CPU/RAM):**\n"
                #         "**Task Mode (if applicable):**\n"
                #         "**Keywords (in the correct format for your bot):**\n"
                #         "**Number of Tasks (Resi/ISP):**\n"
                #         "**Number of Gmails:**\n"
                #         "**In-Bot or AYCD:**\n"
                #         "**3rd Party Solvers:**\n"
                #         "**When do you plan on starting tasks?:**\n"
                #         "**Delays (including delays changes):**\n"
                #         "**Additional Questions:**\n\n"
                #         , color=0xDB0B23)
                    
                #     await self.setFooter(embedVar)

                #     await message.channel.send( embed=embedVar)
                #     await message.channel.send( "Member Asked: " + userQuestion)
                #     break

                # Used for Postal issues.
                if (packagekw[0] in contentStringDesc.lower() and packagekw[1] in contentStringDesc.lower()) or (packagekw[0] in contentStringDesc.lower() and packagekw[2] in contentStringDesc.lower()) or (packagekw[0] in contentStringDesc.lower() and packagekw[3] in contentStringDesc.lower()):

                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)

                    embedVar = discord.Embed(title="Package issues?", description="Unfortunately we can't easily assist with package issues.\nBest plan of action is to make a claim with links below.\n\n", color=0xDB0B23)

                    embedVar.add_field(name = 'FedEx', value = '[FedEx Claims](https://www.fedex.com/en-us/customer-support/claims.html)', inline=False)
                    embedVar.add_field(name = 'UPS', value = '[USP Claims](https://www.ups.com/ca/en/help-center/claims-support.page)', inline=False)
                    embedVar.add_field(name = 'USPS', value = '[USPS Claims](https://www.usps.com/help/claims.htm)', inline=False)
                    embedVar.add_field(name = 'DHL', value = '[DHL Claims](https://www.dhl.com/ca-en/home/our-divisions/ecommerce-solutions/shipping/helpful-information/submit-a-claim.html)', inline=False)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send("Please reference the guides above, if they don't resolve your question please describe your question as best as possible for staff.")
                    await message.channel.send( "Member Asked: " + userQuestion)
                    break

                # Used for Nike Accounts.
                if any(x in contentStringDesc.lower() for x in acckw):

                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)

                    embedVar = discord.Embed(title="Nike Information", description="Here are some recommended by Staff.\n\n", color=0xDB0B23)

                    embedVar.add_field(name = 'Storm', value = '[Storm Twitter](https://twitter.com/stormaccounts?s=21&t=UW5fe2upRasV-nDNfseRmw)', inline=False)
                    embedVar.add_field(name = 'CWK', value = '[CWK Twitter](https://twitter.com/copwithkyle?s=21&t=UW5fe2upRasV-nDNfseRmw)', inline=False)
                    embedVar.add_field(name = 'Swish', value = '[Swish Twitter](https://twitter.com/swish_accounts?s=21&t=UW5fe2upRasV-nDNfseRmw)', inline=False)

                    embedVar.add_field(name = 'Nike J1gging', value = '[Basic J1gging Video Guide](https://www.youtube.com/watch?v=PIjN08e0TCg&ab_channel=Notify)', inline=False)

                    embedVar.add_field(name = 'Top Nike Bots', value = 'At the moment the top 2 performing bots for Nike is Project Enigma (PE) and Wrath. Guides for PE are private so the only way to access them is through their discord.')

                    await message.channel.send( embed=embedVar)
                    await message.channel.send("Please reference the guides above, if they don't resolve your question please describe your question as best as possible for staff.")
                    await message.channel.send( "Member Asked: " + userQuestion)
                    break

                # Used for Card Related Questions
                if any(x in contentStringDesc.lower() for x in cardkw):

                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)

                    embedVar = discord.Embed(title="Card Related Questions?", description="Below are some of the recommended cards and the sites they work on.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    embedVar.add_field(name = 'Personal Hard Cards/Amex Business Hard/Slash VCC', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 | Footsites: 🟢\nNike: 🟢 | Supreme: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    embedVar.add_field(name = 'Privacy', value = 'Shopify: 🔴 | Yeezy Supply: 🟢 | Footsites: 🔴\nNike: 🟢 | Supreme: 🔴 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    #embedVar.add_field(name = 'Amex Business Hard', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 (3DS) | Footsites: 🟢\nNike: 🟢 | Supreme: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    #embedVar.add_field(name = 'Slash VCC', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 | Footsites: 🟢\nNike: 🟢 | Supreme: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    embedVar.add_field(name = 'Eno Mastercard', value = 'Shopify: 🔴 | Yeezy Supply: 🟢 (3DS) | Footsites: 🟢\nNike: 🟢 | Supreme: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    embedVar.add_field(name = 'Tradeshift (Amex)/Stripe', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 (3DS) | Footsites: 🔴\nNike: 🟢 | Supreme: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    #embedVar.add_field(name = 'Stripe', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 | Footsites: 🔴\nNike: 🟢 | Supreme: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    embedVar.add_field(name = 'Eno Visa/Citi VCC', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 (3DS) | Footsites: 🔴\nNike: 🟢 | Supreme: 🔴 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
                    #embedVar.add_field(name = 'Citi VCC', value = 'Shopify: 🟢 | Yeezy Supply: 🟢 (3DS) | Footsites: 🔴\nNike: 🟢 | Supreme: 🔴 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send("Please reference the guides above, if they don't resolve your question please describe your question as best as possible for staff.")
                    await message.channel.send( "Member Asked: " + userQuestion)
                    break

                # Used for membership stuff
                if any(x in contentStringDesc.lower() for x in memkw):

                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)

                    embedVar = discord.Embed(title="Membership", description="Note: To cancel, go to [the dashboard](https://dash.notify.org/notify/hub/) then login and once logged in got to memberships -> click on your membership -> teminate membership. You can also rejoin through the waitlist on the hub [here](https://dash.notify.org/notify/hub/)\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send("Please reference the guides above, if they don't resolve your question please describe your question as best as possible for staff.")
                    await message.channel.send( "Member Asked: " + userQuestion)
                    break

                # # Used for other kws
                # if any(x in contentStringDesc.lower() for x in otherkw):
                #     embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                #     await self.setFooter(embedVar)

                #     await message.channel.send( embed=embedVar)
                #     await message.channel.send( self.alert)
                #     await message.channel.send( "Member Asked: " + userQuestion)
                #     break

                # Used for other kws
                # ["notify app", "notify anywhere", "emerging", "notify tools", "notify helper", "aycd", "aws", "ebay"]
                if otherkw[0] in contentStringDesc.lower() or otherkw[1] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Notify Anywhere App', value = '[Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_SPzNfS4QKhfufh)', inline=False)
                    embedVar.add_field(name = 'Notify Anywhere App', value = '[Info/DL Links](https://discord.com/channels/570142274902818816/991577591158947921/991888970042572851)', inline=False)
                if otherkw[2] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Notify Emerging', value = '[Joining](https://discord.com/channels/570142274902818816/886393025427820554)', inline=False)
                    embedVar.add_field(name = 'Having Issues?', value = 'Roles not syncing and you are stuck in the sync-roles channel? Type `!sync`.\nIf that does not work leave the server then try to relogin.', inline=False)
                if otherkw[3] in contentStringDesc.lower() or otherkw[8] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Notify Tools', value = '[Guide](https://coptools.gitbook.io/coptools/)', inline=False)
                    embedVar.add_field(name = 'Notify Tools', value = '[Info/DL Links](https://discord.com/channels/570142274902818816/991577591158947921/991888985678942208)', inline=False)
                if otherkw[4] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Notify Helper', value = '[Info/DL Links](https://discord.com/channels/570142274902818816/991577591158947921/991888992113016872)', inline=False)
                    embedVar.add_field(name = 'Notify Helper', value = '[Video Guide](https://www.youtube.com/watch?v=W59Hu-_8ZIE&ab_channel=Notify)', inline=False)
                if otherkw[5] in contentStringDesc.lower():
                    embedVar.add_field(name = 'AYCD Partnership', value = '[AYCD Partnership Discount/Info](https://discord.com/channels/570142274902818816/985233858423296150/985241206424469504)', inline=False)
                    embedVar.add_field(name = 'AYCD Video Guides', value = '[Class](https://whop.com/notify/content/?collectionId=exp_hzKE1EcT0puq9h&documentId=doc_QDQ70rN8mvTPUX)', inline=False)
                    embedVar.add_field(name = 'AYCD AWS', value = '[AWS Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_lE3aRUMC4pE6jb)', inline=False)
                if otherkw[6] in contentStringDesc.lower():
                    embedVar.add_field(name = 'General Server Info', value = '[General Server Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_lE3aRUMC4pE6jb)', inline=False)
                    embedVar.add_field(name = 'AYCD AWS', value = '[AYCD AWS Guide](https://whop.com/notify/content/?collectionId=exp_hzKE1EcT0puq9h&documentId=doc_QDQ70rN8mvTPUX)', inline=False)
                if otherkw[7] in contentStringDesc.lower():
                    embedVar.add_field(name = 'eBay Questions?', value = '[Selling on eBay Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_aph58ENuRWoXfU)', inline=False)

                # Bots and Stuff
                if botkw[0] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Balko', value = '[Balko Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_IRgBT5z65yK5eK)', inline=False)
                    #await balko_callback(message)
                if botkw[1] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Cyber', value = '[Cyber Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_F8Rsj1x7KHu2bj)', inline=False)
                    #await cyber_callback(message)
                if botkw[3] in contentStringDesc.lower() or botkw[21] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Mekpreme', value = '[Mekpreme Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_3P7Yjjizlb1T6D)', inline=False)
                    #await mekpreme_callback(message)
                if botkw[6] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Prism', value = '[Prism Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_lr9TpnifvoltKg)', inline=False)
                    #await prism_callback(message)
                if botkw[8] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Hayha', value = 'Guide Coming Soon', inline=False)
                    #await hayha_callback(message)
                if botkw[9] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Kylin', value = '[Kylin Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_pjzaqLZUEyzLdR)', inline=False)
                    #await kylinbot_callback(message)
                if botkw[10] in contentStringDesc.lower() or botkw[21] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Mekaio', value = '[Mekaio Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_l1bfDwkoHbQO8F)', inline=False)
                    embedVar.add_field(name = 'Mekaio Automations', value = '[Mekaio Automations Guide](http://help.mekrobotics.com/en/articles/5755086-automation)', inline=False)
                    #await mekaio_callback(message)
                if botkw[11] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Ominous', value = '[Ominous Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_4Q2C521N3QYzH2)', inline=False)
                    #await ominous_callback(message)
                if botkw[12] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Stellar', value = '[Stellar Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_m5H4qAPrNeT842)', inline=False)
                    #await stellar_callback(message)
                if botkw[14] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Valor', value = '[Valor Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_jSNNxYOuaztkIa)', inline=False)
                    embedVar.add_field(name = 'Valor Automations', value = '[Valor Automations Guide](https://docs.valoraio.com/setting-up-valor/misc/shopify-monitor#creating-monitors)', inline=False)
                    embedVar.add_field(name = 'Automations', value = '[Automations Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_aghPVhEXgsyqfW)', inline=False)
                    #await valor_callback(message)
                if botkw[16] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Velox', value = '[Velox Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_YmhyVYacxB2NEN)', inline=False)
                    #await velox_callback(message)
                if botkw[17] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Dakoza', value = '[Dakoza Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_Y1nJ3RlNuMwQ1x)', inline=False)
                    #await dakoza_callback(message)
                if botkw[18] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Akari', value = '[Akari Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_8TrSPmUssASGBm)', inline=False)
                    #await akari_callback(message)
                if botkw[19] in contentStringDesc.lower():
                    embedVar.add_field(name = 'KSR', value = '[KSR Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_HftU0qsAQMsXP7)', inline=False)
                    #await ksr_callback(message)
                if botkw[20] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Wrath', value = '[Wrath Guide](https://whop.com/notify/content/?collectionId=exp_ib7HCag05uGggq&documentId=doc_gbyKJqWzNGwrmv)', inline=False)
                    embedVar.add_field(name = 'Wrath Automations', value = '[Wrath Automations Guide](https://guides.wrathbots.co/wrath-aio/supported-sites/shopify/shopify-automations)')
                    embedVar.add_field(name = 'Automations', value = '[Automations Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_aghPVhEXgsyqfW)', inline=False)
                    #await wrath_callback(message)
                if botkw[22] in contentStringDesc.lower() or botkw[23] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Chegg', value = '[Coming Soon]()', inline=False)
                    #await wrath_callback(message)

                if sitekw[0] in contentStringDesc.lower() or sitekw[1] in contentStringDesc.lower() or sitekw[2] in contentStringDesc.lower() or sitekw[3] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Finishline & JD', value = '[FNL & JD Guide](https://whop.com/notify/content/?collectionId=exp_0QDNIVolgMe86q&documentId=doc_R8ypapOPncTlOb)', inline=False)
                    #await finishjd_callback(message)
                if sitekw[4] in contentStringDesc.lower() or sitekw[5] in contentStringDesc.lower() or sitekw[6] in contentStringDesc.lower() or sitekw[7] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Footsites', value = '[Footsites Guide](https://whop.com/notify/content/?collectionId=exp_0QDNIVolgMe86q&documentId=doc_6UyxlvFpXMIshg)', inline=False)
                    #await footsites_callback(message)
                if sitekw[8] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Hibbett', value = '[Hibbett Guide](https://whop.com/notify/content/?collectionId=exp_0QDNIVolgMe86q&documentId=doc_Mndsi5iL7pEIWl)', inline=False)
                    #await hibbet_callback(message)
                if sitekw[9] in contentStringDesc.lower() or sitekw[10] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Shopify', value = '[Shopify Botting Guide](https://whop.com/notify/content/?collectionId=exp_0QDNIVolgMe86q&documentId=doc_FOhQiZKwVwHOTz)', inline=False)
                    #await shopify_callback(message)
                if sitekw[11] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Supreme', value = '[Supreme Guide](https://whop.com/notify/content/?collectionId=exp_0QDNIVolgMe86q&documentId=doc_SetowHj3xPavsj)', inline=False)
                    #await supreme_callback(message)
                if sitekw[14] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Target', value = '[Target Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_uRNBc4jlSbXxXt)', inline=False)
                    #await target_callback(message)
                if sitekw[15] in contentStringDesc.lower():
                    embedVar.add_field(name = 'BestBuy', value = '[Bestbuy Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_gFjti5mzrQwTwT)', inline=False)
                    #await bestbuy_callback(message)
                if sitekw[16] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Amazon', value = '[Amazon Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_ZFZTFQ95ffBEDn)', inline=False)
                    #await amazon_callback(message)
                if sitekw[17] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Walmart', value = '[Walmart Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_z8GM4cUeN3KU2w)', inline=False)
                    #await walmart_callback(message)
                if sitekw[18] in contentStringDesc.lower():
                    embedVar.add_field(name = 'AMD', value = '[AMD Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_3vQlIJP0qyIop0)', inline=False)
                    #await amd_callback(message)
                if sitekw[19] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Gamestop', value = '[Gamestop Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_CtCCQh4ZMWxFFZ)', inline=False)
                    #await gamestop_callback(message)
                if sitekw[20] in contentStringDesc.lower():
                    embedVar.add_field(name = 'Microsoft', value = '[Microsoft Guide](https://whop.com/notify/content/?collectionId=exp_Y0FIcR2kEtlfMk&documentId=doc_jtioGodBmBzn7e)', inline=False)
                    #await microsoft_callback(message)

                if any(x in contentStringDesc.lower() for x in proxkw):
                    embedVar.add_field(name = 'Proxies', value = '[Proxies Guide](https://whop.com/notify/content/?collectionId=exp_AW1nGJ7Nns0QIE&documentId=doc_kf5sGPuRaRdCxD)', inline=False)
                    embedVar.add_field(name = 'Proxies', value = '[Proxies Video Guide](https://youtu.be/qMfdkH1fkwY)', inline=False)
                    #await proxy_callback(message)


                if any(x in contentStringDesc.lower() for x in botkw) or any(x in contentStringDesc.lower() for x in sitekw) or any(x in contentStringDesc.lower() for x in memkw) or any(x in contentStringDesc.lower() for x in proxkw) or any(x in contentStringDesc.lower() for x in packagekw) or any(x in contentStringDesc.lower() for x in acckw) or any(x in contentStringDesc.lower() for x in cardkw) or any(x in contentStringDesc.lower() for x in otherkw):
                    
                    embedVar1 = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar1)

                    await message.channel.send( embed=embedVar1)
                    await message.channel.send( self.alert)

                    await message.channel.send( embed=embedVar)
                    await message.channel.send("Please reference the guides above, if they don't resolve your question please describe your question as best as possible for staff.")
                    await message.channel.send( "Member Asked: " + userQuestion)

        ####################################################################################################
        # 
        # Frequency of searched terms
        #
        ####################################################################################################
        if('!kwfrequency' in message.content):
            with open("kwlist.txt", "r") as ch:
                mk = open("kwfrequency.csv", "w")
                content = ch.read()
                content = content.lower()
                content = content.translate(str.maketrans('', '', string.punctuation))
                content = content.split()
                content2 = []
                removeitems = ["i", "help", "a", "for", "need", "on", "the", "to", "with", "do", "in", "if", "you", "my", "was", "and", "can", "get", "of", "w", "some", "up", "good", "has", "or", "are", "just", "got", "an", "as", "have", "so", "me", "how", "know", "that", "it", "from", "please", "make", "sure", "who", "better", "sup", "ago", "asked", "he", "at", "same", "time", "your", "had", "about", "not", "like", "could", "also", "is", "hey", "ty", "when"]
                for i in content:
                    if i not in content2 and i not in removeitems:
                        content2.append(i)
                for i in range(0, len(content2)):
                    mk.write(content2[i] + "," + str(content.count(content2[i])) + "\n")
                mk.close()
                await message.channel.send("CSV", file=discord.File("kwfrequency.csv"))
            ch.close()

        ####################################################################################################
        # 
        # Used to message a user directly with jarvis
        #
        ####################################################################################################
        elif ('!jarvisDM' in message.content) and ( str(message.author) !=  str(self.notiTix) ) and (discord.utils.get(message.channel.guild.roles, name="Staff") in message.author.roles):
            y = message.content.split(",", 2)
            y = [z.strip(' ') for z in y]

            usrName, discrim = y[1].split("#")

            if len(y) != 3:
                print("Please enter all the commands: !jarvisDM,usr#1234,message_here")
            elif len(y) == 3:
                try:
                    mem = discord.utils.get(self.Notiguild.members, name=usrName, discriminator=discrim)
                    await mem.send(str(y[2]))
                except Exception as e:
                    logging.error(e)

        ####################################################################################################
        # 
        # Used to generate ticket info from staff (Chars and Ticket number)
        #
        ####################################################################################################
        elif ('!staffReport' in message.content):
            if message.channel.category_id == 570142944250691585:
                try:
                    self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                    logging.info("Opened database successfully for staff report")
                    cur = self.conn.cursor()
                    cur.execute("""SELECT staff, bot + proxy + site + membership + prflcards + other + support + start + retailsite + retailbot + botsetup as ticket_total, char_bot + char_proxy + char_site + char_membership + char_prflcards + char_other + char_support + char_start + char_retailbot + char_retailsite + char_botsetup as char_total, staff_id FROM PUBLIC.JARVIS_STAFF""" )
                    rows = cur.fetchall()
                    report = ""
                    report2 = ""
                    report3 = ""
                    report4 = ""
                    for staff in rows:
                        logging.info("Staff: " + str(staff[0]) + " | " + str(staff[3]) + " Ticket Total: " + str(staff[1]) + " Character Total: " + str(staff[2]))
                        if len(report)<1800:
                            report += ("Staff: " + str(staff[0]) + " | " + str(staff[3]) + " Ticket Total: " + str(staff[1]) + " Character Total: " + str(staff[2]) + "\n")
                        elif len(report2)<1800 and len(report) > 1700:
                            report2 += ("Staff: " + str(staff[0]) + " | " + str(staff[3]) + " Ticket Total: " + str(staff[1]) + " Character Total: " + str(staff[2]) + "\n")
                        elif len(report3)<1800 and len(report) > 1700:
                            report3 += ("Staff: " + str(staff[0]) + " | " + str(staff[3]) + " Ticket Total: " + str(staff[1]) + " Character Total: " + str(staff[2]) + "\n")
                        else: 
                            report4 += ("Staff: " + str(staff[0]) + " | " + str(staff[3]) + " Ticket Total: " + str(staff[1]) + " Character Total: " + str(staff[2]) + "\n")
                    await message.channel.send(report)
                    if len(report2) > 5:
                        await message.channel.send(report2)
                    if len(report3) > 5:
                        await message.channel.send(report3)
                    if len(report4) > 5:
                        await message.channel.send(report4)
                    logging.info("Start send report csv")
                    sqlStr = """SELECT staff, staff_id, bot + proxy + site + membership + prflcards + other + support + start + retailsite + retailbot + botsetup as ticket_total, char_bot + char_proxy + char_site + char_membership + char_prflcards + char_other + char_support + char_start + char_retailbot + char_retailsite + char_botsetup as char_total FROM PUBLIC.JARVIS_STAFF"""
                    outputQuery = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(sqlStr)
                    timeofreport = str(time.ctime(time.time()))
                    timeofreport = timeofreport.replace(":","_")
                    reportName = 'report/' + timeofreport + ".csv"
                    with open(reportName, "w") as file:
                        cur.copy_expert(outputQuery, file)
                    await message.channel.send("CSV", file=discord.File(reportName))
                    self.conn.close()
                    logging.info("Sent CSV report completed")
                except Exception as e:
                    logging.error(e)
                    self.conn.close()

        ####################################################################################################
        # 
        # Used to clear ticket count and chars
        #
        ####################################################################################################
        elif ('!staffClear' in message.content):
            if message.channel.category_id == 570142944250691585:
                try:
                    self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                    logging.info("Opened database successfully for staff report clear")
                    cur = self.conn.cursor()
                    cur.execute("""UPDATE PUBLIC.JARVIS_STAFF SET "bot" = '0', "proxy" = '0', "site" = '0', "membership" = '0', "prflcards" = '0', "other" = '0', "support" = '0', "start" = '0', "retailbot" = '0', "retailsite" = '0', "botsetup" = '0', "char_bot" = '0', "char_proxy" = '0', "char_site" = '0', "char_membership" = '0', "char_prflcards" = '0', "char_other" = '0', "char_support" = '0', "char_start" = '0', "char_retailsite" = '0', "char_retailbot" = '0', "char_botsetup" = '0' WHERE "id" > 0;""" )
                    self.conn.commit()
                    self.conn.close()
                    await message.channel.send("Staff counts cleared")
                except Exception as e:
                    logging.error(e)
                    self.conn.close()

        try:
            if message.channel.category_id == 570248275374899200:
                staffRole = discord.utils.get(message.channel.guild.roles, name="Staff")
                if staffRole in message.author.roles:
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""SELECT "staff_id" FROM PUBLIC.JARVIS_STAFF """ )
                        rows = cur.fetchall()
                        self.conn.close()
                        staffExist = False
                        for jstaff in rows:
                            if int(message.author.id) == int(jstaff[0]):
                                staffExist = True
                        if staffExist is False:
                            try:
                                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                                logging.info("Opened database successfully")
                                cur = self.conn.cursor()
                                cur.execute("""INSERT INTO PUBLIC.JARVIS_STAFF ("staff", "staff_id") VALUES (%s, %s)""",( str(message.author), int(message.author.id) ) )
                                self.conn.commit()
                                logging.info("New staff member added")
                                logging.info(str(message.author))
                                self.conn.close()
                            except Exception as e:
                                logging.error(e)
                                self.conn.close()    
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()

                if staffRole in message.author.roles:
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""SELECT "staff" FROM PUBLIC.JARVIS WHERE "chId" = %s  """, (int(message.channel.id), ) )
                        row = cur.fetchone()
                        if message.author.name not in str(row):
                            cur.execute("""UPDATE PUBLIC.JARVIS SET "staff" = ("staff" || %s || ',') WHERE "chId" = %s""",(str(message.author),int(message.channel.id)))
                            self.conn.commit()
                            logging.info("Added staff member:")
                            logging.info(str(message.author))
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully for char count Jarvis")
                        cur = self.conn.cursor()
                        cur.execute("""SELECT "mainCat" FROM PUBLIC.JARVIS WHERE "chId" = %s  """, (int(message.channel.id), ) )
                        row = cur.fetchone()
                        self.conn.close()
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully for char count Jarvis.Staff")
                        cur = self.conn.cursor()
                        cur.execute( sql.SQL("SELECT {} FROM PUBLIC.JARVIS_STAFF WHERE staff_id = %s  ").format(sql.Identifier("char_" + row[0]) ),  (int(message.author.id),))
                        row2 = cur.fetchone()
                        self.conn.close()
                        current = row2[0] + len(message.content)
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute( sql.SQL("UPDATE PUBLIC.JARVIS_STAFF SET {} =  %s  WHERE staff_id = %s").format(sql.Identifier("char_" + row[0]) ),  (current, int(message.author.id)))
                        self.conn.commit()
                        logging.info("Counted staff member %s in %s for %s chars in cat %s",str(message.author), message.channel.name, str(len(message.content)), row[0]  )
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
        except Exception as e:
            logging.error(e)

    async def on_guild_channel_delete(self, ch):

        if ch.category_id == 570248275374899200:
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""SELECT * FROM PUBLIC.JARVIS WHERE "chId" = %s  """, (int(ch.id), ) )
                row = cur.fetchone()
                mem = discord.utils.get(ch.guild.members, id=int(row[11]) )
                self.conn.close()
                if discord.utils.get(ch.guild.roles, name="Staff") not in mem.roles:
                    await mem.send("Please fill out this brief survey regarding your ticket experience today to help us better serve you in the future.\nhttps://notify.wiki/ticket-survey")
                    logging.info("Sending survey message to:")
                    logging.info(mem.name)
                logging.info(str(ch))
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""UPDATE PUBLIC.JARVIS SET "resolved" = %s WHERE "chId" = %s""",(True, int(ch.id) ))
                cur.execute("""UPDATE PUBLIC.JARVIS SET "resolvedAt" = %s WHERE "chId" = %s""",(time.ctime(), int(ch.id) ))
                self.conn.commit()
                logging.info("Updated DB for ticket resolution")
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""SELECT * FROM PUBLIC.JARVIS WHERE "chId" = %s  """, (int(ch.id), ) )
                row = cur.fetchone()
                self.conn.close()
                guild = bot.get_guild(570142274902818816)
                support = discord.utils.get(guild.roles, name="Staff")
                user = str(row[9]).split(':')
                usersSplit = str(user[1]).split(',')
                for usr in usersSplit:
                    if usr != ([] or None):
                        memName = usr.split('#')
                        mem = discord.utils.get(guild.members, name=memName[0])
                        if support in mem.roles:
                            try:
                                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                                logging.info("Opened database successfully")
                                cur = self.conn.cursor()
                                cur.execute( sql.SQL("SELECT {} FROM PUBLIC.JARVIS_STAFF WHERE staff_id = %s  ").format(sql.Identifier( row[3] ) ), (int(mem.id),))
                                row2 = cur.fetchone()
                                self.conn.close()
                                current = int(row2[0]) + 1
                                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                                logging.info("Opened database successfully")
                                cur = self.conn.cursor()
                                cur.execute( sql.SQL("UPDATE PUBLIC.JARVIS_STAFF SET {} =  %s  WHERE staff_id = %s").format(sql.Identifier(row[3]) ),  (current, int(mem.id)))
                                self.conn.commit()
                                logging.info("Counted staff member %s in %s for %s cat",str(mem.name), str(ch.name), str(row[3])  )
                                self.conn.close()
                            except Exception as e:
                                logging.error(e)
                                self.conn.close()
            except Exception as e:
                logging.error(e)



####################################################################################################
# Purpose: Ping users after 10min of inactivity
#
#
#
# Inputs: None
#
# Outputs: None
#
# Future:
#
####################################################################################################

    async def reminder(self):
        await self.wait_until_ready()

        while not self.is_closed():
            try:
                guild = bot.get_guild(570142274902818816)
                begRole = discord.utils.get(guild.roles, name="Beginner")
                ninety_days_ago = datetime.today() - timedelta(days=90)
                for mem in guild.members:
                    if mem.joined_at <= ninety_days_ago:
                        await mem.add_roles(begRole)
                        logging.info("Added Begginer role to", mem.name)
                    else:
                        if (begRole in mem.roles) and (mem.joined_at > ninety_days_ago):
                            await mem.remove_roles(begRole)
                            await mem.send("Hello the Beginner role has been removed")
                            logging.info("Removed Begginer role to", mem.name)
            except Exception as e:
                logging.error(e)
                self.conn.close()
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully for reminder")
                cur = self.conn.cursor()
                cur.execute("""SELECT * FROM PUBLIC.JARVIS WHERE "resolved" = %s  """, (False, ) )
                rows = cur.fetchall()
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
            try:
                for row in rows:
                    if (row != None) or (row != 0):
                        try:
                            guild = bot.get_guild(570142274902818816)
                            channel = discord.utils.get(guild.channels, id=row[10])
                            if "-" not in channel.name:
                                if (row[4] == "None") and ("start" not in row[3]):
                                    await channel.edit(name= (row[3]+"-"+channel.name) )
                                elif "start" in row[3]:
                                    await channel.edit(name= ("other"+"-"+channel.name) )
                                else:
                                    await channel.edit(name= (row[3]+"-"+row[4]+"-"+channel.name) )
                                logging.info("edited %s channel name", channel.name)
                        except Exception as e:
                            logging.error(e)
                            logging.error(row[10])
                        hour = time.strftime("%H", time.localtime())
                        if (row[5] == False) and (int(hour) > 6) and (int(hour) < 23):
                            passed = time.time() - row[12]
                            if (passed > 1800) and ('#' not in str(row[9])):
                                try:
                                    support = discord.utils.get(guild.roles, name="Support Services")
                                    channel = discord.utils.get(guild.channels, id=row[10])
                                    for usr in channel.members:
                                        if support in usr.roles:
                                            await usr.send("Hello " + usr.name + " please take a look at un-answered " + channel.mention )
                                            logging.info("Sent %s new reminder for %s ticket", usr.name, channel.name)
                                except Exception as e:
                                    logging.error(e)
                                try:
                                    self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                                    logging.info("Opened database successfully")
                                    cur = self.conn.cursor()
                                    cur.execute("""UPDATE PUBLIC.JARVIS SET "reminder" = %s WHERE "chId" = %s""",(time.time(), row[10] ))
                                    self.conn.commit()
                                    logging.info("Sent new messages to remind staff")
                                    self.conn.close()
                                except Exception as e:
                                    logging.error(e)
                                    self.conn.close()
                            else:
                                try:
                                    guild = bot.get_guild(570142274902818816)
                                    channel = discord.utils.get(guild.channels, id=row[10])
                                    rowAuth = discord.utils.get(guild.members, id=row[11])
                                    support = discord.utils.get(guild.roles, name="Support Services")
                                    lastMsg = await channel.fetch_message(channel.last_message_id)
                                    passed = time.time() - row[12]
                                    if (passed > 1800) and (lastMsg.author == rowAuth):
                                        try:
                                            self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                                            logging.info("Opened database successfully")
                                            cur = self.conn.cursor()
                                            cur.execute("""UPDATE PUBLIC.JARVIS SET "reminder" = %s WHERE "chId" = %s""",(time.time(), row[10] ))
                                            self.conn.commit()
                                            logging.info("Sent messages to remind staff")
                                            self.conn.close()
                                        except Exception as e:
                                            logging.error(e)
                                            self.conn.close()
                                        user = str(row[9]).split(':')
                                        usersSplit = str(user[1]).split(',')
                                        for usr in usersSplit:
                                            if usr != ([] or None):
                                                memName = usr.split('#')
                                                mem = discord.utils.get(guild.members, name=memName[0])
                                                if support in mem.roles and ("help" not in channel.name) and ("issue" not in channel.name) and ("question" not in channel.name) and ("key"not in channel.name) and ("michael" not in channel.name) and ("transfer" not in channel.name):
                                                    await mem.send("Hello " + mem.name + " please take another look at " + channel.mention )
                                                    logging.info("Sent %s reminder for %s ticket", mem.name, channel.name)
                                except Exception as e:
                                    logging.error(e)

            except Exception as e:
                logging.error(e)
            await asyncio.sleep(1800) # task runs every 30 min

####################################################################################################
# Purpose: Possible class for channel states
#
#
#
# Inputs: None
#
# Outputs: None
#
# Future:
#
####################################################################################################
class userSession:

    #tixChannel = []

    def __init__(self,channel,message,cat,subCat, resolved):

        #self.tixChannel[channel] = [channel, message, cat, subCat, resolved]
        self.cat = cat
        self.subCat = subCat
        self.helpMsg = message
        self.channel = channel
        self.resolved = resolved

    def updateSession(self,message,cat,subCat, resolved):
        self.helpMsg = message
        self.cat = cat
        self.subCat = subCat
        self.resolved = resolved

    def getSession(self,channel):
        return self.channel, self.helpMsg, self.cat, self.subCat, self.resolved


bot = DiscordBot(intents=intents)
bot.run(token)
