import discord
import os
import time
import logging
import asyncio
import psycopg2
from psycopg2 import sql

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), filename='info.log', filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')


#Bot Token
token = ''
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

class DiscordBot(discord.Client):

    tixChannels = [0] * 10001
    notibot = 0
    category = "start"
    resolved = False
    tixCounter = [0] * 10
    botTimer = time.time()

    #Discord dev id's
    botEmoji = '<:bot_related:872705898919919666>'
    proxyEmoji = '<:proxy_related:872727550596632586>'
    newEmoji = '<:newrelated:737553433665732648>'
    siteEmoji = '<:site_related:872705898999599134>'
    resellEmoji = '<:resellrelated:737714424219041882>'
    memberEmoji = '<:membership_related:872705899494514758>'
    serverEmoji = '<:server_related:872705899112833054>'
    cardEmoji = '<:cardrelated:737553581808418876>'
    gmailEmoji = '<:gmail_related:872705899284807690>'
    otherEmoji = '<:question_mark:872705899477737482>'
    supportEmoji = '<:support_related:872705899477729310>'
    restartEmoji = '<:restart_prompts:872705977911234590>'
    cookieEmoji = '<:cookie:737719937296105603>'
    canada = '🍁'


    DBTable = ""
    DBHost = ""
    DBUsr = ""
    DBPass = ""
    DBPort = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.reminder())

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
        embedVar.set_footer(text = "Jarvis")
        embedVar.set_thumbnail(url = 'https://dashboard.notify.vip/public/images/logo.png')
        return embedVar

####################################################################################################
# Purpose: Used to reload the main menu once a user clicks restart emoji to begin process again
#
#
#
# Inputs: Discord message and embed object
#
# Outputs: embed of main menu
#
# Future:
#
####################################################################################################
    async def setRestart(self,embedVar,message):

        embedVar = discord.Embed(title="Resolve issue", description='''Please react with the emoji that best fits your question
                                                                        \n''' + self.botEmoji + ''' Bot related
                                                                        \n''' + self.proxyEmoji + ''' Proxy related
                                                                        \n''' + self.siteEmoji + ''' Site related
                                                                        \n''' + self.memberEmoji + ''' Membership
                                                                        \n''' + self.otherEmoji + ''' Other
                                                                        \n''' + self.supportEmoji + ''' Talk to Support
                                                                        \n''' + self.restartEmoji + ''' At any time to start over''', color=0xDB0B23)
        await self.setFooter(embedVar)

        message = await message.channel.send( embed=embedVar)
        await message.add_reaction( self.botEmoji)
        await message.add_reaction( self.proxyEmoji)
        await message.add_reaction( self.siteEmoji)
        await message.add_reaction( self.memberEmoji)
        await message.add_reaction( self.otherEmoji)
        await message.add_reaction( self.supportEmoji)
        await message.add_reaction( self.restartEmoji)
        return embedVar

####################################################################################################
# Purpose: Triggers on each Discord reaction to serve the correct embed of information to the user
#          Gets the state of each ticket channel from tixChannels list
#
#
# Inputs: Discord reaction and the respective user objects
#
# Outputs: None
#
# Future: Use class instead of list?
#
####################################################################################################
    async def on_raw_reaction_add(self, reaction):
        guild = bot.get_guild(570142274902818816)
        ch = bot.get_channel(reaction.channel_id)
        if (reaction.member != self.notibot) and (ch.category_id == 570248275374899200):
            try:
                self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                logging.info("Opened database successfully")
                cur = self.conn.cursor()
                cur.execute("""SELECT * FROM PUBLIC.JARVIS WHERE "chId" = %s  """, (int(ch.id), ) )
                row = cur.fetchone()
                channel = discord.utils.get(guild.channels, id=int(row[10]))
                message = await channel.fetch_message(reaction.message_id)
                category = str(row[3])
                subCat = str(row[4])
                resolved = row[5]
                created = row[6]
                author = row[7]
                resolved = row[8]
                staff = row[9]
                chId = row[10]
                authId = row[11]
                self.conn.close()
            except Exception as e:
                logging.error(e)
                self.conn.close()
                return
            if row == None:
                return

            #Discord Emote Id's
            start = '💌'
            self.balko = '<:balkobot:862470852817059871>'
            self.cybersole = '<:cybersole:732423220577173566>'
            self.kodai = '<:kodai:732423220853997708>'
            self.mekpreme = '<:mekpreme:614273873956831232>'
            self.nsb = '<:nsb:570435569750900758>'
            self.pd = '<:pd:732423220929495141>'
            self.soleaio = '<:soleaio:862469783630774312>'
            self.splashforce = '<:splashforce:641785443125297173>'
            self.whatbot = '<:whatbot:732423221823012897>'
            self.wrath = '<:wrath:619333000072790016>'
            self.tsb = '<:tsb:862469783693164554>'
            self.tohru = '<:tohru:729762487515480144>'
            self.nikeOther = '<:nike_bots:872705946248429589>'
            self.aioOther = '<:other_AIO_bots:872705946655285258>'
            self.prism = '<:prism:753691950502117528>'
            self.nebula = '<:nebula:749721765776719872>'
            self.adidas = '<:adidas_bots:872705946487488542>'

            self.ecb = '<:ecb:862469783386849290>'
            self.dashe = '<:dashe:862469783387242546>'
            self.ganesh = '<:ganesh:862471436370182165>'
            self.galaxsio = '<:galaxsio:862470853013536789>'
            self.kylinbot = '<:kylinbot:862469783478992946>'
            self.mekaio = '<:mekaio:862469783701028904>'
            self.ominous = '<:ominous:864302805971632148>'
            self.phantom = '<:ghost:862469783097704500>'
            self.quickcop = '<:quickcop:862469783676649502>'
            self.stellar = '<:stellar:864302972476325908>'
            self.valor = '<:valoraio:862469783273734185>'
            self.zephyr = '<:zephyraio:862469783757127701>'
            self.noble = '<:noble:887731691815305266>'
            self.nyte = '<:nyte:862469783726981120>'

            self.concepts = '<:concepts:872706006268928030>'
            self.dsm = '<:DSM:872706006247956541>'
            self.finishJd = '<:finishline:872706006092754945>'
            self.footsites = '<:footlocker:872706006315061279>'
            self.hibbet = '<:hibbett:872706006336024606>'
            self.kith = '<:kith:872706006654808095>'
            self.shopify = '<:shopify:872706006377984020>'
            self.supreme = '<:supreme:872706006327656488>'
            self.undef = '<:undefeated:872706006369583124>'
            self.yzy = '<:yeezy:872706006461870100>'
            self.target = '<:target:872706006474432532>'
            self.bestbuy = '<:bestbuy:872706006243754045>'
            self.amazon = '<:amazon:872706006457659442>'
            self.notiLogo = '<:notifylogo:833564290225012766>'
            self.gcs = '<:GCS:872706006587691078>'
            self.aws = '<:AWS:872706006575091713>'
            self.nikesite = '<:nike:872706006453465128>'
            self.adidassite = '<:adidas:872706006214381619>'
            self.walmart = '<:walmart:874529769000144947>'

            self.alert = ' <@&575144399013543977>'

