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
                self.p_bank = 1
                self.p_stockpile = 1
                self.scepter = False
                self.throne = False
                self.crown = False
                self.hand = [0, 1, 2, 3]
                self.exhaust = []
                self.played = [-1, -1]

            def get_banked(self):
                return self.banked
            
            def get_stockpile(self):
                return self.stockpile

            def get_pstock(self):
                return self.p_stockpile
            
            def get_pbank(self):
                return self.p_bank

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
    
            def purchase(self, delta):
                if delta > self.stockpile:
                    difference = delta - self.stockpile
                    
                    if self.banked < difference:
                        return False
                    else:
                        self.banked -= difference
                        self.stockpile = 0
                        return True
                
                else:
                    self.stockpile -= delta
                    return True

            def all_cards_played(self):
                return self.played[0] != -1 and self.played[1] != -1
    
    def __init__(self):
        super().__init__('vp')
        self.deck = pandas.read_csv('data/newvp.csv', index_col='Num')
        #self.shop = pandas.read_csv('data/newvp.csv', index_col='Num').drop([0, 1, 2, 3], axis=0)
        numbers = np.arange(start=4, stop=28)
        self.shop_list = np.random.choice(numbers, 4, replace=False).tolist()
        numbers = numbers.tolist()

        for number in self.shop_list:
            if number in numbers:
                numbers.remove(number)

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

    def find_played_card(self, card_num):
        for i in range(len(self.player_list)):
            for j in range(2):
                if self.player_list[i].played[j] == card_num:
                    return True, i, j
        
        return False, -1, -1

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

    def hand_to_text(self, list_of_nums):
        #list_of_names = []
        to_return = []
        for card_num in list_of_nums:
            temp = self.deck.at[card_num, 'Name'].capitalize()
            to_return.append(card_num + ": " + temp)

        return to_return

    def buy_card(self, player, card_num, cost):
        found, idx = self.find_player(player)
        total_turnips = self.player_list[idx].get_banked() + self.player_list[idx].get_stockpile()

        if found == False:
            return False

        elif card_num not in self.shop_list:
            return False
    
        elif cost > total_turnips:
            return False

        else: 
            self.player_list[idx].purchase(cost)
            self.player_list[idx].hand.append(card_num)
            return True
        
    def get_money_total(self, player):
        found, idx = self.find_player(player)
        if found == False:
            return False
        
        else: 
            return self.player_list[idx].get_banked(), self.player_list[idx].get_stockpile()

    def get_relic_score(self):
        to_return = []

        for player in self.player_list:
            relic_count = 0
            if player.get_scepter():
                relic_count += 1
            if player.get_crown():
                relic_count += 1
            if player.get_throne():
                relic_count += 1
            to_return.append(relic_count)
        return to_return

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

