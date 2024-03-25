import discord
import os
import asyncio
from datetime import datetime
import matplotlib.pyplot as plt
import io

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from database import dbaccess
from embeds import embeds

GUILD = int(os.environ.get('NOTIFYGUILDID'))
NEWMEMBERROLE = int(os.environ.get('NEWMEMBERROLE'))
STAFFMODCHANNEL = int(os.environ.get('STAFFMODCHANNEL'))

async def text_data(msg):
    msgstring = msg.content
    words = len(msgstring.split())
    msgstring = msgstring.replace(" ", "")
    msgstring = msgstring.replace("\n", "")
    chars = len(msgstring)

    return  words, chars

async def get_current_date_str():
    curr_month = datetime.now().month
    curr_year = str(datetime.now().year)[-2:]  # Get last two digits of the year
    return f"{curr_month}_{curr_year}"

async def readwrite(cat_id, auth_id, auth_name, msg, words, chars):

    curr_date = await get_current_date_str()
    await dbaccess.add_new_cols(curr_date)

    # Construct the upsert query
    query = f"""
        INSERT INTO notify_staff_message_data (nameid, name, cat_id, msg_{curr_date}, word_{curr_date}, char_{curr_date})
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (nameid, cat_id) DO UPDATE 
        SET name = EXCLUDED.name,
            msg_{curr_date} = notify_staff_message_data.msg_{curr_date} + EXCLUDED.msg_{curr_date},
            word_{curr_date} = notify_staff_message_data.word_{curr_date} + EXCLUDED.word_{curr_date},
            char_{curr_date} = notify_staff_message_data.char_{curr_date} + EXCLUDED.char_{curr_date};
    """

    # Data to be inserted or updated
    data = (auth_id, str(auth_name), cat_id, msg, words, chars)

    # Execute the query
    await dbaccess.write_data(query, data)

async def messagedata(interaction, user):
    staff_id = user

    query = "SELECT * FROM notify_staff_message_data WHERE nameid = %s"
    data = (staff_id,)

    records = await dbaccess.get_data_role_puller(query, data)

    if not records:
        await interaction.response.send_message("No data found for the user.")
        return

    category_mapping = {
        'Staff': 570142944921911296,
        'Support Tickets': 570248275374899200, 
        'Important': 570142946272477184,
        'Releases': 622110241882112011,
        'Sneakers': 1016090827073798164,
        'Community': 570142948155588608, 
        'Flips': 1099125615728283738
    }

    plt.figure(figsize=(16, 8))

    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#1a55FF', '#2aFF78', '#d4a028', '#c467bd', '#6c564b',
        '#e7a1c2', '#4f9f7f', '#bc8d22', '#57aecf', '#9a77cf'
    ]

    for index, (cat_name, cat_id) in enumerate(category_mapping.items()):
        for record in records:
            if record['cat_id'] == cat_id:
                dates = []
                messages = []

                for column_name, value in record.items():
                    if column_name.startswith('msg_'):
                        date_part = '_'.join(column_name.split('_')[1:])
                        dates.append(date_part)
                        messages.append(value)

                # Plot each record as a separate line on the graph, using the color cycle
                if dates and messages:
                    plt.plot(dates, messages, marker='o', label=f"{cat_name}", color=colors[index % len(colors)])

    plt.title('Message Activity')
    plt.xlabel('Date')
    plt.ylabel('Messages')
    plt.grid(True)

    # Place the legend outside the plot to the right with smaller text
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, fontsize='small')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight")  # Ensure the external legend is included in the saved figure
    buf.seek(0)
    plt.close()

    file = discord.File(fp=buf, filename='graph.png')
    embed = discord.Embed(title="Message Activity")
    embed.set_image(url="attachment://graph.png")
    await interaction.channel.send(embed=embed, file=file)

    buf.close()
