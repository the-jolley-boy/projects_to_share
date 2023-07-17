################################################################################################

# This bot is used for the Notify Marketplace.

# Author: Kian#7777

# To be used only by Notify.

################################################################################################

import os
import discord
from discord.ext import commands
from discord import app_commands
import math
import asyncio
import datetime
from datetime import date
import logging
import psycopg2

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), filename='marketplace.log', filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')

DBTable = "REDACTED"
DBHost = "REDACTED"
DBUsr = "REDACTED"
DBPass = "REDACTED"
DBPort = "REDACTED"

#Bot Token
TOKEN = 'REDACTED'
intents = discord.Intents().all()
intents.members = True

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents = intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await client.sync()
            self.synced = True
        print(f'{self.user} has connected to Discord!')
        await asyncio.gather(tracker())

Client = Client()
client = app_commands.CommandTree(Client)

########################################################
#
# Marketplace commands
#
########################################################

@client.command(name = "marketinfo", description = "Used to get marketplace rating(s) of a user (format is userid: ex: 100108221280186368)")
async def marketinfo(interaction: discord.Interaction, user_id: str):

    buyersucc = 0
    buyerfail = 0
    buyerdays = 0
    buyerseconds = 0
    buyermoney = 0

    sellersucc = 0
    sellerfail = 0
    sellerdays = 0
    sellerseconds = 0
    sellermoney = 0

    # Gets values for both buyer and seller side for user
    try:
        conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
        logging.info("Opened database successfully")
        curr = conn.cursor()

        postgreSQL_select_Query = "select * from marketplacebuyer"
        curr.execute(postgreSQL_select_Query)
        table = curr.fetchall()

        for row in table:
            if row[0] == int(user_id):
                buyersucc = row[1]
                buyerfail = row[2]
                buyerdays = row[3]
                buyerseconds = row[4]
                buyermoney = row[5]

        postgreSQL_select_Query = "select * from marketplaceseller"
        curr.execute(postgreSQL_select_Query)
        table = curr.fetchall()

        for row in table:
            if row[0] == int(user_id):
                sellersucc = row[1]
                sellerfail = row[2]
                sellerdays = row[3]
                sellerseconds = row[4]
                sellermoney = row[5]

        logging.info("Updated and closed")
        conn.close()
    except Exception as e:
        logging.error(e)
        conn.close()

    # Calculate proper avg buyer/seller time
    buyerhours = buyerseconds // 3600
    buyerminutes = (buyerseconds - buyerhours * 3600) // 60

    sellerhours = sellerseconds // 3600
    sellerminutes = (sellerseconds - sellerhours * 3600) // 60

    try:
        username = await Client.fetch_user(int(user_id))

        embedVar = discord.Embed(title = str(username.display_name) + "'s Profile", description = "Below you can find ratings and handling times (total transaction time AVG) for " + str(username.display_name) + " on their buyer and seller side", color=0xDB0B23)
        embedVar.add_field(name = "Buyer: ", value = "Successful Transactions: " + str(buyersucc) + "\nFailed Transactions: " + str(buyerfail) + "\nDeal Completion Time (AVG): " + str(buyerdays) + "D:" + str(buyerhours) + "H:" + str(buyerminutes) + "M" + "\nTotal $ Amount in Deals: $" + str(buyermoney), inline = False)
        embedVar.add_field(name = "Seller: ", value = "Successful Transactions: " + str(sellersucc) + "\nFailed Transactions: " + str(sellerfail) + "\nDeal Completion Time (AVG): "  + str(sellerdays) + "D:" + str(sellerhours) + "H:" + str(sellerminutes) + "M" + "\nTotal $ Amount in Deals: $" + str(sellermoney), inline = False)
        embedVar.set_thumbnail(url = 'https://notify.org/notify.png')

        await interaction.response.send_message(embed=embedVar)
    except Exception as e:
        await interaction.response.send_message("This is not a Discord ID number.\n\nPlease input the 18 digit Discord ID to retrieve the users marketplace stats.")

