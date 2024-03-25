import os
import discord
import chat_exporter
import io
from discord import app_commands
from bs4 import BeautifulSoup
import requests
import asyncio
import requests_html
import json
from discord.utils import get
import random
from github import Github
from dotenv import load_dotenv
import logging
import datetime
load_dotenv()

from utils import utilities_utils
from embeds import embeds

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
log_file_path = os.path.join('logs', 'utilitiesbotlog.log')
file_handler = logging.FileHandler(filename=log_file_path, encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(file_handler)

#Bot Token
TOKEN = os.environ.get('UTILITIES_TOKEN')
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
        print(f'[{datetime.datetime.now()}] | {self.user} has connected (ready) to Discord!')

        #sets some variables used in welcome.py
        await utilities_utils.set_vars(Client)

    async def on_connect(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has connected to Discord!')

    async def on_resumed(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has resumed connection to Discord!')

    async def on_disconnect(self):
        print(f'[{datetime.datetime.now()}] | {self.user} has disconnected from Discord!')

Client = Client()
client = app_commands.CommandTree(Client)

GUILD = int(os.environ.get('NOTIFYGUILDID'))
MARKETPLACECHANNEL = int(os.environ.get('MARKETPLACECHANNEL'))
NOTIFYHELPERROLE = int(os.environ.get('NOTIFYHELPERROLE'))
KIANROLE = int(os.environ.get('KIANROLE'))
ADMINCATEGORY = int(os.environ.get('LOYALMEMBERUSCATID'))
STAFFROLE = int(os.environ.get('STAFFROLE'))

# Used to mass send dms
@client.command(
    name = "memberdm", 
    description = "DMs winners of giveaways their bot key and information."
)
@app_commands.checks.has_role("Staff")
async def memberdm(interaction: discord.Interaction, m: str):
    await utilities_utils.send_member_dms(interaction, m)

# Used to get entries into ufc fight raffles. Formstack site.
@client.command(
    name = "ufcenrollmsg", 
    description = "100 proxies & 100 gmails or 1 catchall. Separate input with comma no spaces."
)
async def ufcenrollmsg(interaction: discord.Interaction, proxy: str, emails: str):

    await interaction.response.send_message("Submitting entries now...")

    loop = asyncio.get_running_loop()
    time, issues = await loop.run_in_executor(None, utilities_utils.msg, proxy, emails)
    i = ', '.join([str(item) for item in issues])
    await interaction.channel.send("Finished Site #1 in " + str(time) + " seconds.\nYou also had a failed entry on entries " + str(i) + ".")

# Used to get entries into ufc fight raffles. UFC site.
@client.command(
    name = "ufcenrollufc", 
    description = "100 proxies & 100 gmails or 1 catchall. Separate input with comma no spaces."
)
async def ufcenrollufc(interaction: discord.Interaction, proxy: str, emails: str):

    await interaction.response.send_message("Submitting entries now...")

    loop = asyncio.get_running_loop()
    time, issues = await loop.run_in_executor(None, utilities_utils.ufc, proxy, emails)
    i = ', '.join([str(item) for item in issues])
    await interaction.channel.send("Finished Site #2 in " + str(time) + " seconds.\nYou also had a failed entry on entries " + str(i) + ".")

# Converting the guides from the site stored on github and sending in discord.
@client.command(
    name = "importguide", 
    description = "Allows guides from the hub to be published to a channel."
)
@app_commands.describe(choices="Start typing some guide you want and options will show up above.")
@app_commands.autocomplete(choices=utilities_utils.guide_autocomplete)
async def importguide(interaction: discord.Interaction, choices: str):
    # Gets the wanted guide from the hub
    g = Github('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')
    repo = g.get_repo('vildzi/notify-site')
    contents = repo.get_contents('outstatic/content/guides/' + choices + '.md')
    decoded = str(contents.decoded_content.decode('utf-8'))

    # Cleaning the string up
    sep = decoded.lstrip().split('---')[2]
    cleaned_str = sep.replace(r"\n", "\n").replace("\n\n    <!-- -->\n\n    <!-- -->\n\n    <!-- -->", "").replace("\n\n  ", "\n").replace("\n\n-", "\n-").replace("\n\n<!-- -->\n\n<!-- -->", "").replace("[https://", "[").replace("png)", "png").replace("webp)", "webp").replace("jpg)", "jpg").replace("![](/images/", "https://notify.org/images/").replace(".png", ".png\n\n").replace(".jpg", ".jpg\n\n").replace(".webp", ".webp\n\n")

    # Splits the string by a delimiter but keeps the delimiter
    splitstring = [e+"\n\n" for e in cleaned_str.split("\n\n") if e]

    # Combine the list elements up to a specific length for discord max of 2000
    split = []
    buff = splitstring[0] if len(splitstring) > 0 else ""
    for i in range(1,len(splitstring)):
        t = splitstring[i]
        if "https://notify.org/images/" in t:
            if "https://notify.org/images/" not in splitstring[i-1]: 
                split.append(buff)
            split.append(t)
            buff = ""
        elif (len(buff) + len(t) + 1) <= 1975:
            buff += t
        else:
            split.append(buff)
            buff = t
    if len(buff) > 0:
        split.append(buff)

    # Sending each string in the list to make the full guide
    title = "# " + choices.replace("-", " ")
    await interaction.response.send_message(title)
    for i in split:
        await interaction.channel.send(i)

# Get reviews and member relation
@client.command(name = "reviews")
async def reviews(interaction: discord.Interaction):

    if interaction.user.id == KIANROLE:
        await interaction.response.send_message("checking now, may take a little since there is a 5s delay between each request.")

        reviewed, countdonthave, counthave, peopletotal, idDict, noacc = await utilities_utils.reviews_finder()

        await interaction.channel.send(reviewed + " Total reviewers according to Whop. " + countdonthave + " members were given the Reviewer role. " + counthave + " have the role already. ")
        await interaction.channel.send(peopletotal + " Total Notify customers according to Whop. " + idDict + " Total customers added that HAVE accounts. " + noacc + " DON'T have accounts.")

    else:
        await interaction.response.send_message("You don't have access to this command.")

# Get non-reviewers and make list
@client.command(name = "nonreviewers")
async def nonreviewers(interaction: discord.Interaction):

    if interaction.user.id == KIANROLE:
        await interaction.response.send_message("fetching now, may take a little since there is a 30s delay between each 100 members requested.")

        tempMembers, tempEmail = await utilities_utils.non_reviews_finder()

        with open("nonreviewer.txt", "w", encoding="utf-8") as file:
            file.write(tempMembers)

        with open("nonrevieweremail.txt", "w", encoding="utf-8") as file:
            file.write(tempEmail)

        with open("nonreviewer.txt", "rb") as file:
            await interaction.channel.send("Non-Reviewers: ", file=discord.File(file, "nonreviewer.txt"))

        with open("nonrevieweremail.txt", "rb") as file:
            await interaction.channel.send("Non-Reviewers Email Only: ", file=discord.File(file, "nonrevieweremail.txt"))
    else:
        await interaction.response.send_message("You don't have access to this command.")

# Archives channels in Notify so they can be saved before being deleted
@client.command(name = "archivechannel", description = "Archives Discord channels as an HTML file")
async def archivechannel(interaction: discord.Interaction, channel_id: str):
    ch = Client.get_channel(int(channel_id))

    await interaction.response.send_message("Archiving, please wait.")

    transcript = await chat_exporter.export(ch)

    transcript_embed = discord.Embed(
        description=f"**Transcript Name:** transcript-{ch.name}\n\n",
        colour=discord.Colour.blurple()
    )

    transcript_file = discord.File(io.BytesIO(transcript.encode()),filename=f"transcript-{ch.name}.html")

    await interaction.channel.send(embed=transcript_embed, file=transcript_file)

# Gets all the Notify Staff
@client.command(name = "getstaffroles")
async def getstaffroles(interaction: discord.Interaction):
    guild = Client.get_guild(GUILD)
    staff = guild.get_role(STAFFROLE)
    st = [str(m.id) for m in staff.members]
    separator = '", "'
    st = '"' + separator.join(st) + '"'

    await interaction.response.send_message(st)

# Member/Staff Commands
@client.command(name = "kian", description = "Gets Kian's PRs")
async def kian(interaction: discord.Interaction):
    embedVar = await embeds.kian()
    await interaction.response.send_message(embed=embedVar)

# Member/Staff Commands
@client.command(name = "cringe", description = "This is for Mike (aka. 18pairsonkith)")
async def cringe(interaction: discord.Interaction):
    embedVar = await embeds.mike()
    await interaction.response.send_message(embed=embedVar)

# Member/Staff Commands
@client.command(name = "p3bl3z", description = "Some classic P3bl3z Quotes")
async def p3bl3z(interaction: discord.Interaction):
    embedVar = await embeds.peblez()
    await interaction.response.send_message(embed=embedVar)

# Links embed for ease of access
@client.command(name = "guides", description = "Gets all the links to Notify guides")
async def guides(interaction: discord.Interaction):
    embedVar = await embeds.guides()
    await interaction.response.send_message(embed=embedVar, ephemeral=True)

# SP Variants and Stock
@client.command(name = "spstock", description = "Gets stock/vars of products on Shoe Palace", guild = discord.Object(id = 570142274902818816))
async def spstock(interaction: discord.Interaction, url: str):
    url = url + ".json"
    try:
        page = requests.get(url)
        page_json = page.json()
        titleJson = page_json["product"]
        title = titleJson['title']
        stock_embed = discord.Embed(
            title= title + f"\n\n",
            colour=0xDB0B23
        )
        jsonData = page_json["product"]["variants"]
        for x in jsonData:
            stock_embed.add_field(name = "Size, Variant, `Quantity`", value = str(x['title']) + ", " + str(x['id']) + ", `{}".format(str(x['inventory_quantity'])) + "`", inline = True)

        await interaction.response.send_message(embed=stock_embed)
    except:
        await interaction.response.send_message("Wrong Name/Doesn't Exist")

# JJ Variants and Stock
@client.command(name = "jjstock", description = "Gets stock/vars of products on Jimmy Jazz", guild = discord.Object(id = 570142274902818816))
async def jjstock(interaction: discord.Interaction, url: str):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        s = soup.find_all('script')
        stock = str(s)
        stockList = []
        for item in stock.split("\n"):
            if "window.inventories['" in item:
                stockList.append(item[item.find("]["):].replace("[", "").replace("]", "").replace(";", "").replace(" = ", ", "))

        sizes = str(s)
        sizeList = []
        for item in sizes.split("\n"):
            if "window.productJSON" in item:
                sizeList.append(item.strip())

        sizestripped = sizeList[0].replace("window.productJSON = ", "").replace(";", "")
        sizeJson = json.loads(sizestripped)
        titleJson = sizeJson["title"]
        handleJson = sizeJson["handle"]
        stock_embed = discord.Embed(
            title = titleJson + " (" + handleJson + f")\n\n",
            colour = 0xDB0B23
        )
        jsonData = sizeJson["variants"]
        for x in jsonData:
            elem = str(x['id'])
            index_pos = [i for i, s in enumerate(stockList) if elem in s]
            stock_embed.add_field(name = "Size, Variant, Quantity", value = str(x['title']) + ", " + stockList[int(index_pos[0])], inline = True)

        await interaction.response.send_message(embed=stock_embed)
    except:
        await interaction.response.send_message("Wrong Name/Doesn't Exist or Some Code Issue/Change.")

# NB Variants
@client.command(name = "nbstock", description = "Gets vars of products on NB", guild = discord.Object(id = 570142274902818816))
async def nbstock(interaction: discord.Interaction, url: str):

    session = requests_html.HTMLSession()
    r = session.get(url)

    print(r.text)

    varBlock = ""
    varsFinal = ""
    varsFinalcomma = ""

    for item in r.html.xpath('//*[@id="maincontent"]/script[3]'):
        varBlock = item.text
    varSep = varBlock[varBlock.find('"variants":'):]
    varSepSep = varSep.split(', "master":',1)[0]
    varSepSepSep = varSepSep[varSepSep.find('{'):]
    varJson = json.loads(varSepSepSep)
    for x in varJson:
        varsFinal += x + "\n"
        varsFinalcomma += x + ","

    varsall = varsFinal

    stock_embed = discord.Embed(
        title= url + f"\n\n",
        description = varsFinal,
        colour=0xDB0B23
    )

    stock_embed_comma = discord.Embed(
        title= url + f"\n\n",
        description = varsFinalcomma,
        colour=0xDB0B23
    )

    await interaction.response.send_message(embed=stock_embed)
    await interaction.channel.send(embed=stock_embed_comma)

# Get members with no roles
@client.command(name = "hasnoroles")
async def hasnoroles(interaction: discord.Interaction):
    if interaction.user.id == KIANROLE:
        members = interaction.guild.members
        memberstr = ""
        for member in members:
            if len(member.roles) == 1:
                memberstr = memberstr + "<@!" + str(member.id) + "> "

        await interaction.response.send_message("List of members with no roles: " + memberstr)
    else:
        await interaction.response.send_message("You don't have access to this command.")

# Get x number of members with certain role
@client.command(name = "randomselect")
async def randomselect(interaction: discord.Interaction, role: str, number: int):
    guild = Client.get_guild(GUILD)
    notifyrole = discord.utils.find(lambda r: r.name == "Staff", interaction.channel.guild.roles)

    if notifyrole in interaction.user.roles:
        members = interaction.guild.members
        memberlist = []

        for member in members:
            for roles in member.roles:
                if role in roles.name:
                    memberlist.append(member.id)

        sample = random.sample(memberlist, number)
        strmem = ""

        for i in sample:
            strmem = strmem + "<@!" + str(i) + "> "

        await interaction.response.send_message("Random list of members:\n\n" + strmem)
    else:
        await interaction.response.send_message("You don't have access to this command.")

@Client.event
async def on_message(msg):
    # Used to remove and dm members if their wts posts don't contain monetary amounts
    if msg.channel.id == MARKETPLACECHANNEL:
        userId = str(msg.author.id)
        user = await Client.fetch_user(userId)

        if any(keyword in msg.content.lower() for keyword in ["$", "shipped", "shipping"]) or msg.author.id == NOTIFYHELPERROLE:
            pass
        else:
            await msg.delete()
            try:
                await user.send("Hey, please include the price in your WTS post, I check for the use of a '$', 'shipped', or 'shipping' to make sure there is a price so please include at least a '$', I have attached your deleted message for you to update.")
                await user.send("`" + msg.content + "`")
            except (discord.errors.Forbidden, discord.errors.HTTPException):
                staff = await Client.fetch_user(KIANROLE)
                guild = Client.get_guild(GUILD)
                user = msg.author
                cat = discord.utils.get(guild.categories, id = ADMINCATEGORY)

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False), #Make default not able to view this private channel
                    guild.me: discord.PermissionOverwrite(read_messages=True), #Add the bot to the channel
                    user: discord.PermissionOverwrite(read_messages=True),
                    staff: discord.PermissionOverwrite(read_messages=True, manage_channels=True)
                }

                ch = await guild.create_text_channel("WTS Issue-" + str(user), overwrites = overwrites, category = cat)
                await ch.send("Hey, please include the price in your WTS post, I check for the use of a '$', 'shipped', or 'shipping' to make sure there is a price so please include at least a '$', I have attached your deleted message for you to update.")
                await ch.send("`" + msg.content + "`")

Client.run(TOKEN, log_handler=None)
