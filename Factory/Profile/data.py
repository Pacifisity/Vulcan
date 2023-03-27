import discord
import sqlite3

from datetime import datetime

class Data:
    def __init__(self, interaction: discord.Interaction):
        self.timestamp = round(datetime.now().timestamp())
        self.interaction = interaction
        self.user = interaction.user

        self.db = sqlite3.connect("vulcan.db")
        self.cursor = self.db.cursor()

        self.user_participated_bets = ""

        self.roblox_user, self.galleons = self.get_user_info(interaction.user)
        self.bets = self.get_user_bets(interaction.user)
        self.amount = 0
        self.info = ""

    def get_user_info(self, member: discord.Member):
        self.cursor.execute("SELECT roblox_user, galleons FROM players WHERE id = ?", (member.id,))
        data = self.cursor.fetchone()

        if data == None:
            return None, None
        else:
            return data
    
    def get_user_bets(self, member: discord.Member):
        self.cursor.execute("SELECT name, bets_made FROM bets")
        bets = self.cursor.fetchall()

        # Loop through each bet
        for bet in bets:
            bet_name, bets_made = bet

            if bets_made == None:
                bets_made = ""

            # If the user has participated in the bet
            if str(member.id) in bets_made:

                # Get the different entries in the bet
                entries = bets_made.split("|")

                # Check if the entry is the user's
                for entry in entries:
                    if str(member.id) in entry:

                        # Get the user's bet data
                        id, galleons, bet_choice = entry.split("-")
                        
                        self.cursor.execute(f"SELECT option_{int(bet_choice)+1} FROM bets WHERE name = ?", (bet_name,))
                        bet_choice = self.cursor.fetchone()

                        # Add that bet information to the users ongoing bets
                        self.user_participated_bets = f"{self.user_participated_bets}\n**{bet_name}**\nBet on **{bet_choice[0]}** with **{galleons}** galleons"
            
        return bets
        
    def not_registered(self, user: discord.Member):
        self.cursor.execute("SELECT roblox_user FROM players WHERE id = ?", (user.id,))
        roblox_user = self.cursor.fetchone()

        if roblox_user == None:
            return True
        else:
            return False
    
    def register_player(self, player: discord.Member, roblox_user: str):
        self.cursor.execute("SELECT id FROM players WHERE id = ?", (player.id,))
        id = self.cursor.fetchone()
        if id is not None:
            return
        
        self.roblox_user = roblox_user
        self.galleons = 0
        
        sql = "INSERT INTO players(id, roblox_user, galleons) VALUES (?, ?, ?)"
        val = (player.id, roblox_user, 0)
        self.cursor.execute(sql, val)
        self.db.commit()