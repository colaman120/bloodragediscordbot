from blood_rage import BloodRage

'''
x = [(7, 1), (8, 1), (9, 1), (6, 1), (0, 1), (1, 1), (2, 1)]


game.player_list[0].set_hand(x)
game.set_upgrades(1, 7, 1, 'p1')
game.set_upgrades(1, 8, 2, 'p1')
game.set_upgrades(1, 9, 3, 'p1')
game.set_upgrades(1, 6, 1, 'p1')
game.set_upgrades(1, 0, 1, 'p1')
game.set_upgrades(1, 1, 2, 'p1')
print(game.get_upgrades('p1'))
game.set_upgrades(1, 2, 1, 'p1')
print(game.get_upgrades('p1'))
#print(game.get_current_hand('p1'))
'''

game = BloodRage()
game.add_player('p1')
game.add_player('p2')
game.summon_unit('p1', 'leader', 'anolang')
game.summon_unit('p1', 'ship', 'anolang')
game.summon_unit('p1', 'warrior', 'anolang')
#print(game.board.get_provinces()[3].get_piece_list())
for i in range(len(game.board.get_provinces()[3].get_piece_list())):
    print(game.board.get_provinces()[3].get_piece_list()[i].get_name())