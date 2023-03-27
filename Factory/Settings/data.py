import discord
import sqlite3

from datetime import datetime

class Data:
    def __init__(self, interaction: discord.Interaction):
        self.timestamp = round(datetime.now().timestamp())
        self.interaction = interaction
        self.host = interaction.user

        self.db = sqlite3.connect("vulcan.db")
        self.cursor = self.db.cursor()