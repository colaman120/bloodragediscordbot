import os
import random
import numpy as np
import pandas
import copy
import enum
from game import BoardGame
from game import Player
from BRPiece import BRPiece
from province import Province

class BloodRage(BoardGame):
    ####################################################################
    #                    ______________________                        #
    #                   |                     |                        #
    #-------------------| Board State Class   |------------------------#
    #                   |_____________________|                        #
    #                                                                  #
    ####################################################################
    class BoardState:
        def __init__(self):
            self.provinces = []
            self.provinces.append(Province('myrkulor', 3, ['manheim']))
            self.provinces.append(Province('elvagar', 4, ['manheim']))
            self.provinces.append(Province('angerboda', 5, ['manheim']))
            self.provinces.append(Province('anolang', 3, ['alfheim']))
            self.provinces.append(Province('gimle', 5, ['alfheim']))
            self.provinces.append(Province('utgard', 3, ['jotunheim']))
            self.provinces.append(Province('horgr', 4, ['jotunheim']))
            self.provinces.append(Province('muspelheim', 5, ['jotunheim']))
            self.provinces.append(Province('yggdrasil', 80, ['yggdrasil']))
            self.provinces.append(Province('ne', 5, ['manheim']))
            self.provinces.append(Province('nw', 5, ['manheim', 'alfheim']))
            self.provinces.append(Province('sw', 5, ['alfheim', 'jotunheim']))
            self.provinces.append(Province('se', 5, ['jotunheim']))

            self.valhalla = []
            self.provinces[8].set_pillage_reward(0)
            self.provinces[8].set_pillage_reward(1)
            self.provinces[8].set_pillage_reward(2)

            x = [0, 0, 0, 1, 1, 2, 2, 3]
            rewards = random.sample(x, 8)

            for i in range(8):
                self.provinces[i].set_pillage_reward(rewards[i])
            
            for i in range(9, 13):
                self.provinces[i].set_pillage_reward(4)

        def get_provinces(self):
            return self.provinces

        def get_valhalla(self):
            return self.valhalla

        def summon(self, province_idx, piece):
            self.provinces[province_idx].piece_list.append(piece)

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

            self.current_rage = 6
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
            self.units = []

            for i in range(8):
                new_unit = BRPiece(set_player, 'warrior')
                self.units.append(new_unit)

            self.units.append(BRPiece(set_player, 'ship'))
            self.units.append(BRPiece(set_player, 'leader'))

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
            for i in range(len(self.hand)):
                if self.hand[i][0] == card and self.hand[i][1] == age:
                    self.hand.pop(i)
                    return 0
            return 1

        def get_quests(self):
            return self.quests
        
        def get_units(self):
            return self.units

        def get_current_rage(self):
            return self.current_rage

        def change_current_rage(self, delta):
            self.current_rage += delta


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
        self.board = self.BoardState()
        self.draftable_cards = []
        self.drafted_cards = []
        self.final_hand_str = []
        self.draft_phase = False
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
            current_hand = self.player_list[index].get_hand()
            hand_num = []
            hand_name = []
            hand_ages = np.zeros(len(current_hand), dtype=np.int32)
            for i in range(len(current_hand)):
                hand_num.append(current_hand[i][0])
                hand_name.append(self.card_name_gen(current_hand[i][1], current_hand[i][0])[0])
                hand_ages[i] = current_hand[i][1]

            return self.num_card_concatenator(np.array(hand_num), hand_name, hand_ages)
        return 'No hand found'

    def set_upgrades(self, age, card, slot, player):
        found, index = self.find_player(player)
        if found == False:
            return 0

        card_found = False
        for i in range(len(self.player_list[index].hand)):
            if self.player_list[index].hand[i][0] == card and self.player_list[index].hand[i][1] == age:
                card_found = True
                break

        if card_found == False:
            return 1

        card_type = ''
        card_name = ''

        if age == 1:
            card_type = self.age1_cards.at[card, 'Card Type']
            card_name = self.age1_cards.at[card, 'Name']
        elif age == 2:
            card_type = self.age2_cards.at[card, 'Card Type']
            card_name = self.age2_cards.at[card, 'Name']
        elif age == 3:
            card_type = self.age3_cards.at[card, 'Card Type']
            card_name = self.age3_cards.at[card, 'Name']
        else:
            return 2

        if card_type == 'Monster':
            self.player_list[index].add_monster_uc(card, age, slot)
            self.player_list[index].units.append(BRPiece(player, card_name.lower()))
        elif card_type == 'Leader':
            self.player_list[index].add_leader_uc(card, age)
        elif card_type == 'Warrior':
            self.player_list[index].add_warrior_uc(card, age)
        elif card_type == 'Ship':
            self.player_list[index].add_ship_uc(card, age)
        elif card_type == 'Clan':
            self.player_list[index].add_clan_uc(card, age, slot)
        else:
            return 3

        self.remove_card(card, age, player)
        return 4

    def get_upgrades(self, player):
        found, index = self.find_player(player)
        if found == False:
            return None
        
        to_return = []
        clan_cards = self.player_list[index].get_clan_uc()
        monster_cards = self.player_list[index].get_monster_uc()
        leader_card = self.player_list[index].get_leader_uc()
        ship_card = self.player_list[index].get_ship_uc()
        warrior_card = self.player_list[index].get_warrior_uc()

        temp = []
        for i in range(len(clan_cards)):
            if clan_cards[i] == (0, 0):
                temp.append('None')
            else:
                x = self.num_card_concatenator(np.array([clan_cards[i][0]]), 
                    self.card_name_gen(clan_cards[i][1], clan_cards[i][0]), np.array([clan_cards[i][1]]))
                temp.append(x[0])
        to_return.append(copy.deepcopy(temp))

        temp.clear()
        for i in range(len(monster_cards)):
            if monster_cards[i] == (0, 0):
                temp.append('None')
            else:
                temp.append(self.num_card_concatenator(np.array([monster_cards[i][0]]), 
                    self.card_name_gen(monster_cards[i][1], monster_cards[i][0]), 
                    np.array([monster_cards[i][1]]))[0])
        to_return.append(temp)

        if leader_card == (0, 0):
            to_return.append('None')
        else:
            to_return.append(self.num_card_concatenator(np.array([leader_card[0]]),
                self.card_name_gen(leader_card[1], leader_card[0]), np.array([leader_card[1]]))[0])

        if ship_card == (0, 0):
            to_return.append('None')
        else:
            to_return.append(self.num_card_concatenator(np.array([ship_card[0]]),
                self.card_name_gen(ship_card[1], ship_card[0]), np.array([ship_card[1]]))[0])
        
        if warrior_card == (0, 0):
            to_return.append('None')
        else:
            to_return.append(self.num_card_concatenator(np.array([warrior_card[0]]),
                self.card_name_gen(warrior_card[1], warrior_card[0]), np.array([warrior_card[1]]))[0])

        return to_return

    def summon_unit(self, player, unit, province):
        found, index = self.find_player(player)
        if found == False:
            return 0

        unit = unit.lower()
        province = province.lower()

        found, province_idx = self.find_province(province)
        if found == False:
            return 1

        if self.board.get_provinces()[province_idx].get_rag() == True:
            return 2

        units_on_board = 0
        for i in self.player_list[index].get_units():
            if i.get_on_board() == True:
                units_on_board += 1

        if units_on_board >= self.player_list[index].get_horns():
            return 3

        unit_found = False
        piece_idx = -1
        player_units = self.player_list[index].get_units()
        for i in range(len(player_units)):
            if player_units[i].get_on_board() == False and player_units[i].get_name() == unit:
                piece_idx = i
                unit_found = True
                break
        
        if unit_found == False:
            return 4

        
        if self.board.get_provinces()[province_idx].get_current_cap() == self.board.get_provinces()[province_idx].get_cap():
            return 5

        if (unit == 'ship' or unit == 'sea serpeant') and province_idx < 9:
            return 6
        
        if (unit != 'ship' and unit != 'sea serpent') and province_idx > 8:
            return 6

        self.board.summon(province_idx, player_units[piece_idx])
        return 7

    def kill(self, player, unit, province):
        player_found, index = self.find_player(player)
        if player_found == False:
            return 2
        
        unit = unit.lower()
        province = province.lower()
        
        found, province_idx = self.find_province(province)
        if found == False:
            return 3

        unit_idx = -1
        piece_list = self.board.get_provinces()[province_idx].get_piece_list()
        for i in range(len(piece_list)):
            if piece_list[i].get_name() == unit and piece_list[i].get_owner() == player:
                unit_idx = i
        
        if unit_idx == -1:
            return 0


        piece_list[unit_idx].kill()
        dead_piece = self.board.provinces[province_idx].piece_list.pop(unit_idx)
        self.board.valhalla.append(dead_piece)
        return 1

    def kill_all(self, province):
        province = province.lower()
        found, province_idx = self.find_province(province)
        if found == False:
            return 0

        piece_list = self.board.get_provinces()[province_idx].get_piece_list()
        for i in range(len(piece_list)):
            piece_list[i].kill()
            dead_piece = self.board.provinces[province_idx].piece_list.pop(i)
            self.board.valhalla.append(dead_piece)



    def move(self, player, unit, num, province_from, province_to):
        unit = unit.lower()
        province_from = province_from.lower()
        province_to = province_to.lower()

        player_found, index = self.find_player(player)
        if player_found == False:
            return 0

        if self.player_list[index].get_current_rage() < 1:
            return 1
        
        pf_found, pf_idx = self.find_province(province_from)
        if pf_found == False:
            return 2

        pt_found, pt_idx = self.find_province(province_to)
        if pt_found == False:
            return 2

        if pf_idx > 8 or pt_idx > 8:
            return 3
        
        if unit == 'ship' or unit == 'sea serpent':
            return 4

        if self.board.get_provinces()[pt_idx].get_cap() - self.board.get_provinces()[pt_idx].get_current_cap() < num:
            return 5
        
        unit_count = 0
        piece_list = self.board.get_provinces()[pf_idx].get_piece_list()
        for i in range(len(piece_list)):
            if piece_list[i].get_owner() == player and unit == piece_list[i].get_name():
                unit_count += 1

        if unit_count < num:
            return 6

        count = 0
        for i in range(len(piece_list)):
            if piece_list[i].get_owner() == player and unit == piece_list[i].get_name():
                self.board.get_provinces()[pt_idx].piece_list.append(self.board.get_provinces()[pf_idx].piece_list.pop(i))
                count += 1
            
            if count == num:
                break
        return 7

    def remove_card(self, card, age, player):
        found, index = self.find_player(player)
        if found:
            return self.player_list[index].remove_card(card, age)
        else: 
            return 2

    def display_board(self):
        to_return = []
        province_list = self.board.get_provinces()
        for i in range(len(province_list)):
            province = []
            province.append(province_list[i].get_name().capitalize())
            province.append(province_list[i].get_sub()[0].capitalize())
            province.append(province_list[i].get_rag())
            province.append(province_list[i].get_cap())
            print(province_list[i].get_pillage_reward())
            if province_list[i].get_pillage_reward()[0] == 0:
                province.append('Rage')
            elif province_list[i].get_pillage_reward()[0] == 1:
                province.append('Axes')
            elif province_list[i].get_pillage_reward()[0] == 2:
                province.append('Horns')
            else:
                province.append('5 Glory')
            province.append(province_list[i].get_piece_list())
            to_return.append(province)
        
        return to_return
    
    #returns whether or not a player was found and at what index they were found
    def find_player(self, player_to_find):
        index = -1

        for i in range(len(self.player_list)):
            if player_to_find == self.player_list[i].get_player_object():
                index = i
                return True, index
        return False, index

    def find_province(self, province_to_find):
        index = -1 
        provinces = self.board.get_provinces()
        for i in range(len(provinces)):
            if provinces[i].get_name() == province_to_find:
                index = i
                return True, index 
        
        return False, index

    #generates hands
    def gen_hands(self, age):
        numbers = np.arange(self.card_counts[age - 1][len(self.player_list) - 2])
        to_return = np.random.choice(numbers, size=(len(self.player_list), 8), replace=False)
        return to_return.tolist()

    #creates a list of cards with numbers and card names to make drafting easier
    def num_card_concatenator(self, list_of_nums, list_of_cards, list_of_ages):
        to_return = []
        list_of_nums_str = list_of_nums.astype(str)
        list_of_ages_str = list_of_ages.astype(str)

        for i in range(len(list_of_cards)):
            card_type = self.get_card_type(list_of_nums[i], list_of_ages[i])
            if card_type == 0:
                to_return.append('(' + list_of_ages_str[i] + ') ' + list_of_nums_str[i] + ": " + '*' + list_of_cards[i] + '*')
            elif card_type == 1:
                to_return.append('(' + list_of_ages_str[i] + ') ' + list_of_nums_str[i] + ": " + '__' + list_of_cards[i] + '__')
            elif card_type == 2:
                to_return.append('(' + list_of_ages_str[i] + ') ' + list_of_nums_str[i] + ": " + '**' + list_of_cards[i] + '**')

        return to_return

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
    def card_name_gen(self, ages, card_num):
        to_return = []
        if type(card_num) == int:
            if ages == 1:
                to_return.append(self.age1_cards.at[card_num, 'Name'])
            elif ages == 2:
                to_return.append(self.age2_cards.at[card_num, 'Name'])
            elif ages == 3:
                to_return.append(self.age3_cards.at[card_num, 'Name'])

        else:
            for i in range(len(card_num)):
                if ages[i] == 1:
                    to_return.append(self.age1_cards.at[card_num[i], 'Name'])
                elif ages[i] == 2:
                    to_return.append(self.age2_cards.at[card_num[i], 'Name'])
                elif ages[i] == 3:
                    to_return.append(self.age3_cards.at[card_num[i], 'Name'])

        return to_return

    #checks if everyone has drafted
    def check_all_draft(self):
        if len(self.player_list) >= 2:
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
            self.player_list[i].add_to_hand(self.drafted_cards[i], self.current_age)

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
            for i in range(len(self.player_list)):
                self.player_list[i].hand.sort(key=lambda tup: tup[0])
                temp_hand = np.asarray(self.player_list[i].get_hand())

                hand_num = np.zeros(len(temp_hand), dtype=np.int32)
                hand_ages = np.zeros(len(temp_hand), dtype=np.int32)

                for j in range(len(temp_hand)):
                    hand_num[j] = temp_hand[j][0]
                    hand_ages[j] = temp_hand[j][1]
                
                self.final_hand_str.append(self.num_card_concatenator(hand_num,
                        self.card_name_gen(hand_ages, hand_num), hand_ages))

            return True
        else:
            self.draftable_cards = self.draftable_cards.tolist()
            return False

    def ragnorok(self, num):
        x = []
        for i in range(len(self.board.provinces)):
            if len(self.board.provinces[i].get_name()) > 3 and self.board.provinces[i].get_rag() == False:
                x.append(i)

        rag = random.sample(x, num)

        for i in range(len(rag)):
            self.kill_all(self.board.provinces[i])
            self.board.provinces[i].set_ragnorok()

    #provides the initial hands per age
    def start_age(self, age):
        if self.draft_phase != False:
            return -1

        for i in range(len(self.player_list)):
            if len(self.player_list[i].get_hand()) > 1:
                return None

        if age == 1:
            self.ragnorok(5 - len(self.player_list))

        self.draft_phase = True
        if len(self.player_list) >= 2:
            self.draftable_cards = copy.deepcopy(self.gen_hands(age))
            self.current_age = copy.copy(age)
            generated_hands = []

            for i in range(len(self.draftable_cards)):
                self.draftable_cards[i] = np.sort(self.draftable_cards[i])
                
                ages = np.zeros(8, dtype=np.int32)
                ages.fill(self.current_age)
                hand = self.card_name_gen(ages, self.draftable_cards[i])
                generated_hands.append(self.num_card_concatenator(self.draftable_cards[i], hand, ages))

            return generated_hands
        else:
            return []

    #advances draft and accepts card inputs
    def draft(self, c_num, player):
        card_drafted = False
        for i in range(len(self.player_list)):
            if player == self.player_list[i].get_player_object():
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

                        ages = np.zeros(8, dtype=np.int32)
                        ages.fill(self.current_age)
                        hand = self.card_name_gen(ages, self.draftable_cards[i])
                        
                        to_return.append(self.num_card_concatenator(self.draftable_cards[i], hand, ages))
                    return to_return

                else:
                    to_return = []
                    for i in range(len(self.final_hand_str)):
                        to_return.append(self.final_hand_str[i])

                    self.drafted_cards.clear()
                    self.draftable_cards = []
                    self.final_hand_str.clear()
                    self.draft_phase = False

                    for i in range(len(self.player_list)):
                        self.drafted_cards.append(-1)

                    return to_return
