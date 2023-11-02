import socketio
import asyncio
import discord
from discord import Webhook
import aiohttp
import datetime

WANTED_SKINS = [
    "M4A4 | Radiation Hazard (Field-Tested)", "UMP-45 | Fallout Warning (Minimal Wear)",
    "UMP-45 | Crime Scene (Factory New)", "Glock-18 | Ramese's Reach (Factory New)", "UMP-45 | Crime Scene (Minimal Wear)", 
    "StatTrak™ AK-47 | Slate (Factory New)", "MAC-10 | Propaganda (Factory New)", "(Foil) | Atlanta 2017",
    "MAC-10 | Propaganda (Minimal Wear)", "M4A4 | The Coalition (Field-Tested)", "P250 | Apep's Curse (Field-Tested)",
    "P250 | Apep's Curse (Minimal Wear)", "M4A4 | Eye of Horus (Field-Tested)"
]

OTHER_PATTERN = [
    1, 5, 14, 16, 35, 57, 72,  93, 98, 104, 116, 127, 132, 177, 196, 213, 217, 225, 226, 255, 262, 265, 271, 282, 288, 303, 333, 348, 378, 
    385, 389, 417,  421, 423, 425, 434, 475, 485, 510, 537, 539, 584, 628, 634, 637, 641, 672, 675, 685, 705, 710, 727, 746, 762, 768, 776, 
    787, 794, 796, 811, 822, 830, 831, 853, 886, 903
]
BLUE_MAG_PATTERN = [
    6, 56, 111, 342, 376, 379, 581, 761, 778
]
BLUE_TOP_PATTERN = [
    37, 48, 55, 62, 63, 65, 78, 125, 142, 149, 163, 178, 200, 209, 215, 227, 235, 281, 287, 312, 319, 325, 349, 350, 365, 397, 401, 454, 456, 
    467, 468, 470, 541, 558, 566, 632, 634, 676, 678, 681, 700, 724, 728, 758, 814, 819, 894, 1000
]
BLUE_BACK_TOP_PATTERN = [
    11, 19, 68, 106, 128, 130, 170, 194, 259, 284, 308, 322, 332, 352, 453, 493, 494, 507, 517, 522, 580, 608, 644, 664, 693, 694, 782, 793, 
    803, 838, 856, 857, 891, 906, 913, 917, 919, 965
]
VERY_BLUE_PATTERN = [
    95, 101, 129, 135, 162, 166, 182, 251, 261, 269, 334, 337, 403, 611, 631, 652, 704, 806, 979
]
TOP_FAV_PATTERN = [
    49, 118, 230, 248, 314, 73, 81, 82, 169, 173, 174, 192, 202, 207, 236, 369, 390, 396, 424, 458, 472, 479, 574, 585, 586, 604, 605, 610, 711, 
    721, 842, 847
]

WANTED_STICKERS = [
    "Sticker | dexter (Glitter) | Paris 2023", "Sticker | Complexity Gaming (Gold) | Paris 2023", "Sticker | Fnatic (Gold) | Paris 2023",
    "Sticker | Natus Vincere (Gold) | Paris 2023", "Sticker | 9INE (Gold) | Paris 2023", "Sticker | GamerLegion (Gold) | Paris 2023",
    "Sticker | Team Liquid (Gold) | Paris 2023", "Sticker | Apeks (Glitter) | Paris 2023", "Sticker | MOUZ (Glitter) | Paris 2023",
    "Sticker | MOUZ (Gold) | Paris 2023", "Sticker | MOUZ (Holo) | Paris 2023", "Sticker | Fnatic (Holo) | Paris 2023",
    "Sticker | Fnatic (Glitter) | Paris 2023", "Sticker | GamerLegion (Holo) | Paris 2023", "Sticker | FURIA (Holo) | Paris 2023",
    "Sticker | Fluxo (Holo) | Paris 2023", "Sticker | ropz (Holo) | Paris 2023", "Sticker | dexter (Holo) | Paris 2023",
    "Sticker | ropz (Glitter) | Paris 2023", "Sticker | dexter (Gold) | Paris 2023", "Sticker | v$m (Holo) | Paris 2023",
    "Sticker | JDC (Gold) | Paris 2023", "Sticker | The MongolZ (Holo) | Paris 2023", "Sticker | Natus Vincere (Holo) | Paris 2023",
    "Sticker | 9INE (Glitter) | Paris 2023", "Sticker | 9INE (Holo) | Paris 2023", "Sticker | Apeks (Holo) | Paris 2023",
    "Sticker | Vitality (Holo) | Paris 2023", "Sticker | JDC (Holo) | Paris 2023"
]

