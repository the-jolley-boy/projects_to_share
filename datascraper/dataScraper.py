################################################################################################

# This bot is used to scrape the staff members with specific roles in Notify.

# Author: Kian#7777

# To be used only by allowed discords.

################################################################################################

import os
import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import datetime
import logging
import psycopg2
from datetime import date
import matplotlib.pyplot as plt
import time
from pytz import timezone
import collections
from decimal import Decimal
import numpy as np

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), filename='rolescraper.log', filemode='a', format='%(asctime)s - [Line:%(lineno)d - Function:%(funcName)s In:%(filename)s From:%(name)s] \n[%(levelname)s] - %(message)s \n', datefmt='%d-%b-%y %H:%M:%S')

DBTable = "REDACTED"
DBHost = "REDACTED"
DBUsr = "REDACTED"
DBPass = "REDACTED"
DBPort = "REDACTED"

TOKEN = 'REDACTED'
GUILD_ID = 570142274902818816
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

Client = discord.Client(intents=intents)
client = commands.Bot(intents=intents, command_prefix = '!', case_insensitive = True)

#embedVar = discord.Embed(title = "Staff List", color = 0x000000)

########################################
# console output if connection success
########################################
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await asyncio.gather(daily_scheduled_message(), monthly_delete())
    # await daily_scheduled_message()
    # await monthly_delete()

########################################
# automation to send muted members
########################################
async def daily_scheduled_message():
    print("started daily")
    while True:
        await asyncio.sleep(180)
        now = datetime.datetime.now()
        then = now.replace(hour = 8, minute = 0)
        wait_time = (then - now).total_seconds()
        if wait_time < 0:
            wait_time = 86400 + wait_time

        print(str(wait_time))

        await asyncio.sleep(wait_time)

        channel = client.get_channel(994478794641506386)

        role_mute1 = 581499488901005313
        role_mute2 = 570142914173337600
        role_mute3 = 1018663023646363679

        guild = client.get_guild(GUILD_ID)
        separator = "\n"

        if guild.get_role(role_mute1) == None:
            m1 = ""
        else:
            mute1 = guild.get_role(role_mute1)
            m1 = ["**Username:** " + m.name + " **ID:** " + str(m.id) for m in mute1.members]
            m1 = separator.join(m1)

        if guild.get_role(role_mute2) == None:
            m2 = ""
        else:
            mute2 = guild.get_role(role_mute2)
            m2 = ["**Username:** " + m.name + " **ID:** " + str(m.id) for m in mute2.members]
            m2 = separator.join(m2)


        if guild.get_role(role_mute3) == None:
            m3 = ""
        else:
            mute3 = guild.get_role(role_mute3)
            m3 = ["**Username:** " + m.name + " **ID:** " + str(m.id) for m in mute3.members]
            m3 = separator.join(m3)


        embedVar = discord.Embed(title = "Muted Members", description = f'{m1}\n' f'{m2}\n' f'{m3}\n', color = 0x000000)

        await channel.send(embed = embedVar)

########################################
# Generates the graphs and saves it
########################################
async def graph(N, height1, height2, height3, tick_label, final_directory, end_directory):
    ind = np.arange(N)
    width = 0.25

    fig = plt.figure(facecolor = "white", figsize = (21,9), dpi = 300)
    #subplot to allow multiple plots
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    #all 3 sets of data into one plot (msg,word,char)
    first = ax2.bar(ind, height1, width, color = ['aqua'])
    second = ax.bar(ind+width, height2, width, color = ['lightgreen'])
    third = ax.bar(ind+width+width, height3, width, color = ['fuchsia'])

    #formatting stuff for the graph
    ax.set_ylabel('Word/Char Totals')
    ax2.set_ylabel('Msg Totals')
    ax.set_title('Category Interaction Graph')
    ax.set_xticks(ind + width / 3)
    ax.set_xticklabels(tick_label)
    ax.legend( (first[0], second[0], third[0]),("Tot Msgs", "Tot Words", "Tot Chars"),loc='upper center', bbox_to_anchor=(1,-0.1) )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_facecolor("black")
    #rotates the names 45 and changes font 
    fig.autofmt_xdate(rotation = 45)
    #fits everything to the borders
    fig.tight_layout()

    plt.savefig(final_directory + end_directory)

