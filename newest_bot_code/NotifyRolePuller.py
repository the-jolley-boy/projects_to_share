import os
import discord
from discord import app_commands
from discord.utils import get
import asyncio
import datetime
from datetime import date
import matplotlib.pyplot as plt
import time
from pytz import timezone
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

from database import dbaccess
from utils import role_puller_utils

TOKEN = os.environ.get('ROLE_PULLER_TOKEN')
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

GUILD_ID = int(os.environ.get('NOTIFYGUILDID'))

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

        #sets some variables used in welcome.py
        await role_puller_utils.set_vars(Client)

        await asyncio.gather(monthly_delete())

Client = Client()
client = app_commands.CommandTree(Client)

# deletes and graphs data monthly
async def monthly_delete():
    while True:
        await asyncio.sleep(3600)  # Wait 60 minutes to check

        # Get current month
        curr_month = await role_puller_utils.get_current_month()
        month = datetime.datetime.now().month

        try:
            if month != curr_month:
                print("Gathering monthly message data then deleting the data.")
                start = time.time()

                # Updating the month since it is a new month in this else
                query = "UPDATE datetracker set value = %s WHERE scriptid = %s"
                data = (month, 1)
                await dbaccess.write_data(query, data)

                # Create directory
                final_directory = os.path.join(os.getcwd(), f'staff_data/data_save_{date.today()}')
                os.makedirs(final_directory, exist_ok=True)

                # Fetch and export data for each category
                categories = [
                    "supporttickets", "staffcategory", "generalcategory",
                    "generalcategory2", "importantcategory", "sneakerinfocategory",
                    "sneakerreleasescategory", "canadacategory"
                ]
                for category_name in categories:
                    final_final_directory = os.path.join(final_directory, r'' + category_name)
                    if not os.path.exists(final_final_directory):
                        os.makedirs(final_final_directory)
                    ids, msgs, words, chars = await role_puller_utils.fetch_data(category_name)
                    names = await role_puller_utils.fetch_user_names(ids, Client)
                    await role_puller_utils.export_data_to_csv(ids, msgs, words, chars, names, category_name, final_directory)

                # Erase all rows in db
                await dbaccess.delete_all_rows()

                end = time.time()
                print(end - start)
        except Exception as e: 
            print(f"Error executing the monthly_delete function.\nError: {e}")

@Client.event
async def on_message(msg):

    if not msg.webhook_id:
        staffRole = discord.utils.get(msg.channel.guild.roles, name="Staff")
        # Support Tickets
        try:
            if msg.channel.category_id == 570248275374899200 and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("supporttickets", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with support tickets message gathering.")

        # Staff
        try:
            if msg.channel.category_id == 570142944921911296 and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("staffcategory", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with staff message gathering.")

        # General (Chat, Lifetime Chat)
        try:
            if msg.channel.category_id == 570142948155588608 and staffRole in msg.author.roles and msg.channel.id != 992842655346196490 and msg.channel.id != 570143030145974302 and msg.channel.id != 570143033337577482:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("generalcategory", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with general message gathering.")

        # General (New Member Chat, Questions)
        try:
            if (msg.channel.id == 992842655346196490 or msg.channel.id == 570143030145974302 or msg.channel.category_id == 1054648731154251796) and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("generalcategory2", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with general 2 message gathering.")

        # Important
        try:
            if msg.channel.category_id == 570142946272477184 and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("importantcategory", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with important message gathering.")

        # Sneaker Info
        try:
            if msg.channel.category_id == 1016090827073798164 and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("sneakerinfocategory", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with sneaker info message gathering.")

        # Sneaker Releases
        try:
            if msg.channel.category_id == 622110241882112011 and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("sneakerreleasescategory", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with sneaker releases message gathering.")

        # Canada
        try:
            if msg.channel.category_id == 839185199673507901 and staffRole in msg.author.roles:
                words, chars = await role_puller_utils.text_data(msg)
                await role_puller_utils.readwrite("canadacategory", msg.author.id, msg.author, 1, words, chars, 0)
        except Exception as e:
            print(f"Issue with canada message gathering.")

Client.run(TOKEN)
