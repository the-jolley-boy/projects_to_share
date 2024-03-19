# encoding: utf-8
import os
import discord
import time
import io
import requests
from requests.exceptions import Timeout
import asyncio
import re
import string
from discord import app_commands
import psycopg
import datetime
from dotenv import load_dotenv
load_dotenv()

from global_vars.global_vars import GlobalVariables
from utils import pinger_utils
from embeds import embeds

#Bot Token
TOKEN = os.environ.get('PINGER_TOKEN')
intents = discord.Intents().all()
intents.members = True
intents.guilds = True

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
        await pinger_utils.setchannelpinger()
        print(f'{self.user} has connected to Discord!')

Client = Client()
client = app_commands.CommandTree(Client)

alert = os.environ.get('TEAM_MONITOR_ALERT')
GUILD = int(os.environ.get('NOTIFYGUILDID'))
NOTIFYPINGERROLE = int(os.environ.get('NOTIFYPINGERROLE'))
MONITORBOTROLE = int(os.environ.get('MONITORBOTROLE'))
CHECKPOINTCHANNEL = int(os.environ.get('CHECKPOINTCHANNEL'))

# Used to add keywords for pings in Notify
@client.command(name = "pingeradd", description = "Allows staff to add/edit ping kw(s) for any channel. Input just ID for role and channel.")
@app_commands.checks.has_role("Staff")
async def pingeradd(interaction: discord.Interaction, keyword: str, roleid: str, channelid: str):
    try:
        await pinger_utils.add_kw(keyword.lower(), "<@&" + str(roleid) + ">", channelid)
        await interaction.response.send_message("Added the data successfully.")
    except:
        await interaction.response.send_message("Something went wrong, please retry.")

# Used to remove keywords for pings in Notify
@client.command(name = "pingerremove", description = "Allows staff to remove ping kw(s) for sneaker-important. Needs the correct kw and channel id.")
@app_commands.checks.has_role("Staff")
async def pingerremove(interaction: discord.Interaction, keyword: str, channelid: str):
    try:
        await pinger_utils.remove_kw(str(keyword.lower()), str(channelid.lower()))
        await interaction.response.send_message("Deleted: " + str(keyword.lower()))
    except:
        await interaction.response.send_message("Something went wrong, please retry.")

# Used to list keywords for pings in Notify
@client.command(name = "pingerlist", description = "Allows staff to see a list of kws.")
@app_commands.checks.has_role("Staff")
async def pingerlist(interaction: discord.Interaction):
    try:
        embedVar = await pinger_utils.list_kw()
        await interaction.response.send_message(embed=embedVar, ephemeral=True)
    except:
        await interaction.response.send_message("Something went wrong, please retry.")

@Client.event
async def on_message(msg):

    # Pinger for KWs
    if msg.channel.id in GlobalVariables().pingchannelslist and msg.author.id != NOTIFYPINGERROLE:
        channel_id = msg.channel.id

        pm = await pinger_utils.send_kw_ping(msg)

        if pm:
            channel_cooldowns = GlobalVariables().channel_cooldowns
            if channel_id not in channel_cooldowns or (datetime.datetime.now() - channel_cooldowns[channel_id]).total_seconds() >= 600:
                await msg.reply(pm)
                channel_cooldowns[channel_id] = datetime.datetime.now()

    # Used to ping when certain sites drop checkpoint.
    if msg.channel.id == CHECKPOINTCHANNEL and msg.author.id == MONITORBOTROLE:
        contents = ""
        channel = msg.channel
        embeds = msg.embeds

        mapping = {
            "shoepalace": "Checkpoint enabled for Shoepalace | <#1042880604234063912> <@&788278120700182538>",
            "snk": "Checkpoint enabled for ShopNiceKicks | <#1042880604234063912> <@&788278120700182538>",
            "kith": "Checkpoint enabled for Kith | <#1042880604234063912> <@&788278120700182538>",
            "DSMShopUS": "Checkpoint enabled for DSM | <#1042880604234063912> <@&788278120700182538>",
            "livestock": "Checkpoint enabled for Deadstock | <#754052922169622688> <@&570142927729328128>",
            "haven": "Checkpoint enabled for Haven | <#754052879006040064> <@&570142927729328128>",
            "sizeca": "Checkpoint enabled for Size | <@&570142927729328128>",
            "canaryyellow": "Checkpoint enabled for Off White | <#1042880604234063912> <@&788278120700182538>",
            "jdsportsca": "Checkpoint enabled for JD Canada | <@&570142927729328128>",
            "mambaandmambacita": "Checkpoint enabled for Mambacita | <#1042880604234063912> <@&788278120700182538>",
            "supremeus": "Checkpoint enabled for Supreme US | <@&788278120700182538>",
            "amamaniere": "Checkpoint enabled for A-Ma-Maniere | <#1042880604234063912> <@&788278120700182538>",
            "socialstatus": "Checkpoint enabled for Social Status | <#1042880604234063912> <@&788278120700182538>",
            "union": "Checkpoint enabled for Union | <#1042880604234063912> <@&788278120700182538>",
            "concepts": "Checkpoint enabled for CNCPTS | <#1042880604234063912> <@&788278120700182538>"
        }

        for embed in embeds:
            contentStringAuthor = str(embed.author)
            contentStringTitle = str(embed.title)

            for substring, message in mapping.items():
                if substring in contentStringAuthor.lower() and "checkpoint" in contentStringTitle.lower() and "enabled" in contentStringTitle.lower():
                    await channel.send(message)
                    break

Client.run(TOKEN)
