import discord
import names
import datetime
import os
import aiohttp
import asyncio
import json
from itertools import cycle, islice
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import List
from github import Github
from discord import app_commands

from database import dbaccess
from embeds import embeds

Client = None

GUILD = int(os.environ.get('NOTIFYGUILDID'))
WHOP_API_KEY = os.environ.get('WHOP_API_KEY')

# Sets client var on bot start
async def set_vars(c):
    global Client

    Client = c

# Used by the NotifyUtilities.py to send keys to members
async def send_member_dms(interaction, m):
    # ID retrieval
    message_parts = m.split('/')
    message_id = int(message_parts.pop())
    channel_id = int(message_parts.pop())
    channel = Client.get_channel(channel_id)
    msg = await channel.fetch_message(message_id)

    # Extract user IDs and mentions
    users = [mention.id for mention in msg.mentions]
    user_mentions = [mention.mention for mention in msg.mentions]
    user_string = ', '.join(user_mentions)

    # Replies saying it found members
    found_embed = await embeds.memberdm_found(str(len(msg.mentions)))
    await interaction.response.send_message(embed=found_embed)

    # Check before waiting response
    def check(mes):
        return mes.channel == interaction.channel and mes.author != Client.user

    # Ask for user response and wait for it
    keystring = await Client.wait_for("message", check = check)
    if keystring.content == "restart":
        return

    # Put the keys into a list
    keys = keystring.content.split(', ')

    # Check if same amount of keys as winners
    if len(keys) != len(users):
        await interaction.channel.send("Key to Winners is not equal, please restart.")
        return

    # What did they win
    what_embed = await embeds.memberdm_what()
    await interaction.channel.send(embed=what_embed)
    what = await Client.wait_for("message", check=check)
    if what.content == "restart":
        return

    # Ask for required URL
    url_embed = await embeds.memberdm_url()
    await interaction.channel.send(embed=url_embed)
    url = await Client.wait_for("message", check=check)
    if url.content == "restart":
        return

    # Ask for a message to send
    message_embed = await embeds.memberdm_message()
    await interaction.channel.send(embed=message_embed)
    dm = await Client.wait_for("message", check = check)
    if dm.content == "restart":
        return

    # Setup sent dm and show ex
    ex_embed = await embeds.memberdm_ex(userstring, str(url.content), str(dm.content))
    await interaction.channel.send(embed=ex_embed)

    # Confirm if correct and send/check/open ticket if no dm is successful
    yes_no = await Client.wait_for("message", check = check)

    if str(yes_no.content) == "n":
        await interaction.channel.send("Please restart.")
    elif str(yes_no.content) == "y":
        await interaction.channel.send("Dming members now.")

        outputstring = ""
        for i, key in enumerate(keys):
            send_embed = await embeds.memberdm_send(str(what.content), key, url.content, dm.content)
            temp = await Client.fetch_user(users[i])
            try:
                await temp.send(embed = send_embed)
                outputstring += f"DM to {temp} ✅ SUCCESSFUL\n"
            except (discord.errors.Forbidden, discord.errors.HTTPException):
                outputstring += f"DM to {temp} ❌ FAILED, Opening Ticket.\n"

                staffId = str(interaction.user.id)
                staff = await Client.fetch_user(staffId)
                guild = Client.get_guild(GUILD)
                user = temp
                cat = discord.utils.get(guild.categories, id = 806215492695883786)

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False), #Make default not able to view this private channel
                    guild.me: discord.PermissionOverwrite(read_messages=True), #Add the bot to the channel
                    user: discord.PermissionOverwrite(read_messages=True),
                    staff: discord.PermissionOverwrite(read_messages=True, manage_channels=True)
                }

                ch = await guild.create_text_channel(f"giveaway winner-{temp}", overwrites=overwrites, category=cat)
                await ch.send(embed=send_embed)

        output_embed = await embeds.memberdm_output(outputstring)

        await interaction.channel.send(embed = output_embed)
    else:
        await interaction.channel.send("Only answer with y/n. Restart please.")

