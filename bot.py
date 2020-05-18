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

#allows players to join a game
@bot.command(name='join', help='Add player to current Blood Rage game')
async def add_player(ctx):
    global current_game, player_list
    if current_game == None:
            await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        if current_game.add_player(ctx.message.author.name,
                                   ctx.message.author.discriminator,
                                   ctx.message.author.id):
            player_list.append(ctx.message.author)
            await ctx.send('Player added to Blood Rage game')

    else:
        await ctx.send('Too many players, player not added to game')

#shows players in chat
@bot.command(name='show_players', help='Displays all current players added')
async def show_players(ctx):
    global current_game, player_list

    if len(player_list) == 0:
        await ctx.send('No players')
    else:
        for i in player_list:
            await ctx.send(i.display_name)

@bot.command(name='add_score', help='Add score to the game being played')
async def add_score(ctx, score: int):
    global current_game
    if current_game == None:
            await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        if current_game.add_glory(ctx.message.author.name,
                                   ctx.message.author.discriminator, score):
            await ctx.send('Score added')

    else:
        await ctx.send('Player not found in current game')

@bot.command(name='show_score', help='Show score of current game')
async def get_score(ctx):
    global current_game, player_list

    if current_game == None:
            await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        scores = current_game.get_glory()
        for i in range(len(scores)):
            await ctx.send(player_list[i].display_name + ": " + str(scores[i]))

    else:
        await ctx.send('No score support for this game')

#clears all players in game
@bot.command(name='clear_game', help='Empties player_list')
async def clear_game(ctx):
    global current_game, player_list
    current_game = None
    player_list.clear()
    await ctx.send('Game cleared')

#removes a single player
@bot.command(name='remove_player', help='Removes one player from the game')
async def remove_player(ctx, un, discrim):
    global current_game, player_list

    if current_game == None:
        await ctx.send('No game selected')

    elif current_game.remove_player(un, discrim):
        for i in range(len(player_list)):
            if player_list[i].name == un and player_list[i].discriminator == discrim:
                player_list.remove(player_list[i])
        await ctx.send(un + ' removed from game')
    else:
        await ctx.send(un + ' not found in game')

@bot.command(name='add_stat', help='Add to your stats')
async def add_stats(ctx, stat, add: int):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        if stat == 'rage':
            current_game.increase_rage(add, ctx.message.author.name, ctx.message.author.discriminator)
        elif stat == 'axes':
            current_game.increase_axes(add, ctx.message.author.name, ctx.message.author.discriminator)
        elif stat == 'horns':
            current_game.increase_horns(add, ctx.message.author.name, ctx.message.author.discriminator)
    else:
        await ctx.send('Stat not found')

@bot.command(name='get_hand', help='Shows your current hand')
async def get_hand(ctx):
    if current_game == None:
        await ctx.send('No game selected')

    elif current_game.game_id == 'br':
        await ctx.send(current_game.get_current_hand(ctx.message.author.name, ctx.message.author.discriminator))

@bot.command(name='get_stats', help='Shows your clan stats')
async def get_stats(ctx):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        rage = current_game.get_rage(ctx.message.author.name, ctx.message.author.discriminator)
        axes = current_game.get_axes(ctx.message.author.name, ctx.message.author.discriminator)
        horns = current_game.get_horns(ctx.message.author.name, ctx.message.author.discriminator)

        if rage == -1 or axes == -1 or horns == -1:
            await ctx.send('Player not found')
        else:
            await ctx.send('Rage: ' + str(rage))
            await ctx.send('Axes: ' + str(axes))
            await ctx.send('Horns: ' + str(horns))
    else:
        await ctx.send('Game not found')

@bot.command(name='card', help='View a specific card')
async def get_card(ctx, age: int, card: int):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        result = current_game.get_card(age, card)
        if result == None:
            await ctx.send('Card not found')
        else:
            await ctx.send('Name: ' + result[0])
            await ctx.send('Card Type: ' + result[1])
            await ctx.send('Cost/Strength: ' + result[2])
            await ctx.send('Description: ' + result[3])
    else:
        await ctx.send('No implementation for current game')


