import os
import asyncio
from game import Game
from player import Player
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

    if len(users) < 2:
        await ctx.send("L no friends")
        return

    players = [Player(user) for user in users]
    game = Game(players)
    game.deal_cards()

    init_embed = discord.Embed(title=f"{game.current_player.name}'s Turn", description=game.turn_order_str)
    await ctx.send(embed=init_embed)

    while not game.is_won:
        while game.current_player.hand_length == 0:
            turn += 1

        print("in main loop")
        action_msg = await bot.wait_for(
            "message",
            check=lambda m: m.author in [player.user for player in game.players] and m.channel == ctx.channel and m.content in ["slap", "play"]
        )
        print("msg detected")

        # current player plays card
        if action_msg.content == "play" and action_msg.author == game.current_player.user:
            played_card = game.current_player.lose_card()
            game_embed = discord.Embed(title=f"{game.current_player.name}'s Turn", description=game.turn_order_str)
            game_embed.set_image(url=f"attachment://{played_card}")
            game.next_turn()
            await ctx.send(file=discord.File(played_card), embed=game_embed)
        elif action_msg.content == "slap":
            return

bot.run(TOKEN)