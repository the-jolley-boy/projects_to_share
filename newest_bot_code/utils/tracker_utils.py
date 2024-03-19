import discord
import os
import asyncio
import datetime
from discord import Webhook
from dotenv import load_dotenv, find_dotenv
import requests
import json
import csv
import aiohttp
load_dotenv(find_dotenv())

from database import dbaccess
from embeds import embeds

GUILD = int(os.environ.get('NOTIFYGUILDID'))
NEWMEMBERROLE = int(os.environ.get('NEWMEMBERROLE'))
STAFFMODCHANNEL = int(os.environ.get('STAFFMODCHANNEL'))
WHOP_REVIEWS_WEBHOOK = os.environ.get("WHOP_REVIEWS_WEBHOOK")

Client = None

# Sets client var on bot start
async def set_vars(c):
    global Client

    Client = c

# Daily check if >= 3m then remove the role
async def checker():
    guild = Client.get_guild(GUILD)
    rolenewmember = guild.get_role(NEWMEMBERROLE)

    while True:
        await asyncio.sleep(180)
        now = datetime.datetime.now()
        then = now.replace(hour = 1, minute = 0)
        wait_time = (then - now).total_seconds()
        if wait_time < 0:
            wait_time = 86400 + wait_time

        print(f"Waiting {wait_time} before checking 3m old members.")

        await asyncio.sleep(wait_time)

        # Get the list of members with a specific role (New Member)
        memberlist = rolenewmember.members

        # check each member element for time in server
        for member in memberlist:
            timeIn = member.joined_at.replace(tzinfo=None)
            now = datetime.datetime.now()
            diff = now - timeIn
            if diff.days >= 90:
                await member.remove_roles(rolenewmember)

# Bot Tracker command to check if a bot is alive 
async def tracker():
    guild = Client.get_guild(GUILD)
    userKian = discord.utils.find(lambda m: str(m) == "smallpeenkeen#0", guild.members)
    userBanksy = discord.utils.find(lambda m: str(m) == "banksybanksy#0", guild.members)

    botlistKian = ["NotifyRolePuller#5028", "Jarvis#6294", "Notify Tracker#8456", "Notify Utilities#9136", "Notify Pinger#8244", "Notify 1on1 Bot#7873"]
    botlistBanksy = ["Notify Toolbox#6012", "Whop Bot#6692"]

    while True:
        await asyncio.sleep(3600)
        for i in botlistKian:
            try:
                bot = discord.utils.find(lambda m: str(m) == i, guild.members)

                if str(bot.status) == "offline":
                    await userKian.send("Bot " + i + " is offline.")
            except Exception as e:
                await userKian.send("Bot " + i + " has been kicked from the serveror Error: " + str(e))
        # for i in botlistBanksy:
        #     try:
        #         bot = discord.utils.find(lambda m: str(m) == i, guild.members)

        #         if str(bot.status) == "offline":
        #             await userBanksy.send("Bot " + i + " is offline.")
        #     except Exception as e:
        #         await userBanksy.send("Bot " + i + " has been kicked from the server or Error: " + str(e))

# automation to send muted members
async def muted():
    while True:
        await asyncio.sleep(180)
        now = datetime.datetime.now()
        then = now.replace(hour = 8, minute = 0)
        wait_time = (then - now).total_seconds()
        if wait_time < 0:
            wait_time = 86400 + wait_time

        print(f"Waiting {wait_time} before checking muted members.")

        await asyncio.sleep(wait_time)

        channel = Client.get_channel(STAFFMODCHANNEL)

        muted_role_list = [581499488901005313, 570142914173337600, 1018663023646363679]

        guild = Client.get_guild(GUILD)
        muted_members = ""

        for i in muted_role_list:
            if guild.get_role(i) != None:
                for m in guild.get_role(i).members:
                    muted_members = muted_members + f"**Username:** {m.name} **ID:** {str(m.id)}\n"

        embedVar = discord.Embed(
            title="Muted Members", 
            description=f'{muted_members}', 
            color=0x000000
        )

        if guild.get_role(muted_role_list[0]) != None and guild.get_role(muted_role_list[1]) != None and guild.get_role(muted_role_list[2]) != None:
            await channel.send(embed=embedVar)