# covered -, +, +*, O, B, S, S*, C, E*, R, E
# need to cover T
# need to add opp_card number or find some other way to do it with out specifically requiring it, would
# need to be another method, not impossible

    def run_code(self, num_card, player_idx, opp_idx, opp_color):
        code = self.deck.at[num_card, opp_color.capitalize()]

        pointer_idx = 0
        while (pointer_idx < len(code)):
            if code[pointer_idx] =='-':
                return

            if code[pointer_idx] == '+':
                if code[pointer_idx + 1] == '*':
                    return
                else:
                    self.add_turnips(int(code[pointer_idx + 1]), player_idx)
                pointer_idx += 2
                continue

            if code[pointer_idx] == 'O':
                self.add_turnips(int(code[pointer_idx + 1]), opp_idx)
                pointer_idx += 2
                continue

            if code[pointer_idx] == 'B':
                self.bank_turnips(int(code[pointer_idx] + 1), player_idx)
                pointer_idx += 2
                continue
                
            if code[pointer_idx] == 'S':
                banked = False
                to_steal = 0
                if code[pointer_idx + 1] == '*':
                    banked = True
                    to_steal = int(code[pointer_idx + 2])
                    pointer_idx += 3
                
                elif code[pointer_idx + 1] != '-':
                    to_steal = int(code[pointer_idx + 1])
                    pointer_idx += 2
                
                else:
                    negative_steal = code[pointer_idx:pointer_idx + 1]
                    to_steal = int(negative_steal)
                    pointer_idx += 2
                
                self.steal_turnips(to_steal, player_idx, opp_idx, banked)
            
            if code[pointer_idx] == 'C':
                self.add_turnips(int(code[pointer_idx + 1]), player_idx)
                pointer_idx += 2
                continue

            if code[pointer_idx] == 'E':
                opp_card = True
                if code[pointer_idx + 1] == '*':
                    opp_card = False
                    self.exhaust_card(num_card, player_idx, opp_idx, opp_card)
                    pointer_idx += 2
                else:
                    self.exhaust_card(num_card, player_idx, opp_idx, opp_card)
                    pointer_idx += 1
                continue
                
            if code[pointer_idx] == 'R':
                cost = 1
                if code[pointer_idx + 1].isnumeric():
                    cost = 0
                    pointer_idx += 1

                self.buy_relic(player_idx, cost)
                pointer_idx += 1
                continue

            if code[pointer_idx] == 'T':
                self.trade_card(player_idx, opp_idx, num_card)
                pointer_idx += 1
                continue

    #need to check turnip amounts before taking away and stuff
    def add_turnips(self, delta, player_idx):
        self.player_list[player_idx].stockpile += delta

    def bank_turnips(self, delta, player_idx):
        player = self.player_list[player_idx]

        if len(self.player_list) > 2:
            if delta > 5 - player.bank:
                delta = 5 - player.bank
            
        elif len(self.player_list) == 2:
            if delta > 4 - player.bank:
                delta = 4 - player.bank
        
        self.player_list[player_idx].stockpile -= delta
        self.player_list[player_idx].stockpile += delta

    def steal_turnips(self, delta, player_idx, opp_idx, banked):
        turnips_stolen = 0

        if delta > self.player_list[opp_idx].get_pstock():
            turnips_stolen += self.player_list[opp_idx].get_pstock()
            self.player_list[opp_idx].stockpile = 0

            if banked and delta - turnips_stolen > 0:
                remaining = delta - turnips_stolen
                if self.player_list[opp_idx].get_pbank() < remaining:
                    turnips_stolen += self.player_list[opp_idx].get_pbank()
                    self.player_list[opp_idx].bank = 0
                
                else:
                    turnips_stolen += self.player_list[opp_idx].get_pbank() - remaining
                    self.player_list[opp_idx].bank -= remaining
            
            else:
                turnips_stolen = delta
                self.player_list[opp_idx].stockpile -= delta
            
        self.player_list[player_idx].stockpile += turnips_stolen

    def exhaust_card(self, card_num, player_idx, opp_idx, opp_card):
        if opp_card:
            found, temp, card_pos = self.find_played_card(card_num)
            if found and card_pos == 1:
                self.player_list[opp_idx].exhaust_card(self.player_list[opp_idx].played[0])

            elif found and card_pos == 0:
                self.player_list[opp_idx].exhaust_card(self.player_list[opp_idx].played[1])

        elif opp_card == False:
            self.player_list[player_idx].exhaust_card(card_num)
    
    def buy_relic(self, player_idx, cost):
        player = self.player_list[player_idx]
        total_turnips = player.get_banked() + player.get_stockpile()

        if len(self.player_list) == 2:
            if player.get_scepter() == False and total_turnips >= 6:
                player.purchase(6)
                player.buy_scepter()

            elif player.get_scepter() and player.get_crown() == False and total_turnips >= 7:
                player.purchase(7)
                player.buy_crown()
            
            elif player.get_scepter() and player.get_crown() and player.get_throne() == False and total_turnips >= 8:
                player.purchase(8)
                player.buy_throne()

        else:
            if player.get_scepter() == False and total_turnips >= 8:
                player.purchase(8)
                player.buy_scepter()

            elif player.get_scepter() and player.get_crown() == False and total_turnips >= 9:
                player.purchase(9)
                player.buy_crown()
            
            elif player.get_scepter() and player.get_crown() and player.get_throne() == False and total_turnips >= 10:
                player.purchase(10)
                player.buy_throne()

    def trade_card(self, player_idx, opp_idx, card_num):
        found, temp, player_card_pos = self.find_played_card(card_num)
        opp_card_pos = -1

        if player_card_pos == 0:
            opp_card_pos = 1
        elif player_card_pos == 1:
            opp_card_pos = 0

        opp_card = self.player_list[opp_idx].played[opp_card_pos]
        player_card = self.player_list[player_idx].played[player_card_pos]

        player_card, opp_card = opp_card, player_card

    def update_p(self):
        for player in self.player_list:
            player.p_bank = player.get_banked()
            player.p_stockpile = player.get_stockpile()

    def unexhaust_all(self):
        for player in self.player_list:
            player.unexhaust_card()

    def clear_played(self):
        for player in self.player_list:
            for i in player.played:
                i  = -1

    def take_turn(self):
        if self.check_all_play():
            g_nums, g_player_idx, g_opp, g_opp_color = self.determine_matchups('green')
            b_nums, b_player_idx, b_opp, b_opp_color = self.determine_matchups('blue')
            r_nums, r_player_idx, r_opp, r_opp_color = self.determine_matchups('red')
            y_nums, y_player_idx, y_opp, y_opp_color = self.determine_matchups('yellow')
            shepard_check, s_player_idx = self.check_shepard(g_player_idx, g_nums)
            #unexhaust any exhausted cards and readd them into hand
            self.unexhaust_all()

            if len(g_nums) != 0:
                for i in range(len(g_nums)):
                    self.run_code(g_nums[i], g_player_idx[i], g_opp[i], g_opp_color[i])
            
            self.update_p()
            
            if len(b_nums) != 0:
                for i in range(len(b_nums)):
                    self.run_code(b_nums[i], b_player_idx[i], b_opp[i], b_opp_color[i])

            self.update_p()

            if len(r_nums) != 0:
                for i in range(len(r_nums)):
                    self.run_code(r_nums[i], r_player_idx[i], r_opp[i], r_opp_color[i])
            
            self.update_p()

            if len(y_nums) != 0:
                for i in range(len(y_nums)):
                    self.run_code(y_nums[i], y_player_idx[i], y_opp[i], y_opp_color[i])
            
            self.update_p()

            if shepard_check:
                self.player_list[s_player_idx].stockpile += 4

            self.update_p()
            # update shop

            self.clear_played()
           
        else:
            return False