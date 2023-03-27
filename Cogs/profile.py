import discord
from discord import app_commands
from discord.ext import commands

from Factory.Profile.logic import Logic

class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description='Open your profile to see your information')
    async def profile(self, interaction: discord.Interaction):
        logic = Logic(interaction)

        await interaction.response.send_message(embed=logic.embed, view=logic.console, ephemeral=True)
    
async def setup(bot: commands.Bot):
    print("Profile Loaded")
    await bot.add_cog(Profile(bot))