from blood_rage import BloodRage

x = [(7, 1), (8, 1), (9, 1), (6, 1), (0, 1), (1, 1), (2, 1)]

game = BloodRage()
game.add_player('p1')
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