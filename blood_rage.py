import os
import random
import numpy as np
import pandas
import copy
from game import *

class BloodRage(BoardGame):
    def __init__(self):
        super.__init__('br')
    #class BoardState:

    class BRPlayer(Player):
        #constructor for the player class
        def __init__(self, set_player):            
            super.__init__(set_player)

            self.rage = 6
            self.axes = 3
            self.horns = 4
            self.clan_uc = [(0, 0), (0, 0), (0, 0)]
            self.monster_uc = [(0, 0), (0, 0)]
            self.warrior_uc = (0, 0)
            self.leader_uc = (0, 0)
            self.ship_uc = (0, 0)
            self.glory = 0

        #changes the rage clan stat of the current player
        def change_rage(self, delta):
            self.rage += delta

        #changes the axes clan stat of the current player
        def change_axes(self, delta):
            self.axes += delta
        
        #changes the horns clan stat of the current player
        def change_horns(self, delta):
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
