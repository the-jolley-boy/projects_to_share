import os
import discord
from discord import app_commands
from discord.utils import get
import asyncio
import datetime
import logging
import matplotlib.pyplot as plt
import time
from pytz import timezone
from decimal import Decimal
from dotenv import load_dotenv

load_dotenv()

from database import dbaccess
from utils import role_puller_utils

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
log_file_path = os.path.join('logs', 'rolepullerbotlog.log')
file_handler = logging.FileHandler(filename=log_file_path, encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(file_handler)

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
        print(f'[{datetime.datetime.now()}] | {self.user} has connected (ready) to Discord!')

        await dbaccess.create_tables()

    async def on_connect(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has connected to Discord!')

    async def on_resumed(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has resumed connection to Discord!')

    async def on_disconnect(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has disconnected from Discord!')

Client = Client()
client = app_commands.CommandTree(Client)

@client.command(name = "selfmessagedata", description = "Used to get self message data")
async def selfmessagedata(interaction: discord.Interaction):
    roles_to_check = ["Staff"]
    guild = Client.get_guild(GUILD_ID)
    member = await guild.fetch_member(interaction.user.id)
    
    if member and any(role.name in roles_to_check for role in member.roles):
        await interaction.response.send_message("Generating report.")
        await role_puller_utils.messagedata(interaction, interaction.user.id)
    else:
        await interaction.response.send_message("You don't have access to this command.")

@client.command(name = "staffselectmessagedata", description = "Used to get staff message data")
async def staffselectmessagedata(interaction: discord.Interaction, staff_id: str):
    roles_to_check = ["Staff"]
    guild = Client.get_guild(GUILD_ID)
    member = await guild.fetch_member(interaction.user.id)
    
    if member and any(role.name in roles_to_check for role in member.roles):
        await interaction.response.send_message("Generating report.")
        await role_puller_utils.messagedata(interaction, int(staff_id))
    else:
        await interaction.response.send_message("You don't have access to this command.")

@Client.event
async def on_message(msg):

    if msg.guild and not msg.webhook_id:
        staffRole = discord.utils.get(msg.channel.guild.roles, name="Staff")
        
        category_id = msg.channel.category_id
        author_roles = msg.author.roles
        words, chars = await role_puller_utils.text_data(msg)

        ticket_categories = [
            570142944921911296, 1084368328673476608, 806215492695883786, 570248275374899200,
            570142946272477184, 622110241882112011, 1016090827073798164, 570142948155588608,
            1099125615728283738
        ]

        for cat_id in ticket_categories:
            try:
                if category_id == cat_id and staffRole in author_roles:
                    if category_id == 1084368328673476608 or category_id == 806215492695883786:
                        cat_id == 570248275374899200
                    await role_puller_utils.readwrite(cat_id, msg.author.id, msg.author, 1, words, chars)
            except Exception as e:
                print(f"Issue with message gathering for category_id {cat_id}. Error: {e}")

Client.run(TOKEN, log_handler=None)
