import os
import discord
from discord import app_commands
import asyncio
import datetime
from datetime import date
from dotenv import load_dotenv
load_dotenv()

from global_vars.global_vars import GlobalVariables
from database import dbaccess
from utils import tracker_utils
from embeds import embeds

#Bot Token
TOKEN = os.environ.get('TRACKER_TOKEN')
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
        print(f'{self.user} has connected to Discord!')

        #sets some variables used in welcome.py
        await tracker_utils.set_vars(Client)

        await asyncio.gather(tracker_utils.tracker(), tracker_utils.checker(), tracker_utils.muted(), tracker_utils.reviews())

Client = Client()
client = app_commands.CommandTree(Client)

GUILD = int(os.environ.get('NOTIFYGUILDID'))
STAFFROLE = int(os.environ.get('STAFFROLE'))
NEWMEMBERROLE = int(os.environ.get('NEWMEMBERROLE'))
ADMINCATEGORY = int(os.environ.get('LOYALMEMBERUSCATID'))

# On member join give them @New Member Role
@Client.event
async def on_member_join(member):
    guild = Client.get_guild(GUILD)
    rolenewmember = guild.get_role(NEWMEMBERROLE)

    await member.add_roles(rolenewmember)

# Update member role to remove New Member if they get staff role
@Client.event
async def on_member_update(before, after):
    guild = Client.get_guild(GUILD)
    rolestaff = guild.get_role(STAFFROLE)
    rolenewmember = guild.get_role(NEWMEMBERROLE)

    if rolestaff in after.roles:
        await after.remove_roles(rolenewmember)

# Command to remove the of the user of the command
@client.command(name = "optout")
async def optout(interaction: discord.Interaction):
    try:
        guild = Client.get_guild(GUILD)
        rolenewmember = guild.get_role(NEWMEMBERROLE)

        await interaction.user.remove_roles(rolenewmember)
        await interaction.response.send_message("Removed the New Member role.")
    except:
        await interaction.response.send_message(f"Issue with the command, you must use the command inside of Notify for it to work.")

# Command to remove the role of a specific member
@client.command(name = "optoutid")
async def optoutid(interaction: discord.Interaction, memberid: str):
    try:
        guild = Client.get_guild(GUILD)
        rolenewmember = guild.get_role(NEWMEMBERROLE)
        member = guild.get_member(int(memberid))

        await member.remove_roles(rolenewmember)
        await interaction.response.send_message("Removed the New Member role.")
    except:
        await interaction.response.send_message(f"Issue with the command, you must use the command inside of Notify for it to work.")

# Command to allow members to check how much time is left
@client.command(name = "timeinnotify")
async def timeinnotify(interaction: discord.Interaction):
    try:
        now = datetime.datetime.now()
        then = interaction.user.joined_at.replace(tzinfo=None)
        diff = now - then

        await interaction.response.send_message(f"You have been in Notify for {diff}")
    except:
        await interaction.response.send_message(f"Issue with the command, you must use the command inside of Notify for it to work.")

# Marketplace command to get a users deals embed
@client.command(name = "marketinfo", description = "Used to get marketplace rating(s) of a user (format is userid: ex: 100108221280186368)")
async def marketinfo(interaction: discord.Interaction, user_id: str):
    try:
        buyer_stats, seller_stats = await tracker_utils.market_info(user_id)
        username = await Client.fetch_user(int(user_id))
        embedVar = await embeds.market_info(str(username.display_name), buyer_stats, seller_stats)

        await interaction.response.send_message(embed=embedVar)
    except Exception as e:
        await interaction.response.send_message("This is not a Discord ID number.\n\nPlease input the 18 digit Discord ID to retrieve the users marketplace stats.")

# Marketplace command to rate each other after a deal
@client.command(name = "donedeal", description = "Used for rating buyers/sellers in the Marketplace")
async def donedeal(interaction: discord.Interaction):
    if interaction.channel.category_id == ADMINCATEGORY:
        await tracker_utils.marketplace_done(interaction)
        await interaction.channel.send("Thanks for the ratings, if you would like to see your marketplace ratings please use `/marketinfo <discorduserid>`")
    else:
        await interaction.response.send_message("You must be in a marketplace ticket in order to use this command.")

# Marketplace command to add tracking
@client.command(name = "tracking", description = "Used to input a tracking number")
async def tracking(interaction: discord.Interaction, tracking_number: str):
    if interaction.channel.category_id == ADMINCATEGORY:
        ticketname = str(Client.get_channel(int(interaction.channel_id)))
        query = "INSERT INTO marketplacedeals (ticketname, trackingnumber) VALUES (%s, %s) ON CONFLICT (ticketname) DO UPDATE set trackingnumber = EXCLUDED.trackingnumber"
        data = (ticketname, tracking_number)

        await dbaccess.write_data(query, data)

        embedVar = await embeds.marketplace_tracking(tracking_number)
        await interaction.response.send_message(embed=embedVar)
    else:
        await interaction.response.send_message("You must be in a marketplace ticket in order to use this command.")

# Bot Tracker command to instantly get bot status
@client.command(name = "bottracker", description = "Gets bot status")
async def bottracker(interaction: discord.Interaction):
    guild = Client.get_guild(GUILD)
    botlistKian = ["NotifyRolePuller#5028", "Jarvis#6294", "Notify Tracker#8456", "Notify Utilities#9136", "Notify Pinger#8244", "Notify 1on1 Bot#7873", "Notify Toolbox#6012", "Whop Bot#6692"]
    embedVar = discord.Embed(title = "Bot Status", description = "Bot Statuses Displayed Here.", color=0xDB0B23)

    for i in botlistKian:
        try:
            bot = discord.utils.find(lambda m: str(m) == i, guild.members)
            if str(bot.status) == "offline":
                embedVar.add_field(name = i, value = "Offline", inline = False)
            elif str(bot.status) == "online":
                embedVar.add_field(name = i, value = "Online", inline = False)
        except Exception as e:
            embedVar.add_field(name = i, value = "Kicked From Server or Error: " + str(e), inline = False)
    await interaction.response.send_message(embed=embedVar)

@Client.event
async def on_message(msg):
    # Marketplace starting point, once a marketplace ticket opens this will start the flow
    if ('please respond to each prompt to properly **host and track** your transaction.' in msg.content) and (msg.channel.category_id == ADMINCATEGORY):
        await tracker_utils.marketplace_initial(msg)

Client.run(TOKEN)

#END
