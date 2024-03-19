import discord
import os
import asyncio
import datetime
from datetime import date
import matplotlib.pyplot as plt
import numpy as np

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from database import dbaccess
from embeds import embeds

GUILD = int(os.environ.get('NOTIFYGUILDID'))
NEWMEMBERROLE = int(os.environ.get('NEWMEMBERROLE'))
STAFFMODCHANNEL = int(os.environ.get('STAFFMODCHANNEL'))

Client = None

# Sets client var on bot start
async def set_vars(c):
    global Client

    Client = c

# Generates the graphs and saves it
async def graph(N, height1, height2, height3, tick_label, final_directory, end_directory):
    ind = np.arange(N)
    width = 0.25

    fig = plt.figure(facecolor = "white", figsize = (21,9), dpi = 300)
    #subplot to allow multiple plots
    ax = fig.add_subplot(111)
    ax2 = ax.twinx()
    #all 3 sets of data into one plot (msg,word,char)
    first = ax2.bar(ind, height1, width, color = ['aqua'])
    second = ax.bar(ind+width, height2, width, color = ['lightgreen'])
    third = ax.bar(ind+width+width, height3, width, color = ['fuchsia'])

    #formatting stuff for the graph
    ax.set_ylabel('Word/Char Totals')
    ax2.set_ylabel('Msg Totals')
    ax.set_title('Category Interaction Graph')
    ax.set_xticks(ind + width / 3)
    ax.set_xticklabels(tick_label)
    ax.legend( (first[0], second[0], third[0]),("Tot Msgs", "Tot Words", "Tot Chars"),loc='upper center', bbox_to_anchor=(1,-0.1) )
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.set_facecolor("black")
    #rotates the names 45 and changes font 
    fig.autofmt_xdate(rotation = 45)
    #fits everything to the borders
    fig.tight_layout()

    plt.savefig(final_directory + end_directory)

async def fetch_data(category_name):
    query = f"SELECT * FROM {category_name}"
    records = await dbaccess.get_data(query, None)
    ids, msgs, words, chars = [], [], [], []
    for row in records:
        ids.append(row[0])
        msgs.append(row[2])
        words.append(row[3])
        chars.append(row[4])
    return ids, msgs, words, chars

async def fetch_user_names(ids, client):
    names = []
    for i in ids:
        user = await client.fetch_user(i)
        names.append(user.name)
    return names

async def export_data_to_csv(ids, msgs, words, chars, names, category_name, final_directory):
    await graph(len(ids), msgs, words, chars, names, final_directory, f'/{category_name}/graph.png')
    csv_filename = f'{final_directory}/{category_name}/csv.csv'
    query = f"SELECT * FROM {category_name}"
    records = await dbaccess.get_data(query, None)
    column_names = ['nameid', 'name', 'msgcount', 'wordcount', 'charcount', 'engage']

    if records:
        # Write column headers to the CSV file
        with open(csv_filename, 'w') as csv_file:
            csv_file.write(",".join(column_names) + "\n")
        # Write data rows to the CSV file
        with open(csv_filename, 'a') as csv_file:
            for row in records:
                csv_file.write(",".join(map(str, row)) + "\n")
    else:
        print("Error with exporting to csv.")

async def get_current_month():
    query = "SELECT * FROM datetracker WHERE scriptid = 1"
    records = await dbaccess.get_data(query, None)
    for row in records:
        if row[0] == 1:
            return row[1]
    return 0  # Return 0 if no record found

async def text_data(msg):
    msgstring = msg.content
    words = len(msgstring.split())
    msgstring = msgstring.replace(" ", "")
    msgstring = msgstring.replace("\n", "")
    chars = len(msgstring)

    return  words, chars

async def readwrite(stringtable, auth, a, count, words, chars, engage):
    query = f"SELECT * FROM {stringtable} WHERE nameid = %s"
    records = await dbaccess.get_data(query, (auth,))

    for row in records:
        if row[0] == auth:
            count += row[2]
            words += row[3]
            chars += row[4]

    query = f"INSERT INTO {stringtable} (nameid, name, msgcount, wordcount, charcount, engage) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (nameid) DO UPDATE set (name, msgcount, wordcount, charcount, engage) = (EXCLUDED.name, EXCLUDED.msgcount, EXCLUDED.wordcount, EXCLUDED.charcount, EXCLUDED.engage)"
    data = (auth, str(a), count, words, chars, engage)
    await dbaccess.write_data(query, data)