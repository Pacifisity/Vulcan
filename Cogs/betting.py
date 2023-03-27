import discord
from discord import app_commands
from discord.ext import commands

from Factory.Betting.logic import Logic

class Betting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Start a bet')
    async def bet(self, interaction: discord.Interaction):
        logic = Logic(interaction)

        await interaction.response.send_modal(logic.console.bet_creation_modal)
    
async def setup(bot: commands.Bot):
    print("Betting Loaded")
    await bot.add_cog(Betting(bot))