@client.command(name = "donedeal", description = "Used for rating buyers/sellers in the Marketplace")
async def donedeal(interaction: discord.Interaction):
    if interaction.channel.category_id == 806215492695883786:
        starttime = ""
        endtime = ""

        buyerid = 0
        sellerid = 0
        dealvalue = 0

        # Gets the Buyer/Seller IDs and start time of deal
        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from marketplacedeals"
            curr.execute(postgreSQL_select_Query)
            marketplacedeals = curr.fetchall()

            for row in marketplacedeals:
                if row[0] == str(Client.get_channel(int(interaction.channel_id))):
                    buyerid = row[1]
                    sellerid = row[2]
                    starttime = row[6]
                    dealvalue = row[4]

            logging.info("Pulled values and closed")
            conn.close()

        except Exception as e:
            logging.error(e)
            conn.close()

        # Get time difference for transaction to add
        endtime = datetime.datetime.now()
        starttimeobj = datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")
        avgtime = endtime - starttimeobj

        days = avgtime.days
        seconds = avgtime.seconds

        # Gets rating of buyer and seller using embeds and buttons
        buyerrating = 0
        sellerrating = 0

        def checkseller(mes):
            return mes.channel == interaction.channel and mes.author != Client.user and mes.author.id == sellerid

        def checkbuyer(mes):
            return mes.channel == interaction.channel and mes.author != Client.user and mes.author.id == buyerid

        buyerEmbed = discord.Embed(title="Buyer Rating", description="> Please rate the Buyer now. (Only to be used by Seller). Type `1` for positive/successful transaction or `0` if unsuccessful/bad experience.", color=0xDB0B23)
        await interaction.response.send_message(embed = buyerEmbed)
        await interaction.followup.send('<@!' + str(sellerid) + '>')
        buyerrat = await Client.wait_for("message", check = checkseller)
        buyerrating = int(buyerrat.content)

        sellerEmbed = discord.Embed(title="Seller Rating", description="> Please rate the Seller now. (Only to be used by Buyer). Type `1` for positive/successful transaction or `0` if unsuccessful/bad experience.", color=0xDB0B23)
        await interaction.channel.send(embed = sellerEmbed)
        await interaction.followup.send('<@!' + str(buyerid) + '>')
        sellerrat = await Client.wait_for("message", check = checkbuyer)
        sellerrating = int(sellerrat.content)

        # Adds the results to the database for buyer
        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from marketplacebuyer"
            curr.execute(postgreSQL_select_Query)
            table = curr.fetchall()

            if buyerrating == 1:
                succ = 1
                fail = 0
            else:
                succ = 0
                fail = 1  
            bdays = days
            bseconds = seconds
            bmoney = dealvalue

            for row in table:
                if row[0] == buyerid:
                    if buyerrating == 1:
                        succ = row[1] + 1
                        fail = row[2]
                    else:
                        succ = row[1]
                        fail = row[2] + 1                        

                    bdays = (row[3] + days) / 2
                    bseconds = (row[4] + seconds) / 2 
                    bmoney = dealvalue + row[5]

            #insert into the db unless already in the db in that case update
            sql = """INSERT INTO marketplacebuyer (buyerid, buyersuccess, buyerfails, days, seconds, dealstotal) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (buyerid) DO UPDATE set (buyersuccess, buyerfails, days, seconds, dealstotal) = (EXCLUDED.buyersuccess, EXCLUDED.buyerfails, EXCLUDED.days, EXCLUDED.seconds, EXCLUDED.dealstotal)"""

            #data for the %s values
            data = (buyerid, succ, fail, bdays, bseconds, bmoney)
            curr.execute(sql, data)
            conn.commit()
            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        # Adds the results to the database for seller
        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from marketplaceseller"
            curr.execute(postgreSQL_select_Query)
            table = curr.fetchall()

            if sellerrating == 1:
                succ = 1
                fail = 0
            else:
                succ = 0
                fail = 1  
            sdays = days
            sseconds = seconds
            smoney = dealvalue

            for row in table:
                if row[0] == sellerid:
                    if sellerrating == 1:
                        succ = row[1] + 1
                        fail = row[2]
                    else:
                        succ = row[1]
                        fail = row[2] + 1                        

                    sdays = (row[3] + days) / 2
                    sseconds = (row[4] + seconds) / 2
                    smoney = dealvalue + row[5]

            #insert into the db unless already in the db in that case update
            sql = """INSERT INTO marketplaceseller (sellerid, sellersuccess, sellerfails, days, seconds, dealstotal) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (sellerid) DO UPDATE set (sellersuccess, sellerfails, days, seconds, dealstotal) = (EXCLUDED.sellersuccess, EXCLUDED.sellerfails, EXCLUDED.days, EXCLUDED.seconds, EXCLUDED.dealstotal)"""

            #data for the %s values
            data = (sellerid, succ, fail, sdays, sseconds, smoney)
            curr.execute(sql, data)
            conn.commit()
            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        await interaction.channel.send("Thanks for the ratings, if you would like to see your marketplace ratings please use `/marketinfo <discorduserid>`")

    else: 
        await interaction.response.send_message("You must be in a marketplace ticket in order to use this command.")