########################################
# deletes and graphs data monthly
########################################
async def monthly_delete():
    print("started monthly")
    while True:
        # Wait 60 minutes to check, 3600
        await asyncio.sleep(3600)

        currmonth = 0

        try:
            conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
            logging.info("Opened database successfully")
            curr = conn.cursor()

            postgreSQL_select_Query = "select * from datetracker"
            curr.execute(postgreSQL_select_Query)
            datetracker = curr.fetchall()

            for row in datetracker:
                if row[0] == 1:
                    currmonth = row[1]

            logging.info("Pulled values and closed")
            conn.close()

        except Exception as e:
            logging.error(e)
            conn.close()

        month = datetime.datetime.now().month
        #month = 2

        if month != currmonth:
            print("inside currmonth")
            start = time.time()

            #Creating a folder
            dateforsave = str(date.today())
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, r'data_save_' + dateforsave)
            final_final_directory = ""
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)
            cats = ["supporttickets", "staffcategory", "generalcategory", "generalcategory2", "importantcategory", "sneakerinfocategory", "sneakerreleasescategory", "canadacategory", "prioritymonitorscategory"]
            for cat in cats:
                final_final_directory = os.path.join(final_directory, r'' + cat)
                if not os.path.exists(final_final_directory):
                    os.makedirs(final_final_directory)

            #Updating the month since it is a new month in this else
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                sql = """UPDATE datetracker set value = %s WHERE scriptid = %s """
                data = (month, 1)
                curr.execute(sql, data)
                conn.commit()
                logging.info("Updated and closed")
                conn.close()
            except Exception as e:
                logging.error(e)
                conn.close()

            # Getting lists of all the data
            supportticketsids = []
            supportticketsmsgs = []
            supportticketswords = []
            supportticketschars = []
            supportticketsengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from supporttickets"
                curr.execute(postgreSQL_select_Query)
                supporttickets = curr.fetchall()

                for row in supporttickets:
                    supportticketsids.append(row[0])
                    supportticketsmsgs.append(row[2])
                    supportticketswords.append(row[3])
                    supportticketschars.append(row[4])
                    supportticketsengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            staffcategoryids = []
            staffcategorymsgs = []
            staffcategorywords = []
            staffcategorychars = []
            staffcategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from staffcategory"
                curr.execute(postgreSQL_select_Query)
                staffcategory = curr.fetchall()

                for row in staffcategory:
                    staffcategoryids.append(row[0])
                    staffcategorymsgs.append(row[2])
                    staffcategorywords.append(row[3])
                    staffcategorychars.append(row[4])
                    staffcategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            generalcategoryids = []
            generalcategorymsgs = []
            generalcategorywords = []
            generalcategorychars = []
            generalcategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from generalcategory"
                curr.execute(postgreSQL_select_Query)
                generalcategory = curr.fetchall()

                for row in generalcategory:
                    generalcategoryids.append(row[0])
                    generalcategorymsgs.append(row[2])
                    generalcategorywords.append(row[3])
                    generalcategorychars.append(row[4])
                    generalcategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            generalcategory2ids = []
            generalcategory2msgs = []
            generalcategory2words = []
            generalcategory2chars = []
            generalcategory2engage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from generalcategory2"
                curr.execute(postgreSQL_select_Query)
                generalcategory2 = curr.fetchall()

                for row in generalcategory2:
                    generalcategory2ids.append(row[0])
                    generalcategory2msgs.append(row[2])
                    generalcategory2words.append(row[3])
                    generalcategory2chars.append(row[4])
                    generalcategory2engage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            importantcategoryids = []
            importantcategorymsgs = []
            importantcategorywords = []
            importantcategorychars = []
            importantcategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from importantcategory"
                curr.execute(postgreSQL_select_Query)
                importantcategory = curr.fetchall()

                for row in importantcategory:
                    importantcategoryids.append(row[0])
                    importantcategorymsgs.append(row[2])
                    importantcategorywords.append(row[3])
                    importantcategorychars.append(row[4])
                    importantcategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            sneakerinfocategoryids = []
            sneakerinfocategorymsgs = []
            sneakerinfocategorywords = []
            sneakerinfocategorychars = []
            sneakerinfocategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from sneakerinfocategory"
                curr.execute(postgreSQL_select_Query)
                sneakerinfocategory = curr.fetchall()

                for row in sneakerinfocategory:
                    sneakerinfocategoryids.append(row[0])
                    sneakerinfocategorymsgs.append(row[2])
                    sneakerinfocategorywords.append(row[3])
                    sneakerinfocategorychars.append(row[4])
                    sneakerinfocategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            sneakerreleasescategoryids = []
            sneakerreleasescategorymsgs = []
            sneakerreleasescategorywords = []
            sneakerreleasescategorychars = []
            sneakerreleasescategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from sneakerreleasescategory"
                curr.execute(postgreSQL_select_Query)
                sneakerreleasescategory = curr.fetchall()

                for row in sneakerreleasescategory:
                    sneakerreleasescategoryids.append(row[0])
                    sneakerreleasescategorymsgs.append(row[2])
                    sneakerreleasescategorywords.append(row[3])
                    sneakerreleasescategorychars.append(row[4])
                    sneakerreleasescategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            canadacategoryids = []
            canadacategorymsgs = []
            canadacategorywords = []
            canadacategorychars = []
            canadacategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from canadacategory"
                curr.execute(postgreSQL_select_Query)
                canadacategory = curr.fetchall()

                for row in canadacategory:
                    canadacategoryids.append(row[0])
                    canadacategorymsgs.append(row[2])
                    canadacategorywords.append(row[3])
                    canadacategorychars.append(row[4])
                    canadacategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            prioritymonitorscategoryids = []
            prioritymonitorscategorymsgs = []
            prioritymonitorscategorywords = []
            prioritymonitorscategorychars = []
            prioritymonitorscategoryengage = []

            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                postgreSQL_select_Query = "select * from prioritymonitorscategory"
                curr.execute(postgreSQL_select_Query)
                prioritymonitorscategory = curr.fetchall()

                for row in prioritymonitorscategory:
                    prioritymonitorscategoryids.append(row[0])
                    prioritymonitorscategorymsgs.append(row[2])
                    prioritymonitorscategorywords.append(row[3])
                    prioritymonitorscategorychars.append(row[4])
                    prioritymonitorscategoryengage.append(row[5])

                logging.info("Pulled values and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # Turn all ID's into discord names
            supportticketnames = []
            staffcategorynames = []
            generalcategorynames = []
            generalcategory2names = []
            importantcategorynames = []
            sneakerinfocategorynames = []
            sneakerreleasescategorynames = []
            canadacategorynames = []
            prioritymonitorscategorynames = []

            for i in supportticketsids:
                user = await client.fetch_user(i)
                supportticketnames.append(user.name)
            for i in staffcategoryids:
                user = await client.fetch_user(i)
                staffcategorynames.append(user.name)
            for i in generalcategoryids:
                user = await client.fetch_user(i)
                generalcategorynames.append(user.name)
            for i in generalcategory2ids:
                user = await client.fetch_user(i)
                generalcategory2names.append(user.name)
            for i in importantcategoryids:
                user = await client.fetch_user(i)
                importantcategorynames.append(user.name)
            for i in sneakerinfocategoryids:
                user = await client.fetch_user(i)
                sneakerinfocategorynames.append(user.name)
            for i in sneakerreleasescategoryids:
                user = await client.fetch_user(i)
                sneakerreleasescategorynames.append(user.name)
            for i in canadacategoryids:
                user = await client.fetch_user(i)
                canadacategorynames.append(user.name)
            for i in prioritymonitorscategoryids:
                user = await client.fetch_user(i)
                prioritymonitorscategorynames.append(user.name)

            # Plotting and sending all the data as files in discord
            # supporttickets
            await graph(len(supportticketsids), supportticketsmsgs, supportticketswords, supportticketschars, supportticketnames, final_directory, '/supporttickets/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/supporttickets/csv.csv', 'w')
                sql = """COPY (SELECT * FROM supporttickets) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # staffcategory
            await graph(len(staffcategoryids), staffcategorymsgs, staffcategorywords, staffcategorychars, staffcategorynames, final_directory, '/staffcategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/staffcategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM staffcategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # generalcategory
            await graph(len(generalcategoryids), generalcategorymsgs, generalcategorywords, generalcategorychars, generalcategorynames, final_directory, '/generalcategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/generalcategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM generalcategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # generalcategory2
            await graph(len(generalcategory2ids), generalcategory2msgs, generalcategory2words, generalcategory2chars, generalcategory2names, final_directory, '/generalcategory2/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/generalcategory2/csv.csv', 'w')
                sql = """COPY (SELECT * FROM generalcategory2) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # importantcategory
            await graph(len(importantcategoryids), importantcategorymsgs, importantcategorywords, importantcategorychars, importantcategorynames, final_directory, '/importantcategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/importantcategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM importantcategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # sneakerinfocategory
            await graph(len(sneakerinfocategoryids), sneakerinfocategorymsgs, sneakerinfocategorywords, sneakerinfocategorychars, sneakerinfocategorynames, final_directory, '/sneakerinfocategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/sneakerinfocategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM sneakerinfocategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # sneakerreleasescategory
            await graph(len(sneakerreleasescategoryids), sneakerreleasescategorymsgs, sneakerreleasescategorywords, sneakerreleasescategorychars, sneakerreleasescategorynames, final_directory, '/sneakerreleasescategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/sneakerreleasescategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM sneakerreleasescategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # canadacategory
            await graph(len(canadacategoryids), canadacategorymsgs, canadacategorywords, canadacategorychars, canadacategorynames, final_directory, '/canadacategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/canadacategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM canadacategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # prioritymonitorscategory
            await graph(len(prioritymonitorscategoryids), prioritymonitorscategorymsgs, prioritymonitorscategorywords, prioritymonitorscategorychars, prioritymonitorscategorynames, final_directory, '/prioritymonitorscategory/graph.png')
            #Save the csv to folder
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()

                fid = open(final_directory + '/prioritymonitorscategory/csv.csv', 'w')
                sql = """COPY (SELECT * FROM prioritymonitorscategory) TO STDOUT WITH CSV HEADER"""
                curr.copy_expert(sql, fid)
                fid.close()

                logging.info("Exported to CSV and closed")
                conn.close()

            except Exception as e:
                logging.error(e)
                conn.close()

            # Erase all rows in db
            try:
                conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
                logging.info("Opened database successfully")
                curr = conn.cursor()
                sql = """DELETE FROM supporttickets"""
                curr.execute(sql)
                sql = """DELETE FROM staffcategory"""
                curr.execute(sql)
                sql = """DELETE FROM generalcategory"""
                curr.execute(sql)
                sql = """DELETE FROM generalcategory2"""
                curr.execute(sql)
                sql = """DELETE FROM importantcategory"""
                curr.execute(sql)
                sql = """DELETE FROM sneakerinfocategory"""
                curr.execute(sql)
                sql = """DELETE FROM sneakerreleasescategory"""
                curr.execute(sql)
                sql = """DELETE FROM canadacategory"""
                curr.execute(sql)
                sql = """DELETE FROM prioritymonitorscategory"""
                curr.execute(sql)
                conn.commit()
                logging.info("Updated and closed")
                conn.close()
            except Exception as e:
                logging.error(e)
                conn.close()
            end = time.time()
            print(end - start)

###################################################################################
# 
# Tracks staff messages in different categories: 
# Support Tickets, Staff, General, Important, Sneaker Info, Sneaker Releases, 
# Canada, Priority Monitors
#
# Each table contains the following rows:
# - Name (ID)
# - Message Count
# - Word Count
# - Char Count
# - Date
# 
###################################################################################
async def get_engagement(word_total, char_total, msg, channel_cat):

    engage = 0
    char = char_total
    word = word_total

    # When a word is too "big"
    if char/word > 6:
        char = 6
        word = 1

    # If sent at peak you get a better score
    time = datetime.datetime.now(timezone('EST'))
    if time.hour > 6 and time.hour < 20:
        created_at = 2
    else:
        created_at = 1

    # Replies/Role mentions
    if msg.mentions or msg.reference:
        mention = 1
    if msg.role_mentions:
        mention = 1
        char = 10
        word = 1
    else:
        mention = 0

    # if you message in any ticket it counts as a reply 
    if channel_cat == 1:
        mention = 1

    # if a link is sent in sneaker info or sneaker releases then you get a better score than a 10+ char/word message
    if char/word > 10 and channel_cat == 3 or char/word > 10 and channel_cat == 6:
        char = 10
        word = 1

    # Getting final values
    #print(str(char) + " " + str(word) + " " + " " + str(created_at) + " " + str(mention))
    charword = char / word * 0.33
    created = created_at * 0.15
    ment = mention * 0.52

    engage = charword + created + ment

    # Channel Category: support tickets = 1, priority monitor = 2, sneaker info = 3, important = 4, general/staff/canada = 5, sneaker releases = 6
    if channel_cat == 1:
        engage = engage * 1.8
    elif channel_cat == 2:
        engage = engage * 1.3
    elif channel_cat == 3:
        engage = engage * 1.2
    elif channel_cat == 4:
        engage = engage * 1.1
    elif channel_cat == 5:
        engage = engage * 1
    elif channel_cat == 6 and msg.role_mentions:
        engage = engage * 1.3
    else:
        engage = engage * 1

    return Decimal(engage)

async def readwrite(stringtable, auth, a, count, words, chars, engage):
    try:
        conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
        logging.info("Opened database successfully")
        curr = conn.cursor()

        postgreSQL_select_Query = "select * from " + stringtable
        curr.execute(postgreSQL_select_Query)
        table = curr.fetchall()

        for row in table:
            if row[0] == auth:
                count = count + row[2]
                words = words + row[3]
                chars = chars + row[4]
                if row[5] == 0:
                    engage = engage
                elif row[5] > 6:
                    engage = 6
                elif engage == 0:
                    engage = row[5]
                else:
                    engage = (engage + row[5])/2

                m = 1.01
                
                if row[2] >= 500:
                    engage = 6
                elif row[2] % 10 == 0:
                    engage = engage * Decimal(m)

        #insert into the db unless already in the db in that case update
        sql = """INSERT INTO """ + stringtable + """ (nameid, name, msgcount, wordcount, charcount, engage) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (nameid) DO UPDATE set (name, msgcount, wordcount, charcount, engage) = (EXCLUDED.name, EXCLUDED.msgcount, EXCLUDED.wordcount, EXCLUDED.charcount, EXCLUDED.engage)"""

        #data for the %s values
        data = (auth, str(a), count, words, chars, engage)
        curr.execute(sql, data)
        conn.commit()
        logging.info("Updated and closed")
        conn.close()
    except Exception as e:
        logging.error(e)
        conn.close()

@client.command()
async def avgengagement(ctx):
    #Dicts for all the engagements
    diclist = []
    sup = {}
    sta = {}
    gen = {}
    ge2 = {}
    imp = {}
    sni = {}
    snr = {}
    can = {}
    pri = {}
    #Get engagement from all tables
    try:
        conn = psycopg2.connect(dbname = DBTable, user = DBUsr, password = DBPass, host = DBHost, port = DBPort)
        logging.info("Opened database successfully")
        curr = conn.cursor()

        postgreSQL_select_Query = "select * from supporttickets"
        curr.execute(postgreSQL_select_Query)
        supporttickets = curr.fetchall()

        for row in supporttickets:
            sup[str(row[0])] = row[5]

        diclist.append(sup)

        postgreSQL_select_Query = "select * from staffcategory"
        curr.execute(postgreSQL_select_Query)
        staffcategory = curr.fetchall()

        for row in staffcategory:
            sta[str(row[0])] = row[5]

        diclist.append(sta)

        postgreSQL_select_Query = "select * from generalcategory"
        curr.execute(postgreSQL_select_Query)
        generalcategory = curr.fetchall()

        for row in generalcategory:
            gen[str(row[0])] = row[5]

        diclist.append(gen)

        postgreSQL_select_Query = "select * from generalcategory2"
        curr.execute(postgreSQL_select_Query)
        generalcategory = curr.fetchall()

        for row in generalcategory:
            gen[str(row[0])] = row[5]

        diclist.append(ge2)

        postgreSQL_select_Query = "select * from importantcategory"
        curr.execute(postgreSQL_select_Query)
        importantcategory = curr.fetchall()

        for row in importantcategory:
            imp[str(row[0])] = row[5]

        diclist.append(imp)

        postgreSQL_select_Query = "select * from sneakerinfocategory"
        curr.execute(postgreSQL_select_Query)
        sneakerinfocategory = curr.fetchall()

        for row in sneakerinfocategory:
            sni[str(row[0])] = row[5]

        diclist.append(sni)

        postgreSQL_select_Query = "select * from sneakerreleasescategory"
        curr.execute(postgreSQL_select_Query)
        sneakerreleasescategory = curr.fetchall()

        for row in sneakerreleasescategory:
            snr[str(row[0])] = row[5]

        diclist.append(snr)

        postgreSQL_select_Query = "select * from canadacategory"
        curr.execute(postgreSQL_select_Query)
        canadacategory = curr.fetchall()

        for row in canadacategory:
            can[str(row[0])] = row[5]

        diclist.append(can)

        postgreSQL_select_Query = "select * from prioritymonitorscategory"
        curr.execute(postgreSQL_select_Query)
        prioritymonitorscategory = curr.fetchall()

        for row in prioritymonitorscategory:
            pri[str(row[0])] = row[5]

        diclist.append(pri)

        logging.info("Updated and closed")
        conn.close()
    except Exception as e:
        logging.error(e)
        conn.close()

        counter = collections.Counter()
        for d in diclist:
            counter.update(d)

        res = dict(counter)

@client.event
async def on_message(msg):

    if not msg.webhook_id:
        staffRole = discord.utils.get(msg.channel.guild.roles, name="Staff")
        # Support Tickets
        if msg.channel.category_id == 570248275374899200 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 1
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("supporttickets", auth, a, count, words, chars, engage)
            else:
                await readwrite("supporttickets", auth, a, count, words, chars, 0)

        # Staff
        if msg.channel.category_id == 570142944921911296 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 5
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("staffcategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("staffcategory", auth, a, count, words, chars, 0)

        # General (Chat, Lifetime Chat)
        if msg.channel.category_id == 570142948155588608 and staffRole in msg.author.roles and msg.channel.id != 992842655346196490 and msg.channel.id != 570143030145974302 and msg.channel.id != 570143033337577482:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 5
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("generalcategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("generalcategory", auth, a, count, words, chars, 0)

        # General (New Member Chat, Questions)
        if (msg.channel.id == 992842655346196490 or msg.channel.id == 570143030145974302 or msg.channel.category_id == 1054648731154251796) and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 5
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("generalcategory2", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("generalcategory2", auth, a, count, words, chars, 0)

        # Important
        if msg.channel.category_id == 570142946272477184 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 4
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("importantcategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("importantcategory", auth, a, count, words, chars, 0)

        # Sneaker Info
        if msg.channel.category_id == 1016090827073798164 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 3
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("sneakerinfocategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("sneakerinfocategory", auth, a, count, words, chars, 0)

        # Sneaker Releases
        if msg.channel.category_id == 622110241882112011 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 6
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("sneakerreleasescategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("sneakerreleasescategory", auth, a, count, words, chars, 0)

        # Canada
        if msg.channel.category_id == 839185199673507901 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 5
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("canadacategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("canadacategory", auth, a, count, words, chars, 0)

        # Priority Monitors
        if msg.channel.category_id == 596137021228056586 and staffRole in msg.author.roles:
            a = msg.author
            auth = msg.author.id
            msgstring = msg.content
            words = len(msgstring.split())
            msgstring = msgstring.replace(" ", "")
            msgstring = msgstring.replace("\n", "")
            chars = len(msgstring)
            count = 1
            channel_cat = 2
            if words != 0:
                engage = await get_engagement(words, chars, msg, channel_cat)
                await readwrite("prioritymonitorscategory", auth, a, count, words, chars, engage)
            else:
                engage = await get_engagement(1, 1, msg, channel_cat)
                await readwrite("prioritymonitorscategory", auth, a, count, words, chars, 0)

        await client.process_commands(msg)

client.run(TOKEN)

#END
