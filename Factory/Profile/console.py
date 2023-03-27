import discord

from Factory.Profile.data import Data

class Console(discord.ui.View):
    def __init__(self, data: Data):
        self.data = data
        super().__init__(timeout = None)

        # Embed
        self.embed = discord.Embed()

        # Buttons
        self.bets_button = discord.ui.Button(label="Ongoing Bets")
        self.deposit_button = discord.ui.Button(label="Deposit")
        self.withdrawal_button = discord.ui.Button(label="Withdrawal")
        self.deposit_2_button = discord.ui.Button(label="Deposit")
        self.withdrawal_2_button = discord.ui.Button(label="Withdrawal")
        self.back_to_main_button = discord.ui.Button(label="Back")
        self.confirm_deposit_button = discord.ui.Button(label="Confirm Deposit")
        self.confirm_withdrawal_button = discord.ui.Button(label="Confirm Withdrawal")
        self.registration_button = discord.ui.Button(label="Register")

        # Modal
        self.modals = Modals(data)
        self.withdrawal_modal = self.modals.Withdrawal_Modal()
        self.deposit_modal = self.modals.Deposit_Modal()
        self.registration_modal = self.modals.Registration_Modal()

        # Modifiers
        self.modifiers = Modifiers(self.embed, self.data)

class Modifiers:
    def __init__(self, embed: discord.Embed, data: Data):
        self.data = data
        self.embed = embed
        self.embed.color = 0x800080

    def Main_Console(self):
        self.embed.title = "Profile"
        self.embed.description = f"**Username**: {self.data.roblox_user}\n**Galleons**: {self.data.galleons}"

    def Bets_Console(self):
        self.embed.title = "Ongoing Bets"
        self.embed.description = self.data.user_participated_bets

    def Deposit_Console(self):
        self.embed.title = "Deposit"
        self.embed.description = "Click the button below and give us a number of galleons you'd like to deposit so that staff can help you when they have time. Also let us know what times you are on or other useful information as staff may not be able to get to you instantly, rest assured that we will help you as soon as we have time!"

    def Withdrawal_Console(self):
        self.embed.title = "Withdrawal"
        self.embed.description = "Click the button below and give us a number of galleons you'd like to withdrawal so that staff can help you when they have time. Also let us know what times you are on or other useful information as staff may not be able to get to you instantly, rest assured that we will help you as soon as we have time!"

    def Deposit_Confirmation_Console(self):
        self.embed.title = "Deposit Request Sent!"
        self.embed.description = "Please wait, rest assured that we will help you as soon as we have time!"

    def Withdrawal_Confirmation_Console(self):
        self.embed.title = "Withdrawal Request Sent!"
        self.embed.description = "Please wait, rest assured that we will help you as soon as we have time!"

    def Request_Failed(self):
        self.embed.title = "Request Failed"
        self.embed.description = f"Please notify staff that there is a problem with the channel id settings"

    def Insufficient_Permissions(self):
        self.embed.title = "Insufficient Permissions"
        self.embed.description = f"You need to be an administrator to use this feature."

    def Deposit_Request_Console(self):
        self.embed.title = "Deposit Request"
        self.embed.description = f"{self.data.interaction.user.mention} has requested to deposit {self.data.amount} galleons into their profile.\nUsername: {self.data.roblox_user}\n\n**Info**:\n{self.data.info}"

    def Withdrawal_Request_Console(self):
        self.embed.title = "Withdrawal Request"
        self.embed.description = f"{self.data.interaction.user.mention} has requested to withdrawal {self.data.amount} galleons from their profile.\nUsername: {self.data.roblox_user}\n\n**Info**:\n{self.data.info}"
        
    def Confirmation_Complete_Console(self):
        self.embed.title = "Confirmation Complete"
        self.embed.description = f"The request has been completed and {self.data.user.mention}'s galleons have been modified."
        
    def Registration_Console(self):
        self.embed.title = "Register"
        self.embed.description = f"You're new here? Welcome to Vulcan Tournaments, i'm your handy dandy gambling bot here to make you gamble away you hard earned money! Click below to let me know who you are."

    def Overdrawn_Console(self):
        self.embed.title = "Insufficient Galleons"
        self.embed.description = "You can't withdrawal more galleons than you have"
        
class Modals:
    def __init__(self, data: Data):
        self.data = data

    def Deposit_Modal(self):
        modal = discord.ui.Modal(title="Deposit")

        modal.add_item(discord.ui.TextInput(label="Amount:", min_length=1, max_length=5))
        modal.add_item(discord.ui.TextInput(label="Info:", required=False, style=discord.TextStyle.long))

        return modal
    
    def Withdrawal_Modal(self):
        modal = discord.ui.Modal(title="Withdrawal")

        modal.add_item(discord.ui.TextInput(label="Amount:", min_length=1, max_length=5))
        modal.add_item(discord.ui.TextInput(label="Info:", required=False, style=discord.TextStyle.long))

        return modal
    
    def Registration_Modal(self):
        modal = discord.ui.Modal(title="Register")

        modal.add_item(discord.ui.TextInput(label="Roblox Username:", min_length=3, max_length=20))

        return modal
    