@client.command(name = "tracking", description = "Used to input a tracking number")
async def tracking(interaction: discord.Interaction, tracking_number: str):
    if interaction.channel.category_id == 806215492695883786:

        ticketname = str(Client.get_channel(int(interaction.channel_id)))

        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            #insert into the db unless already in the db in that case update
            sql = """INSERT INTO marketplacedeals (ticketname, trackingnumber) VALUES (%s, %s) ON CONFLICT (ticketname) DO UPDATE set trackingnumber = EXCLUDED.trackingnumber"""

            #data for the %s values
            data = (ticketname, tracking_number)
            curr.execute(sql, data)
            conn.commit()
            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        embedVar = discord.Embed(title="Next Steps", description="Done: tracking number is: " + tracking_number + "\n\n **Buyer:** \n > Once you receive the items and have confirmed they are correct, please use the command `/donedeal`. Both you, and the seller will need to review each other.", color=0xDB0B23)

        await interaction.response.send_message(embed=embedVar)

    else: 
        await interaction.response.send_message("You must be in a marketplace ticket in order to use this command.")

########################################################
#
# Marketplace commands end
#
########################################################

########################################################
#
# Flips commands
#
########################################################

# Shows Staff all the eBay and FB linked accounts, ONLY STAFF CAN USE.
@client.command(name = "showallflippers", description = "Shows all members that have registered their eBay/FB accounts.")
async def showallflippers(interaction: discord.Interaction):
    if interaction.user.id == 100108221280186368:
        name = []
        ebay = []
        fb = []

        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from flipschecker"
            curr.execute(postgreSQL_select_Query)
            table = curr.fetchall()

            for row in table:
                name.append(row[1])
                ebay.append(row[2])
                fb.append(row[3])

            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        fulllist = []

        for i in range(len(name)):
            newlist = []
            newlist.append(name[i])
            newlist.append(ebay[i])
            newlist.append(fb[i])
            fulllist.append(newlist)

        header = ['Member', 'eBay', 'Facebook']

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(header)
        writer.writerows(fulllist)
        buffer.seek(0)

        embed = discord.Embed(title="Download the CSV below to see all the members registered.", color=0xDB0B23)

        await interaction.response.send_message(embed=embed, ephemeral = True)
        await interaction.followup.send(file=discord.File(buffer, 'registered_members.csv'), ephemeral = True)

    else:
        await interaction.response.send_message("You don't have access to this command.")

