# bot.py
import os
import random
import numpy as np
import pandas
import copy

import discord
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
player_list = []
cards = np.zeros(1)
draft = []
current_age = 0
final_hand = []
final_hand_str = []
glory_counter = []
# [i] = age
# [j] = players



card_counts = np.array([[22, 28, 36, 44],
                        [21, 27, 35, 43],
                        [21, 27, 35, 43]])

age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

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
@bot.command(name='join_game', help='Add player to current Blood Rage game')
async def add_player(ctx):
    player_list.append(ctx.message.author)
    draft.append(-1)
    final_hand.append([])
    glory_counter.append(0)
    await ctx.send('Player added')

#shows players in chat
@bot.command(name='show_players', help='Displays all current players added')
async def show_players(ctx):
    for i in range(len(player_list)):
        await ctx.send(player_list[i].display_name)
    if len(player_list) == 0:
        await ctx.send('No players')

#clears all players in game
@bot.command(name='clear_game', help='Empties player_list')
async def empty_player_list(ctx):
    global player_list, cards, draft, current_age, final_hand, final_hand_str
    player_list.clear()
    cards = np.zeros(1)
    draft.clear()
    current_age = 0
    final_hand.clear()
    final_hand_str.clear()
    await ctx.send('Game cleared')

#drafts cards based on age and number of players
@bot.command(name='start_age', help='Begins a new age of drafting')
async def draft_cards(ctx, age: int):

    if len(player_list) > 2:
        temp = gen_hands(age)
        global cards, current_age
        cards = np.copy(temp)
        current_age = copy.copy(age)

        for i in range(len(cards)):
            cards[i] = np.sort(cards[i])
            hand = card_name_gen(age, cards[i])
            await player_list[i].send(num_card_concatenator(cards[i], hand))
#        await player_list[i].send(num_concatenator(cards[i]))
#        await player_list[i].send(card_concatenator(hand))

@bot.command(name='draft', help='Draft a card from the given hand')
async def draft_from_dm(ctx, c_num: int):
    global current_age, cards, draft, final_hand

    card_drafted = False
    for i in range(len(player_list)):
        if ctx.message.author.id == player_list[i].id:
            for j in range(cards[i].size):
                if c_num == cards[i][j]:
                    draft[i] = c_num
                    card_drafted = True
                    await ctx.send('Card drafted')
                    break
    if card_drafted == False:
        await ctx.send('Card not in hand')

    if card_drafted:
        if check_all_draft():
            add_to_final_hand()
            remove_cards()
            if check_end_draft() == False:
                advance_draft()

                for i in range(len(cards)):
                    cards[i] = np.sort(cards[i])
                    hand = card_name_gen(current_age, cards[i])
                    await player_list[i].send(num_card_concatenator(cards[i], hand))
#                    await player_list[i].send(card_concatenator(hand))

            else:
                for i in range(len(final_hand_str)):
                    await player_list[i].send(final_hand_str[i])

                draft.clear()
                cards = np.zeros(1)
                for i in player_list:
                    draft.append(-1)

#generates hands
def gen_hands(age: int):
    numbers = np.arange(card_counts[age - 1][len(player_list) - 2])
    return np.random.choice(numbers, size=(len(player_list), 8), replace=False)

#make number array look nice
def num_concatenator(list_of_nums):
    to_string = ''
    list_of_nums = list_of_nums.astype(str)

    for i in range(list_of_nums.size):
        to_string = to_string + list_of_nums[i]
        if i != list_of_nums.size - 1:
            to_string = to_string + ', '

    return to_string

#makes card array look nice
def card_concatenator(list_of_cards):
    to_string = ''

    for i in range(len(list_of_cards)):
        to_string = to_string + list_of_cards[i]
        if i != len(list_of_cards) - 1:
            to_string = to_string + ', '

    return to_string

def num_card_concatenator(list_of_nums, list_of_cards):
    to_string = ''
    list_of_nums = list_of_nums.astype(str)

    for i in range(len(list_of_cards)):
        to_string = to_string + list_of_nums[i] + ": " + list_of_cards[i]
        if i != len(list_of_cards) - 1:
            to_string = to_string + ', '

    return to_string

#generates the names of the cards based on the number and age
def card_name_gen(age, card_num):
    to_return = []
    for i in card_num:
        if age == 1:
            to_return.append(age1_cards.at[i, 'Name'])
        elif age == 2:
            to_return.append(age2_cards.at[i, 'Name'])
        elif age == 3:
            to_return.append(age3_cards.at[i, 'Name'])

    return to_return

#checks if everyone has drafted
def check_all_draft():
    global draft, final_hand
    for i in range(len(draft)):
        if draft[i] == -1:
            return False

    return True;


def remove_cards():
    global cards, draft
    for i in range(np.size(cards, 0)):
        cards[i] = np.roll(cards[i], cards[i].size - np.where(cards[i] == draft[i])[0][0])

    cards = np.delete(cards, 0, 1)

def add_to_final_hand():
    global draft, final_hand
    for i in range(len(draft)):
        final_hand[i].append(draft[i])

#advance the draft by passing the cards around
def advance_draft():
    global cards, draft
    temp = np.copy(cards[np.size(cards, 0) - 1])
    for i in range(np.size(cards, 0) - 2, -1, -1):
        cards[i + 1] = cards[i]
    cards[0] = temp

    draft.clear()
    for i in player_list:
        draft.append(-1)

#checks if draft is over
def check_end_draft():
    global cards,final_hand, current_age, final_hand_str
    if cards.size <= len(player_list) * 2:
        for i in range(len(final_hand)):
            final_hand_str.append(card_concatenator(card_name_gen(current_age, final_hand[i])))
        return True
    else:
        return False

bot.run(TOKEN)
