import discord
from discord import app_commands
from discord.ext import commands

from Factory.Settings.logic import Logic

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Modify the bot's channel settings")
    async def settings(self, interaction: discord.Interaction):
        logic = Logic(interaction)

        await interaction.response.send_message(embed=logic.embed, view=logic.console, ephemeral=True)
    
async def setup(bot: commands.Bot):
    print("Settings Loaded")
    await bot.add_cog(Settings(bot))