########################################################
#START OF RED/GREEN REACTION EMOTE
########################################################

            if str(reaction.emoji) == '🟢':
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
                await message.clear_reactions()
                embedVar = None
                await self.setRestart(embedVar,message)

            elif str(reaction.emoji) == '🔴':
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
                await message.clear_reactions()
                embedVar = discord.Embed(title="Resolved issue", description="Ticket will be closed by support.", color=0xDB0B23)
                await self.setFooter(embedVar)
                message = await message.channel.send( embed=embedVar)

########################################################
#END OF RED/GREEN REACTION EMOTE
########################################################

########################################################
#START OF CATEGORY SELECTION / SUPPORT TREE
########################################################

            if category == "start":
                if (str(reaction.emoji) == self.botEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "menu", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Bot Related", description=self.siteEmoji + " Site related" + "\n\n" + self.botEmoji + " General\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.siteEmoji)
                    await message.add_reaction( self.botEmoji)
                    await message.add_reaction( self.restartEmoji)

                #Begin proxy related support tree

                #PROXY
                elif (str(reaction.emoji) == self.proxyEmoji):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Proxy Related", description=self.notiLogo + " Notify Proxy related" + "\n" + self.proxyEmoji + " General?\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.notiLogo)
                    await message.add_reaction( self.proxyEmoji)
                    await message.add_reaction( self.restartEmoji)
                    #PROXY

                #NEW TO BOTTING
                elif (str(reaction.emoji) == self.newEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("newbotter", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="New to botting", description="Refer to https://hub.notify.org/guides/general/introduction-to-botting.\n Did it solve your issue?\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #NEW TO BOTTING

                #SITE
                elif (str(reaction.emoji) == self.siteEmoji):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Site Related", description= self.concepts + ''' Concepts
                                                                                    \n''' + self.dsm + ''' DSM
                                                                                    \n''' + self.finishJd + ''' Finishline and JD Sports
                                                                                    \n''' + self.footsites + ''' Footsites
                                                                                    \n''' + self.hibbet + ''' Hibbett
                                                                                    \n''' + self.kith + ''' Kith
                                                                                    \n''' + self.shopify + ''' Shopify General
                                                                                    \n''' + self.supreme + ''' Supreme
                                                                                    \n''' + self.undef + ''' Undefeated
                                                                                    \n''' + self.yzy + ''' Yeezy Supply and Adidas
                                                                                    \n''' + self.notiLogo + ''' Talk to Support
                                                                                    \n''' + self.restartEmoji + ''' At any time to start over''', color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.concepts)
                    await message.add_reaction( self.dsm)
                    await message.add_reaction( self.finishJd)
                    await message.add_reaction( self.footsites)
                    await message.add_reaction( self.hibbet)
                    await message.add_reaction( self.kith)
                    await message.add_reaction( self.shopify)
                    await message.add_reaction( self.supreme)
                    await message.add_reaction( self.undef)
                    await message.add_reaction( self.yzy)
                    await message.add_reaction( self.notiLogo)
                    await message.add_reaction( self.restartEmoji)
                    #SITE

                #RESELL
                elif (str(reaction.emoji) == self.resellEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("upcoming", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Upcoming and Resell", description="📅 What is releasing this week/month\n🚩 Upcoming release resell value\n" + self.resellEmoji + " Selling or holding and investing\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '📅')
                    await message.add_reaction( '🚩')
                    await message.add_reaction( self.resellEmoji)
                    await message.add_reaction( self.restartEmoji)
                    #RESELL

                #CANADA
                elif (str(reaction.emoji) == self.canada):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("canada", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Canada", description="Refer to this guide: https://bit.ly/2Z12Zy6. Did it solve your issue?\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #CANADA

                #MEMBER
                elif (str(reaction.emoji) == self.memberEmoji):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Membership", description="⛔Cancellation\n❓Other\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '⛔')
                    await message.add_reaction( '❓')
                    await message.add_reaction( self.restartEmoji)
                    #MEMBER

                #SERVER
                elif (str(reaction.emoji) == self.serverEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("servers", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Servers", description=self.gcs + " Google Cloud Services(GCS)" + "\n" + self.aws + " Amazon Web Services(AWS)\n❓ Other\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.gcs)
                    await message.add_reaction( self.aws)
                    await message.add_reaction( '❓')
                    await message.add_reaction( self.restartEmoji)
                    #SERVER

                #CARDS
                elif (str(reaction.emoji) == self.cardEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("prflcards", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Profiles and Cards", description=self.memberEmoji + " Profile j!gging" + "\n" + self.cardEmoji + " Cards\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.memberEmoji)
                    await message.add_reaction( self.cardEmoji)
                    await message.add_reaction( self.restartEmoji)
                    #CARDS

                #GMAIL
                elif (str(reaction.emoji) == self.gmailEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("captcha", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Captcha, Gmails, and Cookies", description=self.gmailEmoji + " Captcha/Gmails" + "\n" + self.cookieEmoji + " Cookies\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.gmailEmoji)
                    await message.add_reaction( self.cookieEmoji)
                    await message.add_reaction( self.restartEmoji)
                    #GMAIL

                #OTHER
                elif (str(reaction.emoji) == self.otherEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("other", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Other", description="Refer to https://hub.notify.org/guides/general/other-guides. Did it solve your issue?\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #OTHER

                #DIRECT SUPPORT
                elif (str(reaction.emoji) == self.supportEmoji):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #DIRECT SUPPORT

                #Restart the process at any point to the start
                elif (str(reaction.emoji) == self.restartEmoji):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("start", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                #Needed for the restart process
                elif str(reaction.emoji) == start:
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("start", "None", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)

########################################################
#END OF CATEGORY SELECTION / SUPPORT TREE
########################################################

########################################################
#START OF BOT CATEGORY SELECTION
########################################################

            #EMBED WITH EMOTE SELECTION TO CHOOSE NEXT BOT
            elif category == "bot":
                if (str(reaction.emoji) == self.siteEmoji) and (subCat == "menu"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "site", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Bot Site Related", description= self.amazon + ''' Amazon
                                                                                    \n''' + self.bestbuy + ''' BestBuy
                                                                                    \n''' + self.finishJd + ''' Finishline and JD Sports
                                                                                    \n''' + self.footsites + ''' Footsites
                                                                                    \n''' + self.hibbet + ''' Hibbett
                                                                                    \n''' + self.nikesite + ''' Nike
                                                                                    \n''' + self.shopify + ''' Shopify General
                                                                                    \n''' + self.supreme + ''' Supreme
                                                                                    \n''' + self.target + ''' Target
                                                                                    \n''' + self.walmart + ''' Walmart
                                                                                    \n''' + self.yzy + ''' Yeezy Supply and Adidas
                                                                                    \n''' + self.notiLogo + ''' Talk to Support
                                                                                    \n''' + self.restartEmoji + ''' At any time to start over''', color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.amazon)
                    await message.add_reaction( self.bestbuy)
                    await message.add_reaction( self.finishJd)
                    await message.add_reaction( self.footsites)
                    await message.add_reaction( self.hibbet)
                    await message.add_reaction( self.nikesite)
                    await message.add_reaction( self.shopify)
                    await message.add_reaction( self.supreme)
                    await message.add_reaction( self.target)
                    await message.add_reaction( self.walmart)
                    await message.add_reaction( self.yzy)
                    await message.add_reaction( self.notiLogo)
                    await message.add_reaction( self.restartEmoji)

                #AWAITING USER REACTION TO EMOTE IF BOT SUPPORT WAS SELECTED
                if (str(reaction.emoji) == self.botEmoji) and (subCat == "menu"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "general", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Bot Related 1/2", description="Please choose a bot you need help with below\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction(self.balko)
                    await message.add_reaction(self.cybersole)
                    await message.add_reaction(self.ecb)
                    await message.add_reaction(self.dashe)
                    await message.add_reaction(self.ganesh)
                    await message.add_reaction(self.kodai)
                    await message.add_reaction(self.kylinbot)
                    await message.add_reaction(self.mekpreme )
                    await message.add_reaction(self.mekaio)
                    await message.add_reaction(self.nebula )
                    await message.add_reaction(self.ominous)
                    await message.add_reaction(self.pd )
                    await message.add_reaction(self.phantom)
                    await message.add_reaction(self.prism)
                    await message.add_reaction(self.quickcop)
                    await message.add_reaction(self.stellar)
                    await message.add_reaction(self.soleaio )
                    await message.add_reaction(self.splashforce )
                    await message.add_reaction(self.tohru)
                    await message.add_reaction(self.tsb)

                    embedVar = discord.Embed(title="Bot Related 2/2", description= self.nikeOther + " For Other Nike Bots\n\n"+ self.aioOther + " For Other AIO Bots\n\n" + self.restartEmoji + " At any time to start over", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction(self.valor)
                    await message.add_reaction(self.whatbot )
                    await message.add_reaction(self.wrath )
                    await message.add_reaction(self.zephyr)
                    await message.add_reaction(self.nikeOther )
                    await message.add_reaction(self.aioOther )

                    await message.add_reaction( self.restartEmoji)

                #AWAITING USER REACTION TO EMOTE IF SITE SPECIFIC BOT SUPPORT WAS SELECTED
                if (str(reaction.emoji) == self.siteEmoji) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "site", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Bot Site Related", description= self.amazon + ''' Amazon
                                                                                    \n''' + self.bestbuy + ''' BestBuy
                                                                                    \n''' + self.finishJd + ''' Finishline and JD Sports
                                                                                    \n''' + self.footsites + ''' Footsites
                                                                                    \n''' + self.hibbet + ''' Hibbett
                                                                                    \n''' + self.nikesite + ''' Nike
                                                                                    \n''' + self.shopify + ''' Shopify General
                                                                                    \n''' + self.supreme + ''' Supreme
                                                                                    \n''' + self.target + ''' Target
                                                                                    \n''' + self.walmart + ''' Walmart
                                                                                    \n''' + self.yzy + ''' Yeezy Supply and Adidas
                                                                                    \n''' + self.notiLogo + ''' Talk to Support
                                                                                    \n''' + self.restartEmoji + ''' At any time to start over''', color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.amazon)
                    await message.add_reaction( self.bestbuy)
                    await message.add_reaction( self.finishJd)
                    await message.add_reaction( self.footsites)
                    await message.add_reaction( self.hibbet)
                    await message.add_reaction( self.nikesite)
                    await message.add_reaction( self.shopify)
                    await message.add_reaction( self.supreme)
                    await message.add_reaction( self.target)
                    await message.add_reaction( self.walmart)
                    await message.add_reaction( self.yzy)
                    await message.add_reaction( self.notiLogo)
                    await message.add_reaction( self.restartEmoji)

########################################################
#END OF CATEGORY SELECTION / SUPPORT TREE
########################################################

########################################################
#START OF SITE GUIDE REFERENCE
########################################################

                #AMAZON
                if (str(reaction.emoji) == self.amazon) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "amazon", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Amazon", description="Refer to https://hub.notify.org/guides/sites/amazon\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #AMAZON

                #BESTBUY
                if (str(reaction.emoji) == self.bestbuy) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "bestbuy", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="BestBuy", description="Refer to https://hub.notify.org/guides/sites/bestbuy\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #BESTBUY

                #JDFNL
                if (str(reaction.emoji) == self.finishJd) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "finishjd", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Finishline and JDSports", description="Refer to https://hub.notify.org/guides/sites/fnl-jd\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #JDFNL

                #FOOTSITES
                if (str(reaction.emoji) == self.footsites) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "footsites", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Footsites", description="Refer to https://hub.notify.org/guides/sites/footsites\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #FOOTSITES

                #HIBBETT
                if (str(reaction.emoji) == self.hibbet) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "hibbett", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Hibbett", description="Refer to https://hub.notify.org/guides/sites/hibbett\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #HIBBETT

                #NIKE
                if (str(reaction.emoji) == self.nikesite) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "nike", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Nike", description="Refer to https://hub.notify.org/guides/sites/nike\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #NIKE

                #SHOPIFY
                if (str(reaction.emoji) == self.shopify) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "shopify", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Shopify", description="Refer to https://hub.notify.org/guides/sites/shopify\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SHOPIFY

                #SUPREME
                if (str(reaction.emoji) == self.supreme) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "supreme", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Supreme", description="Refer to https://hub.notify.org/guides/sites/supreme\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SUPREME

                #TARGET
                if (str(reaction.emoji) == self.target) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "target", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Target", description="Refer to https://hub.notify.org/guides/sites/target-walmart\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #TARGET

                #WALMART
                if (str(reaction.emoji) == self.walmart) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "walmart", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Walmart", description="Refer to https://hub.notify.org/guides/sites/target-walmart\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #WALMART

                #YEEZYSUPPLY
                if (str(reaction.emoji) == self.yzy) and (subCat == "site"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "yzy", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Yeezy Supply and Adidas", description="Refer to https://hub.notify.org/guides/sites/ys-adidas\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #YEEZYSUPPLY

########################################################
#END OF SITE GUIDE REFERENCE
########################################################

########################################################
#START OF BOTS GUIDE REFERENCE
########################################################

                #BALKOBOT
                if (str(reaction.emoji) == self.balko) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Balkobot", description="Refer to https://hub.notify.org/guides/bots/balkobot\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #BALKOBOT

                #CYBER
                elif (str(reaction.emoji)== self.cybersole) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Cybersole", description="Refer to https://hub.notify.org/guides/bots/cybersole\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #CYBER

                #KODAI
                elif (str(reaction.emoji)== self.kodai) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Kodai", description="Refer to https://hub.notify.org/guides/bots/kodai\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #KODAI

                #MEKPREME
                elif (str(reaction.emoji)== self.mekpreme) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Mekpreme", description="Refer to https://hub.notify.org/guides/bots/mekpreme\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #MEKPREME

                #NSB
                elif (str(reaction.emoji)== self.nsb) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "nsb", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="NSB", description="Refer to https://hub.notify.org/guides/bots/nsb\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #NSB

                #PD
                elif (str(reaction.emoji)== self.pd) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "pd", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Project Destroyer", description="Refer to https://hub.notify.org/guides/bots/project-destroyer\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #PD

                #SOLE
                elif (str(reaction.emoji)== self.soleaio) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "sole", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="SoleAIO", description="Refer to https://hub.notify.org/guides/bots/sole-aio\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SOLE

                #SPLASHFORCE
                elif (str(reaction.emoji)== self.splashforce) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "splashforce", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Splashforce", description="Refer to https://hub.notify.org/guides/bots/splashforce\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SPLASHFORCE

                #WHATBOT
                elif (str(reaction.emoji)== self.whatbot) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Whatbot", description="Refer to https://hub.notify.org/guides/bots/whatbot\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #WHATBOT

                #WRATH
                elif (str(reaction.emoji)== self.wrath) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Wrath", description="Refer to https://hub.notify.org/guides/bots/wrathaio\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #WRATH

                #TSB
                elif (str(reaction.emoji)== self.tsb) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "tsb", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="TSB", description="Refer to https://hub.notify.org/guides/bots/tsb\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #TSB

                #TOHRU
                elif (str(reaction.emoji)== self.tohru) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Tohru", description="Refer to https://hub.notify.org/guides/bots/tohru\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #TOHRU

                #PRISM
                elif (str(reaction.emoji)== self.prism) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Prism", description="Refer to https://hub.notify.org/guides/bots/prism\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #PRISM

                #NEBULA
                elif (str(reaction.emoji)== self.nebula) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "nebula", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Nebula", description="Refer to https://hub.notify.org/guides/bots/nebula\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #NEBULA

                #ECB
                elif (str(reaction.emoji)== self.ecb) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "ecb", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Easy Cop Bot", description="Refer to https://hub.notify.org/guides/bots/ecb\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #ECB

                #DASHE
                elif (str(reaction.emoji)== self.dashe) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "dashe", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Dashe", description="Refer to https://hub.notify.org/guides/bots/dashe\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #DASHE

                #GANESH
                elif (str(reaction.emoji)== self.ganesh) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Ganesh", description="Refer to ttps://hub.notify.org/guides/bots/ganesh\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #GANESH

                #GALAXIO
                elif (str(reaction.emoji)== self.galaxsio) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "galaxsio", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Galaxsio", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&864303571305758720>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #GALAXIO

                #KYLINBOT
                elif (str(reaction.emoji)== self.kylinbot) and (subCat == "general"):
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
                    embedVar = discord.Embed(title="Kylin Bot", description="Refer to https://hub.notify.org/guides/bots/kylin\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #KYLINBOT

                #MEKAIO
                elif (str(reaction.emoji)== self.mekaio) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="MEKaio", description="Refer to https://hub.notify.org/guides/bots/mekaio\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #MEKAIO

                #OMINOUS
                elif (str(reaction.emoji)== self.ominous) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "ominous", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Ominous", description="Refer to https://hub.notify.org/guides/bots/ominous\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #OMINOUS

                #PHANTOM
                elif (str(reaction.emoji)== self.phantom) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat") = (%s, %s) WHERE "chId" = %s""",("bot", "phantom", chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Phantom", description="Refer to https://hub.notify.org/guides/bots/phantom\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #PHANTOM

                #QUICKCOP
                elif (str(reaction.emoji)== self.quickcop) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "quickcop", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="QuickCop", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&864302283927060480>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #QUICKCOP

                #STELLAR
                elif (str(reaction.emoji)== self.stellar) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "stellar", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Stellar", description="Refer to https://hub.notify.org/guides/bots/stellar\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #STELLAR

                #VALOR
                elif (str(reaction.emoji)== self.valor) and (subCat == "general"):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Valor", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&864302286943944724>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #VALOR

                #ZEPHYR
                elif (str(reaction.emoji)== self.zephyr) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "zephyr", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Zephyr", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&864302292589346846>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #ZEPHYR

                #NOBLE
                elif (str(reaction.emoji)== self.noble) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "noble", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Noble", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&887730506815373352>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #NOBLE

                #NYTE
                elif (str(reaction.emoji)== self.nyte) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "nyte", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Nyte", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&887730501031444490>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #NYTE

                #OTHER AIO
                elif (str(reaction.emoji)== self.aioOther) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "aioOther", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Other AIO Bots", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&732428090931806292> ")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #OTHER AIO

                #NIKE BOTS
                elif (str(reaction.emoji) == self.nikeOther) and (subCat == "general"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "nikeOther", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Nike Bots", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( "<@&570142940253388801>")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #NIKE BOTS

########################################################
#END OF BOTS GUIDE REFERENCE
########################################################

########################################################
#START OF SITES NOT RESOLVED
########################################################

                #AMAZON
                elif (str(reaction.emoji) == '❌')  and (subCat == "amazon"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "amazon", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Amazon", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #AMAZON

                #BESTBUY
                elif (str(reaction.emoji) == '❌')  and (subCat == "bestbuy"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "bestbuy", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="BestBuy", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #BESTBUY

                #FNLJD
                elif (str(reaction.emoji) == '❌')  and (subCat == "finishjd"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "finishjd", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Finishline and JDSports", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #FNLJD

                #FOOTSITES
                elif (str(reaction.emoji) == '❌')  and (subCat == "footsites"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "footsites", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Footsites", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #FOOTSITES

                #HIBBETT
                elif (str(reaction.emoji) == '❌')  and (subCat == "hibbett"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "hibbett", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Hibbett", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #HIBBETT

                #NIKE
                elif (str(reaction.emoji) == '❌')  and (subCat == "nike"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "nike", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Nike", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #NIKE

                #SHOPIFY
                elif (str(reaction.emoji) == '❌')  and (subCat == "shopify"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "shopify", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Shopify", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #SHOPIFY

                #SUPREME
                elif (str(reaction.emoji) == '❌')  and (subCat == "supreme"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "supreme", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Supreme", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #SUPREME

                #TARGET
                elif (str(reaction.emoji) == '❌')  and (subCat == "target"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "target", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Target", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #TARGET

                #WALMART
                elif (str(reaction.emoji) == '❌')  and (subCat == "walmart"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "walmart", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Walmart", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #WALMART

                #YEEZYSUPPLY
                elif (str(reaction.emoji) == '❌')  and (subCat == "yzy"):
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "yzy", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Yeezy Supply and Adidas", description="Staff will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #YEEZYSUPPLY

########################################################
#END OF SITES NOT RESOLVED
########################################################

########################################################
#START OF BOTS NOT RESOLVED
########################################################

                #ECB
                elif (str(reaction.emoji) == '❌')  and (subCat == "ecb"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302269365354538> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "ecb", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #ECB

                #DASHE
                elif (str(reaction.emoji) == '❌')  and (subCat == "dashe"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302272229015552> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "dashe", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #DASHE

                #GANESH
                elif (str(reaction.emoji) == '❌')  and (subCat == "ganesh"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302275299508224> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
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
                        #GANESH

                #GALAXIO
                elif (str(reaction.emoji) == '❌')  and (subCat == "galaxsio"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864303571305758720> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "galaxsio", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #GALAXIO

                #KYLINBOT
                elif (str(reaction.emoji) == '❌')  and (subCat == "kylinbot"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302277506105366> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "kylinbot", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #KYLINBOT

                #MEKAIO
                elif (str(reaction.emoji) == '❌')  and (subCat == "mekaio"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302280731656192> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
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
                        #MEKAIO

                #OMINOUS
                elif (str(reaction.emoji) == '❌')  and (subCat == "ominous"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302633426354177> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "ominous", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #OMINOUS

                #PHANTOM
                # elif (str(reaction.emoji) == '❌')  and (subCat == "phantom"):
                #     await message.clear_reactions()
                #     await message.channel.send( "<@&732426641606705244> Will be with you shortly.")
                #     await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                #     try:
                #         self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                #         logging.info("Opened database successfully")
                #         cur = self.conn.cursor()
                #         cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "phantom", False, chId ))
                #         self.conn.commit()
                #         logging.info("Updated DB for resolved")
                #         self.conn.close()
                #     except Exception as e:
                #         logging.error(e)
                #         self.conn.close()
                #ADDED TWICE??????? LOL

                #QUICKCOP
                elif (str(reaction.emoji) == '❌')  and (subCat == "quickcop"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302283927060480> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "quickcop", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #QUICKCOP

                #STELLAR
                elif (str(reaction.emoji) == '❌')  and (subCat == "stellar"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302295738744872> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "stellar", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #STELLAR

                #VALOR
                elif (str(reaction.emoji) == '❌')  and (subCat == "valor"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302286943944724> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
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
                        #VALOR

                #ZEPHYR
                elif (str(reaction.emoji) == '❌')  and (subCat == "zephyr"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&864302292589346846> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "zephyr", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #ZEPHYR

                #NOBLE
                elif (str(reaction.emoji) == '❌')  and (subCat == "noble"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&887730506815373352> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "noble", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOBLE

                #NYTE
                elif (str(reaction.emoji) == '❌')  and (subCat == "nyte"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&887730501031444490> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "nyte", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NYTE

                #BALKO
                elif (str(reaction.emoji) == '❌') and (subCat == "balko"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&572634780345040906> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "balko", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #BALKO

                #CYBER
                elif (str(reaction.emoji) == '❌') and (subCat == "cyber"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&570142934935142412> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "cyber", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #CYBER

                #KODAI
                elif (str(reaction.emoji) == '❌') and (subCat == "kodai"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&606319522374483978> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "kodai", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #KODAI

                #MEKPREME
                elif (str(reaction.emoji) == '❌') and (subCat == "mekpreme"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&732426610078384169> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "mekpreme", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #MEKPREME

                #NSB
                elif (str(reaction.emoji) == '❌') and (subCat == "nsb"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&570142936369594373> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "nsb", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NSB

                #PHANTOM
                elif (str(reaction.emoji) == '❌') and (subCat == "phantom"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&732426641606705244> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "phantom", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #PHANTOM

                #PD
                elif (str(reaction.emoji) == '❌') and (subCat == "pd"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&570142937766428682> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "pd", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #PD

                #SOLE
                elif (str(reaction.emoji) == '❌') and (subCat == "sole"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&570142938718535719> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "sole", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #SOLE

                #SPLASHFORCE
                elif (str(reaction.emoji) == '❌') and (subCat == "splashforce"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&641813014445817864> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "splashforce", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #SPLASHFORCE

                #WHATBOT
                elif (str(reaction.emoji) == '❌') and (subCat == "whatbot"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&570142941436313601> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "whatbot", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #WHATBOT

                #WRATH
                elif (str(reaction.emoji) == '❌') and (subCat == "wrath"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&641812933340430357> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "wrath", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #WRATH

                #TSB
                elif (str(reaction.emoji) == '❌') and (subCat == "tsb"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&732427085515063328> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "tsb", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #TSB

                #TOHRU
                elif (str(reaction.emoji) == '❌') and (subCat == "tohru"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&732426890689904662> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "tohru", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #TOHRU

                #PRISM
                elif (str(reaction.emoji) == '❌') and (subCat == "prism"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&753692572576120862> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "prism", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #PRISM

                #NEBULA
                elif (str(reaction.emoji) == '❌') and (subCat == "nebula"):
                    await message.clear_reactions()
                    await message.channel.send( "<@&749723458547613747> Will be with you shortly.")
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("bot", "nebula", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NEBULA

########################################################
#END OF BOTS NOT RESOLVED
########################################################

########################################################
#START OF BOTS RESOLVED
########################################################

                #RESOLVED IN BOT
                elif str(reaction.emoji) == '✔':
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED IN BOT

                #RESTART EMOJI
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART EMOJI

########################################################
#END OF BOTS RESOLVED
########################################################

########################################################
#START OF PROXY RELATED
########################################################

            elif category == "proxy":

                #NOTIFY PROXY RELATED
                if (str(reaction.emoji)== self.notiLogo) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Notify Proxies", description="The Judge will be with you shortly", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( '<@!657653463051927572>')
                    await message.channel.send( "Please state your question now so The Judge can better help when he arrives, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("proxy", "notify", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOTIFY PROXY RELATED

                #GENERAL PROXY
                elif (str(reaction.emoji)== self.proxyEmoji):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="General Proxy Info", description="Refer to https://hub.notify.org/guides/general/proxies \nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #GENERAL PROXY

                #RESOLVED
                elif str(reaction.emoji) == '✔':
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    # 733906246184337479 is @Alert
                    embedVar = discord.Embed(title="Not Resolved", description="Staff will be with you shortly.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET "resolved" = %sWHERE "chId" = %s""",(False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOT RESOLVED

                #RESTART EMOTE
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART EMOTE

########################################################
#END OF PROXY RELATED
########################################################

########################################################
#START OF NEW TO BOTTING
########################################################

            elif category == "newbotter":

                #RESOLVED
                if str(reaction.emoji) == '✔':
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("newbotter", "None", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="Staff member will be with you shortly.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("newbotter", "None", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOT RESOLVED

                #RESTART EMOJI
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART EMOJI

########################################################
#END OF NEW TO BOTTING
########################################################

########################################################
#END OF SITE RELATED
########################################################

            elif category == "site":

                #CNCPTS
                if (str(reaction.emoji)== self.concepts) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Concepts", description="Refer to https://hub.notify.org/guides/sites/shopify\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #CNCPTS

                #DSM
                elif (str(reaction.emoji)== self.dsm) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="DSM", description="Refer to https://hub.notify.org/guides/sites/shopify\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #DSM

                #FNLJD
                elif (str(reaction.emoji)== self.finishJd) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Finishline and JD Sports", description="Refer to https://hub.notify.org/guides/sites/finishline-and-jdsports\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #FNLJD

                #FOOTSITES
                elif (str(reaction.emoji)== self.footsites) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Footsites", description="Refer to https://hub.notify.org/guides/sites/footsites\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #FOOTSITES

                #HIBBETT
                elif (str(reaction.emoji)== self.hibbet) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Hibbett", description="Refer to https://hub.notify.org/guides/sites/hibbett\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #HIBBETT

                #KITH
                elif (str(reaction.emoji)== self.kith) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Kith", description="Refer to https://hub.notify.org/guides/sites/shopify\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #KITH

                #SHOPIFY
                elif (str(reaction.emoji)== self.shopify) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Shopify General", description="Refer to https://hub.notify.org/guides/sites/shopify\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SHOPIFY

                #SUPREME
                elif (str(reaction.emoji)== self.supreme) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Supreme", description="Refer to https://hub.notify.org/guides/sites/supreme\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SUPREME

                #UNDFTD
                elif (str(reaction.emoji)== self.undef) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Undefeated", description="Refer to https://hub.notify.org/guides/sites/shopify\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #UNDFTD

                #YEEZYSUPPLY
                elif (str(reaction.emoji)== self.yzy) :
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Yeezy Supply and Adidas", description="Refer to https://hub.notify.org/guides/sites/yeezy-supply-and-adidas\nDid it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #YEEZYSUPPLY

                #OTHER
                elif (str(reaction.emoji)== self.notiLogo):
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Talk to support", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    #OTHER

                #RESOLVED
                elif str(reaction.emoji) == '✔':
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET "resolved" = %s WHERE "chId" = %s""",( False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOT RESOLVED

                #RESTART EMOJI
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART EMOJI

########################################################
#END OF SITE RELATED
########################################################

########################################################
#START OF UPCOMING AND RESELL VALUE
########################################################

            elif category == "upcoming":

                #UPCOMING
                if str(reaction.emoji) == '📅':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="What is releasing this week/month", description="Refer to <#570143008662618114> and <#728428682682695690> for release info. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #UPCOMING

                #RED FLAG (LIKE MY LAST GF :( )
                elif str(reaction.emoji) == '🚩':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Upcoming release & resell value", description="Refer to the release channels and <#570143010088681473>. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #RED FLAG

                #RESELL INFO
                elif str(reaction.emoji) == self.resellEmoji:
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Selling or holding and investing", description="Refer to <#570143018804314114> and <#727733279834374174>. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #RESELL INFO

                #RESOLVED
                elif str(reaction.emoji) == '✔':
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("start", "None", True, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="Staff member will be with you shortly.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
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
                        #NOT RESOLVED

                #RESTART
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART

########################################################
#END OF UPCOMING AND RESELL VALUE
########################################################

#########################################################################################

        ########        #        ##      #        #        #########          #
        #              # #       # #     #       # #       #         #       # #
        #             #   #      #  #    #      #   #      #         #      #   #
        #            #     #     #   #   #     #     #     #         #     #     #
        #           #########    #    #  #    #########    #         #    #########
        #          #         #   #     # #   #         #   #         #   #         #
        ########  #           #  #      ##  #           #  #########    #           #

#########################################################################################

#Canada related (The best category ever)
            elif category == "canada":

                #RESOLVED
                if str(reaction.emoji) == '✔':
                    self.tixChannels[channel] = [ch2, message, "start", "None", True, tixTime, author]
                    resolved = True
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    resolved = False
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="Staff member will be with you shortly.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    self.tixChannels[channel] = [ch2, message, "start", "None", False, tixTime, author]
                elif (str(reaction.emoji) == self.restartEmoji):
                    self.tixChannels[channel] = [ch2, message, "start", "None", False, tixTime, author]
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #NOT RESOLVED

########################################################
#END OF CANADA
########################################################

########################################################
#START OF MEMBERSHIP STUFF
########################################################

            elif category == "membership":

                #CANCELLATION
                if str(reaction.emoji) == '⛔':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Cancellation", description="Please state the reason for your cancellation and staff will be with you shortly.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
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
                if str(reaction.emoji) == '❓':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Other", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
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

                #RESOLVED
                elif str(reaction.emoji) == '✔':
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET  "resolved" = %s WHERE "chId" = %s""",(False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOT RESOLVED

                #RESTART
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART

########################################################
#END OF MEMBERSHIP STUFF
########################################################

########################################################
#START OF SERVERS
########################################################

            elif category == "servers":

                #GOOGLE CLOUD
                if (str(reaction.emoji)== self.gcs):
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Google Cloud Services (GCS)", description="Refer to https://bit.ly/2ypDKaq. Did it solver your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #GOOGLE CLOUD

                #AMAZON WEB SERVICE
                elif (str(reaction.emoji)== self.aws):
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Amazon Web Services (AWS)", description="Refer to http://bit.ly/2ypFy3n. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #AMAZON WEB SERVICE

                #OTHER
                elif str(reaction.emoji) == '❓':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Other", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    self.tixChannels[channel] = [ch2, message, "start", "None", True, tixTime, author]
                    #OTHER

                #RESOLVED
                elif str(reaction.emoji) == '✔':
                    self.tixChannels[channel] = [ch2, message, "start", "None", True, tixTime, author]
                    resolved = True
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    resolved = False
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    self.tixChannels[channel] = [ch2, message, "start", "None", True, tixTime, author]
                    #NOT RESOLVED

                #RESTART
                elif (str(reaction.emoji) == self.restartEmoji):
                    self.tixChannels[channel] = [ch2, message, "start", "None", False, tixTime, author]
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART

########################################################
#END OF SERVERS
########################################################

########################################################
#START OF PROFILES AND CARDS
########################################################

            elif category == "prflcards":

                #SITE SELECTION FOR CARDS
                if (str(reaction.emoji) == self.memberEmoji) and subCat == "None":
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("prflcards", "prfls", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Profile J!gging", description= self.footsites + " Footsites" + "\n" +  self.finishJd +" Finishline and JD Sports"+ "\n" +  self.shopify +" Shopify"+ "\n" +  self.supreme +" Supreme\n❓ Decision", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.footsites)
                    await message.add_reaction( self.finishJd)
                    await message.add_reaction( self.shopify)
                    await message.add_reaction( self.supreme)
                    await message.add_reaction( '❓')
                    await message.add_reaction( self.restartEmoji)
                    #SITE SELECTION FOR CARDS

                #CARD INFO
                elif (str(reaction.emoji) == self.cardEmoji) and subCat == "None":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Cards", description="Refer to http://bit.ly/2ysrndW. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #CARD INFO

                #FOOTSITES
                elif (str(reaction.emoji)== self.footsites) and subCat == "prfls":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Footsites", description="Refer to https://hub.notify.org/guides/sites/footsites. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #FOOTSITES

                #FNLJD
                elif (str(reaction.emoji)== self.finishJd) and subCat == "prfls":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Finishline and JD Sports", description="Refer to https://hub.notify.org/guides/sites/finishline-and-jdsports. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #FNLJD

                #SHOPIFY
                elif (str(reaction.emoji)== self.shopify) and subCat == "prfls":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Shopify", description="Refer to Refer to https://hub.notify.org/guides/sites/shopify. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SHOPIFY

                #SUPREME
                elif (str(reaction.emoji)== self.supreme) and subCat == "prfls":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Supreme", description="Refer to https://hub.notify.org/guides/sites/supreme. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SUPREME

                #OTHER
                elif str(reaction.emoji) == '❓' and subCat == "prfls":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Decision", description="Refer to the addresses section in https://hub.notify.org/guides/general/other-guides. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #OTHER

                #RESOLVED
                elif str(reaction.emoji) == '✔':
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET  "resolved" = %s WHERE "chId" = %s""",(True, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET "resolved" = %s WHERE "chId" = %s""",(False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOT RESOLVED

                #RESTART
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART

########################################################
#END OF PROFILES AND CARDS
########################################################

########################################################
#START OF CAPTCHAS GMAILS AND COOKIES
########################################################

            elif category == "captcha":

                #CATEGORY SELECTION FOR CAPTCHAS GMAILS AND COOKIES
                if (str(reaction.emoji) == self.gmailEmoji) and subCat == "None":
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("captcha", "capt", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()

                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Gmails", description=self.gmailEmoji + " Acquiring Gmails" + "\n" +  self.supportEmoji + " Captcha scores" + "\n" +  self.serverEmoji +" Farming/AYCD\n❓ Other", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.gmailEmoji)
                    await message.add_reaction( self.supportEmoji)
                    await message.add_reaction( self.serverEmoji)
                    await message.add_reaction( '❓')
                    await message.add_reaction( self.restartEmoji)
                    #CATEGORY SELECTION FOR CAPTCHAS GMAILS AND COOKIES

                #COOKIES
                elif (str(reaction.emoji) == self.cookieEmoji)  and subCat == "None":
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("captcha", "cookies", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()

                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Cookies", description=self.supportEmoji + " How many do I need?\n❓ General Info", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( self.supportEmoji)
                    await message.add_reaction( '❓')
                    await message.add_reaction( self.restartEmoji)
                    #COOKIES

                #GMAILS
                elif (str(reaction.emoji) == self.gmailEmoji) and subCat == "capt":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Acquiring Gmails", description="<#736386564837474325> or other providers such as Blaze Gmails run by our very own 18pairsonkith. Refer to <#714175191470702652> as well. Did it resolve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #GMAILS

                #SCORES
                elif (str(reaction.emoji) == self.supportEmoji)  and subCat == "capt":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Captcha Scores", description="Scores seem to be reset every month for many Gmails, if this happens just keep farming them with human like farming. Refer to https://hub.notify.org/guides/general/captchas as well. Did it resolve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #SCORES

                #FARMNG/AYCD
                elif (str(reaction.emoji) == self.serverEmoji) and subCat == "capt":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Farming/AYCD", description="We have a partnership with AYCD, you can find it here <#719301283663839373>. Did it resolve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #FARMNG/AYCD

                #OTHER
                elif str(reaction.emoji) == '❓' and subCat == "capt":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Other", description="Refer to https://hub.notify.org/guides/general/captchas. Did it resolve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #OTHER

                #COOKIES
                elif (str(reaction.emoji) == self.supportEmoji) and subCat == "cookies":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="How many do I need?", description="Generate as many as you can. 10:1(cookies:task) ratio is ideal, but the more, the better. Did it resolve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #COOKIES

                #OTHER COOKIES
                elif str(reaction.emoji) == '❓' and subCat == "cookies":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="General Info", description="Refer to https://hub.notify.org/guides/general/cookie-generation. Did it solve your issue?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '✔')
                    await message.add_reaction( '❌')
                    await message.add_reaction( self.restartEmoji)
                    #OTHER COOKIES

                #RESOLVED
                elif str(reaction.emoji) == '✔':
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
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="A staff member will be with you shortly.\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET  "resolved" =  %s WHERE "chId" = %s""",(False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #NOT RESOLVED

                #RESTART
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART

########################################################
#END OF CAPTCHAS GMAILS AND COOKIES
########################################################

########################################################
#START OF OTHER
########################################################

            elif category == "other":

                #TEXT SUPPORT
                if str(reaction.emoji) == '0️⃣' and subCat == "No":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Text Support", description="Please describe your issue as detailed as possible and staff will be with you shortly\n", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("other", "text", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #TEXT SUPPORT

                #VOICE SUPPORT
                elif str(reaction.emoji) == '1️⃣' and subCat == "No":
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Voice Support", description="A staff member will let you know in the ticket when available to speak in voice.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.channel.send( self.alert)
                    await message.channel.send( "Please state your question now so staff can better help when they arrive, Thanks!")
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("other", "voice", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                        #VOICE SUPPORT

                #RESOLVED
                elif str(reaction.emoji) == '✔':
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET  "resolved" =  %s WHERE "chId" = %s""",(True, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Resolved", description="Anything else?", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '🟢')
                    await message.add_reaction( '🔴')
                    await message.add_reaction( self.restartEmoji)
                    #RESOLVED

                #NOT RESOLVED
                elif str(reaction.emoji) == '❌':
                    try:
                        self.conn = psycopg2.connect(database = self.DBTable, user = self.DBUsr, password = self.DBPass, host = self.DBHost, port = self.DBPort)
                        logging.info("Opened database successfully")
                        cur = self.conn.cursor()
                        cur.execute("""UPDATE PUBLIC.JARVIS SET ("mainCat", "subCat", "resolved") = (%s, %s, %s) WHERE "chId" = %s""",("other", "No", False, chId ))
                        self.conn.commit()
                        logging.info("Updated DB for resolved")
                        self.conn.close()
                    except Exception as e:
                        logging.error(e)
                        self.conn.close()
                    await message.clear_reactions()
                    embedVar = discord.Embed(title="Not Resolved", description="0️⃣ Text Support\n1️⃣ Voice Support.", color=0xDB0B23)
                    await self.setFooter(embedVar)
                    message = await message.channel.send( embed=embedVar)
                    await message.add_reaction( '0️⃣')
                    await message.add_reaction( '1️⃣')
                    await message.add_reaction( self.restartEmoji)
                    #NOT RESOLVED

                #RESTART
                elif (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)
                    #RESTART

########################################################
#END OF OTHER
########################################################

########################################################
#START OF TALK TO SUPPORT
########################################################

            elif category == "support":

                if (str(reaction.emoji) == self.restartEmoji):
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
                    await message.clear_reactions()
                    embedVar = None
                    await self.setRestart(embedVar,message)

########################################################
#END OF TALK TO SUPPORT
########################################################

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

        if ('Initiating Jarvis...' in message.content) and ( str(message.author) ==  str(self.notiTix) ) :
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

            embedVar = discord.Embed(title="Resolve issue", description='''Please react with the emoji that best fits your question
                                                                        \n''' + self.botEmoji + ''' Bot related
                                                                        \n''' + self.proxyEmoji + ''' Proxy related
                                                                        \n''' + self.siteEmoji + ''' Site related
                                                                        \n''' + self.memberEmoji + ''' Membership
                                                                        \n''' + self.otherEmoji + ''' Other
                                                                        \n''' + self.supportEmoji + ''' Talk to Support
                                                                        \n''' + self.restartEmoji + ''' At any time to start over''', color=0xDB0B23)
            await self.setFooter(embedVar)

            message = await message.channel.send( embed=embedVar)
            await message.add_reaction( self.botEmoji)
            await message.add_reaction( self.proxyEmoji)
            await message.add_reaction( self.siteEmoji)
            await message.add_reaction( self.memberEmoji)
            await message.add_reaction( self.otherEmoji)
            await message.add_reaction( self.supportEmoji)
            await message.add_reaction( self.restartEmoji)
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
        try:
            if message.channel.category_id == 570248275374899200:
                if discord.utils.get(message.channel.guild.roles, name="Staff") in message.author.roles:
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
                support = discord.utils.get(guild.roles, name="Support Services")
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
