import io
import logging
import asyncio
from typing import List
import discord
from discord.ui import Button, View
import pandas as pd
import datetime

from database import dbaccess

Client = None

# Sets client var on bot start
async def set_vars(c):
    global Client

    Client = c

#############################################################
# Used to get the survey data given some input parameters
#############################################################
async def generate_survey_report(
    interaction: discord.Interaction,
    query: str,
    column_names: List[str],
    filename: str,
    extra_fields: str = None,
):
    try:
        df, total_rows = await dbaccess.get_data_as_dataframe(query)

        if len(df) == 0:
            await interaction.response.send_message("No survey data available.")
            return

        df.columns = column_names

        df_sorted = df.sort_values(by="Time")

        q2avg = df_sorted['Q2'].mean()
        q3avg = df_sorted['Q3'].mean()
        q4avg = df_sorted['Q4'].mean()
        countq1 = df_sorted['Q1'].ne("Redacted").sum()
        countq5 = df_sorted['Q5'].str.lower().isin(["na", "nothing"]).sum()
        rowcount = len(df_sorted)

        ratio = len(df_sorted) / total_rows * 100

        header = column_names
        buffer = io.StringIO()
        df_sorted.to_csv(buffer, index=False, header=header)

        embed = discord.Embed(title="Survey Summary", description="See below for a brief summary.", color=0xDB0B23)
        embed.add_field(name="Total surveys completed compared to tickets opened.", value=f"`{len(df_sorted)}/{total_rows}` Totalling {ratio:.2f}% of tickets.", inline=False)
        embed.add_field(name="Q1: Are you fine with sharing your name for this survey?", value=f"`{countq1}/{len(df_sorted)}` Gave their name.", inline=False)
        embed.add_field(name="Q2: How would you rate the speed of the support you received?", value=f"`{q2avg:.2f}` Was the average score of {len(df_sorted)} responses.", inline=False)
        embed.add_field(name="Q3: How would you rate the quality of the info received?", value=f"`{q3avg:.2f}` Was the average score of {len(df_sorted)} responses.", inline=False)
        embed.add_field(name="Q4: How likely are you to renew your Notify subscription?", value=f"`{q4avg:.2f}` Was the average score of {len(df_sorted)} responses.", inline=False)
        if extra_fields:
            embed.add_field(name="Q5: If you would like to commend a staff member for their assistance please write their name now.", value=f"`{len(df_sorted)-countq5}/{len(df_sorted)}` Gave staff commendations.", inline=False)
            countq6 = df_sorted['Q6'].str.lower().isin(["na", "nothing"]).sum()
            embed.add_field(name=extra_fields, value=f"`{len(df_sorted)-countq6}/{len(df_sorted)}` Suggested Improvements.", inline=False)
        else:
            embed.add_field(name="Q5: Is there anything you feel we can improve on regarding support?", value=f"`{len(df_sorted)-countq5}/{len(df_sorted)}` Suggested Improvements.", inline=False)

        await interaction.response.send_message(embed=embed)
        await interaction.channel.send(file=discord.File(io.BytesIO(buffer.getvalue().encode()), filename))
    except Exception as e:
        logging.error(f"Error in generating survey report: {e}")
        await interaction.response.send_message("An error occurred while processing the survey report.")

#############################################################
# Used to send the survey to the member of the closed ticket
#############################################################
async def send_survey(uid, GUILD, tickType):
    if uid and uid != "Nothing":
        try:
            u = int(uid)
        except ValueError:
            print("Invalid UID format:", uid)
            return
            
        if GUILD.get_member(u) is not None:
            user = GUILD.get_member(u)

            print("Member element: " + str(user) + ", DM attempt")

            try:
                await user.send("**Please help us improve our support by giving feedback.** \nIt will take just 30 seconds. Survey expires after 24 hours.")
                print("DM sent")
            except Exception as e:
                print("User cannot be DM'd.")
                print(e)
                return

            if tickType == 0:
                await initial_func(user, tickType)
            else:
                await initial_func(user, tickType)
        else:
            print("member is not in Notify anymore.")
    else:
        print("ticket made when bot/survey was not setup.")

#############################################################
# Classes and functions for survey flow
#############################################################
async def initial_func(user, tickType):
    view = SurveyViewMain(tickType)
    await user.send("**Question 1:** \nAre you fine with sharing your name for this survey?", view=view)