STICKER_ON_GUNS = [
    "Katowice 2014", "(Holo) | Cologne 2014", "(Blue) | Cologne 2014", "(Red) | Cologne 2014", "(Foil) | DreamHack 2014", "(Holo) | DreamHack 2014",
    "(Foil) | Katowice 2015", "(Holo) | Katowice 2015", "(Foil) | Cologne 2015", "(Holo) | Cologne 2015", "(Foil) | Cluj-Napoca 2015", 
    "(Holo) | Cluj-Napoca 2015", "(Foil) | MLG Columbus 2016", "(Holo) | MLG Columbus 2016", "(Foil) | Cologne 2016", "(Holo) | Cologne 2016",
    "(Foil) | Atlanta 2017", "(Holo) | Atlanta 2017", "(Gold) | Krakow 2017", "(Foil) | Krakow 2017", "(Gold) | Boston 2018", "(Foil) | Boston 2018",
    "(Gold) | London 2018", "(Gold) | Katowice 2019"
]

sticker_webhook_kian = 'REDACTED'
sticker_webhook_notify = 'REDACTED'
low_float_webhook_kian = 'REDACTED'
low_float_webhook_notify = 'REDACTED'
sold_webhook_kian = 'REDACTED'
sold_webhook_notify = 'REDACTED'
listed_webhook_kian = 'REDACTED'
listed_webhook_notify = 'REDACTED'
looking_for_webhook_kian = 'REDACTED'
cases_webhook_kian = 'REDACTED'
listed_good_deal_webhook_kian = 'REDACTED'
listed_good_deal_webhook_notify = 'REDACTED'
wanted_sticker_guns = "REDACTED"

async def send_to_webhook(embed, webhooks):
    async with aiohttp.ClientSession() as session:
        for webhook_url in webhooks:
            webhook = Webhook.from_url(webhook_url, session=session)
            await webhook.send(embed=embed)

sio = socketio.AsyncClient()

@sio.event
def connect_error():
    print("The connection failed... Reconnecting")

@sio.event
async def disconnect():
    print("Disconnected... Reconnecting")
    print(datetime.datetime.now())

async def connect_with_retry():
    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            await sio.connect('https://skinport.com/', transports=['websocket'])
            print("Connected to the server.")
            break
        except Exception as e:
            print(f"Reconnection attept {attempt + 1} failed: {e}")
            await asyncio.sleep(retry_delay)
            retry_delay *= 2

