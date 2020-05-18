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
    rage = []
    axes = []
    horns = []
    clan_upgrade_cards = []
    warrior_upgrade_cards = []
    leader_upgrade_cards = []
    ship_upgrade_cards = []
    monster_upgrade_cards = []
    game_id = 'br'

    card_counts = np.array([[22, 28, 36, 44],
                            [21, 27, 35, 43],
                            [21, 27, 35, 43]])

    age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
    age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
    age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

    def __init__(self):
        global player_list, cards, draft, current_age, final_hand, final_hand_str, glory_counter
        global game_id, card_counts, age1_cards, age2_cards, age3_cards, rage, axes, horns
        global clan_upgrade_cards, warrior_upgrade_cards, leader_upgrade_cards, ship_upgrade_cards, monster_upgrade_cards

        player_list = []
        cards = []
        draft = []
        current_age = 0
        final_hand = []
        final_hand_str = []
        glory_counter = []
        rage = []
        axes = []
        horns = []
        clan_upgrade_cards = []
        warrior_upgrade_cards = []
        leader_upgrade_cards = []
        ship_upgrade_cards = []
        monster_upgrade_cards = []
        game_id = 'br'

        card_counts = np.array([[22, 28, 36, 44],
                                [21, 27, 35, 43],
                                [21, 27, 35, 43]])

        age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
        age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
        age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

    #adds a player to the blood rage game
    def add_player(self, un, discrim, id):
        global player_list, draft, final_hand, glory_counter, rage, axes, horns, clan_upgrade_cards, monster_upgrade_cards
        if len(player_list) < 5:
            player_list.append([un, discrim, id])
            draft.append(-1)
            glory_counter.append(0)
            final_hand.append([])
            rage.append(6)
            axes.append(3)
            horns.append(4)
            clan_upgrade_cards.append([None, None, None])
            monster_upgrade_cards.append([None, None])
            warrior_upgrade_cards.append(None)
            leader_upgrade_cards.append(None)
            ship_upgrade_cards.append(None)
            return True
        else:
            return False

    # returns a list of strings of the players display names
    def get_num_of_players(self):
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

    def increase_rage(self, increase, un, discrim):
        global player_list, rage

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                rage[i] += increase
                return True
        return False

    def get_rage(self, un, discrim):
        global player_list, rage

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                return rage[i]
        return -1

    def increase_axes(self, increase, un, discrim):
        global player_list, axes

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                axes[i] += increase
                return True
        return False

    def get_axes(self, un, discrim):
        global player_list, axes

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                return axes[i]
        return -1

    def increase_horns(self, increase, un, discrim):
        global player_list, horns

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                horns[i] += increase
                return True
        return False

    def get_horns(self, un, discrim):
        global player_list, horns

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                return horns[i]
        return -1

    def get_current_hand(self, un, discrim):
        global player_list, final_hand, current_age

        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                return self.num_card_concatenator(np.sort(final_hand[i]), self.card_name_gen(current_age, final_hand[i]))
        return 'No hand found'

    def get_card(self, age, card):
        global age1_cards, age2_cards, age3_cards
        to_return = []

        if age == 1:
            to_return.append(str(age1_cards.at[card, 'Name']))
            to_return.append(str(age1_cards.at[card, 'Card Type']))
            to_return.append(str(age1_cards.at[card, 'Rage']))
            to_return.append(str(age1_cards.at[card, 'Card Description']))
        elif age == 2:
            to_return.append(str(age2_cards.at[card, 'Name']))
            to_return.append(str(age2_cards.at[card, 'Card Type']))
            to_return.append(str(age2_cards.at[card, 'Rage']))
            to_return.append(str(age2_cards.at[card, 'Card Description']))
        elif age == 3:
            to_return.append(str(age3_cards.at[card, 'Name']))
            to_return.append(str(age3_cards.at[card, 'Card Type']))
            to_return.append(str(age3_cards.at[card, 'Rage']))
            to_return.append(str(age3_cards.at[card, 'Card Description']))

        return to_return

    def set_upgrades(self, card, slot, un, discrim):
        global player_list, clan_upgrade_cards, warrior_upgrade_cards, leader_upgrade_cards, ship_upgrade_cards, monster_upgrade_cards, current_age, cards

        index = -1
        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                index = i

        if index == -1:
            return 0

        print(index)

        card_found = False
        for j in final_hand[index]:
            if j == card:
                card_found = True
                break

        if card_found == False:
            return 1

        card_name = ''
        card_type = ''

        if current_age == 1:
            card_name = age1_cards.at[card, 'Name']
            card_type = age1_cards.at[card, 'Card Type']
        elif current_age == 2:
            card_name = age2_cards.at[card, 'Name']
            card_type = age2_cards.at[card, 'Card Type']
        elif current_age == 3:
            card_name = age3_cards.at[card, 'Name']
            card_type = age3_cards.at[card, 'Card Type']
        else:
            return 2

        if card_type == 'Monster':
            monster_upgrade_cards[index][slot - 1] = card_name
        elif card_type == 'Leader':
            leader_upgrade_cards[index] = card_name
        elif card_type == 'Warrior':
            warrior_upgrade_cards[index] = card_name
        elif card_type == 'Ship':
            ship_upgrade_cards[index] = card_name
        elif card_type == 'Clan':
            clan_upgrade_cards[index][slot - 1] = card_name
        else:
            return 3

        self.remove_card(card, un, discrim)
        return 4


    def get_upgrades(self, un, discrim):
        global player_list, clan_upgrade_cards, warrior_upgrade_cards, leader_upgrade_cards, ship_upgrade_cards, monster_upgrade_cards

        to_return = []
        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                to_return.append(clan_upgrade_cards[i])
                to_return.append(monster_upgrade_cards[i])
                to_return.append(leader_upgrade_cards[i])
                to_return.append(ship_upgrade_cards[i])
                to_return.append(warrior_upgrade_cards[i])
        return to_return

    # removes a single player based on their username and discord discriminator
    def remove_player(self, un, discrim):
        global player_list, final_hand, final_hand_str
        player_removed = False
        for player in player_list:
            if player[0] == un and player[1] == discrim:
                player_list.remove(player)
                player_removed = True
        return player_removed

    def remove_card(self, card, un, discrim):
        global player_list, final_hand
        index = -1
        for i in range(len(player_list)):
            if player_list[i][0] == un and player_list[i][1] == discrim:
                index = i

        if index == -1:
            return 0

        card_index = -1
        for j in range(len(final_hand[index])):
            if j == card:
                card_index = j
                break

        if card_index == -1:
            return 1

        final_hand[index].pop(card_index)
        final_hand_str[index] = self.num_card_concatenator(np.sort(final_hand[index]),
                                                            self.card_name_gen(current_age, np.sort(final_hand[i])))

        return 2

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

        return True


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
    def start_age(self, age):
        global player_list, cards, current_age, final_hand, final_hand_str

        if len(player_list) >= 2:
            cards = copy.deepcopy(self.gen_hands(age))
            current_age = copy.copy(age)
            generated_hands = []

            for i in range(len(cards)):
                cards[i] = np.sort(cards[i])
                hand = self.card_name_gen(age, cards[i])
                generated_hands.append(self.num_card_concatenator(cards[i], hand))

            return generated_hands
        else:
            return []

    #advances draft and accepts card inputs
    def draft(self, c_num, author_id):
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
            if self.check_all_draft():
                self.add_to_final_hand()
                self.remove_cards()
                if self.check_end_draft() == False:
                    self.advance_draft()

                    to_return = []
                    for i in range(len(cards)):
                        cards[i] = np.sort(cards[i])
                        hand = self.card_name_gen(current_age, cards[i])
                        to_return.append(self.num_card_concatenator(cards[i], hand))
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
                    for i in player_list:
                        draft.append(-1)

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
