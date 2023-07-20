import socketio
import asyncio
import discord
from discord import Webhook
import aiohttp
import datetime

async def main():
    sio = socketio.AsyncClient(reconnection_attempts=5)
    await sio.connect('https://skinport.com/', transports=['websocket'])
    await sio.emit('saleFeedJoin', {'currency': 'CAD', 'locale': 'en', 'appid': 730})

    wanted = ["9191","9139","10318","9124","10318","18296","20699","60771","55047","55084","55046","55045","9164","9161","9141","1461","74464","259","310","60320","48583","130097"]

    @sio.event
    def connect():
        print("I'm connected again!")

    @sio.event
    def connect_error():
        print("The connection failed... Reconnecting")
        # await sio.connect('https://skinport.com/', transports=['websocket'])
        # await sio.emit('saleFeedJoin', {'currency': 'CAD', 'locale': 'en', 'appid': 730})

    @sio.event
    async def disconnect():
        print("Disconnected... Reconnecting")
        print(datetime.datetime.now())

    @sio.on('saleFeed')
    async def on_message(data):

        eventType = data.get("eventType")
        print(eventType)

        # print(data)

        # Gathering what I need for the enbeds from the dict
        marketName = data["sales"][0]["marketName"]
        url = "https://skinport.com/item/" + str(data["sales"][0]["url"]) + "/" + str(data["sales"][0]["saleId"])
        lock = data["sales"][0]["lock"]
        deal = round((1 - (int(data["sales"][0]["salePrice"])/int(data["sales"][0]["suggestedPrice"]))) * 100, 2)
        stickers = data["sales"][0]["stickers"]
        itemid = data["sales"][0]["itemId"]
        pattern = data["sales"][0]["pattern"]
        finish = data["sales"][0]["finish"]
        img = "https://community.cloudflare.steamstatic.com/economy/image/" + data["sales"][0]["image"]
        
        sale = str(data["sales"][0]["salePrice"])
        if len(sale) > 2:
            saleNoCents = sale[:-2]
        else:
            saleNoCents = 0
        salePrice = sale[:-2] + "." + sale[-2:]
        
        if data["sales"][0]["wear"]:
            wear = round(data["sales"][0]["wear"], 6)
        else:
            wear = data["sales"][0]["wear"]
        exterior = data["sales"][0]["exterior"]
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

        if data["sales"][0]["stickers"]:
            sticker = True
            s = data["sales"][0]["stickers"]

            for x in s:
                stickerimg.append(x["img"])
                stickername = stickername + "\n" + x["name"]

        # Low Float Channel
        if eventType == "listed" and deal >= 15 and wear != None and wear < 0.01:
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)
                webhook2 = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Listed", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)
                await webhook2.send(embed=embed)

        # Sticker Channel
        if eventType == "listed" and deal >= 10 and sticker == True and "souvenir" not in marketName.lower():
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)
                webhook2 = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Listed", description="PRICE: " + str(salePrice) + "\n Stickers: " + stickername, url=url, color=0x54bedd).set_image(url=stickerimg[0])
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                if len(stickerimg) == 1:
                    await webhook.send(embed=embed)
                    await webhook2.send(embed=embed)
                if len(stickerimg) == 2:
                    embed2 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[1])
                    await webhook.send(embeds = [embed, embed2])
                    await webhook2.send(embeds = [embed, embed2])
                if len(stickerimg) == 3:
                    embed2 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[1])
                    embed3 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[2])
                    await webhook.send(embeds = [embed, embed2, embed3])
                    await webhook2.send(embeds = [embed, embed2, embed3])
                if len(stickerimg) == 4:
                    embed2 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[1])
                    embed3 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[2])
                    embed4 = discord.Embed(url=url, color=0x54bedd).set_image(url=stickerimg[3])
                    await webhook.send(embeds = [embed, embed2, embed3, embed4])
                    await webhook2.send(embeds = [embed, embed2, embed3, embed4])

        # Sold Channel
        if eventType == "sold":
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)
                webhook2 = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Sold", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)
                await webhook2.send(embed=embed)

        # Listed Channel
        if eventType == "listed":
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)
                webhook2 = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Listed", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)
                await webhook2.send(embed=embed)

        # What I Am Looking For Channel
        if eventType == "listed" and any(x in str(itemid) for x in wanted):
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Listed", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)

        # What I Am Looking For Channel Sold
        if eventType == "sold" and str(itemid) in wanted:
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Sold", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)

        # Cases
        if eventType == "listed" and deal >= 20 and (data["sales"][0]["category"] == "Cases" or data["sales"][0]["category"] == "Container"):
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Listed", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)

        # Listed + Good Deal Channel
        if eventType == "listed" and deal >= 25 and int(saleNoCents) > 4:
            async with aiohttp.ClientSession() as s:
                webhook = Webhook.from_url('REDACTED', session=s)
                webhook2 = Webhook.from_url('REDACTED', session=s)

                embed = discord.Embed(title=marketName + " Listed", description="PRICE: " + str(salePrice), url=url, color=0x54bedd)
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Wear | Float", value=str(exterior) + " | " + str(wear), inline=True)
                embed.add_field(name="Locked Until", value=str(lock), inline=True)
                embed.add_field(name="Pattern", value=str(pattern), inline=True)
                embed.add_field(name="Item Id", value=str(itemid), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url="https://notify.org/notify.png")
                embed.set_author(name="SkinPort", icon_url="https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/8ue6qgH__400x400.jpg")

                await webhook.send(embed=embed)
                await webhook2.send(embed=embed)

if __name__ == '__main__':
    asyncio.run(main())