# Used to fill in UFC entry forms
async def fill_form(browser, proxylist, emails, isgmail, form_url, field_ids):
    issues = []
    for i in range(25):
        try:
            proxy_parts = proxylist[i].split(":")
            browser.proxy = {
                'http': f'http://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}',
                'https': f'https://{proxy_parts[2]}:{proxy_parts[3]}@{proxy_parts[0]}:{proxy_parts[1]}'
            }
            browser.get(form_url)
            wait = WebDriverWait(browser, 10)
            element = wait.until(EC.presence_of_element_located((By.ID, field_ids['first_name'])))
            first_name = browser.find_element(By.ID, field_ids['first_name'])
            last_name = browser.find_element(By.ID, field_ids['last_name'])
            email_field = browser.find_element(By.ID, field_ids['email'])
            submit_button = browser.find_element(By.ID, field_ids['submit'])

            first = names.get_first_name()
            last = names.get_last_name()
            first_name.send_keys(first)
            last_name.send_keys(last)
            email = emails.split(",")[i] if isgmail else first + last + emails
            email_field.send_keys(email)
            submit_button.click()

            wait.until(lambda driver: browser.current_url != form_url)
        except Exception as e:
            print(f"Exception: {str(e)}\nMay be due to a proxy being banned on the site.")
            issues.append(i)
    return issues

# Creates the browser
async def initialize_browser(headless):
    options = Options()
    if headless == 1:
        options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-logging')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    options.add_experimental_option("useAutomationExtension", False) 
    options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    return webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

# Used to send entries to Formstack for UFC
async def msg(proxy, emails):
    isgmail = "@gmail.com" in emails
    browser = await initialize_browser(0)
    proxylist = list(islice(cycle(proxy.split(",")), 25))
    time = datetime.datetime.now()
    issues = await fill_form(browser, proxylist, emails, isgmail, "https://msg-wmzqo.formstack.com/forms/ufc_295", 
                       {'first_name': "field147946152-first", 'last_name': "field147946152-last", 
                        'email': "field147946153", 'submit': "fsSubmitButton5363561"})
    browser.close()
    browser.quit()
    print(datetime.datetime.now() - time)
    return (datetime.datetime.now() - time), issues

# Used to send entries for UFC
async def ufc(proxy, emails):
    isgmail = "@gmail.com" in emails
    browser = await initialize_browser(1)
    proxylist = list(islice(cycle(proxy.split(",")), 25))
    time = datetime.datetime.now()
    issues = await fill_form(browser, proxylist, emails, isgmail, "https://form.jotform.com/231917397920161", 
                       {'first_name': "input_3", 'last_name': "input_4", 'email': "input_5", 'submit': "input_2"})
    browser.close()
    browser.quit()
    print(datetime.datetime.now() - time)
    return (datetime.datetime.now() - time), issues

# Gets all the guides you can pull from git.
async def get_guides():
    strippedlist = []
    g = Github('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')
    repo = g.get_repo('vildzi/notify-site')
    c = repo.get_contents("outstatic/content/guides")
    while len(c) >= 1:
        file_content = c.pop(0)
        if file_content.type == "dir":
            c.extend(repo.get_contents(file_content.path))
        else:
            stripped = file_content.path.lstrip().split('outstatic/content/guides/')[1].rstrip().split(".")[0]
            strippedlist.append(stripped)

    strippedlist.pop(0)

    return strippedlist

# Allows to have variable selection length in discord dropdown
async def guide_autocomplete(
    interaction: discord.Interaction, 
    current:str, 
) -> List[app_commands.Choice[str]]:
    choices = await get_guides()
    return [
        app_commands.Choice(name=choice, value=choice)
        for choice in choices if current.lower() in choice.lower()
    ]

