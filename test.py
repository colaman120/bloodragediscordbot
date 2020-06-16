from blood_rage import BloodRage
import numpy as np


x = [(7, 1), (8, 1), (9, 1), (6, 1), (5, 1), (1, 1), (2, 1)]

game = BloodRage()
game.add_player('p1')
game.player_list[0].set_hand(x)
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 7, 1, 'p1')
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 8, 2, 'p1')
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 9, 3, 'p1')
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 6, 1, 'p1')
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 5, 1, 'p1')
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 1, 2, 'p1')
print("Remaining rage: " + str(game.player_list[0].get_current_rage()))
game.set_upgrades(1, 2, 1, 'p1')
print("remaining rage: " + str(game.player_list[0].get_current_rage()))
print(game.get_upgrades('p1'))
#print(game.get_current_hand('p1'))


# game = BloodRage()
# game.add_player('p1')
# game.add_player('p2')
# game.summon_unit('p1', 'leader', 'anolang')
# game.summon_unit('p1', 'warrior', 'anolang')
# game.summon_unit('p1', 'warrior', 'anolang')
# game.summon_unit('p1', 'warrior', 'myrkulor')
# result = game.summon_unit('p1', 'warrior', 'myrkulor')
# print(result)
# #print(game.board.get_provinces()[3].get_piece_list())
# print('Anolang')
# for i in range(len(game.board.get_provinces()[3].get_piece_list())):
#    print(game.board.get_provinces()[3].get_piece_list()[i].get_name())

# print('Myrkulor')
# for i in range(len(game.board.get_provinces()[0].get_piece_list())):
#    print(game.board.get_provinces()[0].get_piece_list()[i].get_name())

# x = '2*'
# bad_chars = [';', ':', '!', "*"] 
# for i in bad_chars : 
#     x = x.replace(i, '') 
# print(int(x))