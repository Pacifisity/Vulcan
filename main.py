import discord
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv

# Config
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)
load_dotenv()

@bot.command(name="sync")  # Sync Command for testing
@commands.is_owner()
async def sync(ctx: commands.Context):
    async with ctx.typing():
        await bot.tree.sync()
        await ctx.send("Synchronized!")

# Cogs
async def load_extensions():
    await bot.load_extension('Cogs.betting')
    await bot.load_extension('Cogs.profile')
    await bot.load_extension('Cogs.settings')

# Bot events
@bot.event
async def on_ready():
    await load_extensions()
    print("Vulcan Online")

# Token
token = getenv("TESTBOTTOKEN")
bot.run(token)