async def main():

    await connect_with_retry()
    await sio.emit('saleFeedJoin', {'currency': 'CAD', 'locale': 'en', 'appid': 730})

    @sio.event
    def connect():
        print("I'm connected again!")

    @sio.on('saleFeed')
    async def on_message(data):
        eventType = data.get("eventType")
        print(eventType)

        # Making sure there is sales data
        sales = data.get("sales")
        if not sales:
            return

        # Gathering what is needed from the websocket data
        sale = sales[0]
        marketName = sale.get("marketName")
        url = f"https://skinport.com/item/{sale['url']}/{sale['saleId']}"
        lock = sale.get("lock")

        sp = sale.get("salePrice")
        suggestedPrice = sale.get("suggestedPrice")
        deal = round((1 - (sp/suggestedPrice)) * 100, 2)

        # To not put cheap items in good deal list
        if len(str(sp)) > 2:
            saleNoCents = str(sp)[:-2]
        else:
            saleNoCents = 0
        # Adds proper format to prices
        salePrice = str(sp)[:-2] + "." + str(sp)[-2:]

        stickers = sale.get("stickers", [])
        itemid = sale.get("itemId")
        pattern = sale.get("pattern")
        finish = sale.get("finish")
        img = f"https://community.cloudflare.steamstatic.com/economy/image/{sale['image']}"

        if sale.get("wear"):
            wear = round(sale.get("wear"), 6)
        else:
            wear = sale.get("wear")

        exterior = sale.get("exterior")
        if exterior == "Factory New":
            exterior = "FN"
        if exterior == "Minimal Wear":
            exterior = "MW"
        if exterior == "Field-Tested":
            exterior = "FT"
        if exterior == "Well-Worn":
            exterior = "WW"
        if exterior == "Battle-Scarred":
            exterior = "BS"
        if exterior == "None":
            exterior = "NA"

        sticker = False
        stickerimg = []
        stickername = ""

        if sale.get("stickers"):
            sticker = True
            s = sale.get("stickers")

            for x in s:
                stickerimg.append(x["img"])
                stickername = stickername + "\n" + x["name"]

        # Create the embed
        newline = "\n"
        embed = discord.Embed(
            title = f"{marketName} {'Listed' if eventType == 'listed' else 'Sold'}",
            description = f"PRICE: {salePrice} {newline + 'Stickers: ' + stickername if stickername != '' else ''}",
            url=url,
            color=0x54bedd
        )
        embed.add_field(name="Deal %", value=str(deal), inline=True)
        embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
        embed.add_field(name="Locked Until", value=str(lock), inline=True)
        embed.add_field(name="Pattern", value=str(pattern), inline=True)
        embed.add_field(name="Item Id", value=str(itemid), inline=True)
        embed.set_thumbnail(url=img)
        embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
        embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

        # Sticker Channels
        if any(sticker in marketName for sticker in WANTED_STICKERS) and deal >= 10 and (eventType == "listed" or eventType == "sold") :      
            await send_to_webhook(embed, [sticker_webhook_kian, sticker_webhook_notify])

        # Low Float Channel
        if deal >= 15 and wear != None and wear < 0.01 and (eventType == "listed" or eventType == "sold"):
            await send_to_webhook(embed, [low_float_webhook_kian, low_float_webhook_notify])

        # Sticker Channel
        if eventType == "listed" and sticker == True and "souvenir" not in marketName.lower() and float(salePrice) < 850 and deal > -50:
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)
                webhook2 = Webhook.from_url('REDACTED', session=s)
                webhook3 = Webhook.from_url('REDACTED', session=s)

                embed.set_image(url=stickerimg[0])

                if len(stickerimg) == 1:
                    await webhook.send(embed=embed)
                    await webhook2.send(embed=embed)
                    if any(sticker in stickername for sticker in STICKER_ON_GUNS):
                        await webhook3.send(embed=embed)
                if len(stickerimg) == 2:
                    embed2 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[1])
                    await webhook.send(embeds = [embed, embed2])
                    await webhook2.send(embeds = [embed, embed2])
                    if any(sticker in stickername for sticker in STICKER_ON_GUNS):
                        await webhook3.send(embeds = [embed, embed2])
                if len(stickerimg) == 3:
                    embed2 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[1])
                    embed3 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[2])
                    await webhook.send(embeds = [embed, embed2, embed3])
                    await webhook2.send(embeds = [embed, embed2, embed3])
                    if any(sticker in stickername for sticker in STICKER_ON_GUNS):
                        await webhook3.send(embeds = [embed, embed2, embed3])
                if len(stickerimg) == 4:
                    embed2 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[1])
                    embed3 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[2])
                    embed4 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[3])
                    await webhook.send(embeds = [embed, embed2, embed3, embed4])
                    await webhook2.send(embeds = [embed, embed2, embed3, embed4])
                    if any(sticker in stickername for sticker in STICKER_ON_GUNS):
                        await webhook3.send(embeds = [embed, embed2, embed3, embed4])

        # Sold Channel
        if eventType == "sold":
            await send_to_webhook(embed, [sold_webhook_kian, sold_webhook_notify])

        # Listed Channel
        if eventType == "listed":
            await send_to_webhook(embed, [listed_webhook_kian, listed_webhook_notify])

        # What I Am Looking For Channel
        if "AK-47 | Case Hardened" in marketName and (eventType == "sold" or eventType == "listed"):
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url(looking_for_webhook_kian, session=s)
                if "AK-47 | Case Hardened" in marketName and pattern in OTHER_PATTERN:
                    await send_to_webhook(embed, [looking_for_webhook_kian])
                    await webhook.send("Other patter detected.")
                if "AK-47 | Case Hardened" in marketName and pattern in BLUE_MAG_PATTERN:
                    await send_to_webhook(embed, [looking_for_webhook_kian])
                    await webhook.send("Blue Mag patter detected.")
                if "AK-47 | Case Hardened" in marketName and pattern in BLUE_TOP_PATTERN:
                    await send_to_webhook(embed, [looking_for_webhook_kian])
                    await webhook.send("Blue Top patter detected.")
                if "AK-47 | Case Hardened" in marketName and pattern in BLUE_BACK_TOP_PATTERN:
                    await send_to_webhook(embed, [looking_for_webhook_kian])
                    await webhook.send("Blue Back Top patter detected.")
                if "AK-47 | Case Hardened" in marketName and pattern in VERY_BLUE_PATTERN:
                    await send_to_webhook(embed, [looking_for_webhook_kian])
                    await webhook.send("Very Blue patter detected.")
                if "AK-47 | Case Hardened" in marketName and pattern in TOP_FAV_PATTERN:
                    await send_to_webhook(embed, [looking_for_webhook_kian])
                    await webhook.send("Top patter detected.")

        # What I Am Looking For Channel
        if any(skin in marketName for skin in WANTED_SKINS) and (eventType == "sold" or eventType == "listed"):
            await send_to_webhook(embed, [looking_for_webhook_kian])

        # Cases
        if eventType == "listed" and deal >= 20 and (data["sales"][0]["category"] == "Cases" or data["sales"][0]["category"] == "Container"):
            await send_to_webhook(embed, [cases_webhook_kian])

        # Listed + Good Deal Channel
        if eventType == "listed" and deal >= 20 and deal <= 26 and int(saleNoCents) > 4:
            await send_to_webhook(embed, [listed_good_deal_webhook_kian, listed_good_deal_webhook_notify])

if __name__ == '__main__':
    asyncio.run(main())
