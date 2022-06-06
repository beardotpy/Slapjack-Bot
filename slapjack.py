import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
from pprint import pprint
class Game:
    pass

class Player:
    pass


load_dotenv()
TOKEN = os.getenv("TOKEN")
INTENTS = discord.Intents.all()

bot = commands.Bot(command_prefix="s!", intents = INTENTS)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready.")

@bot.command()
async def rules(ctx):
    await ctx.send("Rules")

@bot.command(aliases = ["game"])
async def slapjack(ctx):
    await ctx.send("React to this message to enter a slapjack game.")
    timer_msg = await ctx.send("⏱️⏱️⏱️⏱️⏱️")
    await timer_msg.add_reaction("🃏")
    for i in range(5, 0, -1):
        await timer_msg.edit(content="⏱️"*i)
        await asyncio.sleep(1)
    
    timer_msg = await ctx.channel.fetch_message(timer_msg.id)
    msg_reactions = timer_msg.reactions[0]
    users = [user async for user in msg_reactions.users()]
    users.pop(0)

bot.run(TOKEN)