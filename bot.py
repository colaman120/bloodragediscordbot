# bot.py
import os
import random
import numpy as np
import pandas
import copy
from blood_rage import BloodRage

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
current_game = None
player_list = []
#cards = np.zeros(1)
#draft = []
#current_age = 0
#final_hand = []
#final_hand_str = []
#glory_counter = []
# [i] = age
# [j] = players



#card_counts = np.array([[22, 28, 36, 44],
#                        [21, 27, 35, 43],
#                        [21, 27, 35, 43]])

#age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
#age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
#age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

# displays bot connection to discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

'''
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
'''

#sets the game on the bot to be Blood Rage
@bot.command(name='game_br', help='Creates a Blood Rage Game')
async def create_br(ctx):
    global current_game
    current_game = BloodRage()
    await ctx.send('Game set to Blood Rage')

#allows players to join a game
@bot.command(name='join_br', help='Add player to current Blood Rage game')
async def add_player(ctx):
    global current_game, player_list
    if current_game.game_id == 'br':
        if current_game.add_player(ctx.message.author.name,
                                   ctx.message.author.discriminator,
                                   ctx.message.author.id):
            player_list.append(ctx.message.author)
            await ctx.send('Player added to Blood Rage game')
        else:
            await ctx.send('Too many players, player not added to Blood Rage game')

#shows players in chat
@bot.command(name='show_players', help='Displays all current players added')
async def show_players(ctx):
    global current_game

    players = current_game.get_players()
    if len(players) == 0:
        await ctx.send('No players')
    else:
        for i in players:
            await ctx.send(player_list[i].display_name)

#clears all players in game
@bot.command(name='clear_game', help='Empties player_list')
async def empty_player_list(ctx):
    global current_game
    current_game = None
    await ctx.send('Game cleared')

#removes a single player
@bot.command(name='remove_player', help='Removes one player from the game')
async def remove_player(ctx, un, discrim: int):
    global current_game, player_list

    if bool = current_game.remove_player(un, discrim):
        for i in player_list:
            if i.username == un and i.discriminator = discrim:
                player_list.remove(i)
        await ctx.send(un + ' removed from game')
    else:
        await ctx.send(un + ' not found in game')

#drafts cards based on age and number of players
@bot.command(name='start_age', help='Begins a new age of drafting')
async def draft_cards(ctx, age: int):
    global current_game
    hands = current_game.start_age(age)
    for i in hands:
        await player_list[i].send(i)


@bot.command(name='draft', help='Draft a card from the given hand')
async def draft_from_dm(ctx, c_num: int):
    global current_game
    final_hands = current_game.draft(c_num, ctx.message.author.id)

    if len(final_hands) == 0:
        return "Card not in hand"
    else:
        return "Card Drafted"



####################################################################
#                    _____________________                         #
#                   |                    |                         #
#-------------------| Server Kill Switch |-------------------------#
#                   |____________________|                         #
#                                                                  #
####################################################################

def check_if_it_is_me(ctx):
    return ctx.message.author.id == 88463772489908224

@bot.command(name='kill', help='Kills the server')
@commands.check(check_if_it_is_me)
async def kill_server(ctx):
    await ctx.send('Killing bot')
    await bot.logout()

@kill_server.error
async def kill_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You do not have permission to access this command')



bot.run(TOKEN)
