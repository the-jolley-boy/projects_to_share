import asyncio
import websockets
import json
import discord
from discord import Webhook
import aiohttp
import datetime

apikey_bit_skins = "REDACTED"

sticker_webhook_kian = 'REDACTED'
sticker_webhook_notify = 'REDACTED'
looking_for_webhook_kian = 'REDACTED'
listed_good_deal_webhook_kian = 'REDACTED'
listed_good_deal_webhook_notify = 'REDACTED'

icon_url_bit_skins = "https://cdn.jsdelivr.net/gh/the-jolley-boy/static-files/static/bitskins.webp"
icon_url_notify = "https://notify.org/notify.png"

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

WANTED = [
    "AK-47 | Case Hardened", "M4A1-S | Atomic Alloy (Minimal Wear)",            
    "UMP-45 | Crime Scene (Factory New)", "Glock-18 | Ramese's Reach (Factory New)", "MAC-10 | Propaganda (Factory New)", 
    "MAC-10 | Propaganda (Factory New)", "MAC-10 | Propaganda (Minimal Wear)",
    "UMP-45 | Crime Scene (Minimal Wear)", "StatTrak™ AK-47 | Slate (Factory New)"
]

async def send_to_webhook(embed, webhooks):
    async with aiohttp.ClientSession() as session:
        for webhook_url in webhooks:
            webhook = Webhook.from_url(webhook_url, session=session)
            await webhook.send(embed=embed)

async def main():
    uri = "wss://ws.bitskins.com"
    async with websockets.connect(uri) as socket:
        await socket.send(json.dumps(["WS_AUTH_APIKEY", apikey_bit_skins]))
        await socket.send(json.dumps(["WS_SUB", "listed"]))
        await socket.send(json.dumps(["WS_SUB", "delisted_or_sold"]))
        await socket.send(json.dumps(["WS_SUB", "price_changed"]))
        
        skin_id_old = 0

        while True:
            message = await socket.recv()
            action, data = json.loads(message)
            # print("Message from server", {"action": action, "data": data})

            if isinstance(data, dict) and data.get("app_id") == 730 and (action == "delisted_or_sold" or action == "listed"):
                skin_id = data["skin_id"]
                p = str(data["price"])[:-1]
                price = p[:-2] + "." + p[-2:]
                s = str(data["suggested_price"])[:-1]
                suggested_price = s[:-2] + "." + s[-2:]
                name = data["name"]
                unique_id = data["id"]
                url_name = name.lower().replace("(","").replace(")","").replace(" ","-")
                url = "https://bitskins.com/item/csgo/" + str(unique_id) + "/" + url_name
                deal = round(((1 - int(p)/int(s)) * 100), 2)
                img = "https://steamcommunity-a.akamaihd.net/economy/image/class/730/" + str(data["class_id"])

                print(
                    "Name: " + name + " | skin_id: " + str(skin_id) + " | price: " + str(price) + " | suggested_price: " + str(suggested_price)
                )

                embed = discord.Embed(
                    title=f"{name} {'Listed' if action == 'listed' else ('Price Updated' if action == 'price_changed' else 'Delisted or Sold')}",
                    url=url,
                    color=0x54bedd
                )
                embed.add_field(name="Deal %", value=str(deal), inline=True)
                embed.add_field(name="Item Id", value=str(skin_id), inline=True)
                embed.set_thumbnail(url=img)
                embed.set_footer(text="Notify Monitors | " + str(datetime.datetime.now()), icon_url=icon_url_notify)
                embed.set_author(name="BitSkins", icon_url=icon_url_bit_skins)

                if skin_id_old != skin_id:

                    # Sticker Channels
                    if name in WANTED_STICKERS and deal >= 10 and (action == "listed" or action == "delisted_or_sold"):
                        await send_to_webhook(embed, [sticker_webhook_kian, sticker_webhook_notify])

                    # What I Am Looking For Channel
                    if any(skin in name for skin in WANTED) and (action == "listed" or action == "price_changed" or action == "delisted_or_sold"):
                        await send_to_webhook(embed, [looking_for_webhook_kian])

                    # Listed + Good Deal Channel
                    if (action == "listed" or action == "price_changed") and deal >= 25:
                        await send_to_webhook(embed, [listed_good_deal_webhook_kian, listed_good_deal_webhook_notify])

                    skin_id_old = skin_id

if __name__ == '__main__':
    asyncio.run(main())