# Shows Staff selected eBay and FB linked accounts, ONLY STAFF CAN USE.
@client.command(name = "showflipper", description = "Shows if a specific member has eBay/FB account registered.")
async def showflipper(interaction: discord.Interaction, userid: str):
    if interaction.user.id == 100108221280186368:
        name = ""
        ebay = ""
        fb = ""

        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from flipschecker"
            curr.execute(postgreSQL_select_Query)
            table = curr.fetchall()

            for row in table:
                if row[0] == int(userid):
                    name = row[1]
                    ebay = row[2]
                    fb = row[3]

            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        embedVar = discord.Embed(title="Users eBay/FB", color=0x000000)
        embedVar.add_field(name=str(name), value="eBay: " + str(ebay) + "\nFB: " + str(fb), inline=True)

        await interaction.response.send_message(embed = embedVar, ephemeral = True)

    else:
        await interaction.response.send_message("You don't have access to this command.")

# Syncs the flips role to members WITH eBay and/or FB accounts, ONLY STAFF CAN USE.
@client.command(name = "syncflippers", description = "Useable by staff only, gives member flips role IF they have an eBay and/or FB account linked.")
async def syncflippers(interaction: discord.Interaction):
    guild = Client.get_guild(570142274902818816)
    #guild = Client.get_guild(542527925967126528)
    if interaction.user.id == 100108221280186368:
        nameid = []

        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from flipschecker"
            curr.execute(postgreSQL_select_Query)
            table = curr.fetchall()

            for row in table:
                nameid.append(row[0])

            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

        role = interaction.guild.get_role(1099136299035803680)
        #role = interaction.guild.get_role(1081863065991139368)

        for i in nameid:
            member = guild.get_member(i)
            try:
                await member.add_roles(role)
            except Exception as e:
                print("Can't give role to someone not in server. Error: " + str(e))
        
        await interaction.channel.send("All Stored Users Synced.")

    else:
        await interaction.response.send_message("You don't have access to this command.")

# Members can use this to add their eBay account.
@client.command(name = "addebay", description = "Please add the link to your eBay account.")
async def addebay(interaction: discord.Interaction, ebayurl: str):
    guild = Client.get_guild(570142274902818816)
    user = str(interaction.user)
    userid = interaction.user.id
    ebay = ebayurl

    try:
        conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
        logging.info("Opened database successfully")
        curr = conn.cursor()

        #insert into the db unless already in the db in that case update
        sql = """INSERT INTO flipschecker (id, name, ebay) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set ebay = EXCLUDED.ebay"""

        #data for the %s values
        data = (userid, user, ebay)
        curr.execute(sql, data)
        conn.commit()
        logging.info("Updated and closed")
        conn.close()
    except Exception as e:
        logging.error(e)
        conn.close()

    role = interaction.guild.get_role(1099136329620668497)
    #role = interaction.guild.get_role(1081863065991139368)
    await interaction.user.add_roles(role)

    await interaction.response.send_message("Done! You should now have the role, if not already. If you put the wrong link in, just do the command again.", ephemeral = True)

# Members can use this to add their FB account.
@client.command(name = "addfacebook", description = "Please add the link to your Facebook account.")
async def addfacebook(interaction: discord.Interaction, fburl: str):
    guild = Client.get_guild(570142274902818816)
    user = str(interaction.user)
    userid = interaction.user.id
    fb = fburl

    try:
        conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
        logging.info("Opened database successfully")
        curr = conn.cursor()

        #insert into the db unless already in the db in that case update
        sql = """INSERT INTO flipschecker (id, name, fb) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set fb = EXCLUDED.fb"""

        #data for the %s values
        data = (userid, user, fb)
        curr.execute(sql, data)
        conn.commit()
        logging.info("Updated and closed")
        conn.close()
    except Exception as e:
        logging.error(e)
        conn.close()

    role = interaction.guild.get_role(1099136329620668497)
    #role = interaction.guild.get_role(1081863065991139368)
    await interaction.user.add_roles(role)

    await interaction.response.send_message("Done! You should now have the role, if not already. If you put the wrong link in, just do the command again.", ephemeral = True)

########################################################
#
# Flips commands end
#
########################################################

########################################################
#
# Bot Tracker commands
#
########################################################

