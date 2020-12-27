from blood_rage import BloodRage
from villpill import VillPill
import numpy as np


# x = [(7, 1), (8, 1), (9, 1), (6, 1), (5, 1), (1, 1), (2, 1)]

# game = BloodRage()
# game.add_player('p1')
# game.add_player('p2')
# for i in range(8):
#     print(game.board.get_provinces()[i].get_name() + ': ' + str(game.board.get_provinces()[i].get_rag()))
# game.game_start_ragnorok(3)
# for i in range(8):
#     print(game.board.get_provinces()[i].get_name() + ': ' + str(game.board.get_provinces()[i].get_rag()))
# print(game.rag_check())

# game.player_list[0].set_hand(x)
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 8, 1, 'p1')
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 7, 2, 'p1')
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 9, 3, 'p1')
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 6, 1, 'p1')
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 5, 1, 'p1')
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 1, 2, 'p1')
# print("Remaining rage: " + str(game.player_list[0].get_current_rage()))
# game.set_upgrades(1, 2, 1, 'p1')
# print("remaining rage: " + str(game.player_list[0].get_current_rage()))
# print(game.get_upgrades('p1'))
#print(game.get_current_hand('p1'))
# p1 = [(11, 1), (10, 1)]


game = BloodRage()
game.add_player('p1')
game.add_player('p2')
game.current_age = 3
game.player_list[0].set_hand('p1')
game.summon_unit('p1', 'warrior', 'horgr')
game.summon_unit('p1', 'warrior', 'horgr')
game.summon_unit('p1', 'warrior', 'horgr')
game.summon_unit('p1', 'warrior', 'horgr')
# game.add_quest(1, 11, 'p1')
# game.add_quest(1, 10, 'p1')
# print(game.get_quests('p1'))
# print(game.end_age('horgr'))
# print(game.get_glory())
# print(game.board.get_provinces()[6].get_piece_list())
print('Anolang')
for i in range(len(game.board.get_provinces()[6].get_piece_list())):
   print(game.board.get_provinces()[6].get_piece_list()[i].get_name())
print(game.player_list[0].get_current_rage())

print('Myrkulor')
for i in range(len(game.board.get_provinces()[0].get_piece_list())):
   print(game.board.get_provinces()[0].get_piece_list()[i].get_name())

# x = '2*'
# bad_chars = [';', ':', '!', "*"] 
# for i in bad_chars : 
#     x = x.replace(i, '') 
# print(int(x))

#game = VillPill()
#print(game.deck.at[, 'Name'])
