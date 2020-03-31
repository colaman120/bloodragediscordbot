import os
import random
import numpy as np
import pandas
import copy
import discord


class BloodRage:
    player_list = []
    player_id = []
    cards = []
    draft = []
    current_age = 0
    final_hand = []
    final_hand_str = []
    glory_counter = []
    game_id = 'br'

    card_counts = np.array([[22, 28, 36, 44],
                            [21, 27, 35, 43],
                            [21, 27, 35, 43]])

    age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
    age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
    age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

    def __init__(self):
        self.data = 0

    #adds a player to the blood rage game
    def add_player(un, discrim, id):
        if len(player_list) < 5:
            player_list.append([un, discrim, id])
            draft.append(-1)
            final_hand.append([])
            glory_counter.append(0)
            return True
        else:
            return False

    # returns a list of strings of the players display names
    def get_num_of_players():
        return len(player_list)

    # removes a single player based on their username and discord discriminator
    def remove_player(un, discrim):
        player_removed = False
        for player in player_list:
            if player[0] == un and player[1]] == discrim:
                player_list.remove(player)
                player_removed = True
        return player_removed

    #provides the initial hands per age
    def start_age(age):
        if len(player_list) > 3:
            global cards, current_age
            cards = copy.deepcopy(gen_hands(age))
            current_age = copy.copy(age)

        generated_hands = []

        for i in range(len(cards)):
            cards[i] = np.sort(cards[i])
            hand = card_name_gen(age, cards[i])
            generated_hands = num_card_concatenator(cards[i], hand)
        return generated_hands

    #advances draft and accepts card inputs
    def draft(c_num, author_id):
        global current_age, cards, draft, final_hand

        card_drafted = False
        for i in range(len(player_list)):
            if author_id == player_list[i][2]:
                for j in range(len(cards[i])):
                    if c_num == cards[i][j]:
                        draft[i] = c_num
                        card_drafted = True
                        break

        if card_drafted == False:
            return []

        if card_drafted:
            if check_all_draft():
                add_to_final_hand()
                remove_cards()
                if check_end_draft() == False:
                    advance_draft()

                    to_return = []
                    for i in range(len(cards)):
                        cards[i] = np.sort(cards[i])
                        hand = card_name_gen(current_age, cards[i])
                        to_return.append(num_card_concatenator(cards[i], hand))
    #                    await player_list[i].send(num_card_concatenator(cards[i], hand))
    #                    await player_list[i].send(card_concatenator(hand))
                    return to_return

                else:
                    to_return = []
                    for i in range(len(final_hand_str)):
                        to_return.append(final_hand_str[i])
    #                    await player_list[i].send(final_hand_str[i])

                    draft.clear()
                    cards = np.zeros(1)
                    for i in player_list:
                        draft.append(-1)

    #generates hands
    def gen_hands(age: int):
        numbers = np.arange(card_counts[age - 1][len(player_list) - 2])
        to_return = np.random.choice(numbers, size=(len(player_list), 8), replace=False)
        return to_return.tolist()

    #TODO: Fix list_of_nums to understand that it is a list and not an array
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

    #TODO: Fix list_of_nums to understand that it is a list and not an array 
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
        cards = np.asarray(cards)
        for i in range(np.size(cards, 0)):
            cards[i] = np.roll(cards[i], cards[i].size - np.where(cards[i] == draft[i])[0][0])

        cards = np.delete(cards, 0, 1)
        cards = cards.tolist()

    def add_to_final_hand():
        global draft, final_hand
        for i in range(len(draft)):
            final_hand[i].append(draft[i])

    #advance the draft by passing the cards around
    def advance_draft():
        global cards, draft
        cards = np.asarray(cards)
        temp = np.copy(cards[np.size(cards, 0) - 1])
        for i in range(np.size(cards, 0) - 2, -1, -1):
            cards[i + 1] = cards[i]
        cards[0] = temp
        cards = cards.tolist()

        draft.clear()
        for i in player_list:
            draft.append(-1)

    #checks if draft is over
    def check_end_draft():
        global cards,final_hand, current_age, final_hand_str
        cards = np.asarray(cards)
        if cards.size <= len(player_list) * 2:
            for i in range(len(final_hand)):
                final_hand_str.append(card_concatenator(card_name_gen(current_age, final_hand[i])))
                cards = cards.tolist()
            return True
        else:
            cards = cards.tolist()
            return False
