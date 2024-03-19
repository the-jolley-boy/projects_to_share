import discord

from global_vars.global_vars import GlobalVariables
from database import dbaccess
from embeds import embeds

async def setchannelpinger():
    users_data = {}
    user_data_list = []
    query = "select * from pingerkw"
    records = await dbaccess.get_data(query, None)

    for row in records:
        pk_id = row[0]
        user_data = {
            "role": row[1],
            "channel": row[2],
            "keyword": row[3]
        }
        users_data[pk_id] = user_data
        user_data_list.append(int(row[2]))

    GlobalVariables().pingchannelslist = user_data_list
    GlobalVariables().pingchannels = users_data

async def add_kw(keyword, roleid, channelid):
    query = "INSERT INTO pingerkw (keyword, rolestr, channel) VALUES (%s, %s, %s)"

    await dbaccess.write_data(query, (keyword, roleid, channelid))
    await setchannelpinger()

async def remove_kw(keyword, channelid):
    query = "DELETE FROM pingerkw WHERE (keyword, channel) = (%s, %s)"

    await dbaccess.write_data(query, (keyword, channelid))
    await setchannelpinger()

async def list_kw():
    query = "select * from pingerkw"
    records = await dbaccess.get_data(query, None)

    desc = ""
    for row in records:
        desc = desc + "Keyword: " + row[3] + " | Message (Ping): " + row[1] + " | Channel: <#" + row[2] + ">\n"

    embedVar = await embeds.kw_list(desc)

    return embedVar

async def send_kw_ping(msg):

    pm = ""
    embeds = msg.embeds

    if msg.embeds:
        for embed in embeds:
            for key,value in GlobalVariables().pingchannels.items():
                if msg.channel.id != int(value["channel"]):
                    continue  # Skip iteration if channel doesn't match
                if value["keyword"] in (embed.description.lower() if embed.description else "") or value["keyword"] in (embed.title.lower() if embed.title else ""):
                    pm = f"Ping on kw {value['keyword']} {value['role']}"
                    break  # Exit loop since keyword found
    else:
        for key,value in GlobalVariables().pingchannels.items():
            if value["keyword"] in msg.content.lower() and msg.channel.id == int(value["channel"]):
                pm = f"Ping on kw {value['keyword']} {value['role']}"

    return pm