class SurveyViewMain(View):
    def __init__(self, tickType):
        super().__init__(timeout=86400)
        self.tickType = tickType

        if self.tickType == 0:
            self.query1 = "select * from ticketsurvey where name = %s"
            self.query2 = "INSERT INTO ticketsurvey (id, name, q1) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q1 = EXCLUDED.q1"
        else:
            self.query1 = "select * from ticketsurveywelcomes where name = %s"
            self.query2 = "INSERT INTO ticketsurveywelcomes (id, name, q1) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q1 = EXCLUDED.q1"

        self.question_2 = "**Question 2:** \nHow would you rate the speed of the support you received, with 1 being terrible and 5 being great?"

    # Define Buttons
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="Yes")
    async def yes_callback(self, interaction, button):
        view = SurveyViewSecond(self.tickType)
        await interaction.user.send(self.question_2, view=view)
        await interaction.response.edit_message(view = None)
    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="No")
    async def no_callback(self, interaction, button):
        await dbaccess.write_to_db(self.query1, self.query2, "Redacted", (str(interaction.user.id),))
        view = SurveyViewSecond(self.tickType)
        await interaction.user.send(self.question_2, view=view)
        await interaction.response.edit_message(view = None)

class SurveyViewSecond(View):
    def __init__(self, tickType):
        super().__init__(timeout=86400)
        self.tickType = tickType

        if self.tickType == 0:
            self.query1 = "select * from ticketsurvey where name = %s"
            self.query2 = "INSERT INTO ticketsurvey (id, name, q2) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q2 = EXCLUDED.q2"
        else:
            self.query1 = "select * from ticketsurveywelcomes where name = %s"
            self.query2 = "INSERT INTO ticketsurveywelcomes (id, name, q2) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q2 = EXCLUDED.q2"

        self.question_3 = "**Question 3:** \nHow would you rate the quality of the info received, with 1 being terrible and 5 being great?"

    @discord.ui.button(label="1", style=discord.ButtonStyle.grey, custom_id="q2_1")
    async def one_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 1)
    @discord.ui.button(label="2", style=discord.ButtonStyle.grey, custom_id="q2_2")
    async def two_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 2)
    @discord.ui.button(label="3", style=discord.ButtonStyle.grey, custom_id="q2_3")
    async def three_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 3)
    @discord.ui.button(label="4", style=discord.ButtonStyle.grey, custom_id="q2_4")
    async def four_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 4)
    @discord.ui.button(label="5", style=discord.ButtonStyle.grey, custom_id="q2_5")
    async def five_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 5)

    async def manage_callbacks(self, interaction, rating):
        await dbaccess.write_to_db(self.query1, self.query2, rating, (str(interaction.user.id),))
        view = SurveyViewThird(self.tickType)
        await interaction.user.send(self.question_3, view = view)
        await interaction.response.edit_message(view = None)

class SurveyViewThird(View):
    def __init__(self, tickType):
        super().__init__(timeout=86400)
        self.tickType = tickType

        if self.tickType == 0:
            self.query1 = "select * from ticketsurvey where name = %s"
            self.query2 = "INSERT INTO ticketsurvey (id, name, q3) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q3 = EXCLUDED.q3"
        else:
            self.query1 = "select * from ticketsurveywelcomes where name = %s"
            self.query2 = "INSERT INTO ticketsurveywelcomes (id, name, q3) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q3 = EXCLUDED.q3"
        
        self.question_4 = "**Question 4:** \nHow likely are you to renew your Notify subscription, with 1 being very unlikely and 5 being very likely?"

    @discord.ui.button(label="1", style=discord.ButtonStyle.grey, custom_id="q3_1")
    async def one_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 1)
    @discord.ui.button(label="2", style=discord.ButtonStyle.grey, custom_id="q3_2")
    async def two_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 2)
    @discord.ui.button(label="3", style=discord.ButtonStyle.grey, custom_id="q3_3")
    async def three_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 3)
    @discord.ui.button(label="4", style=discord.ButtonStyle.grey, custom_id="q3_4")
    async def four_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 4)
    @discord.ui.button(label="5", style=discord.ButtonStyle.grey, custom_id="q3_5")
    async def five_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 5)

    async def manage_callbacks(self, interaction, rating):
        await dbaccess.write_to_db(self.query1, self.query2, rating, (str(interaction.user.id),))
        view = SurveyViewFourth(self.tickType)
        await interaction.user.send(self.question_4, view = view)
        await interaction.response.edit_message(view = None)

