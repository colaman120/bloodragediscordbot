class BoardGame:
    def __init__(self, set_id):
        self.game_id = set_id
        self.player_list = []
        self.game_over = False

    def get_game_id(self):
        return self.game_id

    def get_player_list(self):
        return self.player_list

class Player:
    def __init__(self, set_player):
        self.player_object = set_player

    def get_player_object(self):
        return self.player_object