async def reviews_finder():
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + WHOP_API_KEY
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        i = 1
        noacc = 0
        idDict = {}
        idList = []
        guild = Client.get_guild(GUILD)
        role = discord.utils.find(lambda r: r.name == 'Reviewer', guild.roles)

        # Gets the discord ids of each whop user and makes a dict with them
        pagestotal = 0
        peopletotal = 0
        url = "https://api.whop.com/api/v2/customers?page=1&per=50"
        async with session.get(url) as r:
            data = await r.read()
            page_json = json.loads(data)

            pagestotal = int(page_json["pagination"]["total_page"])
            peopletotal = int(page_json["pagination"]["total_count"])

        while i <= pagestotal:
            await asyncio.sleep(5)
            url = "https://api.whop.com/api/v2/customers?page=" + str(i) + "&per=50"

            async with session.get(url) as r:
                data = await r.read()
                page_json = json.loads(data)

                if not page_json["data"]:
                    break
                else:
                    j = 0
                    while j < 50:
                        try:
                            if page_json["data"][j]["social_accounts"]:
                                whopid = page_json["data"][j]["id"]
                                discid = page_json["data"][j]["social_accounts"][0]["id"]
                                idDict[whopid] = str(discid) 
                            else:
                                noacc = noacc + 1
                        except Exception as e:
                            print("End of list of users: " + str(e))
                        j = j + 1
            i = i + 1

        # Gets the whop ids of users that reviewed
        i = 1
        reviewed = 0
        while i <= 1000:
            url = "https://api.whop.com/api/v2/reviews?page=" + str(i) + "&per=50"

            async with session.get(url) as r:
                data = await r.read()
                page_json = json.loads(data)

                if not page_json["data"]:
                    break
                else:
                    j = 0
                    while j < 50:
                        try:
                            reviewed = int(page_json["pagination"]["total_count"])
                            whopid = page_json["data"][j]["user"]
                            idList.append(whopid)
                        except Exception as e:
                            print("End of list of reviews: " + str(e))
                        j = j + 1
            i = i + 1

        # Compares and assigns the new roles as needed.
        countdonthave = 0
        counthave = 0
        for k in idList:
            if k in idDict:
                try:
                    userid = idDict[k]
                    user = guild.get_member(int(userid))
                    if role not in user.roles:
                        await user.add_roles(role)
                        countdonthave = countdonthave + 1
                    else:
                        counthave = counthave + 1
                except Exception as e:
                    print("Exception: " + str(e))
                    print(k + " " + idDict[k])

    return str(reviewed), str(countdonthave), str(counthave), str(peopletotal), str(len(idDict)), str(noacc)

async def non_reviews_finder():
    guild = Client.get_guild(GUILD)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + WHOP_API_KEY
    }
    roleAllAccess = discord.utils.find(lambda r: r.name == 'All Access', guild.roles)
    roleReviewer = discord.utils.find(lambda r: r.name == 'Reviewer', guild.roles)
    tempMembers = ""
    tempEmail = ""
    timepause = 0
    async with aiohttp.ClientSession(headers=headers) as session:
        for member in guild.members:
            if not roleReviewer in member.roles and roleAllAccess in member.roles: 

                if timepause == 100:
                    await asyncio.sleep(30)
                    timepause = 0

                url = f"https://api.whop.com/api/v2/customers/{member.id}"
                email = ""
                try:
                    async with session.get(url) as r:
                        data = await r.read()
                        page_json = json.loads(data)
                        if page_json["email"]:
                            email = page_json["email"]
                        else:
                            email = f"No email for {member.name}"
                except Exception as e:
                    email = f"No Whop account for {member.name}"

                tempMembers = tempMembers + "ID: <@" + str(member.id) + ">  |  Email: " + email + "\n"
                tempEmail = tempEmail + email + "\n"

            timepause = timepause + 1

    return tempMembers, tempEmail
