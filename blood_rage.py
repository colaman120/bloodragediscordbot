import os
import random
import numpy as np
import pandas
import copy
from game import *

class BloodRage(BoardGame):
    #class BoardState:


####################################################################
#                    ______________________                        #
#                   |                     |                        #
#-------------------| BR Player Specific  |------------------------#
#                   |_____________________|                        #
#                                                                  #
####################################################################
    class BRPlayer(Player):
        #constructor for the player class
        def __init__(self, set_player):            
            super().__init__(set_player)

            self.rage = 6
            self.axes = 3
            self.horns = 4
            self.clan_uc = [(0, 0), (0, 0), (0, 0)]
            self.monster_uc = [(0, 0), (0, 0)]
            self.warrior_uc = (0, 0)
            self.leader_uc = (0, 0)
            self.ship_uc = (0, 0)
            self.glory = 0
            self.hand = []
            self.quests = []

        #gets the discord player object of the blood rage player
        def get_player_object(self):
            return self.player_object

        #changes the rage clan stat of the current player
        def change_rage(self, delta):
            if self.rage < 12:
                self.rage += delta

        #changes the axes clan stat of the current player
        def change_axes(self, delta):
            if self.axes < 10:
                self.axes += delta
        
        #changes the horns clan stat of the current player
        def change_horns(self, delta):
            if self.horns < 10:
                self.horns += delta

        #changes the glory of the current player
        def change_glory(self, delta):
            self.glory += delta

        #returns the rage clan stat of the player
        def get_rage(self):
            return self.rage

        #returns the axes clan stat of the player
        def get_axes(self):
            return self.axes

        #returns the horns clan stat of the player
        def get_horns(self):
            return self.horns

        #returns current player's glory
        def get_glory(self):
            return self.glory
        
        #add clan upgrade card. This will replace a card if there exists a card
        #in that slot
        def add_clan_uc(self, card_num, age, slot):
            self.clan_uc[slot - 1] = (card_num, age)

        #add monster upgrade card. This will replace a card if there exists a card
        #in that slot
        def add_monster_uc(self, card_num, age, slot):
            self.monster_uc[slot - 1] = (card_num, age)

        #add leader upgrade card. This will replace a card if there exists a card
        #in that slot
        def add_leader_uc(self, card_num, age):
            self.leader_uc = (card_num, age)

        #add warrior upgrade card. This will replace a card if there exists a card
        #in that slot
        def add_warrior_uc(self, card_num, age):
            self.warrior_uc = (card_num, age)

        #add ship upgrade card. This will replace a card if there exists a card
        #in that slot
        def add_ship_uc(self, card_num, age):
            self.ship_uc = (card_num, age)

        #returns the clan upgrade cards
        def get_clan_uc(self):
            return self.clan_uc

        #returns the monster upgrade cards
        def get_monster_uc(self):
            return self.monster_uc

        #returns the leader upgrade cards
        def get_leader_uc(self):
            return self.leader_uc

        #returns the warrior upgrade cards
        def get_warrior_uc(self):
            return self.warrior_uc

        #returns the ship upgrade cards
        def get_ship_uc(self):
            return self.ship_uc

        #set new hand
        def set_hand(self, new_hand):
            self.hand = new_hand
        
        #add new card to hand
        def add_to_hand(self, new_card, age):
            self.hand.append((new_card, age))

        #returns the current state of the hand
        def get_hand(self):
            return self.hand

        def set_quest(self, new_quest, age):
            self.quests.append((new_quest, age))

        def get_quest(self):
            return self.quests

        def clear_quest(self, slot):
            self.quests.pop(slot - 1)

        def clear_quests(self):
            self.quests.clear()

        def remove_card(self, card, age):
            for i in len(range(self.hand)):
                if self.hand[i][0] == card and self.hand[i][1] == age:
                    self.hand.pop(i)
                    return 0
            return 1


