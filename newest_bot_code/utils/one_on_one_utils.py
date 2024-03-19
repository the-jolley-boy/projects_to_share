import discord
from discord.ui import Button, View
import asyncio
import functools

from global_vars.global_vars import GlobalVariables
from database import dbaccess
from embeds import embeds

async def get_all_values():
    users_data = {}

    query = "select * from oneonone"

    records = await dbaccess.get_data(query, None)

    for row in records:
        user_id = row[0]
        user_data = {
            "remaining": row[2],
            "calendar": row[3],
            "description_sneakers": row[4] if len(row) > 4 else None
        }
        users_data[user_id] = user_data

    return users_data

async def initial_func(ch):
    embedVar = await embeds.advisor_initial()
    view = AdvisorMain()
    await ch.send(embed=embedVar, view=view)

class AdvisorMain(View):
    def __init__(self):
        super().__init__(timeout=None)

    # Define Buttons
    @discord.ui.button(label = "Sneakers", style = discord.ButtonStyle.grey, emoji = "👟", custom_id="sneakers")
    async def sneakers_callback(self, interaction, button):
        await interaction.response.edit_message(view = None)
        embedVar, embedVar1 = await embeds.advisor_sneaker()
        view = StaffView(0)
        await interaction.channel.send(embed=embedVar)
        await interaction.channel.send(embed=embedVar1, view=view)
    @discord.ui.button(label = "Flips", style = discord.ButtonStyle.grey, emoji = "⚡", custom_id="flips")
    async def flips_callback(self, interaction, button):
        await interaction.response.edit_message(view = None)
        embedVar = await embeds.advisor_flips()
        view = StaffView(1)
        await interaction.channel.send(embed=embedVar, view=view)
    @discord.ui.button(label = "Amazon FBA/Freebies", style = discord.ButtonStyle.grey, emoji = "📦", custom_id="amazon")
    async def amazon_callback(self, interaction, button):
        await interaction.response.edit_message(view = None)
        embedVar = await embeds.advisor_amazon()
        view = StaffView(2)
        await interaction.channel.send(embed=embedVar, view=view)
    @discord.ui.button(label = "Sports Betting", style = discord.ButtonStyle.grey, emoji = "🥇", custom_id="sports")
    async def sports_betting_callback(self, interaction, button):
        await interaction.response.edit_message(view = None)
        embedVar = await embeds.advisor_sports()
        view = StaffView(3)
        await interaction.channel.send(embed=embedVar, view=view)
    @discord.ui.button(label = "General/Other", style = discord.ButtonStyle.grey, emoji = "💸", custom_id="general")
    async def general_callback(self, interaction, button):
        await interaction.response.edit_message(view = None)
        embedVar = await embeds.advisor_general()
        view = StaffView(4)
        await interaction.channel.send(embed=embedVar, view=view)

class StaffView(View):
    def __init__(self, category):
        super().__init__(timeout=None)
        self.category = category

        self.matching_ids = []
        for user_id, session_info in GlobalVariables().staff_session_types.items():
            if session_info[self.category] == 1 and GlobalVariables().advisorDict[user_id]["remaining"] != 0:
                self.matching_ids.append(user_id)

        for user_id in self.matching_ids:
            member_name = GlobalVariables().id_to_member[user_id]
            button = discord.ui.Button(
                label=member_name,
                style=discord.ButtonStyle.grey,
                emoji=GlobalVariables().staff_emotes[member_name],
                custom_id=member_name
            )
            button.callback = functools.partial(self.handle_callback, user_id=user_id)
            self.add_item(button)

        button = discord.ui.Button(
            style = discord.ButtonStyle.red,
            label = "Restart",
            custom_id="restart"
        )
        button.callback = self.restart_callback
        self.add_item(button)

    async def handle_callback(self, interaction, user_id):
        member_name = GlobalVariables().id_to_member[user_id]
        remaining = GlobalVariables().advisorDict[user_id]["remaining"]
        await interaction.response.send_message(f"{GlobalVariables().staff_pings[member_name]} Will be with you shortly.\n\nPlease fill this out now: {GlobalVariables().advisorDict[user_id]['calendar']} and let your coach know when you have finished.\n\nMake sure to schedule it at least 48 hours from now.\n\nIf the advisor has a full schedule, feel free to choose someone else.")
        GlobalVariables().advisorDict[user_id]["remaining"] = remaining - 1
        query = "UPDATE oneonone set sessions = %s WHERE id = %s"
        await dbaccess.write_data(query, (remaining - 1, user_id))

    async def restart_callback(self, interaction):
        await interaction.response.edit_message(view = None)
        embedVar = await embeds.advisor_initial()
        view = AdvisorMain()
        await interaction.channel.send(embed=embedVar, view=view)