# bot.py
import os
import random
import numpy as np
import pandas
import copy
from blood_rage import BloodRage
from villpill import VillPill

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
current_game = None

# displays bot connection to discord
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#shows the current selected game
@bot.command(name='show_game', help='Displays the current game')
async def show_game(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.get_game_id() == 'br':
        await ctx.send('Blood Rage')
    elif current_game.get_game_id() == 'vp':
        await ctx.send('Village Pillage')
    else:
        await ctx.send(current_game.get_game_id())

#allows players to join a game
@bot.command(name='join', help='Add player to current Blood Rage game')
async def add_player(ctx):
    global current_game
    if current_game == None:
            await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        if current_game.add_player(ctx.message.author):
            await ctx.send('Player added to Blood Rage game')
        else:
            await ctx.send('Player already in game or too many players')

    elif current_game.game_id == 'vp':
        if current_game.add_player(ctx.message.author):
            await ctx.send('Player added to Village Pillage game')
        else:
            await ctx.send('Player already in game or too many players')

    else:
        await ctx.send('Player not added to game')

#shows players in chat
@bot.command(name='show_players', help='Displays all current players added')
async def show_players(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    player_list = current_game.get_player_list()

    if len(player_list) == 0:
        await ctx.send('No players')
    else:
        for i in player_list:
            await ctx.send(i.get_player_object().display_name)

@bot.command(name='add_score', help='Add score to the game being played')
async def add_score(ctx, score: int):
    global current_game
    if current_game == None:
            await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        if current_game.add_glory(ctx.message.author, score):
            await ctx.send('Score added')
        else:
            await ctx.send('Player not found')

    else:
        await ctx.send('Player not found in current game')

@bot.command(name='show_score', help='Show score of current game')
async def get_score(ctx):
    global current_game

    if current_game == None:
            await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        scores = current_game.get_glory()
        player_list = current_game.get_player_list()

        for i in range(len(scores)):
            await ctx.send(player_list[i].get_player_object().display_name + ": " + str(scores[i]))

    elif current_game.game_id == 'vp':
        relic_score = current_game.get_relic_score()
        player_list = current_game.get_player_list()

        for i in range(len(relic_score)):
            await ctx.send(player_list[i].get_player_object().display_name + ": " + str(relic_score[i]))

    else:
        await ctx.send('No score support for this game')

#clears all players in game
@bot.command(name='clear_game', help='Empties player_list')
async def clear_game(ctx):
    global current_game
    current_game = None
    await ctx.send('Game cleared')

#removes a single player
@bot.command(name='remove_player', help='Removes one player from the game')
async def remove_player(ctx, un, discrim):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.remove_player(un, discrim):
        await ctx.send(un + ' removed from game')
    else:
        await ctx.send(un + ' not found in game')

@bot.command(name='add_stat', help='Add to your stats')
async def add_stats(ctx):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')        
        
    elif current_game.game_id == 'br':
        while True:
            await ctx.send('What stat would you like to modify?')
            msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            stat = msg.content.lower()

            if stat == 'rage' or stat == 'axes' or stat == 'horns':
                break
            elif stat == 'quit':
                await ctx.send('Stat not added')
                return

        await ctx.send('How much?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            add = int(msg.content)
        except ValueError:
            await ctx.send('Not an integer value. Try command again')
            return

        found, index = current_game.find_player(ctx.message.author)
        if found:
            stat = stat.lower()

            if stat == 'rage':
                current_game.player_list[index].change_rage(add)
            elif stat == 'axes':
                current_game.player_list[index].change_axes(add)
            elif stat == 'horns':
                current_game.player_list[index].change_horns(add)
            else:
                await ctx.send('Stats added')
            
        found, index = current_game.find_player(ctx.message.author)

        if found:
            rage = current_game.get_player_list()[index].get_rage()
            axes = current_game.get_player_list()[index].get_axes()
            horns = current_game.get_player_list()[index].get_horns()

            await ctx.send('Rage: ' + str(rage))
            await ctx.send('Axes: ' + str(axes))
            await ctx.send('Horns: ' + str(horns))

        else:
            await ctx.send('Player not found')
    else:
        await ctx.send('how did you even get here')

@bot.command(name='get_stats')
async def get_stats(ctx):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        found, index = current_game.find_player(ctx.message.author)

        if found:
            rage = current_game.get_player_list()[index].get_rage()
            axes = current_game.get_player_list()[index].get_axes()
            horns = current_game.get_player_list()[index].get_horns()

            await ctx.send('Rage: ' + str(rage))
            await ctx.send('Axes: ' + str(axes))
            await ctx.send('Horns: ' + str(horns))
        else:
            await ctx.send('Player not found')

    elif current_game.game_id == 'vp':
        money = current_game.get_all_money_total()
        for i in range(len(money)):
            await ctx.send('**' + current_game.get_player_list()[i].get_player_object().display_name + ':**')
            await ctx.send('Bank: ' + str(money[i][0]))
            await ctx.send('Stockpile: ' + str(money[i][1]))
    else:
        await ctx.send('Game not found')

@bot.command(name='get_hand', help='Shows your current hand')
async def get_hand(ctx):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        hand = current_game.get_current_hand(ctx.message.author)
        if hand == '':
            await ctx.send('Empty hand')
        else:
            for i in range(len(hand)):
                await ctx.send(hand[i])
    
    elif current_game.get_game_id() == 'vp':
        hand = current_game.get_current_hand(ctx.message.author)

        if hand == '':
            await ctx.send('Empty hand')
        else:
            for i in range(len(hand)):
                await ctx.send(hand[i])

@bot.command(name='card', help='View a specific card')
async def get_card(ctx):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        while True:
            await ctx.send('What age?')
            msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            try:
                age = int(msg.content)
            except ValueError:
                await ctx.send('Not an integer value. Try command again')
                return

            if age > 0 and age < 4:
                break
            else:
                ctx.send('Not a valid age')
        
        await ctx.send('What card number?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            card = int(msg.content)
        except ValueError:
            await ctx.send('Not an integer value. Try command again')
            return

        result = current_game.get_card(age, card)
        if result == None:
            await ctx.send('Card not found')
        else:
            await ctx.send('Name: ' + result[0])
            await ctx.send('Card Type: ' + result[1])
            await ctx.send('Cost/Strength: ' + result[2])
            await ctx.send('Description: ' + result[3])

    elif current_game.get_game_id() == 'vp':
        await ctx.send('What card?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        card_path = 'data/vp_cards/' + msg.content.lower() + '.png'

        if os.path.exists(card_path):
            await ctx.send(file=discord.File('data/vp_cards/' + msg.content.lower() + '.png'))
        else:
            await ctx.send('Not a card or the file does not exist')
    else:
        await ctx.send('No implementation for current game')

@bot.command(name='remove_card', help='Removes card from hand')
async def remove_card(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        while True:
            await ctx.send('What age?')
            msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            try:
                age = int(msg.content)
            except ValueError:
                await ctx.send('Not an integer value. Try command again')
                return
                
            if age > 0 and age < 4:
                break
            else:
                ctx.send('Not a valid age')
        
        await ctx.send('What card number?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            card = int(msg.content)
        except ValueError:
            await ctx.send('Not an integer value. Try command again')
            return
        
        result = current_game.remove_card(card, age, ctx.message.author)
        if result == 0:
            await ctx.send('Card removed from hand')
        elif result == 1:
            await ctx.send('Card not found')
        else:
            await ctx.send('Player not found')
    else:
        await ctx.send('No implementation for game yet')

@bot.command(name='summon')
async def summon(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        val_summon = current_game.check_val_summon(ctx.message.author)
        # summoning_from_val = False

        # if val_summon:
        #     await ctx.send('Would you like to summon from Valhalla?')
        #     msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
            
        #     if msg.lower() == 'yes' or msg.lower() == 'y':
        #         summoning_from_val = True

        await ctx.send('What unit would you like to summon?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        unit = msg.content.lower()

        await ctx.send('What province would you like to summon to?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        province = msg.content.lower()

        result = current_game.summon_unit(ctx.message.author, unit, province)
        if result == -1:
            await ctx.send('No rage remaining')
        elif result == 0:
            await ctx.send('Player not found')
        elif result == 1:
            await ctx.send('Province not found')
        elif result == 2:
            await ctx.send('Province is ragnoroked')
        elif result == 3:
            await ctx.send('Not enough horns')
        elif result == 4:
            await ctx.send('Unit not found')
        elif result == 5:
            await ctx.send('Province is full')
        elif result == 6:
            await ctx.send('Trying to summon ship on land or vice versa')
        else:
            await ctx.send(unit.capitalize() + ' summoned to ' + province.capitalize())
        
    else:
        await ctx.send('No implementation for game yet')

@bot.command(name='kill_piece')
async def kill(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        await ctx.send('What unit would you like to kill?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        unit = msg.content.lower()

        await ctx.send('What province is that unit in?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        province = msg.content.lower()

        result = current_game.kill(ctx.message.author, unit, province)
        if result == 0:
            await ctx.send('Unit not found')
        elif result == 1:
            await ctx.send(unit + ' killed from '+ province)
        elif result == 2:
            await ctx.send('Player not found')
        else:
            await ctx.send(province + ' not found')
    else:
        await ctx.send('No implementation for game yet')

@bot.command(name='move')
async def move(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        await ctx.send('What type of unit would you like to move?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        unit = msg.content.lower()

        await ctx.send('How many would you like to move?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        try:
            num = int(msg.content)
        except ValueError:
            await ctx.send('Not an integer value. Try command again')
            return

        await ctx.send('Province from?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        province_from = msg.content.lower()

        await ctx.send('Province to?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        province_to = msg.content.lower()        
        
        result = current_game.move(ctx.message.author, unit, num, province_from, province_to)
        if result == 0:
            await ctx.send('Player not found')
        elif result == 1:
            await ctx.send('Not enough rage')
        elif result == 2:
            await ctx.send('Province not found')
        elif result == 3:
            await ctx.send('Cannot move from/to fjords')
        elif result == 4:
            await ctx.send('Cannot move ships')
        elif result == 5:
            await ctx.send('Not enough space in destination')
        elif result == 6:
            await ctx.send('Not enough units in province')
        else:
            await ctx.send(unit + ' moved from ' + province_from + ' to ' + province_to)
    else:
        await ctx.send('No implementation for game yet')

@bot.command(name='play')
async def play_card(ctx):
    global current_game

    if current_game == None:
        await ctx.send('No game selected')
    
    elif current_game.get_game_id() == 'vp':
        await ctx.send('What card would you like to play?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        card = int(msg.content.lower())

        await ctx.send('Which side?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        msg = msg.content.lower()
        position = -1
        if msg == 'l' or msg == 'left' or msg == '0':
            position = 0
        
        if msg == 'r' or msg == 'right' or msg == '1':
            position = 1
        
        result = current_game.play_card(ctx.message.author, card, position)
        if result == 1:
            await ctx.send('Card not in hand')
        elif result == 2:
            await ctx.send('Player not found')
        elif result == 3:
            await ctx.send('Incorrect positioning')
        else:
            await ctx.send('Card played')
        
@bot.command(name='show_board_image')
async def show_board_image(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        await ctx.send(file=discord.File('data/BR_map.jpg'))

@bot.command(name='show_board')
async def show_board(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        result = current_game.display_board()

        for i in range(8):
            await ctx.send('**' + result[i][0] + ':** __' + result[i][1] + '__ (' + str(result[i][2]) + ')')
            if len(result[i][3]) == 0:
                await ctx.send('Province empty')
            else:
                for j in range(len(result[i][3])):
                    await ctx.send(result[i][3][j].to_string())
        
        await ctx.send('**Yggdrasil**')
        if len(result[8][3]) == 0:
            await ctx.send('Province empty')
        else:
            for j in range(len(result[i][3])):
                await ctx.send(result[i][3][j].to_string())
        
        for i in range(9, 13):
            await ctx.send('**' + result[i][0].upper() + ' Fjord**')
            if len(result[i][3]) == 0:
                await ctx.send('Province empty')
            else:
                for j in range(len(result[i][3])):
                    await ctx.send(result[i][3][j].to_string())

    else:
        await ctx.send('No implementation for game yet')

@bot.command(name='shop')
async def show_shop(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.get_game_id() == 'vp':
        shop = current_game.show_shop()
        for card in shop:
            await ctx.send(card)

@bot.command(name='end_round')
async def end_round(ctx):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        await ctx.send('What age?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        province = msg.content.lower()

        result = current_game.end_age(province)
        if result == 0:
            await ctx.send('Players must discard to one card in hand')
        elif result == 1:
            await ctx.send(province.capitalize() + ' does not exist')
        else:
            quests = result[0]
            valhalla = result[1]
            for i in range(len(current_game.get_player_list())):
                await ctx.send(current_game.get_player_list()[i].get_player_object().display_name + ": ")
                for j in range(len(result[i])):
                    await ctx.send(str(quests[i][j]))
            
            await ctx.send(valhalla)

    elif current_game.get_game_id() == 'vp':
        result = current_game.take_turn()

        if result == False:
            await ctx.send('Not all cards played yet')
        else:
            #replace with history over the turn
            await ctx.send('Great job :)')
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
    if hands == None:
        await ctx.send('Discard to 1 card in hand')
    elif hands == -1:
        await ctx.send('Currently drafting')
    elif len(hands) == 0:
        await ctx.send('Not enough players')
    else:
        player_list = current_game.get_player_list()
        for i in range(len(hands)):
            await player_list[i].get_player_object().send('Cards to Draft:')
            for j in range(len(hands[i])):
                await player_list[i].get_player_object().send(hands[i][j])

@bot.command(name='draft', help='Draft a card from the given hand (Blood Rage Specific)')
async def draft_from_dm(ctx, c_num: int):
    global current_game
    if current_game == None:
        await ctx.send('Current game not Blood Rage')

    final_hands = current_game.draft(c_num, ctx.message.author)

    if final_hands == None:
        await ctx.send('Card Drafted')

    elif len(final_hands) == 0:
        await ctx.send('Card not in hand')
    else:
        await ctx.send('Card Drafted')
        player_list = current_game.get_player_list()
        for i in range(len(player_list)):
            for j in range(len(final_hands[i])):
                await player_list[i].get_player_object().send(final_hands[i][j])

@bot.command(name='set_upgrade', help='Set upgrade cards in your clan data (Blood Rage Specific)')
async def set_upgrade(ctx, age: int, card: int, slot: int):
    global current_game

    if current_game == None:
        await ctx.send('Current game not Blood Rage')
    elif current_game.game_id == 'br':
        result = current_game.set_upgrades(age, card, slot, ctx.message.author)
        card_name = current_game.card_name_gen(age, card)

        if result == 0:
            await ctx.send('Player not found')
        elif result == 1:
            await ctx.send(card_name + ' not in hand')
        elif  result == 2:
            await ctx.send(card_name + ' could not be found')
        elif result == 3:
            await ctx.send(card_name + ' could not be set')
        else:
            await ctx.send(card_name + ' set in slot ' + slot)

        rage = current_game.get_current_rage(ctx.message.author)
        if rage == -1:
            await ctx.send('Player not found')
        else:
            await ctx.send('You have ' + str(rage) + ' rage remaining.')

    else:
        await ctx.send('Not Blood Rage, command unused')

@bot.command(name='show_upgrades', help='View clan upgrade cards (Blood Rage Specific)')
async def view_upgrades(ctx):
    global current_game

    if current_game == None:
        await ctx.send('Current game not Blood Rage')
    elif current_game.game_id == 'br':
        upgrades = current_game.get_upgrades(ctx.message.author)
        if upgrades == None:
            await ctx.send('Player not found')

        clan = ', '.join(filter(None, (upgrades[0][0], upgrades[0][1], upgrades[0][2])))
        monster = ', '.join(filter(None, (upgrades[1][0], upgrades[1][1])))
        leader = upgrades[2]
        ship = upgrades[3]
        warrior = upgrades[4]


        await ctx.send('Clan Upgrades: ' + clan)
        await ctx.send('Monster Upgrades: ' + monster)
        await ctx.send('Leader Upgrade: ' + leader)
        await ctx.send('Ship Upgrade: ' + ship)
        await ctx.send('Warrior Upgrade: ' + warrior)
    else:
        await ctx.send('Not Blood Rage, command unused')

@bot.command(name='rag_check')
async def rag_check(ctx):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.rag_check()
        province_list = current_game.board.get_provinces()
        await ctx.send('Provinces getting ragnoroked: ' + province_list[result[0]].get_name().capitalize() 
            + ', ' + province_list[result[1]].get_name().capitalize() + ', '
            + province_list[result[2]].get_name().capitalize())
            
@bot.command(name='pillage_rewards')
async def show_pillage_rewards(ctx):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.pillage_rewards()
        for i in range(len(result)):
            await ctx.send('**' + current_game.board.get_provinces()[i].get_name().capitalize() + ':** ' + result[i])

@bot.command(name='valhalla')
async def show_valhalla(ctx):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.show_valhalla()
        if len(result) == 0:
            await ctx.send('no units in valhalla')
        else:
            for i in range(len(result)):
                await ctx.send('**' + result[i].get_name() + '**: ' + result[i].get_owner())

@bot.command(name='add_rage')
async def change_rage(ctx, delta: int):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.change_rage(delta, ctx.message.author)
        if result:
            found, index = current_game.find_player(ctx.message.author)
            await ctx.send(str(delta) + ' added to current rage. You have ' + str(current_game.get_player_list()[index].get_current_rage()) + ' rage left.')
        else:
            await ctx.send('Player not found')

@bot.command(name='get_rage')
async def show_current_rage(ctx):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.get_current_rage(ctx.message.author)
        if result < -9:
            await ctx.send('Player not found')
        else:
            await ctx.send('Current rage: ' + str(result))

@bot.command(name='get_quests')
async def get_quests(ctx):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.get_quests(ctx.message.author)
        if result == -1:
            await ctx.send('Player not found')
        else:
            await ctx.send(result)

@bot.command(name='set_quest')
async def add_quest(ctx, age: int, card: int):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.add_quest(age, card, ctx.message.author)
        if result == -1:
            await ctx.send('No rage remaining')
        elif result == 0:
            await ctx.send('Card not in hand')
        elif result == 1:
            await ctx.send('Already too many copies of this quest')
        elif result == 2:
            await ctx.send('Quest set')
        else:
            await ctx.send('Player not found')

@bot.command(name='show_province')
async def show_province(ctx, province):
    global current_game
    if current_game == None:
        await ctx.send('No game selected')
    elif current_game.game_id == 'br':
        result = current_game.display_province(province)
        if len(result[0]) == 2:
            await ctx.send('**Province:** ' + province.capitalize() + ' (*' + result[0][0].capitalize() + ', ' + result[0][1].capitalize() + '*)')
        else:
            await ctx.send('**Province:** ' + province.capitalize() + ' (*' + result[0][0].capitalize() + '*)')
        await ctx.send('Ragnorok: ' + str(result[1]))
        await ctx.send('Capacity: ' + str(result[2]))
        await ctx.send('Reward: ' + result[3])
        await ctx.send('Pieces: ')
        if len(result[4]) == 0:
            await ctx.send('Province empty')
        else:
            for j in range(len(result[4])):
                await ctx.send(result[4][j].to_string())

@bot.command(name='ragnorok')
async def rag(ctx, province):
    global current_game
    if current_game.get_game_id() == 'br':
        result = current_game.rag(province)
        if result == 0:
            await ctx.send(province.capitalize() + '  does not exist')
        elif result == 1:
            await ctx.send(province.capitalize() + ' already ragnoroked')
        elif result == 2:
            await ctx.send('?')
        else:
            await ctx.send(province.capitalize() + ' was ragonoroked')
    else:
        await ctx.send('wrong game')

####################################################################
#                    ______________________                        #
#                   |                     |                        #
#-------------------|     VP Specific     |------------------------#
#                   |_____________________|                        #
#                                                                  #
####################################################################
@bot.command(name='game_vp')
async def create_vp(ctx):
    global current_game
    current_game = None
    current_game = VillPill()
    await ctx.send('Game set to Village Pillage')

@bot.command(name='opponents')
async def get_opponent_positions(ctx):
    global current_game
    if current_game.get_game_id() == 'vp':
        found, idx = current_game.find_player(ctx.message.author)
        length = len(current_game.get_player_list())

        if found:
            if idx == length - 1:
                await ctx.send('**Left side:** ' + current_game.get_player_list()[idx - 1].get_player_object().display_name)
                await ctx.send('**Right side:** ' + current_game.get_player_list()[0].get_player_object().display_name)
            else:
                await ctx.send('**Left side:** ' + current_game.get_player_list()[idx - 1].get_player_object().display_name)
                await ctx.send('**Right side:** ' + current_game.get_player_list()[idx + 1].get_player_object().display_name)
        
        else:
            await ctx.send('Player not found')
    else:
        await ctx.send('No implementation for current game')

@bot.command(name='view_played')
async def get_played_cards(ctx):
    global current_game
    if current_game.get_game_id() == 'vp':
        found, idx = current_game.find_player(ctx.message.author)

        if found:
            current_player = current_game.get_player_list()[idx]
            result = current_game.hand_to_text(current_player.get_played())
            await ctx.send('**Left side:** ')
            await ctx.send(result[0])
            await ctx.send('**Right side:** ')
            await ctx.send(result[1])
        
        else:
            await ctx.send('Player not found')
    else:
        await ctx.send('No implementation for current game')

@bot.command(name='buy')
async def buy_card(ctx):
    global current_game
    if current_game.get_game_id() == 'vp':
        await ctx.send('What card would you like to buy?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        card_num = int(msg.content)

        await ctx.send('At what price?')
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        cost = int(msg.content)

        result = current_game.buy_card(ctx.message.author, card_num, cost)
        
        if result == False:
            await ctx.send('Could not buy card')
        else:
            await ctx.send('Card successfully bought')
    else:
        await ctx.send('No implementation for current game')

@bot.command(name='restore_shop')
async def restore_shop_front(ctx):
    global current_game
    if current_game.get_game_id() == 'vp': 
        current_game.restore_shop()
    else:
        await ctx.send('No implementation for current game')
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
