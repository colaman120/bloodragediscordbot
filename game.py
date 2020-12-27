class BoardGame:
    def __init__(self, set_id):
        self.game_id = set_id
        self.player_list = []
        self.game_over = False

    def get_game_id(self):
        return self.game_id

    def get_player_list(self):
        return self.player_list
    
    #remove a player from the game
    def remove_player(self, player_un, player_discrim):
        for i in range(len(self.player_list)):
            if self.player_list[i].get_player_object().name == player_un and self.player_list[i].get_player_object().discriminator == player_discrim:
                self.player_list.pop(i)
                return True
        return False

class Player:
    def __init__(self, set_player):
        self.player_object = set_player

    def get_player_object(self):
        return self.player_object

class Piece:
    def __init__(self, owner):
        self.player = owner

    def get_owner(self): 
        return self.player

    