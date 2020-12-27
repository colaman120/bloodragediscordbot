import random
import numpy as np
import pandas
import copy
from game import BoardGame
from game import Player

class VillPill(BoardGame):
    class VPPlayer(Player):
            def __init__(self, set_player):
                super().__init__(set_player)
                self.banked = 1
                self.stockpile = 1
                # self.p_bank = 1
                # self.p_stockpile = 1
                # self.f_stockpile = 1
                self.sceptre = False
                self.throne = False
                self.crown = False
                self.hand = [0, 1, 2, 3]
                self.exhaust = []
                self.played = [-1, -1]

            def get_banked(self):
                return self.banked
            
            def get_stockpile(self):
                return self.stockpile

            # def get_pstock(self):
            #     return self.p_stockpile
            
            # def get_pbank(self):
            #     return self.p_bank
            
            # def get_fstock(self):
            #     return self.f_stockpile

            def get_scepter(self):
                return self.sceptre

            def get_throne(self):
                return self.throne
            
            def get_crown(self):
                return self.crown
            
            def get_hand(self):
                return self.hand
            
            def get_exhaust(self):
                return self.exhaust
            
            def get_played(self):
                return self.played
            
            def change_stockpile(self, delta):
                self.stockpile += delta
            
            def change_fstock(self, delta):
                self.f_stockpile += delta

            def buy_sceptre(self):
                self.sceptre = True
            
            def buy_throne(self):
                self.throne = True
            
            def buy_crown(self):
                self.crown = True
            
            def add_card(self, card_num):
                self.hand.append(card_num)
            
            def exhaust_card(self, card_num):
                self.hand.remove(card_num)
                self.exhaust.append(card_num)

            def unexhaust_card(self):
                for i in self.exhaust:
                    self.hand.append(i)
                self.exhaust.clear()
            
            def play_card(self, card_num, side):
                self.played[side] = card_num

            def move_to_bank(self, num, num_players):
                if num_players == 2:
                    bank_cap = 4
                else:
                    bank_cap = 5
                    
                if num > bank_cap:
                    return False

                if num > self.stockpile:
                    return False

                bank_remaining = bank_cap - self.banked
                if num > bank_remaining:
                    return False

                self.stockpile -= num
                self.banked += num
    
            def all_cards_played(self):
                return self.played[0] != -1 and self.played[1] != -1
    
    def __init__(self):
        super().__init__('vp')
        self.deck = pandas.read_csv('data/newvp.csv', index_col='Num')
        self.shop = pandas.read_csv('data/newvp.csv', index_col='Num').drop([0, 1, 2, 3], axis=0)

    def add_player(self, player_to_add):
        if len(self.player_list) > 6:
            return False

        for i in range(len(self.player_list)):
            if self.player_list[i] == player_to_add:
                return False
            
        new_player = self.VPPlayer(player_to_add)
        self.player_list.append(new_player)
        return True
    
    def find_player(self, player_to_find):
        index = -1

        for i in range(len(self.player_list)):
            if player_to_find == self.player_list[i].get_player_object():
                index = i
                return True, index
        return False, index

    def check_card_in_hand(self, card, player_index):
        for i in self.player_list[player_index].get_hand():
            if i == card:
                return True
        return False

    def play_card(self, player, card, side):
        found, index = self.find_player(player)
        if found:
            if self.check_card_in_hand(card, index):
                self.player_list[index].play_card(card, side)

                if self.check_all_play() == False:
                    return self.deck.at[card, 'Name']
                else:
                    #TODO: Implement card checking and card reading code and methods to automatically play out rounds
                    pass
            else:
                return 1
        else:
            return 2
    
    def check_all_play(self):
        for player in self.player_list:
            if player.get_played()[0] == -1 or player.get_played()[1] == -1:
                return False
        return True

    def check_shepard(self, player_idxs, nums):
        for i in range(len(nums)):
            if nums[i] == 12:
                return True, player_idxs[i]
        return False, -1

    def determine_matchups(self, color):
        card_nums = []
        player_idxs = []
        opp_idxs = []
        opp_colors = []

        for i in range(len(self.player_list)):
            for j in range(len(self.player_list[i].played)):
                if self.deck.at[self.player_list[i].played[j], 'Color'] == color.capitalize():
                    card_nums.append(self.player_list[i].played[j])
                    player_idxs.append(i)

                    if j == 0:
                        opp_idxs.append(i - 1)
                    else:
                        if i != 3:
                            opp_idxs.append(i + 1)
                        else:
                            opp_idxs.append(0)

                    opp_player = self.player_list[opp_idxs[len(opp_idxs)]]
                    opp_card_color = ''
                    if j == 0:
                        opp_card_color = self.deck.at[opp_player.played[1], 'Color']
                    else:
                        opp_card_color = self.deck.at[opp_player.played[0], 'Color']
                    opp_colors.append(opp_card_color)
        
        return card_nums, player_idxs, opp_idxs, opp_colors
        # matchups = []
        # nums = []
        # temp_1 = []
        # temp_2 = []
        # temp_1.append(self.deck.at[self.player_list[len(self.player_list) - 1].get_played()[1], 'Color'])
        # temp_1.append(self.deck.at[self.player_list[0].get_played()[0], 'Color'])
        # temp_2.append(self.deck.at[self.player_list[len(self.player_list) - 1].get_played()[1]])
        # temp_2.append(self.deck.at[self.player_list[0].get_played()[0]])
        # matchups.append(temp_1)
        # nums.append(temp_2)
        # for i in range(len(self.player_list)):
        #     if i != len(self.player_list) - 1:
        #         temp_1 = []
        #         temp_2 = []
        #         temp_1.append(self.deck.at[self.player_list[i].get_played()[1], 'Color'])
        #         temp_1.append(self.deck.at[self.player_list[i + 1].get_played()[0], 'Color'])
        #         temp_2.append(self.deck.at[self.player_list[i].get_played()[1]])
        #         temp_2.append(self.deck.at[self.player_list[i + 1].get_played()[0]])
        #         matchups.append(temp_1)
        #         nums.append(temp_2)
        # return matchups, nums

    def run_code(self, num_card, player_idx, opp_idx, opp_color):
        code = self.deck.at[num_card, opp_color.capitalize()];


    def take_turn(self):
        if self.check_all_play():
            g_nums, g_player_idx, g_opp, g_opp_color = self.determine_matchups('green')
            b_nums, b_player_idx, b_opp, b_opp_color = self.determine_matchups('blue')
            r_nums, r_player_idx, r_opp, r_opp_color = self.determine_matchups('red')
            y_nums, y_player_idx, y_opp, y_opp_color = self.determine_matchups('yellow')
            shepard_check, s_player_idx = self.check_shepard(g_player_idx, g_nums)

            if len(g_nums) != 0:
                for i in range(len(g_nums)):
                    self.run_code(g_nums[i], g_player_idx[i], g_opp[i], g_opp_color[i])
            
            if len(b_nums) != 0:
                for i in range(len(b_nums)):
                    self.run_code(b_nums[i], b_player_idx[i], b_opp[i], b_opp_color[i])

            if len(r_nums) != 0:
                for i in range(len(r_nums)):
                    self.run_code(r_nums[i], r_player_idx[i], r_opp[i], r_opp_color[i])

            if len(y_nums) != 0:
                for i in range(len(y_nums)):
                    self.run_code(y_nums[i], y_player_idx[i], y_opp[i], y_opp_color[i])

            if shepard_check:
                self.player_list[s_player_idx].stockpile += 4
                
        # if self.check_all_play():
        #     matchups, nums = self.determine_matchup()
        #     for i in range(stop=4, step=2):
        #         for j in range(len(matchups)):
        #             if i == 1:
        #                 if matchups[j][1] == 'Green':
        #                     code = self.deck.at[nums[j], matchups[j][0]]
        #                 if matchups[j + 1][0] == 'Green':
        #                     code = self.deck.at[nums[j + 1], matchups[j + 1][1]]
                    
        #             if i == 2:
        #                 if matchups[j][1] == 'Blue':
        #                     code = self.deck.at[nums[j], matchups[j][0]]
        #                 if matchups[j + 1][0] == 'Blue':
        #                     code = self.deck.at[nums[j + 1], matchups[j + 1][1]]

        #             if i == 3:
        #                 if matchups[j][1] == 'Red':
        #                     code = self.deck.at[nums[j], matchups[j][0]]
        #                 if matchups[j + 1][0] == 'Red':
        #                     code = self.deck.at[nums[j + 1], matchups[j + 1][1]]

        #             if i == 4:
        #                 if matchups[j][1] == 'Yellow':
        #                     code = self.deck.at[nums[j], matchups[j][0]]
        #                 if matchups[j + 1][0] == 'Yellow':
        #                     code = self.deck.at[nums[j + 1], matchups[j + 1][1]]
                
        #         for player in self.player_list:
        #             player.p_bank = player.get_banked()
        #             player.p_stockpile = player.get_stockpile()
        #     player.stockpile = player.get_fstock()
        #     player.p_stockpile = player.get_stockpile()
