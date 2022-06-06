import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

class Game:
    pass

class Player:
    pass


load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="s!")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")

@bot.command()
async def rules(ctx):
    await ctx.send("Rules")

@bot.command(aliases = ["game"])
async def slapjack(ctx):
    init_msg = await ctx.send("React to this message to enter a slapjack game.")


bot.run(TOKEN)