async def reviews():
    while True:
        await asyncio.sleep(180)
        now = datetime.datetime.now()
        then = now.replace(hour = 0, minute = 0)
        wait_time = (then - now).total_seconds()
        if wait_time < 0:
            wait_time = 86400 + wait_time

        print(f"Waiting {wait_time} before checking for new reviews.")

        await asyncio.sleep(wait_time)

        url = 'https://whop.com/api/graphql/fetchMarketplacePageReviews/'

        variables = {
            "id": "pge_bSKWtJeggxG147",
            "after": "MA==",
            "stars": None
        }

        headers = {
            'Referer': 'https://whop.com/marketplace/notify/'
        }

        query = '''
            query fetchMarketplacePageReviews($id: ID!, $after: String, $stars: Int) {
                publicPage(id: $id) {
                    ...PublicMarketplacePageReviewsData
                }
            }
            
            fragment PublicMarketplacePageReviewsData on PublicPage {
                reviewsAverage
                reviews(first: 20, after: $after, stars: $stars) {
                    nodes {
                        ...PublicMarketplacePageReview
                    }
                }
            }
            
            fragment PublicMarketplacePageReview on Review {
                user {
                    header
                    profilePic32: profilePicSrcset(style: s32, allowAnimation: true) {
                        original
                        double
                        isVideo
                    }
                }
                joinedAt
                createdAt
                stars
                description
            }
        '''

        payload = {'query': query, 'variables': variables, 'operationName': 'fetchMarketplacePageReviews'}

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            reviews = data['data']['publicPage']['reviews']['nodes']
            avg_review = data['data']['publicPage']['reviewsAverage']

            async with aiohttp.ClientSession() as session:

                webhook = Webhook.from_url(WHOP_REVIEWS_WEBHOOK, session=session)
            
                for review in reversed(reviews):
                    name = review['user']['header']
                    created_at = datetime.datetime.utcfromtimestamp(review['createdAt']).strftime('%Y-%m-%d %H:%M:%S')
                    joined = datetime.datetime.utcfromtimestamp(review['joinedAt']).strftime('%Y-%m-%d')
                    rating = "⭐" * review['stars']
                    rev = review['description']
                    pfp = review['user']['profilePic32']['double']

                    current_time = datetime.datetime.now()
                    old_time = datetime.datetime.utcfromtimestamp(review['createdAt'])
                    time_diff = current_time - old_time

                    if time_diff <= datetime.timedelta(days=1):
                        embedVar = discord.Embed(
                            description=f"{rating}\n\n{rev}\n\n[Reviewed on {created_at}](https://whop.com/notify)", 
                            color=0xFF7673
                        )
                        embedVar.set_footer(
                            text = f"Rated {avg_review}/5 Based on {total_count} Reviews", 
                        )
                        embedVar.set_author(
                            name=f"{name} | Member Since {joined}", 
                            icon_url = pfp
                        )

                        await webhook.send(embed=embedVar)
                        await asyncio.sleep(1)

                        print("Added new review(s).")
        else:
            print('Request failed with status code:', response.status_code)

