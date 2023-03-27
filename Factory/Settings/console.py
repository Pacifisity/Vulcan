import discord

from Factory.Settings.data import Data

class Console(discord.ui.View):
    def __init__(self, data: Data):
        self.data = data
        super().__init__(timeout = None)

        # Embed
        self.embed = discord.Embed()

        # Buttons
        self.back_to_main_button = discord.ui.Button(label="Back")
        self.bets_button = discord.ui.Button(label="Bets")
        self.deposit_button = discord.ui.Button(label="Deposits")
        self.withdrawal_button = discord.ui.Button(label="Withdrawals")

        # Modal
        self.modals = Modals()

        # Modifiers
        self.modifiers = Modifiers(self.embed, self.data)

class Modifiers:
    def __init__(self, embed: discord.Embed, data: Data):
        self.data = data
        self.embed = embed
        self.embed.color = 0x800080

    def Main_Console(self):
        self.embed.title = "Channel Settings"
        self.embed.description = "**DO NOT CLICK ANY BUTTONS WITHOUT READING**\n\nThe buttons below will automatically set whichever channel this command was sent in to have the logic relating to specific things.\n• Bet - This will make all /bet entries be sent to this channel\n• Deposit - this will make all deposit requests be sent to this channel\n• Withdrawal - This will make all withdrawal requests be sent to this channel\n\nP.S. You can set 1 channel to have multiple such as deposit/withdrawal, up to you."

    def Bets_Console(self):
        self.embed.title = "Bets Channel Set"
        self.embed.description = "All future bets will be sent to this channel"

    def Deposit_Console(self):
        self.embed.title = "Deposit Channel Set"
        self.embed.description = "All future deposit requests will be sent to this channel"

    def Withdrawal_Console(self):
        self.embed.title = "Withdrawal Channel Set"
        self.embed.description = "All future withdrawal requests will be sent to this channel"

class Modals:
    pass