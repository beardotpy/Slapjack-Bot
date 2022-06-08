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

    init_embed = discord.Embed(title=f"{game.current_player.user.name}'s Turn", description=game.turn_order_str)
    await ctx.send(embed=init_embed)

    while game.winner == None:
        while game.current_player.hand_length == 0:
            game.next_turn()

        action_msg = await bot.wait_for(
            "message",
            check=lambda m: m.author in game.user_list and m.channel == ctx.channel and m.content in ["slap", "play"]
        )

        # current player plays card
        if action_msg.content == "play" and action_msg.author == game.current_player.user:
            game.add_to_deck(game.current_player.lose_card())
            game.next_turn()
            game_embed = discord.Embed(title=f"{game.current_player.user.name}'s Turn", description=game.turn_order_str)
            game_embed.set_image(url=f"attachment://{game.deck[0]}")
            await ctx.send(file=discord.File(f"cards/{game.deck[0]}"), embed=game_embed)
        elif action_msg.content == "slap" and game.check_if_slap():
            game.turn = game.user_list.index(action_msg.author)
            await ctx.send(f"**{action_msg.author}** slapped first and gained **{len(game.deck)}** cards!")
            game.current_player.pickup_deck(game.deck)
            game.empty_deck()
            game_embed = discord.Embed(title=f"{game.current_player.user.name}'s Turn", description=game.turn_order_str)
            await ctx.send(embed=game_embed)
        elif action_msg.content == "slap" and not game.check_if_slap():
            await ctx.send(f"**{action_msg.author}** slapped incorrectly and loses a card!")
            game.add_to_deck(game.players[game.user_list.index(action_msg.author)].lose_card())
            game_embed = discord.Embed(title=f"{game.current_player.user.name}'s Turn", description=game.turn_order_str)
            game_embed.set_image(url=f"attachment://{game.deck[0]}")
            await ctx.send(file=discord.File(f"cards/{game.deck[0]}"), embed=game_embed)

    await ctx.send(f"{game.winner.user.mention} is the winner!")

bot.run(TOKEN)