async def market_info(user_id):
    buyer_stats = {
        "success": 0,
        "fail": 0,
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "money": 0
    }
    seller_stats = {
        "success": 0,
        "fail": 0,
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "money": 0
    }

    buyer_query = f"SELECT * FROM marketplacebuyer WHERE buyerid = {int(user_id)}"
    seller_query = f"SELECT * FROM marketplaceseller WHERE sellerid = {int(user_id)}"

    result_buyer = await dbaccess.get_data(buyer_query, None)
    result_seller = await dbaccess.get_data(seller_query, None)

    if result_buyer:
        for row in result_buyer:
            buyer_stats = {
                "success": row[1],
                "fail": row[2],
                "days": row[3],
                "hours": row[4] // 3600,
                "minutes": (row[4] - (row[4] // 3600) * 3600) // 60,
                "money": row[5]
            }
    if result_seller:
        for row in result_seller:
            seller_stats = {
                "success": row[1],
                "fail": row[2],
                "days": row[3],
                "hours": row[4] // 3600,
                "minutes": (row[4] - (row[4] // 3600) * 3600) // 60,
                "money": row[5]
            }

    return buyer_stats, seller_stats

async def marketplace_done(interaction):
    starttime = ""
    buyerid = 0
    sellerid = 0
    dealvalue = 0
    buyerrating = 0
    sellerrating = 0

    query = "select * from marketplacedeals where channel_id = %s"
    data = (str(Client.get_channel(int(interaction.channel_id))),)

    # Gets the Buyer/Seller IDs and start time of deal
    records = await dbaccess.get_data(query, data)
    for row in records:
        buyerid = row[1]
        sellerid = row[2]
        dealvalue = row[4]
        starttime = row[6]

    # Get time difference for transaction to add
    avgtime = datetime.datetime.now() - datetime.datetime.strptime(starttime, "%Y-%m-%d %H:%M:%S.%f")
    days = avgtime.days
    seconds = avgtime.seconds  

    def checkseller(mes):
        return mes.channel == interaction.channel and mes.author != Client.user and mes.author.id == sellerid

    def checkbuyer(mes):
        return mes.channel == interaction.channel and mes.author != Client.user and mes.author.id == buyerid

    buyerEmbed = await embeds.marketplace_buyer()
    await interaction.response.send_message(embed = buyerEmbed)
    await interaction.followup.send('<@!' + str(sellerid) + '>')
    br = await Client.wait_for("message", check = checkseller)
    buyerrating = int(br.content)

    sellerEmbed = await embeds.marketplace_seller()
    await interaction.channel.send(embed = sellerEmbed)
    await interaction.followup.send('<@!' + str(buyerid) + '>')
    sr = await Client.wait_for("message", check = checkbuyer)
    sellerrating = int(sr.content)

    # Gets old buyer results from db then manipulates them and adds them back to the db
    query = "select * from marketplacebuyer where buyerid = %s"
    data = (buyerid,)
    buyer_records = await dbaccess.get_data(query, data)

    # Initialize default values
    succ = 1 if buyerrating == 1 else 0
    fail = 0 if buyerrating == 1 else 1
    bdays = days
    bseconds = seconds
    bmoney = dealvalue

    # Update values if the buyer's record exists
    if buyer_records:
        for row in buyer_records:
            succ = row[1] + (1 if buyerrating == 1 else 0)
            fail = row[2] + (0 if buyerrating == 1 else 1)
            bdays = (row[3] + days) / 2
            bseconds = (row[4] + seconds) / 2
            bmoney = dealvalue + row[5]

    # Adding them back to the db
    query = "INSERT INTO marketplacebuyer (buyerid, buyersuccess, buyerfails, days, seconds, dealstotal) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (buyerid) DO UPDATE set (buyersuccess, buyerfails, days, seconds, dealstotal) = (EXCLUDED.buyersuccess, EXCLUDED.buyerfails, EXCLUDED.days, EXCLUDED.seconds, EXCLUDED.dealstotal)"
    data = (buyerid, succ, fail, bdays, bseconds, bmoney)
    await dbaccess.write_data(query, data)

    # Gets old seller results from db then manipulates them and adds them back to the db
    query = "select * from marketplaceseller where sellerid = %s"
    data = (sellerid,)
    seller_records = await dbaccess.get_data(query, data)

    # Initialize default values
    succ = 1 if sellerrating == 1 else 0
    fail = 0 if sellerrating == 1 else 1
    sdays = days
    sseconds = seconds
    smoney = dealvalue

    # Update values if the seller's record exists
    if seller_records:
        for row in seller_records:
            succ = row[1] + (1 if sellerrating == 1 else 0)
            fail = row[2] + (0 if sellerrating == 1 else 1)
            sdays = (row[3] + days) / 2
            sseconds = (row[4] + seconds) / 2
            smoney = dealvalue + row[5]

    query = "INSERT INTO marketplaceseller (sellerid, sellersuccess, sellerfails, days, seconds, dealstotal) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (sellerid) DO UPDATE set (sellersuccess, sellerfails, days, seconds, dealstotal) = (EXCLUDED.sellersuccess, EXCLUDED.sellerfails, EXCLUDED.days, EXCLUDED.seconds, EXCLUDED.dealstotal)"
    data = (sellerid, succ, fail, sdays, sseconds, smoney)
    await dbaccess.write_data(query, data)

async def marketplace_initial(msg):
    marketplace_dict = {
        "ticketname": str(Client.get_channel(int(msg.channel.id))),
        "buyerid": 0,
        "sellerid": 0,
        "items": "",
        "dealprice": 0,
        "trackingnumber": "",
        "starttime": str(datetime.datetime.now()),
        "endtime": ""
    }

    for embed in msg.embeds:
        try:
            contentStringDesc = str(embed.description)
            contentStringDescTrim = contentStringDesc.split('> **Discord ID:** ', 1)[1]
            memberidstr = contentStringDescTrim
            member = await Client.fetch_user(int(memberidstr))
            overwrites = discord.PermissionOverwrite()
            overwrites.send_messages = True
            overwrites.read_messages = True
            await msg.channel.set_permissions(member, overwrite = overwrites)
        except:
            await msg.channel.send("This is not a Discord ID number.\n\nA staff member will add the user you've requested once you answer the questions. <@&575144399013543977>")

    # initial message
    initialEmbed = await embeds.marketplace_intial()
    await msg.channel.send(embed=initialEmbed)

    finished = "0"

    restartEmbed = await embeds.marketplace_restart()
    await msg.channel.send(embed=restartEmbed)

    while finished != "1":
        try:
            # Asks for Buyer id
            buyerEmbed = await embeds.marketplace_buyer_input()
            await msg.channel.send(embed=buyerEmbed)
            m = await Client.wait_for("message", check=check)
            if (m.content != "restart"):
                marketplace_dict["buyerid"] = int(m.content)
            else:
                await msg.channel.send("Restarting...")
                continue
        except:
            await msg.channel.send("This is not a Discord ID number, please restart.")
            continue

        try:
            # Asks for Seller id
            sellerEmbed = await embeds.marketplace_seller_input()
            await msg.channel.send(embed=sellerEmbed)
            m = await Client.wait_for("message", check=check)
            if (m.content != "restart"):
                marketplace_dict["sellerid"] = int(m.content)
            else:
                await msg.channel.send("Restarting...")
                continue
        except:
            await msg.channel.send("This is not a Discord ID number, please restart.")
            continue

        try:
            # Asks for Items
            itemEmbed = await embeds.marketplace_items()
            await msg.channel.send(embed=itemEmbed)
            m = await Client.wait_for("message", check=check)
            if (m.content != "restart"):
                marketplace_dict["items"] = m.content
            else:
                await msg.channel.send("Restarting...")
                continue
        except:
            await msg.channel.send("Item list entry is not correct, please restart.")
            continue

        try:
            # Asks for Deal Price
            priceEmbed = await embeds.marketplace_deal()
            await msg.channel.send(embed=priceEmbed)
            m = await Client.wait_for("message", check=check)
            if (m.content != "restart"):
                marketplace_dict["dealprice"] = int(m.content)
            else:
                await msg.channel.send("Restarting...")
                continue
        except:
            await msg.channel.send("Deal price was not entered correctly, please restart.")
            continue

        try:
            # Asks if info correct
            finalEmbed = await embeds.marketplace_final()
            await msg.channel.send(embed=finalEmbed)
            m = await Client.wait_for("message", check=check)
            if (m.content != "n"):
                await msg.channel.send("Great, you are done for now!")
            else:
                await msg.channel.send("Restarting...")
                continue
        except:
            await msg.channel.send("Make sure to only type `y` or `n`, please restart.")
            continue

        finished = "1"

    nextStepEmbed = await embeds.marketplace_next_step()
    await msg.channel.send(embed = nextStepEmbed)

    query = "INSERT INTO marketplacedeals (ticketname, buyerid, sellerid, items, dealprice, trackingnumber, starttime, endtime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    data = (marketplace_dict["ticketname"], marketplace_dict["buyerid"], marketplace_dict["sellerid"], marketplace_dict["items"], marketplace_dict["dealprice"], marketplace_dict["trackingnumber"], marketplace_dict["starttime"], marketplace_dict["endtime"])

    await dbaccess.write_data(query, data)