@bot.command(name='remove_card', help='Removes card from hand')
async def remove_card(ctx, card: int):
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        result = current_game.remove_card(card, ctx.message.author.name, ctx.message.author.discriminator)
        if result == 0:
            await ctx.send('Player not found')
        elif result == 1:
            await ctx.send('Card not found')
        else:
            await ctx.send('Card removed from hand')
    else:
        await ctx.send('No implementation for game yet')

####################################################################
#                    ______________________                        #
#                   |                     |                        #
#-------------------| Blood Rage Specific |------------------------#
#                   |_____________________|                        #
#                                                                  #
####################################################################

#sets the game on the bot to be Blood Rage
@bot.command(name='game_br', help='Creates a Blood Rage Game')
async def create_br(ctx):
    global current_game
    current_game = None
    current_game = BloodRage()
    await ctx.send('Game set to Blood Rage')

#drafts cards based on age and number of players
@bot.command(name='start_age', help='Begins a new age of drafting (Blood Rage Specific)')
async def start_age(ctx, age: int):
    global current_game
    if current_game == None:
        await ctx.send('Current game not Blood Rage')

    hands = current_game.start_age(age)
    if len(hands) == 0:
        await ctx.send('Not enough players')
    else:
        for i in range(len(hands)):
            await player_list[i].send(hands[i])


@bot.command(name='draft', help='Draft a card from the given hand (Blood Rage Specific)')
async def draft_from_dm(ctx, c_num: int):
    global current_game, player_list
    if current_game == None:
        await ctx.send('Current game not Blood Rage')

    final_hands = current_game.draft(c_num, ctx.message.author.id)

    if final_hands == None:
        await ctx.send('Card Drafted')

    elif len(final_hands) == 0:
        await ctx.send('Card not in hand')
    else:
        for i in range(len(player_list)):
            await player_list[i].send(final_hands[i])

@bot.command(name='set_upgrade', help='Set upgrade cards in your clan data (Blood Rage Specific)')
async def set_upgrade(ctx, card: int, slot: int):
    if current_game == None:
        await ctx.send('Current game not Blood Rage')
    elif current_game.game_id == 'br':
        result = current_game.set_upgrades(card, slot, ctx.message.author.name, ctx.message.author.discriminator)

        if result == 0:
            await ctx.send('Player not found')
        elif result == 1:
            await ctx.send('Card not in hand')
        elif  result == 2:
            await ctx.send('Card could not be found')
        elif result == 3:
            await ctx.send('Upgrade card could not be set')
        else:
            await ctx.send('Upgrade Card set')

    else:
        await ctx.send('Not Blood Rage, command unused')

@bot.command(name='show_upgrades', help='View clan upgrade cards (Blood Rage Specific)')
async def view_upgrades(ctx):
    global current_game

    if current_game == None:
        await ctx.send('Current game not Blood Rage')
    elif current_game.game_id == 'br':
        upgrades = current_game.get_upgrades(ctx.message.author.name, ctx.message.author.discriminator)
        if upgrades == None:
            await ctx.send('Player not found')

        clan = ', '.join(filter(None, (str(upgrades[0][0]), str(upgrades[0][1]), str(upgrades[0][2]))))
        monster = ', '.join(filter(None, (str(upgrades[1][0]), str(upgrades[1][1]))))
        leader = None
        ship = None
        warrior = None
        if upgrades[2] == None:
            leader = 'None'
        else:
            leader = upgrades[2]

        if upgrades[3] == None:
            ship = 'None'
        else:
            ship = upgrades[3]

        if upgrades[4] == None:
            warrior = 'None'
        else:
            warrior = upgrades[4]

        await ctx.send('Clan Upgrades: ' + clan)
        await ctx.send('Monster Upgrades: ' + monster)
        await ctx.send('Leader Upgrade: ' + leader)
        await ctx.send('Ship Upgrade: ' + ship)
        await ctx.send('Warrior Upgrade: ' + warrior)
    else:
        await ctx.send('Not Blood Rage, command unused')



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
