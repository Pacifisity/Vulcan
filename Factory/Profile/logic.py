import discord

from Factory.Profile.data import Data
from Factory.Profile.console import Console

class Logic:
    def __init__(self, interaction: discord.Interaction):
        # Inheritance
        self.data = Data(interaction)
        self.console = Console(self.data)
        self.embed = self.console.embed

        # Database Vars
        self.db = self.data.db
        self.cursor = self.data.cursor

        # Button Logic
        self.buttons = Buttons(self.data, self.console)
        self.console.back_to_main_button.callback = self.buttons.Main_Console_Callback
        self.console.bets_button.callback = self.buttons.Bets_Console_Callback
        self.console.deposit_button.callback = self.buttons.Deposit_Console_Callback
        self.console.withdrawal_button.callback = self.buttons.Withdrawal_Console_Callback
        self.console.deposit_2_button.callback = self.buttons.Deposit_2_Callback
        self.console.withdrawal_2_button.callback = self.buttons.Withdrawal_2_Callback
        self.console.confirm_deposit_button.callback = self.buttons.Confirm_Deposit_Callback
        self.console.confirm_withdrawal_button.callback = self.buttons.Confirm_Withdrawal_Callback
        self.console.registration_button.callback = self.buttons.Registration_Callback

        # Modal Logic
        self.modals = Modals(self.data, self.console)
        self.console.deposit_modal.on_submit = self.modals.Deposit_Callback
        self.console.withdrawal_modal.on_submit = self.modals.Withdrawal_Callback
        self.console.registration_modal.on_submit = self.modals.Registration_Modal_Callback

        # Init Profile

        if self.data.not_registered(self.data.user):
            self.console.modifiers.Registration_Console()
            self.console.add_item(self.console.registration_button)
        else:
            self.console.modifiers.Main_Console()
            self.console.add_item(self.console.bets_button)
            self.console.add_item(self.console.deposit_button)
            self.console.add_item(self.console.withdrawal_button)


class Buttons():
    def __init__(self, data: Data, console: Console):
        self.data = data
        self.console = console
        self.embed = console.embed

    async def Main_Console_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        self.console.modifiers.Main_Console()
        self.console.add_item(self.console.bets_button)
        self.console.add_item(self.console.deposit_button)
        self.console.add_item(self.console.withdrawal_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Bets_Console_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        self.console.modifiers.Bets_Console()
        self.console.add_item(self.console.back_to_main_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Deposit_Console_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        self.console.modifiers.Deposit_Console()
        self.console.add_item(self.console.back_to_main_button)
        self.console.add_item(self.console.deposit_2_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Withdrawal_Console_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        self.console.modifiers.Withdrawal_Console()
        self.console.add_item(self.console.back_to_main_button)
        self.console.add_item(self.console.withdrawal_2_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Deposit_2_Callback(self, interaction: discord.Interaction):

        await interaction.response.send_modal(self.console.deposit_modal)

    async def Withdrawal_2_Callback(self, interaction: discord.Interaction):

        await interaction.response.send_modal(self.console.withdrawal_modal)

    async def Confirm_Deposit_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if interaction.user.guild_permissions.administrator:
            self.data.cursor.execute("SELECT galleons FROM players WHERE id = ?", (self.data.user.id,))
            old_galleons = self.data.cursor.fetchone()

            new_galleons = old_galleons[0] + int(self.data.amount)
            self.data.cursor.execute("UPDATE players SET galleons = ? WHERE id = ?", (new_galleons, self.data.user.id))
            self.data.db.commit()
            
            self.console.modifiers.Confirmation_Complete_Console()
            await interaction.response.edit_message(embed=self.embed, view=self.console)
        else:
            self.console.modifiers.Insufficient_Permissions()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)
        
    async def Confirm_Withdrawal_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()
        if interaction.user.guild_permissions.administrator:
            self.data.cursor.execute("SELECT galleons FROM players WHERE id = ?", (self.data.user.id,))
            old_galleons = self.data.cursor.fetchone()

            new_galleons = old_galleons[0] - int(self.data.amount)
            self.data.cursor.execute("UPDATE players SET galleons = ? WHERE id = ?", (new_galleons, self.data.user.id))
            self.data.db.commit()

            self.console.modifiers.Confirmation_Complete_Console()
            await interaction.response.edit_message(embed=self.embed, view=self.console)
        else:
            self.console.modifiers.Insufficient_Permissions()
            await interaction.response.send_message(embed=self.embed, view=self.console, ephemeral=True)


    async def Registration_Callback(self, interaction: discord.Interaction):

        await interaction.response.send_modal(self.console.registration_modal)
        

class Modals():
    def __init__(self, data: Data, console: Console):
        self.data = data
        self.console = console
        self.embed = console.embed

    async def Deposit_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        self.data.amount = interaction.data["components"][0]["components"][0]["value"]
        self.data.info = interaction.data["components"][1]["components"][0]["value"]

        self.data.cursor.execute("SELECT deposit_requests_id FROM settings WHERE guild_id = ?", (interaction.guild.id,))
        deposit_requests_id = self.data.cursor.fetchone()

        if deposit_requests_id == None:
            self.console.modifiers.Request_Failed()
            await interaction.response.send_message(embed=self.embed, view=self.console)
            return
        else:
            deposit_requests_id = deposit_requests_id[0]
            channel = discord.utils.get(interaction.guild.channels, id=deposit_requests_id)
            self.console.modifiers.Deposit_Request_Console()
            self.console.add_item(self.console.confirm_deposit_button)
            await channel.send(embed=self.embed, view=self.console)

        self.console.modifiers.Deposit_Confirmation_Console()
        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Withdrawal_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        self.data.amount = interaction.data["components"][0]["components"][0]["value"]
        self.data.info = interaction.data["components"][1]["components"][0]["value"]

        self.data.cursor.execute("SELECT withdrawal_requests_id FROM settings WHERE guild_id = ?", (interaction.guild.id,))
        withdrawal_requests_id = self.data.cursor.fetchone()

        if withdrawal_requests_id == None:
            self.console.modifiers.Request_Failed()
            await interaction.response.edit_message(embed=self.embed, view=self.console)
            return
        elif int(self.data.amount) > self.data.galleons:
            self.console.modifiers.Overdrawn_Console()
            await interaction.response.edit_message(embed=self.embed, view=self.console)
            return
        else:
            withdrawal_requests_id = withdrawal_requests_id[0]
            channel = discord.utils.get(interaction.guild.channels, id=withdrawal_requests_id)
            self.console.modifiers.Withdrawal_Request_Console()
            self.console.add_item(self.console.confirm_withdrawal_button)
            await channel.send(embed=self.embed, view=self.console)

        self.console.modifiers.Withdrawal_Confirmation_Console()
        self.console.clear_items()
        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Registration_Modal_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        roblox_user = interaction.data["components"][0]["components"][0]["value"]
        self.data.register_player(interaction.user, roblox_user)

        self.console.modifiers.Main_Console()
        self.console.add_item(self.console.bets_button)
        self.console.add_item(self.console.deposit_button)
        self.console.add_item(self.console.withdrawal_button)
        await interaction.response.edit_message(embed=self.embed, view=self.console)
    
    