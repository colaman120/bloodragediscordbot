import os
import random
import numpy as np
import pandas
import copy
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

        def get_quests(self):
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

    #returns the current hand of the player
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

    #takes a card that is input by the player and places it in the slot as designated by the player
    #for leader, ship, and warrior cards, the slot parameter is unused
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
        card_cost = ''

        if age == 1:
            card_type = self.age1_cards.at[card, 'Card Type']
            card_name = self.age1_cards.at[card, 'Name']
            card_cost = self.age1_cards.at[card, 'Rage']
        elif age == 2:
            card_type = self.age2_cards.at[card, 'Card Type']
            card_name = self.age2_cards.at[card, 'Name']
            card_cost = self.age2_cards.at[card, 'Rage']
        elif age == 3:
            card_type = self.age3_cards.at[card, 'Card Type']
            card_name = self.age3_cards.at[card, 'Name']
            card_cost = self.age3_cards.at[card, 'Rage']
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

        if card_name != 'Dwarf Chieftain' and card_name != 'Soldier of Hel':
            bad_chars = [';', ':', '!', "*"] 
            for i in bad_chars: 
                card_cost = card_cost.replace(i, '')
            
            card_cost = int(card_cost)
            
            player_upgrades = self.player_list[index].get_clan_uc()
            for i in player_upgrades:
                if i == (8, 1) and card_cost > 0:
                    card_cost -= 1

            self.player_list[index].change_current_rage(card_cost * -1)

        self.remove_card(card, age, player)
        return 4

    #returns all upgrade cards that a player has in a format that is read by the bot
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

    #summons a unit onto self.board
    def summon_unit(self, player, unit, province):
        found, index = self.find_player(player)
        if found == False:
            return 0
        
        if self.player_list[index].get_current_rage() <= 0:
            return -1

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
        self.player_list[index].units[piece_idx].set_on_board()
        return 7

    #kills a unit specified by the player
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

    #kills all units in a province
    def kill_all(self, province_idx):
        piece_list = self.board.get_provinces()[province_idx].get_piece_list()
        for i in range(len(piece_list) - 1, -1 , -1):
            piece_list[i].kill()
            dead_piece = self.board.provinces[province_idx].piece_list.pop(i)
            self.board.valhalla.append(dead_piece)

    #allows players to move as many of one type of unit as they want from one province to another
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

    #performs a random num gen based on the provinces that have yet to be ragnoroked 
    #based on the provinces that have already been ragnoroked due to the number of players
    def rag_check(self):
        x = np.arange(8)
        y = []
        for i in range(8):
            if self.board.get_provinces()[i].get_rag() == False:
                y.append(x[i])
        
        result = np.random.choice(y, 3, replace=False)
        return result

    #removes a card from ones hand
    def remove_card(self, card, age, player):
        found, index = self.find_player(player)
        if found:
            return self.player_list[index].remove_card(card, age)
        else: 
            return 2

    #returns a board that is parsed and displayed by the bot
    def display_board(self):
        to_return = []
        province_list = self.board.get_provinces()
        for i in range(len(province_list)):
            province = []
            province.append(province_list[i].get_name().capitalize())
            if province_list[i].get_pillage_reward()[0] == 0:
                province.append('Rage')
            elif province_list[i].get_pillage_reward()[0] == 1:
                province.append('Axes')
            elif province_list[i].get_pillage_reward()[0] == 2:
                province.append('Horns')
            else:
                province.append('5 Glory')
            province.append(province_list[i].get_rag())
            province.append(province_list[i].get_piece_list())
            to_return.append(province)
        return to_return

    #returns a single province that is parsed and displayed by the bot
    def display_province(self, province):
        to_return = []
        found, province_idx = self.find_province(province.lower())
        temp_prov = self.board.get_provinces()[province_idx]
        if found:
            to_return.append(temp_prov.get_sub())
            to_return.append(temp_prov.get_rag())
            to_return.append(temp_prov.get_cap())
            if province_idx > 8:
                to_return.append('None')
            elif temp_prov.get_pillage_reward()[0] == 0:
                to_return.append('Rage')
            elif temp_prov.get_pillage_reward()[0] == 1:
                to_return.append('Axes')
            elif temp_prov.get_pillage_reward()[0] == 2:
                to_return.append('Horns')
            else:
                to_return.append('5 Glory')
            to_return.append(temp_prov.get_piece_list())
        return to_return

    #returns a list of the pillage rewards for each province
    def pillage_rewards(self):
        to_return = []
        for i in range(8):
            if self.board.get_provinces()[i].get_rag():
                to_return.append('Ragnoroked')
            elif self.board.get_provinces()[i].get_pillage_reward()[0] == 0:
                to_return.append('Rage')
            elif self.board.get_provinces()[i].get_pillage_reward()[0] == 1:
                to_return.append('Axes')
            elif self.board.get_provinces()[i].get_pillage_reward()[0] == 2:
                to_return.append('Horns')
            else:
                to_return.append('5 Glory')
        return to_return

    #returns a list of all units in valhalla
    def show_valhalla(self):
        return self.board.get_valhalla()
    
    #allows a player to change their rage
    def change_rage(self, delta, player):
        found, index = self.find_player(player)
        if found:
            self.player_list[index].change_current_rage(delta)
            return True
        return False

    def get_current_rage(self, player):
        found, index = self.find_player(player)
        if found:
            return self.player_list[index].get_current_rage()
        else:
            return -1

    def check_val_summon(self, player):
        found, index = self.find_player(player)
        if found:
            clan_upgrades = self.player_list[index].get_clan_uc()
            for card in clan_upgrades:
                if card == (7, 3):
                    return True

        return False

    def get_quests(self, player):
        found, index = self.find_player(player)
        if found:
            quest_list = self.player_list[index].get_quests()
            to_return = []
            for i in range(len(quest_list)):
                to_return.append(self.card_name_gen(quest_list[i][1], quest_list[i][0])[0])
            return to_return
        else:
            return -1

    def add_quest(self, age, card, player):
        found, index = self.find_player(player)
        if found:
            if self.player_list[index].get_current_rage() <= 0:
                return -1
            card_found = False
            player_hand = self.player_list[index].get_hand()
            for i in range(len(player_hand)):
                if age == player_hand[i][1] and card == player_hand[i][0]:
                    card_found = True
                    break
            
            if card_found == False:
                return 0
            
            player_quests = self.player_list[index].get_quests()
            if len(player_quests) == 0:
                self.player_list[index].set_quest(card, age)
                return 2
            else:
                card_name = self.card_name_gen(age, card)[0]
                quest_count = 0
                for i in range(len(player_quests)):
                    if self.card_name_gen(player_quests[i][1], player_quests[i][0])[0] == card_name:
                        quest_count += 1
                    
                    if quest_count > 2:
                        return 1
                
                self.player_list[index].set_quest(card, age)
                self.player_list[index].remove_card(card, age)
                return 2
        else:
            return 3
           
    def end_age(self, province):
        for i in range(len(self.player_list)):
            if len(self.player_list[i].get_hand()) > 1:
                return 0
        
        quests = self.check_completed_quests()
        found, index = self.find_province(province)
        if found:
            self.rag(province)
        else:
            return 1
        
        release = self.show_valhalla()
        to_return = []
        to_return.append(quests)
        to_return.append(release)
        for unit in self.board.valhalla:
            unit.revive()
        
        return to_return
        
    def rag(self, province):
        province = province.lower()
        found, province_idx = self.find_province(province)
        if found == False:
            return 0
        temp_province = self.board.get_provinces()[province_idx]

        if temp_province.get_rag():
            return 1
        piece_list = copy.deepcopy(temp_province.get_piece_list())
        
        if province_idx == 1 or province_idx == 2:
            piece_list += copy.deepcopy(self.board.get_provinces()[9].get_piece_list())
            self.kill_all(9)
        elif province_idx == 0 or province_idx == 4:
            piece_list += copy.deepcopy(self.board.get_provinces()[10].get_piece_list())
            self.kill_all(10)
        elif province_idx == 3 or province_idx == 5:
            piece_list += copy.deepcopy(self.board.get_provinces()[11].get_piece_list())
            self.kill_all(11)
        elif province_idx == 6 or province_idx == 7:
            piece_list += copy.deepcopy(self.board.get_provinces()[12].get_piece_list())
            self.kill_all(12)
        
        self.kill_all(province_idx)

        print(piece_list)
        if len(piece_list) == 0:
            return 3
        else:
            for i in range(len(piece_list)):
                temp_player = piece_list[i].get_owner()
                found, player_idx = self.find_player(temp_player)
                if self.current_age == 1:
                    self.player_list[player_idx].change_glory(2)
                elif self.current_age == 2:
                    self.player_list[player_idx].change_glory(3)
                elif self.current_age == 3:
                    self.player_list[player_idx].change_glory(4)
                else:
                    return 2
            
            return 3
        
    def check_completed_quests(self):
        completed_quests = []
        for i in range(len(self.player_list)):
            completed_quests.append([]) 
            for j in range(len(self.player_list[i].get_quests())):
                completed_quests[i].append(False)
                quest_name = self.card_name_gen(self.player_list[i].get_quests()[j][1], self.player_list[i].get_quests()[j][0])[0]
                if quest_name == 'Alfheim Quest':
                    alf1 = self.calculate_strength('gimle')
                    alf2 = self.calculate_strength('anolang')
                    if alf1 == i or alf2 == i:
                        completed_quests[i][j] = True
                elif quest_name == 'Jotunheim Quest':
                    jot1 = self.calculate_strength('utgard')
                    jot2 = self.calculate_strength('horgr')
                    jot3 = self.calculate_strength('muspelheim')
                    if jot1 == i or jot2 == i or jot3 == i:
                        completed_quests[i][j] = True
                elif quest_name == 'Manheim Quest':
                    man1 = self.calculate_strength('myrkulor')
                    man2 = self.calculate_strength('elvagar')
                    man3 = self.calculate_strength('angerboda')
                    if man1 == i or man2 == i or man3 == i:
                        completed_quests[i][j] = True
                elif quest_name == 'Glorious Death':
                    temp_val = self.board.get_valhalla()
                    count = 0
                    for piece in temp_val:
                        if piece.get_owner() == self.player_list[i]:
                            count += 1
                    if count >= 4:
                        completed_quests[i][j] = True
                elif quest_name == 'Yggdrasil Quest':
                    ygg = self.calculate_strength('yggdrasil')
                    if ygg == i:
                        completed_quests[i][j] = True
                elif quest_name == 'Widespread':
                    p1 = self.calculate_strength('gimle')
                    p2 = self.calculate_strength('anolang')
                    p3 = self.calculate_strength('utgard')
                    p4 = self.calculate_strength('horgr')
                    p5 = self.calculate_strength('muspelheim')
                    p6 = self.calculate_strength('myrkulor')
                    p7 = self.calculate_strength('elvagar')
                    p8 = self.calculate_strength('angerboda')
                    p9 = self.calculate_strength('yggdrasil')

                    count = 0
                    if p1 == i:
                        count += 1
                    elif p2 == i:
                        count += 1
                    elif p3 == i:
                        count += 1
                    elif p4 == i:
                        count += 1
                    elif p5 == i:
                        count += 1
                    elif p6 == i:
                        count += 1
                    elif p7 == i:
                        count += 1
                    elif p8 == i:
                        count += 1
                    elif p9 == i:
                        count += 1
                    if count >= 2:
                        completed_quests[i][j] = True
        return completed_quests
                                    
    def calculate_strength(self, province):
        province = province.lower()
        found, province_idx = self.find_province(province)
        if found == False:
            return -2
        
        strengths = []
        warrior_count = []
        wucs = []
        for i in range(len(self.player_list)):
            strengths.append(0)
            warrior_count.append(0)
            brothers = False
            experts = False
            masters = False
            wuc = self.player_list[i].get_warrior_uc()
            if wuc == (5, 1) or wuc == (37, 1):
                brothers = True
                experts = False
                masters = False
            elif wuc == (4, 2) or wuc == (36, 2):
                brothers = False
                experts = True
                masters = False
            elif wuc == (4, 3) or wuc == (36, 3):
                brothers = False
                experts = False
                masters = True
            wucs.append([brothers, experts, masters])
        
        temp_province = self.board.get_provinces()[province_idx]
        piece_list = temp_province.get_piece_list()
        
        if province_idx == 1 or province_idx == 2:
            piece_list += self.board.get_provinces()[9].get_piece_list()

        elif province_idx == 0 or province_idx == 4:
            piece_list += self.board.get_provinces()[10].get_piece_list()

        elif province_idx == 3 or province_idx == 5:
            piece_list += self.board.get_provinces()[11].get_piece_list()

        elif province_idx == 6 or province_idx == 7:
            piece_list += self.board.get_provinces()[12].get_piece_list()

        for piece in piece_list:
            found, player_idx = self.find_player(piece.get_owner())
            strengths[player_idx] += piece.get_strength()

            if piece.get_type() == 'warrior':
                warrior_count[player_idx] += 1

            if piece.get_name() == 'dark elf' and province_idx == 8:
                strengths[player_idx] += 2
        
        for i in range(len(strengths)):
            if wucs[i][1]:
                strengths[i] += warrior_count[i]
            elif wucs[i][0] or wucs[i][2]:
                pairs = int(warrior_count[i]/2)
                if wucs[i][0]:
                    strengths[i] += pairs
                else:
                    strengths[i] += pairs * 4
        
        greatest_idx = -1
        max_strength = 0
        
        for i in range(len(strengths)):
            if strengths[i] > max_strength:
                max_strength = strengths[i]
                greatest_idx = i
            elif strengths[i] == max_strength:
                greatest_idx = -1
        
        return greatest_idx

    #returns whether or not a player was found and at what index they were found
    def find_player(self, player_to_find):
        index = -1

        for i in range(len(self.player_list)):
            if player_to_find == self.player_list[i].get_player_object():
                index = i
                return True, index
        return False, index

    #returns whether or not a province was found and at what index that province was found at
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

    #removes the drafted cards from the draftable caards
    def remove_cards(self):
        self.draftable_cards = np.asarray(self.draftable_cards)
        for i in range(np.size(self.draftable_cards, 0)):
            self.draftable_cards[i] = np.roll(self.draftable_cards[i],
                self.draftable_cards[i].size - np.where(self.draftable_cards[i] == self.drafted_cards[i])[0][0])

        self.draftable_cards = np.delete(self.draftable_cards, 0, 1)
        self.draftable_cards = self.draftable_cards.tolist()

    #adds cards that were drafted into players hands
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

    #begins the game by ragnoroking however provinces must be ragnoroked
    def game_start_ragnorok(self, num):
        x = np.arange(8).tolist()

        rag = random.sample(x, num)

        for i in range(len(rag)):
            self.kill_all(rag[i])
            self.board.provinces[rag[i]].set_ragnorok()

    #provides the initial hands per age
    def start_age(self, age):
        if self.draft_phase != False:
            return -1

        for i in range(len(self.player_list)):
            if len(self.player_list[i].get_hand()) > 1:
                return None

        if age == 1:
            self.game_start_ragnorok(5 - len(self.player_list))

        if len(self.player_list) >= 2:
            self.draft_phase = True
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