async def tracker():
    guild = Client.get_guild(570142274902818816)
    userKian = discord.utils.find(lambda m: str(m) == "REDACTED", guild.members)
    userBanksy = discord.utils.find(lambda m: str(m) == "REDACTED", guild.members)   

    botlistKian = ["REDACTED"]
    botlistBanksy = ["REDACTED"]

    while True:
        await asyncio.sleep(3600)
        for i in botlistKian:
            try:
                bot = discord.utils.find(lambda m: str(m) == i, guild.members)

                if str(bot.status) == "offline":
                    await userKian.send("Bot " + i + " is offline.")
            except Exception as e:
                await userKian.send("Bot " + i + " has been kicked from the serveror Error: " + str(e))
        for i in botlistBanksy:
            try:
                bot = discord.utils.find(lambda m: str(m) == i, guild.members)

                if str(bot.status) == "offline":
                    await userBanksy.send("Bot " + i + " is offline.")
            except Exception as e:
                await userBanksy.send("Bot " + i + " has been kicked from the server or Error: " + str(e))

@client.command(name = "bottracker", description = "Gets bot status")
async def bottracker(interaction: discord.Interaction):

    guild = Client.get_guild(570142274902818816)
    userKian = discord.utils.find(lambda m: str(m) == "Kian#7777", guild.members) 

    botlistKian = ["REDACTED"]

    embedVar = discord.Embed(title = "Bot Status", description = "Bot Statuses Displayed Here.", color=0xDB0B23)

    for i in botlistKian:
        try:
            bot = discord.utils.find(lambda m: str(m) == i, guild.members)

            if str(bot.status) == "offline":
                embedVar.add_field(name = i, value = "Offline", inline = False)
                #await userBanksy.send("Bot " + i + " is offline.")
            elif str(bot.status) == "online":
                embedVar.add_field(name = i, value = "Online", inline = False)
        except Exception as e:
            embedVar.add_field(name = i, value = "Kicked From Server or Error: " + str(e), inline = False)

    await interaction.response.send_message(embed=embedVar)

########################################################
#
# Bot Tracker commands end
#
########################################################

