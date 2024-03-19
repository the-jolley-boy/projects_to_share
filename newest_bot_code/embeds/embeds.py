# encoding: utf-8
import discord

from global_vars.global_vars import GlobalVariables

#Sets the footers as needed.
async def setFooter(embedVar):
    embedVar.set_footer(
        text = "Jarvis", 
        icon_url = "https://cdn.discordapp.com/avatars/730136171983667280/7804ea245de12dd9a124e761b55eb97a.webp"
    )
    embedVar.set_thumbnail(
        url = 'https://notify.org/notify.png'
    )
    return embedVar

async def setFooterEU(embedVar):
    embedVar.set_footer(
        text = "Jarvis", 
        icon_url = "https://cdn.discordapp.com/avatars/730136171983667280/7804ea245de12dd9a124e761b55eb97a.webp"
    )
    embedVar.set_thumbnail(
        url = 'https://media.discordapp.net/attachments/719312417200537670/909442302366339142/NEU_NBG.png'
    )
    return embedVar

async def loyalMemberUS():
    embedVar = discord.Embed(
        title="Do you pay $40 or $49 a month for your renewal?",
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def loyalMemberEU():
    embedVar = discord.Embed(
        title="Click The Buttons Below If You Would Like A 3 Or 6 Month Renewal.", description='''Please react with the option that you would like to go with.
                \n\n `-` **Top-Up 3 months for £89 instead of £105 (15%) off**
                \n `-` **Top-Up 6 months for £163 instead of £210 (22%) off**
                \n\n `-` **Once you're done, please let us know your purchase email and tag Michael. If you have questions please let us know.**
                ''', 
        color=0x563ef0
    )
    await setFooterEU(embedVar)

    return embedVar

async def talkToSupport():
    embedVar = discord.Embed(
        title="A staff member will be with you shortly.", 
        description="Please refer to any of the guides below to help answer your question.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def ticketInfo(user_question):
    embedVar = discord.Embed(
        title="FAQ", 
        description="Please also check out our [FAQ](https://notify.org/guides/faq) to see if you can get your question answered there.\n\nMember asked: " + user_question, 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def shipping():
    embedVar = discord.Embed(
        title="Package issues?", 
        description="Unfortunately we can't easily assist with package issues.\nBest plan of action is to make a claim with links below.\n\n", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    embedVar.add_field(name='FedEx', value='[FedEx Claims](https://www.fedex.com/en-us/customer-support/claims.html)', inline=True)
    embedVar.add_field(name='UPS', value='[USP Claims](https://www.ups.com/ca/en/help-center/claims-support.page)', inline=True)
    embedVar.add_field(name='USPS', value='[USPS Claims](https://www.usps.com/help/claims.htm)', inline=True)
    embedVar.add_field(name='DHL', value='[DHL Claims](https://www.dhl.com/ca-en/home/our-divisions/ecommerce-solutions/shipping/helpful-information/submit-a-claim.html)', inline=True)

    return embedVar

async def nike():
    embedVar = discord.Embed(
        title="Nike Information", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    embedVar.add_field(name='Storm', value='[Storm Twitter](https://twitter.com/stormaccounts?s=21&t=UW5fe2upRasV-nDNfseRmw)', inline=True)
    embedVar.add_field(name='CWK', value='[CWK Twitter](https://twitter.com/copwithkyle?s=21&t=UW5fe2upRasV-nDNfseRmw)', inline=True)
    embedVar.add_field(name='Swish', value='[Swish Twitter](https://twitter.com/swish_accounts?s=21&t=UW5fe2upRasV-nDNfseRmw)', inline=True)

    embedVar.add_field(name='Nike J1gging', value='[Nike J1gging Guide](https://notify.org/guides/nike/nike-jigging)', inline=True)
    embedVar.add_field(name='Nike Account Info', value='[Nike Account Guide](https://notify.org/guides/nike/nike-accounts)', inline=True)
    embedVar.add_field(name='Nike General', value='[Nike General Guide](https://notify.org/guides/nike/nike-general)', inline=True)

    embedVar.add_field(name='Top Nike Bots', value='At the moment the top 2 performing bots for Nike is Project Enigma (PE) and Valor. Guides for PE are private so the only way to access them is through their discord.')

    return embedVar

async def creditCards():
    embedVar = discord.Embed(
        title="Card Related Questions?", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    embedVar.add_field(name='Personal Hard Cards/Amex Business Hard/Slash VCC', value='Shopify/Supreme: 🟢 | Footsites: 🟢\nNike: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
    embedVar.add_field(name='Privacy', value='Shopify/Supreme: 🔴 Footsites: 🔴\nNike: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
    embedVar.add_field(name='Eno Mastercard', value='Shopify/Supreme: 🔴 | Footsites: 🟢\nNike: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
    embedVar.add_field(name='Tradeshift (Amex)/Stripe', value='Shopify/Supreme: 🟢 | Footsites: 🔴\nNike: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)
    embedVar.add_field(name='Eno Visa/Citi VCC', value='Shopify/Supreme: 🟢 | Footsites: 🔴\nNike: 🟢 | FNL & JD/Dicks/Hibbett: 🟢 |', inline=False)

    return embedVar

async def membership():
    embedVar = discord.Embed(
        title="Membership", 
        description="Note: To cancel, go to [the dashboard](https://dash.notify.org/notify/hub/) then login and once logged in got to memberships -> click on your membership -> teminate membership. You can also rejoin through the waitlist on the hub [here](https://dash.notify.org/notify/hub/)\n\n", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def proxy():
    embedVar = discord.Embed(
        title="Proxies", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    embedVar.add_field(name = 'Proxies', value = '[Proxies Guide](https://notify.org/guides/intro-to-botting-guides/proxies)', inline=True)
    embedVar.add_field(name = 'Proxies Video', value = '[Proxies Video Guide](https://youtu.be/qMfdkH1fkwY)', inline=True)

    return embedVar

async def other(content, otherkw):
    embedVar = discord.Embed(
        title="Other Guides", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    cont = content.lower()

    if otherkw[0] in cont or otherkw[1] in cont:
        embedVar.add_field(name='Notify Anywhere App', value='[Guide](https://notify.org/guides/intro-to-botting-guides/notify-anywhere-app)', inline=True)
        embedVar.add_field(name='Notify Anywhere App', value='[Info/DL Links](https://discord.com/channels/570142274902818816/991577591158947921/991888970042572851)', inline=True)
    if otherkw[3] in cont or otherkw[8] in cont:
        embedVar.add_field(name='Notify Tools', value='[Guide](https://coptools.gitbook.io/coptools/)', inline=True)
        embedVar.add_field(name='Notify Tools', value='[Info/DL Links](https://discord.com/channels/570142274902818816/991577591158947921/991888985678942208)', inline=True)
    if otherkw[4] in cont:
        embedVar.add_field(name='Notify Helper', value='[Info/DL Links](https://discord.com/channels/570142274902818816/991577591158947921/991888992113016872)', inline=True)
        embedVar.add_field(name='Notify Helper', value='[Video Guide](https://www.youtube.com/watch?v=W59Hu-_8ZIE&ab_channel=Notify)', inline=True)
    if otherkw[5] in cont:
        embedVar.add_field(name='AYCD Partnership', value='[AYCD Partnership Discount/Info](https://discord.com/channels/570142274902818816/985233858423296150/985241206424469504)', inline=True)
        embedVar.add_field(name='AYCD Video Guides', value='[Class](https://notify.org/guides/notify-university/notify-university-aycd)', inline=True)
        embedVar.add_field(name='AYCD AWS', value='[AWS AYCD Guide](https://notify.org/guides/intro-to-botting-guides/aws-aycd-setup)', inline=True)
    if otherkw[6] in cont:
        embedVar.add_field(name='General Server Info', value='[General Server Guide](https://notify.org/guides/intro-to-botting-guides/servers)', inline=True)
        embedVar.add_field(name='AYCD AWS', value='[AYCD AWS Guide](https://notify.org/guides/intro-to-botting-guides/aws-aycd-setup)', inline=True)
    if otherkw[7] in cont:
        embedVar.add_field(name='eBay Questions?', value='[Selling on eBay Guide](https://notify.org/guides/intro-to-botting-guides/selling-on-ebay)', inline=True)
    if otherkw[9] in cont or otherkw[10] in cont:
        embedVar.add_field(name='Automations Guides', value='[Automations Guide](https://notify.org/guides/bot-guides/automations)', inline=True)
    if otherkw[11] in cont:
        embedVar.add_field(name='AYCD AI Guide', value='[Guide (scroll down to the AYCD section)](https://notify.org/guides/bot-guides/automations)', inline=True)

    return embedVar

async def bots(content, botkw):
    embedVar = discord.Embed(
        title="Bot Guides", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    cont = content.lower()

    if botkw[1] in cont:
        embedVar.add_field(name = 'Cyber Shopify/Supreme', value = '[Cyber Shopify/Supreme Guide](https://notify.org/guides/bot-guides/cyber-shopify-supreme)', inline=True)
        embedVar.add_field(name = 'Cyber Automations', value = '[Cyber Automations Guide](https://notify.org/guides/bot-guides/cyber-automations)', inline=True)
    if botkw[2] in cont:
        embedVar.add_field(name = 'Prism Footsites', value = '[Prism Footsites Guide](https://notify.org/guides/bot-guides/prism-footsites)', inline=True)
        embedVar.add_field(name = 'Prism Hibbett', value = '[Prism Hibett Guide](https://notify.org/guides/bot-guides/prism-hibbett)', inline=True)
    if botkw[3] in cont:
        embedVar.add_field(name = 'Hayha', value = 'Guide Coming Soon', inline=True)
    if botkw[5] in cont or botkw[8] in cont:
        embedVar.add_field(name = 'Mekaio Shopify', value = '[Mekaio Shopify Guide](https://notify.org/guides/bot-guides/mekaio-shopify)', inline=True)
        embedVar.add_field(name = 'Mekaio Automations', value = '[Mekaio Automations Guide](https://notify.org/guides/bot-guides/mekaio-automations)', inline=True)
        embedVar.add_field(name = 'Mekaio Nike Flow', value = '[Mekaio Nike Flow Guide](https://notify.org/guides/bot-guides/mekaio-nike-flow-automations)', inline=True)
    if botkw[6] in cont:
        embedVar.add_field(name = 'KSR', value = '[KSR Guide](https://notify.org/guides/bot-guides/ksr)', inline=True)
    if botkw[11] in cont:
        embedVar.add_field(name = 'Refract', value = '[Refract Guide](https://notify.org/guides/bot-guides/refract)', inline=True)
    if botkw[7] in cont:
        embedVar.add_field(name = 'Valor Shopify/Supreme', value = '[Valor Shopify/Supreme Guide](https://notify.org/guides/bot-guides/valor-shopify-supreme)', inline=True)
        embedVar.add_field(name = 'Valor Automations', value = '[Valor Automations Guide](https://notify.org/guides/bot-guides/valor-automations)', inline=True)
        embedVar.add_field(name = 'Valor Nike', value = '[Valor Nike Guide](https://notify.org/guides/bot-guides/valor-nike)', inline=True)
    if botkw[9] in cont or botkw[10] in cont:
        embedVar.add_field(name = 'Chegg Shopify', value = '[Chegg Shopify Guide](https://notify.org/guides/bot-guides/chegg-shopify)', inline=True)

    return embedVar

async def sites(content, sitekw):
    embedVar = discord.Embed(
        title="Site Guides", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    cont = content.lower()

    if any(keyword in cont for keyword in sitekw[:4]):
        embedVar.add_field(name = 'Finishline & JD', value = '[FNL & JD Guide](https://notify.org/guides/sneaker-sites/finishline-and-jdsports)', inline=True)
    if any(keyword in cont for keyword in sitekw[4:8]):
        embedVar.add_field(name = 'Footsites', value = '[Footsites Guide](https://notify.org/guides/sneaker-sites/footsites)', inline=True)
        embedVar.add_field(name = 'Footsites Queue-It', value = '[Footsites Queue-It Guide](https://notify.org/guides/sneaker-sites/footsites-queue-it)', inline=True)
        embedVar.add_field(name = 'Footsites Raffles', value = '[Footsites Raffles Guide](https://notify.org/guides/sneaker-sites/footsites-raffles)', inline=True)
    if sitekw[8] in cont:
        embedVar.add_field(name = 'Hibbett', value = '[Hibbett Guide](https://notify.org/guides/sneaker-sites/hibbett)', inline=True)
    if sitekw[9] in cont or sitekw[10] in cont:
        embedVar.add_field(name = 'Shopify', value = '[Shopify Botting Guide](https://notify.org/guides/sneaker-sites/shopify-botting)', inline=True)
    if sitekw[11] in cont:
        embedVar.add_field(name = 'Supreme', value = '[Supreme Guide](https://notify.org/guides/sneaker-sites/supreme)', inline=True)
    if sitekw[14] in cont:
        embedVar.add_field(name = 'Target', value = '[Target Guide](https://notify.org/guides/retail-sites/targe)', inline=True)
    if sitekw[15] in cont:
        embedVar.add_field(name = 'BestBuy', value = '[Bestbuy Guide](https://notify.org/guides/retail-sites/best-buy)', inline=True)
    if sitekw[16] in cont:
        embedVar.add_field(name = 'Amazon', value = '[Amazon Guide](https://notify.org/guides/retail-sites/amazon)', inline=True)
    if sitekw[17] in cont:
        embedVar.add_field(name = 'Walmart', value = '[Walmart Guide](https://notify.org/guides/retail-sites/walmart)', inline=True)
    if sitekw[18] in cont:
        embedVar.add_field(name = 'AMD', value = '[AMD Guide](https://notify.org/guides/retail-sites/amd)', inline=True)
    if sitekw[19] in cont:
        embedVar.add_field(name = 'Gamestop', value = '[Gamestop Guide](https://notify.org/guides/retail-sites/gamestop)', inline=True)
    if sitekw[20] in cont:
        embedVar.add_field(name = 'Microsoft', value = '[Microsoft Guide](https://notify.org/guides/retail-sites/microsoft)', inline=True)

    return embedVar

async def welcome_ticket(user):
    embedVar = discord.Embed(
        title="Welcome " + str(user.name) + " 👋", 
        description="""Our <@&570142915326771218> is always here:\n`•` Customize the channels you see <#1091086648734916758>\n`•` Need 24/7 support? <#712154540576866354>\n`•` Get personalized support: <#915302513127874611>\n`•` Introduce yourself: <#992842655346196490>\n`•` Download our Mobile App: <#991577591158947921>\n`•` Jumpstart your journey: <#598105432103583744> \n\n **Note:** You **must** respond in this welcome ticket to receive chat access.""", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def topup_us_40():
    embedVar = discord.Embed(
        title="$40/m License Top-Up", 
        description='''Please react with the option that you would like to go with.\n\n `-` **Top-Up 3 months for $105 (13%) off**\n `-` **Top-Up 6 months for $199 (17%) off**''', 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def topup_us_49():
    embedVar = discord.Embed(
        title="$49/m License Top-Up", 
        description='''Please react with the option that you would like to go with.\n\n `-` **Top-Up 3 months for $125 (15%) off**\n `-` **Top-Up 6 months for $239 (20%) off**\n\n**Once you're done, please let us know your purchase email.**''', 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def topup_us_40_final(value):
    embedVar = discord.Embed(
        title=f"$40/m License {value} Month Top-Up", 
        description="An Admin will be with you shortly, please wait.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def topup_us_49_final(value, url):
    embedVar = discord.Embed(
        title=f"$49/m License {value} Month Top-Up", 
        description=f"Please use this link: {url}\n\nOnce you're done, please let us know your purchase email.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def advisor_initial():
    embedVar = discord.Embed(
        title="Category Selection", 
        description='''Please react with the emoji that best fits your desired 1on1 support.''', 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def advisor_sneaker():
    embedVar = discord.Embed(
        title="Sneaker Staff List", 
        description=f'''Please react with the staff member below that best fits your needs.\n
                    {GlobalVariables().staff_emotes["ashton"]} - {GlobalVariables().staff_pings["ashton"]}: `{GlobalVariables().advisorDict[310135558460669972]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redx"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[310135558460669972]["description_sneakers"]}
                    ''' + \
                    f'''
                    {GlobalVariables().staff_emotes["dooley"]} - {GlobalVariables().staff_pings["dooley"]}: `{GlobalVariables().advisorDict[297893394691260418]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redcheck"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[297893394691260418]["description_sneakers"]}
                    ''' + \
                    f'''
                    {GlobalVariables().staff_emotes["eddy"]} - {GlobalVariables().staff_pings["eddy"]}: `{GlobalVariables().advisorDict[719973042134056980]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redx"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[719973042134056980]["description_sneakers"]}
                    ''' + \
                    f'''
                    {GlobalVariables().staff_emotes["kang"]} - {GlobalVariables().staff_pings["kang"]}: `{GlobalVariables().advisorDict[708445384774778881]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redcheck"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[708445384774778881]["description_sneakers"]}
                    ''',
        color=0x54bedd
    )
    await setFooter(embedVar)

    embedVar1 = discord.Embed(
        title="Sneaker Staff List cont'd", 
        description=f'''
                    {GlobalVariables().staff_emotes["kian"]} - {GlobalVariables().staff_pings["kian"]}: `{GlobalVariables().advisorDict[100108221280186368]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redcheck"]} | Nike: {GlobalVariables().other_emotes["redx"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[100108221280186368]["description_sneakers"]}

                    {GlobalVariables().staff_emotes["moumou"]} - {GlobalVariables().staff_pings["moumou"]}: `{GlobalVariables().advisorDict[243617717809053707]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redcheck"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[243617717809053707]["description_sneakers"]}

                    {GlobalVariables().staff_emotes["sloth"]} - {GlobalVariables().staff_pings["sloth"]}: `{GlobalVariables().advisorDict[380544631600840705]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redx"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[380544631600840705]["description_sneakers"]}

                    {GlobalVariables().staff_emotes["vorlin"]} - {GlobalVariables().staff_pings["vorlin"]}: `{GlobalVariables().advisorDict[143113639371603968]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redcheck"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[143113639371603968]["description_sneakers"]}

                    {GlobalVariables().staff_emotes["warchief"]} - {GlobalVariables().staff_pings["warchief"]}: `{GlobalVariables().advisorDict[729093172222754837]["remaining"]}` Sessions Remaining
                    Footsites: {GlobalVariables().other_emotes["redx"]} | Nike: {GlobalVariables().other_emotes["redcheck"]} | Shopify: {GlobalVariables().other_emotes["redcheck"]}
                    > {GlobalVariables().advisorDict[729093172222754837]["description_sneakers"]}

                    Click `Restart` at any time.
                    ''', 
        color=0x54bedd
    )
    await setFooter(embedVar1)

    return embedVar, embedVar1

async def advisor_flips():
    embedVar = discord.Embed(
        title="Flips Staff List", 
        description=f'''Please react with the staff member below that best fits your needs.\n
                    {GlobalVariables().staff_emotes["kian"]} - {GlobalVariables().staff_pings["kian"]}: `{GlobalVariables().advisorDict[100108221280186368]["remaining"]}` Sessions Remaining
                    > `-`General flips
                    > `-`EDC flips

                    {GlobalVariables().staff_emotes["kang"]} - {GlobalVariables().staff_pings["kang"]}: `{GlobalVariables().advisorDict[708445384774778881]["remaining"]}` Sessions Remaining
                    > `-`Ticket Flips

                    {GlobalVariables().staff_emotes["moumou"]} - {GlobalVariables().staff_pings["moumou"]}: `{GlobalVariables().advisorDict[243617717809053707]["remaining"]}` Sessions Remaining
                    > `-`Ticket Flips

                    {GlobalVariables().staff_emotes["vorlin"]} - {GlobalVariables().staff_pings["vorlin"]}: `{GlobalVariables().advisorDict[143113639371603968]["remaining"]}` Sessions Remaining
                    > `-`Clothing Flips

                    Click `Restart` at any time.
                    ''', 
        color=0xffc83d
    )
    await setFooter(embedVar)

    return embedVar

async def advisor_amazon():
    embedVar = discord.Embed(
        title="Amazon FBA/Freebies Staff List", 
        description=f'''Please react with the staff member below that best fits your needs.\n
                    {GlobalVariables().staff_emotes["nef"]} - {GlobalVariables().staff_pings["nef"]}: `{GlobalVariables().advisorDict[208479361664286721]["remaining"]}` Sessions Remaining
                    > `-`Freebies

                    {GlobalVariables().staff_emotes["kang"]} - {GlobalVariables().staff_pings["kang"]}: `{GlobalVariables().advisorDict[708445384774778881]["remaining"]}` Sessions Remaining
                    > `-`FBA

                    {GlobalVariables().staff_emotes["warchief"]} - {GlobalVariables().staff_pings["warchief"]}: `{GlobalVariables().advisorDict[729093172222754837]["remaining"]}` Sessions Remaining
                    > `-`FBA

                    Click `Restart` at any time.
                    ''', 
        color=0xbb9167
    )
    await setFooter(embedVar)

    return embedVar

async def advisor_sports():
    embedVar = discord.Embed(
        title="Sports Betting Staff List", 
        description=f'''Please react with the staff member below that best fits your needs.\n
                    {GlobalVariables().staff_emotes["eddy"]} - {GlobalVariables().staff_pings["eddy"]}: `{GlobalVariables().advisorDict[719973042134056980]["remaining"]}` Sessions Remaining
                    > `-`Getting started betting
                    > `-`Basketball, Baseball, Soccer

                    Click `Restart` at any time.
                    ''', 
        color=0xef8a0c
    )
    await setFooter(embedVar)

    return embedVar

async def advisor_general():
    embedVar = discord.Embed(
        title="General/Other Staff List", 
        description=f'''Please react with the staff member below that best fits your needs.\n
                    {GlobalVariables().staff_emotes["nef"]} - {GlobalVariables().staff_pings["nef"]}: `{GlobalVariables().advisorDict[208479361664286721]["remaining"]}` Sessions Remaining
                    > `-`Credit Management, Credit Building
                    > `-`3D Printing
                    > `-`Amazon Freebies
                    > `-`Bankruptcy Advice

                    Click `Restart` at any time.
                    ''', 
        color=0x28c88e
    )
    await setFooter(embedVar)

    return embedVar

async def kw_list(desc):
    embedVar = discord.Embed(
        title="See a list of all the kw below.", 
        description = desc, 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_found(mentions):
    embedVar = discord.Embed(
        title="Found " + mentions + " Winners, please specify keys equal to number of winners.", 
        description="Separate with a , and a space: `mikes, twitter, is, washed, ...`.\nType restart to stop action.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_what():
    embedVar = discord.Embed(
        title="What did they win?", 
        description="Please specify what they won (bot/server/proxies/etc).\nType restart to stop action.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_url():
    embedVar = discord.Embed(
        title="Please specify the required URL once.", 
        description="Only specify the URL once just like this: `https://www.helpmeimtrappedinmichaelscage.com/`.\nType restart to stop action.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_message():
    embedVar = discord.Embed(
        title="Please specify a message to go along with the dm.", 
        description="Can be whatever as long as it is all contained in a single message.\nType restart to stop action.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_ex(userstring, url, dm):
    embedVar = discord.Embed(
        title="Confirm if it looks good. Reply y/n.",
        description="Will DM the following: " + userstring + "\nWith the following: \n\n" + "Key: `This is your key`\n" + "Click the link to bind: " + url + "\n" + dm,
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_send(what, key, url, dm):
    embedVar = discord.Embed(
        title=what,
        description=f"Key: `{key}`\nClick the link to bind: {url}\n{dm}",
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def memberdm_output(outputstring):
    embedVar = discord.Embed(
        title = "DM Tracker", 
        description = outputstring, 
        color = 0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def kian():
    embedVar = discord.Embed(
        title = "Kian the Great", 
        description = "Kian is a pure athletic specimen.\nHe is 5 ft 7 inch weighing 170 lbs.\nHis bench PR is 345.\nHis squat PR is 435.\nHis deadlift PR is 495.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def mike():
    embedVar = discord.Embed(
        title = "Mike", 
        description = "Mike Oxlong aka 18pairsonkith", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def peblez():
    embedVar = discord.Embed(
        title="Pl3bl3s", 
        description="Ok I am very stupid Do i put US for state or Washington???\n\nOnly reason why anyone is watching the World Cup is cause of ishowspeed", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def guides():
    embedVar = discord.Embed(
        title="Notify Guides", 
        color=0xDB0B23
    )
    embedVar.add_field(name = "Intro to Botting Guides", value = "https://notify.org/guides/intro-to-botting-guides", inline = False)
    embedVar.add_field(name = "Bot Guides", value = "https://notify.org/guides/bot-guides", inline = False)
    embedVar.add_field(name = "Sneaker Site Guides", value = "https://notify.org/guides/sneaker-sites", inline = False)
    embedVar.add_field(name = "Retail Site Guides", value = "https://notify.org/guides/retail-sites", inline = False)
    embedVar.add_field(name = "Channel Archives", value = "https://notify.org/guides/channel-archives", inline = False)
    embedVar.add_field(name = "Notify Trading Archives", value = "https://notify.org/guides/trading-archives", inline = False)
    embedVar.add_field(name = "Notify Flips", value = "https://notify.org/guides/flips", inline = False)
    embedVar.add_field(name = "Notify University Class Recordings", value = "https://notify.org/guides/notify-university", inline = False)
    embedVar.add_field(name = "FAQ", value = "https://notify.org/guides/faq", inline = False)
    embedVar.add_field(name = "Nike", value = "https://notify.org/guides/nike", inline = False)
    await setFooter(embedVar)

    return embedVar

async def market_info(username, buyer_stats, seller_stats):
    embedVar = discord.Embed(
        title=username + "'s Profile", 
        description="Below you can find ratings and handling times (total transaction time AVG) for " + username + " on their buyer and seller side", 
        color=0xDB0B23
    )
    embedVar.add_field(name="Buyer:", value=f"Successful Transactions: {str(buyer_stats['success'])}\nFailed Transactions: {str(buyer_stats['fail'])}\nDeal Completion Time (AVG): {str(buyer_stats['days'])}D:{str(buyer_stats['hours'])}H:{str(buyer_stats['minutes'])}M\nTotal $ Amount in Deals: ${str(buyer_stats['money'])}", inline = False)
    embedVar.add_field(name="Seller:", value=f"Successful Transactions: {str(seller_stats['success'])}\nFailed Transactions: {str(seller_stats['fail'])}\nDeal Completion Time (AVG): {str(seller_stats['days'])}D:{str(seller_stats['hours'])}H:{str(seller_stats['minutes'])}M\nTotal $ Amount in Deals: ${str(seller_stats['money'])}", inline = False)
    await setFooter(embedVar)

    return embedVar

async def marketplace_buyer():
    embedVar = discord.Embed(
        title="Buyer Rating", 
        description="> Please rate the Buyer now. (Only to be used by Seller). Type `1` for positive/successful transaction or `0` if unsuccessful/bad experience.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_seller():
    embedVar = discord.Embed(
        title="Seller Rating", 
        description="> Please rate the Seller now. (Only to be used by Buyer). Type `1` for positive/successful transaction or `0` if unsuccessful/bad experience.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_tracking(tracking_number):
    embedVar = discord.Embed(title="Next Steps", 
        description=f"Done: tracking number is: {tracking_number}\n\n **Buyer:** \n > Once you receive the items and have confirmed they are correct, please use the command `/donedeal`. Both you, and the seller will need to review each other.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_intial():
    embedVar = discord.Embed(
        title="Buyer/Seller Ticket", 
        description="> Please answer the following questions carefully.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_restart():
    embedVar = discord.Embed(
        title="To Restart", 
        description="Type `restart` at any time to start over (in case you make a mistake on the steps below, thanks!)", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_buyer_input():
    embedVar = discord.Embed(
        title="Buyer ID", 
        description="Enter the Buyers Discord ID ONLY.\n\n> Ex: 100108221280186368 | Not sure how to find it? [Click here.](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_seller_input():
    embedVar = discord.Embed(title="Seller ID", 
        description="Enter the Sellers Discord ID ONLY.\n\n> Ex: 100108221280186368 | Not sure how to find it? [Click here.](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_items():
    embedVar = discord.Embed(
        title="Items", 
        description="List the item(s) in the deal, separated by a comma (space).\n\n> Ex: Jordan 1 L&F size 10, Jordan 4 Military Black size 12, etc", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_deal():
    embedVar = discord.Embed(
        title="Total Price", 
        description="Enter total deal price (not including shipping). DO NOT include a dollar sign($).\n\n> Ex: 1025", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_final():
    embedVar = discord.Embed(
        title="Is All The Info Correct?", 
        description="Please make sure the information above is correct. If so, type `y`. If not, type `n`", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar

async def marketplace_next_step():
    embedVar = discord.Embed(
        title="Next Steps", 
        description="**Seller:** \n > Once you have shipped the item(s), use `/tracking` to add the tracking number(s). \n\n **Buyer:** \n > Once you receive the items and have confirmed they are correct, please use the command `/donedeal`. Both you, and the seller will need to review each other. \n\n Do NOT use these commands until the steps above are completed.", 
        color=0xDB0B23
    )
    await setFooter(embedVar)

    return embedVar