class SurveyViewFourth(View):
    def __init__(self, tickType):
        super().__init__(timeout=86400)
        self.tickType = tickType

        if self.tickType == 0:
            self.query1 = "select * from ticketsurvey where name = %s"
            self.query2 = "INSERT INTO ticketsurvey (id, name, q4) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q4 = EXCLUDED.q4"
        else:
            self.query1 = "select * from ticketsurveywelcomes where name = %s"
            self.query2 = "INSERT INTO ticketsurveywelcomes (id, name, q4) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q4 = EXCLUDED.q4"

    @discord.ui.button(label="1", style=discord.ButtonStyle.grey, custom_id="q4_1")
    async def one_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 1)
    @discord.ui.button(label="2", style=discord.ButtonStyle.grey, custom_id="q4_2")
    async def two_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 2)
    @discord.ui.button(label="3", style=discord.ButtonStyle.grey, custom_id="q4_3")
    async def three_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 3)
    @discord.ui.button(label="4", style=discord.ButtonStyle.grey, custom_id="q4_4")
    async def four_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 4)
    @discord.ui.button(label="5", style=discord.ButtonStyle.grey, custom_id="q4_5")
    async def five_callback(self, interaction, button):
        await self.manage_callbacks(interaction, 5)

    async def manage_callbacks(self, interaction, rating):
        await dbaccess.write_to_db(self.query1, self.query2, rating, (str(interaction.user.id),))
        await interaction.response.edit_message(view = None)

        user = interaction.user
        userID = interaction.user.id
        # Last two question answers
        def check(m):
            return user == m.author and isinstance(m.channel, discord.DMChannel)

        if self.tickType == 0:
            query5_1 = "select * from ticketsurvey where name = %s"
            query5_2 = "INSERT INTO ticketsurvey (id, name, q5) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q5 = EXCLUDED.q5"

            query6_1 = "select * from ticketsurvey where name = %s"
            query6_2 = "INSERT INTO ticketsurvey (id, name, q6) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q6 = EXCLUDED.q6"

            query6_1_time = "select * from ticketsurvey where name = %s"
            query6_2_time = "INSERT INTO ticketsurvey (id, name, timefinished) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set timefinished = EXCLUDED.timefinished"
        else:
            query5_1_welcome = "select * from ticketsurveywelcomes where name = %s"
            query5_2_welcome = "INSERT INTO ticketsurveywelcomes (id, name, q5) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set q5 = EXCLUDED.q5"

            query6_1_time = "select * from ticketsurvey where name = %s"
            query6_2_time = "INSERT INTO ticketsurvey (id, name, timefinished) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE set timefinished = EXCLUDED.timefinished"

        if self.tickType == 0:
            await user.send("**Question 5:** \nIf you would like to commend a staff member for their assistance please write their name now (if not just type NA).")
            try:
                q5 = await Client.wait_for("message", timeout = 300, check = check)
            except asyncio.TimeoutError:
                await dbaccess.write_to_db(query5_1, query5_2, "NA", (str(userID),))
                await user.send("Didn't get an input, so moving to the last question.")
            else:
                await dbaccess.write_to_db(query5_1, query5_2, q5.content, (str(userID),))

        if self.tickType == 0:
            await user.send("**Question 6:** \nIs there anything you feel we can improve on regarding support? (if not just type NA).")
            try:
                q6 = await Client.wait_for("message", timeout = 300, check = check)
            except asyncio.TimeoutError:
                await dbaccess.write_to_db(query6_1, query6_2, "NA", (str(userID),))
                await user.send("Didn't get an input.")
                t = str(datetime.datetime.now())
                await dbaccess.write_to_db(query6_1_time, query6_2_time, t, (str(userID),))
                query = "UPDATE ticketsurvey SET name = %s WHERE name = %s"
                data = ("Survey Completed", str(userID))
                await dbaccess.write_data(query, data)
                await user.send("Thanks for taking part in the feedback form!")
            else:
                await dbaccess.write_to_db(query6_1, query6_2, q6.content, (str(userID),))
                t = str(datetime.datetime.now())
                await dbaccess.write_to_db(query6_1_time, query6_2_time, t, (str(userID),))
                query = "UPDATE ticketsurvey SET name = %s WHERE name = %s"
                data = ("Survey Completed", str(userID))
                await dbaccess.write_data(query, data)
                await user.send("Thanks for taking part in the feedback form!")
        else:
            await user.send("**Question 5:** \nIs there anything you feel we can improve on regarding support? (if not just type NA).")
            try:
                q6 = await Client.wait_for("message", timeout = 300, check = check)
            except asyncio.TimeoutError:
                await dbaccess.write_to_db(query5_1_welcome, query5_2_welcome, "NA", (str(userID),))
                await user.send("Didn't get an input.")
                t = str(datetime.datetime.now())
                await dbaccess.write_to_db(query6_1_time, query6_2_time, t, (str(userID),))
                query = "UPDATE ticketsurveywelcomes SET name = %s WHERE name = %s"
                data = ("Survey Completed", str(userID))
                await dbaccess.write_data(query, data)
                await user.send("Thanks for taking part in the feedback form!")
            else:
                await dbaccess.write_to_db(query5_1_welcome, query5_2_welcome, q6.content, (str(userID),))
                t = str(datetime.datetime.now())
                await dbaccess.write_to_db(query6_1_time, query6_2_time, t, (str(userID),))
                query = "UPDATE ticketsurveywelcomes SET name = %s WHERE name = %s"
                data = ("Survey Completed", str(userID))
                await dbaccess.write_data(query, data)
                await user.send("Thanks for taking part in the feedback form!")