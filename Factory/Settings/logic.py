import discord

from Factory.Settings.data import Data
from Factory.Settings.console import Console

from Factory.utils import all_different

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
        self.console.bets_button.callback = self.buttons.Bets_Setting_Callback
        self.console.deposit_button.callback = self.buttons.Deposit_Requests_Callback
        self.console.withdrawal_button.callback = self.buttons.Withdrawal_Requests_Callback

        # Modal Logic
        self.modals = Modals(self.data, self.console)

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

    async def Bets_Setting_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        # Channel set logic
        self.data.cursor.execute("UPDATE settings SET bets_channel_id = ? WHERE guild_id = ?", (interaction.channel.id, interaction.guild.id))
        self.data.db.commit()

        self.console.modifiers.Bets_Console()
        self.console.add_item(self.console.back_to_main_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Deposit_Requests_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        # Channel set logic
        self.data.cursor.execute("UPDATE settings SET deposit_requests_id = ? WHERE guild_id = ?", (interaction.channel.id, interaction.guild.id))
        self.data.db.commit()

        self.console.modifiers.Deposit_Console()
        self.console.add_item(self.console.back_to_main_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

    async def Withdrawal_Requests_Callback(self, interaction: discord.Interaction):
        self.console.clear_items()

        # Channel set logic
        self.data.cursor.execute("UPDATE settings SET withdrawal_requests_id = ? WHERE guild_id = ?", (interaction.channel.id, interaction.guild.id))
        self.data.db.commit()

        self.console.modifiers.Withdrawal_Console()
        self.console.add_item(self.console.back_to_main_button)

        await interaction.response.edit_message(embed=self.embed, view=self.console)

class Modals():
    def __init__(self, data: Data, console: Console):
        self.data = data
        self.console = console
        self.embed = console.embed