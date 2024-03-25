import os
import discord
from discord.ui import Button, View
import asyncio
from discord import app_commands
import psycopg
from psycopg import sql
from dotenv import load_dotenv
import logging
import datetime

from global_vars.global_vars import GlobalVariables
from utils import one_on_one_utils
from database import dbaccess

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
log_file_path = os.path.join('logs', '1on1botlog.log')
file_handler = logging.FileHandler(filename=log_file_path, encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(file_handler)

load_dotenv()
TOKEN = os.environ.get('ONE_ON_ONE_TOKEN')
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

NOTIFYGUILDID = int(os.environ.get('NOTIFYGUILDID'))

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
        print(f'[{datetime.datetime.now()}] | {self.user} has connected (ready) to Discord!')

        GlobalVariables().advisorDict = await one_on_one_utils.get_all_values()

        Client.add_view(one_on_one_utils.AdvisorMain())
        Client.add_view(one_on_one_utils.StaffView(category=0))

    async def on_connect(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has connected to Discord!')

    async def on_resumed(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has resumed connection to Discord!')

    async def on_disconnect(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has disconnected from Discord!')

Client = Client()
client = app_commands.CommandTree(Client)

# Used by staff to update their sessions
@client.command(name = "updatesessions")
async def updatesessions(interaction: discord.Interaction, number: int):
    guild = Client.get_guild(NOTIFYGUILDID)
    role = discord.utils.find(lambda r: r.name == "Team: Coaches", interaction.channel.guild.roles)

    if role in interaction.user.roles:
        staff = interaction.user.id

        query = """UPDATE oneonone set sessions = %s WHERE id = %s """

        await dbaccess.write_data(query, (number, staff))

        # Update dict
        GlobalVariables().advisorDict[staff]["remaining"] = number

        await interaction.response.send_message("Set total to " + str(number) + " sessions.")
    else:
        await interaction.response.send_message("You don't have access to this command.")

@Client.event
async def on_message(message):

    # Initializes the bot flow
    if ('Initiating Jarvis 1on1...' in message.content) and (message.channel.category_id == 915303264889749544):

        await one_on_one_utils.initial_func(message.channel)

Client.run(TOKEN, log_handler=None)
