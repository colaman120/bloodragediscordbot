import os
import random
import numpy as np
import pandas
import copy
import discord


class BloodRage:
    player_list = []
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
        global player_list, cards, draft, current_age, final_hand, final_hand_str, glory_counter, game_id, card_counts, age1_cards, age2_cards, age3_cards
        player_list = []
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

    #adds a player to the blood rage game
    def add_player(br, un, discrim, id):
        global player_list, draft, final_hand, glory_counter
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
        global player_list, glory_counter
        return len(player_list)

    def add_glory(self, un, discrim, score):
        global player_list, glory_counter

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                glory_counter[i] += score
                return True
        return False

    def get_glory(self):
        global glory_counter
        return glory_counter


    # removes a single player based on their username and discord discriminator
    def remove_player(br, un, discrim):
        global player_list
        player_removed = False
        for player in player_list:
            if player[0] == un and player[1] == discrim:
                player_list.remove(player)
                player_removed = True
        return player_removed

    #generates hands
    def gen_hands(self, age):
        global card_counts, player_list
        numbers = np.arange(card_counts[age - 1][len(player_list) - 2])
        to_return = np.random.choice(numbers, size=(len(player_list), 8), replace=False)
        return to_return.tolist()





    #makes card array look nice
    def card_concatenator(self, list_of_nums, list_of_cards):
        global current_age
        to_string = ''

        for i in range(len(list_of_cards)):
            card_type = self.get_card_type(list_of_nums[i], current_age)
            if card_type == 0:
                to_string = to_string + '*' + list_of_cards[i] + '*'
            elif card_type == 1:
                to_string = to_string + '__' + list_of_cards[i] + '__'
            elif card_type == 2:
                to_string = to_string + '**' + list_of_cards[i] + '**'

            if i != len(list_of_cards) - 1:
                to_string = to_string + ', '

        return to_string

    #TODO: Fix list_of_nums to understand that it is a list and not an array
    def num_card_concatenator(self, list_of_nums, list_of_cards):
        global current_age
        to_string = ''
        #list_of_nums_int = list_of_nums.astype(int)
        list_of_nums_str = list_of_nums.astype(str)

        for i in range(len(list_of_cards)):
            card_type = self.get_card_type(list_of_nums[i], current_age)
            if card_type == 0:
                to_string = to_string + list_of_nums_str[i] + ": " + '*' + list_of_cards[i] + '*'
            elif card_type == 1:
                to_string = to_string + list_of_nums_str[i] + ": " + '__' + list_of_cards[i] + '__'
            elif card_type == 2:
                to_string = to_string + list_of_nums_str[i] + ": " + '**' + list_of_cards[i] + '**'

            if i != len(list_of_cards) - 1:
                to_string = to_string + ', '

        return to_string

    # get the type of card. 0 = upgrade, 1 = quest, 2 = battle
    def get_card_type(self, card_num, age):
        global age1_cards, age2_cards, age3_cards
        card_type = 0
        type_str = None

        if age == 1:
            type_str = age1_cards.at[card_num, 'Card Type']

        elif age == 2:
            type_str = age2_cards.at[card_num, 'Card Type']

        elif age == 3:
            type_str = age3_cards.at[card_num, 'Card Type']

        if type_str == 'Battle':
            card_type = 2
        elif type_str == 'Quest':
            card_type = 1
        else:
            card_type = 0

        return card_type


    #generates the names of the cards based on the number and age
    def card_name_gen(self, age, card_num):
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
    def check_all_draft(self):
        global draft, final_hand
        for i in range(len(draft)):
            if draft[i] == -1:
                return False

        return True;


    def remove_cards(self):
        global cards, draft
        cards = np.asarray(cards)
        for i in range(np.size(cards, 0)):
            cards[i] = np.roll(cards[i], cards[i].size - np.where(cards[i] == draft[i])[0][0])

        cards = np.delete(cards, 0, 1)
        cards = cards.tolist()

    def add_to_final_hand(self):
        global draft, final_hand
        for i in range(len(draft)):
            final_hand[i].append(draft[i])

    #advance the draft by passing the cards around
    def advance_draft(self):
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
    def check_end_draft(self):
        global cards,final_hand, current_age, final_hand_str
        cards = np.asarray(cards)
        if cards.size <= len(player_list) * 2:
            for i in range(len(final_hand)):
                final_hand[i] = np.sort(final_hand[i])
                final_hand_str.append(self.num_card_concatenator(final_hand[i],
                                        self.card_name_gen(current_age, final_hand[i])))
                final_hand[i] = final_hand[i].tolist()
            return True
        else:
            cards = cards.tolist()
            return False

    #provides the initial hands per age
    def start_age(br, age):
        global player_list, cards, current_age

        if len(player_list) >= 2:
            cards = copy.deepcopy(br.gen_hands(age))
            current_age = copy.copy(age)
            generated_hands = []

            for i in range(len(cards)):
                cards[i] = np.sort(cards[i])
                hand = br.card_name_gen(age, cards[i])
                generated_hands.append(br.num_card_concatenator(cards[i], hand))

            return generated_hands
        else:
            return []

    #advances draft and accepts card inputs
    def draft(br, c_num, author_id):
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
            if br.check_all_draft():
                br.add_to_final_hand()
                br.remove_cards()
                if br.check_end_draft() == False:
                    br.advance_draft()

                    to_return = []
                    for i in range(len(cards)):
                        cards[i] = np.sort(cards[i])
                        hand = br.card_name_gen(current_age, cards[i])
                        to_return.append(br.num_card_concatenator(cards[i], hand))
                        #                    await player_list[i].send(num_card_concatenator(cards[i], hand))
                        #                    await player_list[i].send(card_concatenator(hand))
                    return to_return

                else:
                    to_return = []
                    for i in range(len(final_hand_str)):
                        to_return.append(final_hand_str[i])
                        #                    await player_list[i].send(final_hand_str[i])

                    draft.clear()
                    cards = []
                    final_hand.clear()
                    final_hand_str.clear()
                    for i in player_list:
                        draft.append(-1)
                        final_hand.append([])

                    return to_return

'''
#TODO: Fix list_of_nums to understand that it is a list and not an array
#make number array look nice
def num_concatenator(self, list_of_nums):
    to_string = ''

    for i in range(len(list_of_nums)):
        to_string = to_string + str(list_of_nums[i])
        if i != len(list_of_nums) - 1:
            to_string = to_string + ', '

    return to_string
'''