####################################################################
#                    ______________________                        #
#                   |                     |                        #
#-------------------|  Blood Rage Class   |------------------------#
#                   |_____________________|                        #
#                                                                  #
####################################################################

    def __init__(self):
        super().__init__('br')
        self.current_age = 0
        self.draftable_cards = []
        self.drafted_cards = []
        self.final_hand = []
        self.final_hand_str = []

        self.card_counts = np.array([[22, 28, 36, 44],
                                     [21, 27, 35, 43],
                                     [21, 27, 35, 43]])

        self.age1_cards = pandas.read_csv('data/age_1.csv', index_col='Card #')
        self.age2_cards = pandas.read_csv('data/age_2.csv', index_col='Card #')
        self.age3_cards = pandas.read_csv('data/age_3.csv', index_col='Card #')

    #add a player to the current instance of blood rage
    def add_player(self, player_to_add):
        if len(self.player_list) > 5:
            return False

        for i in range(len(self.player_list)):
            if self.player_list[i] == player_to_add:
                return False
            
        new_player = self.BRPlayer(player_to_add)
        self.player_list.append(new_player)
        self.final_hand.append([])
        self.drafted_cards.append(-1)
        return True

    #remove a player from the game
    def remove_player(self, player_un, player_discrim):
        for i in range(len(self.player_list)):
            if self.player_list[i].get_player_object().name == player_un and self.player_list[i].get_player_object().discriminator == player_discrim:
                self.player_list.pop(i)
                return True
        return False

    # return the number of players in the current game
    def num_of_players(self):
        return len(self.player_list)

    #adds or subtracts glory to the given player
    def add_glory(self, player, delta):
        found, index = self.find_player(player)
        if found:
            self.player_list[index].change_glory(delta)
            return True
        else:
            return False

    #returns the scores of all players
    def get_glory(self):
        to_return = []
        for i in range(len(self.player_list)):
            to_return.append(self.player_list[i].get_glory())
        return to_return

    #returns a description of the card based on the number and age of the card
    def get_card(self, age, card):
        to_return = []

        if age == 1:
            to_return.append(str(self.age1_cards.at[card, 'Name']))
            to_return.append(str(self.age1_cards.at[card, 'Card Type']))
            to_return.append(str(self.age1_cards.at[card, 'Rage']))
            to_return.append(str(self.age1_cards.at[card, 'Card Description']))
        elif age == 2:
            to_return.append(str(self.age2_cards.at[card, 'Name']))
            to_return.append(str(self.age2_cards.at[card, 'Card Type']))
            to_return.append(str(self.age2_cards.at[card, 'Rage']))
            to_return.append(str(self.age2_cards.at[card, 'Card Description']))
        elif age == 3:
            to_return.append(str(self.age3_cards.at[card, 'Name']))
            to_return.append(str(self.age3_cards.at[card, 'Card Type']))
            to_return.append(str(self.age3_cards.at[card, 'Rage']))
            to_return.append(str(self.age3_cards.at[card, 'Card Description']))

        return to_return

    def get_current_hand(self, player):
        found, index = self.find_player(player)
        if found:
            return self.num_card_concatenator(np.sort(self.player_list[index].get_hand()),
                 self.card_name_gen(self.current_age, self.player_list[index].get_hand()))
        return 'No hand found'
    
    #returns whether or not a player was found and at what index they were found
    def find_player(self, player_to_find):
        index = -1

        for i in range(len(self.player_list)):
            if player_to_find == self.player_list[i].get_player_object():
                index = i
                return True, index
        return False, index

    def remove_card(self, card, age, player):
        found, index = self.find_player(player)
        if found:
            return self.player_list[index].remove_card(card, age)
        else: 
            return 2
        
        

    #generates hands
    def gen_hands(self, age):
        numbers = np.arange(self.card_counts[age - 1][len(self.player_list) - 2])
        to_return = np.random.choice(numbers, size=(len(self.player_list), 8), replace=False)
        return to_return.tolist()

    #makes card array look nice
    def card_concatenator(self, list_of_nums, list_of_cards):
        to_string = ''

        for i in range(len(list_of_cards)):
            card_type = self.get_card_type(list_of_nums[i], self.current_age)
            if card_type == 0:
                to_string = to_string + '*' + list_of_cards[i] + '*'
            elif card_type == 1:
                to_string = to_string + '__' + list_of_cards[i] + '__'
            elif card_type == 2:
                to_string = to_string + '**' + list_of_cards[i] + '**'

            if i != len(list_of_cards) - 1:
                to_string = to_string + ', '

        return to_string

    #creates a list of cards with numbers and card names to make drafting easier
    def num_card_concatenator(self, list_of_nums, list_of_cards):
        to_string = ''
        list_of_nums_str = list_of_nums.astype(str)

        for i in range(len(list_of_cards)):
            card_type = self.get_card_type(list_of_nums[i], self.current_age)
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
        card_type = 0
        type_str = None

        if age == 1:
            type_str = self.age1_cards.at[card_num, 'Card Type']

        elif age == 2:
            type_str = self.age2_cards.at[card_num, 'Card Type']

        elif age == 3:
            type_str = self.age3_cards.at[card_num, 'Card Type']

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
                to_return.append(self.age1_cards.at[i, 'Name'])
            elif age == 2:
                to_return.append(self.age2_cards.at[i, 'Name'])
            elif age == 3:
                to_return.append(self.age3_cards.at[i, 'Name'])

        return to_return

    #checks if everyone has drafted
    def check_all_draft(self):
        for i in range(len(self.drafted_cards)):
            if self.drafted_cards[i] == -1:
                return False

        return True


    def remove_cards(self):
        self.draftable_cards = np.asarray(self.draftable_cards)
        for i in range(np.size(self.draftable_cards, 0)):
            self.draftable_cards[i] = np.roll(self.draftable_cards[i],
                self.draftable_cards[i].size - np.where(self.draftable_cards[i] == self.drafted_cards[i])[0][0])

        self.draftable_cards = np.delete(self.draftable_cards, 0, 1)
        self.draftable_cards = self.draftable_cards.tolist()

    def add_to_final_hand(self):
        for i in range(len(self.drafted_cards)):
            self.final_hand[i].append(self.drafted_cards[i])

    #advance the draft by passing the cards around
    def advance_draft(self):
        self.draftable_cards = np.asarray(self.draftable_cards)
        temp = np.copy(self.draftable_cards[np.size(self.draftable_cards, 0) - 1])

        for i in range(np.size(self.draftable_cards, 0) - 2, -1, -1):
            self.draftable_cards[i + 1] = self.draftable_cards[i]

        self.draftable_cards[0] = temp
        self.draftable_cards = self.draftable_cards.tolist()

        self.drafted_cards.clear()
        for i in self.player_list:
            self.drafted_cards.append(-1)

    #checks if draft is over
    def check_end_draft(self):
        self.draftable_cards = np.asarray(self.draftable_cards)
        if self.draftable_cards.size <= len(self.player_list) * 2:
            for i in range(len(self.final_hand)):
                self.final_hand[i] = np.sort(self.final_hand[i])
                self.final_hand_str.append(self.num_card_concatenator(self.final_hand[i],
                                        self.card_name_gen(self.current_age, self.final_hand[i])))
                self.final_hand[i] = self.final_hand[i].tolist()
            return True
        else:
            self.draftable_cards = self.draftable_cards.tolist()
            return False

    #provides the initial hands per age
    def start_age(self, age):
        if len(self.player_list) >= 2:
            self.draftable_cards = copy.deepcopy(self.gen_hands(age))
            self.current_age = copy.copy(age)
            generated_hands = []

            for i in range(len(self.draftable_cards)):
                self.draftable_cards[i] = np.sort(self.draftable_cards[i])
                hand = self.card_name_gen(age, self.draftable_cards[i])
                generated_hands.append(self.num_card_concatenator(self.draftable_cards[i], hand))

            return generated_hands
        else:
            return []

    #advances draft and accepts card inputs
    def draft(self, c_num, author_id):
        card_drafted = False
        for i in range(len(self.player_list)):
            if author_id == self.player_list[i].get_player_object().id:
                for j in range(len(self.draftable_cards[i])):
                    if c_num == self.draftable_cards[i][j]:
                        self.drafted_cards[i] = c_num
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
                    for i in range(len(self.draftable_cards)):
                        self.draftable_cards[i] = np.sort(self.draftable_cards[i])
                        hand = self.card_name_gen(self.current_age, self.draftable_cards[i])
                        to_return.append(self.num_card_concatenator(self.draftable_cards[i], hand))
                    return to_return

                else:
                    to_return = []
                    for i in range(len(self.final_hand_str)):
                        to_return.append(self.final_hand_str[i])

                    self.drafted_cards.clear()
                    self.draftable_cards = []
                    for i in range(len(self.player_list)):
                        self.drafted_cards.append(-1)
                        for j in range(len(self.final_hand[i])):
                            self.player_list[i].add_to_hand(self.final_hand[i][j], self.current_age)

                    return to_return