@Client.event
async def on_message(msg):

    ########################################################
    #
    # Marketplace on_message
    #
    ########################################################
    if ('please respond to each prompt to properly **host and track** your transaction.' in msg.content) and (msg.channel.category_id == 806215492695883786):

        # Write to DB Stuff
        ticketname = ""
        buyerid = 0
        sellerid = 0
        items = ""
        dealprice = 0
        trackingnumber = ""
        starttime = ""
        endtime = ""

        channelId = str(msg.channel.id)
        ticketname = str(Client.get_channel(int(msg.channel.id)))

        starttime = str(datetime.datetime.now())

        embeds = msg.embeds

        for embed in embeds:

            contentStringDesc = str(embed.description)
            contentStringDescTrim = contentStringDesc.split('> **Discord ID:** ', 1)[1]

            channelId = str(msg.channel.id)

            try:
                memberidstr = contentStringDescTrim
                member = await Client.fetch_user(int(memberidstr))
                overwrites = discord.PermissionOverwrite()
                overwrites.send_messages = True
                overwrites.read_messages = True

                await msg.channel.set_permissions(member, overwrite = overwrites)

            except:
                await msg.channel.send("This is not a Discord ID number.\n\nA staff member will add the user you've requested once you answer the questions. <@&575144399013543977>")

        #
        # initial message
        #
        initialEmbed = discord.Embed(title="Buyer/Seller Ticket", description="> Please answer the following questions carefully.", color=0xDB0B23)
        initialEmbed.set_thumbnail(url = 'https://notify.org/notify.png')

        await msg.channel.send(embed = initialEmbed)

        #
        # Check before waiting response
        #
        def check(mes):
            return mes.channel == msg.channel and mes.author != msg.author

        finished = "0"

        restartEmbed = discord.Embed(title="To Restart", description="Type `restart` at any time to start over (in case you make a mistake on the steps below, thanks!)", color=0xDB0B23)
        await msg.channel.send(embed = restartEmbed)

        while finished != "1":
            try:
                # Asks for Buyer id
                buyerEmbed = discord.Embed(title="Buyer ID", description="Enter the Buyers Discord ID ONLY.\n\n> Ex: 100108221280186368 | Not sure how to find it? [Click here.](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xDB0B23)
                await msg.channel.send(embed = buyerEmbed)
                m = await Client.wait_for("message", check = check)
                if (m.content != "restart"):
                    buyerid = int(m.content)
                else:
                    await msg.channel.send("Restarting...")
                    continue
            except:
                await msg.channel.send("This is not a Discord ID number, please restart.")
                continue

            try:
                # Asks for Seller id
                sellerEmbed = discord.Embed(title="Seller ID", description="Enter the Sellers Discord ID ONLY.\n\n> Ex: 100108221280186368 | Not sure how to find it? [Click here.](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", color=0xDB0B23)
                await msg.channel.send(embed = sellerEmbed)
                m = await Client.wait_for("message", check = check)
                if (m.content != "restart"):
                    sellerid = int(m.content)
                else:
                    await msg.channel.send("Restarting...")
                    continue
            except:
                await msg.channel.send("This is not a Discord ID number, please restart.")
                continue

            try:
                # Asks for Items
                itemEmbed = discord.Embed(title="Items", description="List the item(s) in the deal, separated by a comma (space).\n\n> Ex: Jordan 1 L&F size 10, Jordan 4 Military Black size 12, etc", color=0xDB0B23)
                await msg.channel.send(embed = itemEmbed)
                m = await Client.wait_for("message", check = check)
                if (m.content != "restart"):
                    items = m.content
                else:
                    await msg.channel.send("Restarting...")
                    continue
            except:
                await msg.channel.send("Item list entry is not correct, please restart.")
                continue

            try:
                # Asks for Deal Price
                priceEmbed = discord.Embed(title="Total Price", description="Enter total deal price (not including shipping). DO NOT include a dollar sign($).\n\n> Ex: 1025", color=0xDB0B23)
                await msg.channel.send(embed = priceEmbed)
                m = await Client.wait_for("message", check = check)
                if (m.content != "restart"):
                    dealprice = int(m.content)
                else:
                    await msg.channel.send("Restarting...")
                    continue
            except:
                await msg.channel.send("Deal price was not entered correctly, please restart.")
                continue

            try:
                # Asks if info correct
                finalEmbed = discord.Embed(title="Is All The Info Correct?", description="Please make sure the information above is correct. If so, type `y`. If not, type `n`", color=0xDB0B23)
                await msg.channel.send(embed = finalEmbed)
                m = await Client.wait_for("message", check = check)
                if (m.content != "n"):
                    await msg.channel.send("Great, you are done for now!")
                else:
                    await msg.channel.send("Restarting...")
                    continue
            except:
                await msg.channel.send("Make sure to only type `y` or `n`, please restart.")
                continue

            finished = "1"

        nextStepEmbed = discord.Embed(title="Next Steps", description="**Seller:** \n > Once you have shipped the item(s), use `/tracking` to add the tracking number(s). \n\n **Buyer:** \n > Once you receive the items and have confirmed they are correct, please use the command `/donedeal`. Both you, and the seller will need to review each other. \n\n Do NOT use these commands until the steps above are completed.", color=0xDB0B23)
        await msg.channel.send(embed = nextStepEmbed)

        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            #insert into the db unless already in the db in that case update
            sql = """INSERT INTO marketplacedeals (ticketname, buyerid, sellerid, items, dealprice, trackingnumber, starttime, endtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            #data for the %s values
            data = (ticketname, buyerid, sellerid, items, dealprice, trackingnumber, starttime, endtime)
            curr.execute(sql, data)
            conn.commit()
            logging.info("Updated and closed")
            conn.close()
        except Exception as e:
            logging.error(e)
            conn.close()

Client.run(TOKEN)

#END