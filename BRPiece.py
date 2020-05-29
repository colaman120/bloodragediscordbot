from game import Piece

class BRPiece(Piece):
    def __init__(self, owner, set_name):
        super().__init__(owner)
        self.name = set_name
        self.on_board = False
        self.dead = False
        self.type = []
        self.strength = 0

        if self.name == 'warrior':
            self.strength = 1
        elif self.name == 'ship':
            self.strength = 2
        elif self.name == 'leader':
            self.strength = 3
        elif self.name == 'troll':
            self.strength = 2
        elif self.name == 'dwarf chieftain':
            self.strength = 2
        elif self.name == 'mountain giant':
            self.strength = 3
        elif self.name == 'garm':
            self.strength = 2
        elif self.name == 'valkyrie':
            self.strength = 2
        elif self.name == 'dark elf':
            self.strength = 1
        elif self.name == 'wolfman':
            self.strength = 3
        elif self.name == 'frost giant':
            self.strength = 4
        elif self.name == 'soldier of hel':
            self.strength = 3
        elif self.name == 'mystic troll':
            self.strength = 2
        elif self.name == 'sea serpent':
            self.strength = 3
        elif self.name == 'hildisvini':
            self.strength = 1
        elif self.name == 'fire giant':
            self.strength = 4
        elif self.name == 'nidhoggr':
            self.strength = 2
        elif self.name == 'volur witch':
            self.strength = 3
        elif self.name == 'ymir':
            #TODO: fix based on yggdrasil
            self.strength = 1

        if self.name == 'warrior':
            self.type.append('warrior')
        elif self.name == 'ship':
            self.type.append('ship')
        elif self.name == 'leader':
            self.type.append('leader')
        elif self.name == 'mountain giant':
            self.type.append('leader')
            self.type.append('monster')
        elif self.name == 'sea serpent':
            self.type.append('ship')
            self.type.append('monster')
        else:
            self.type.append('monster')
    
    def kill(self):
        self.dead = True

    def revive(self):
        self.dead = False

    def get_on_board(self):
        return self.on_board

    def get_health(self):
        return self.dead

    def get_type(self):
        return self.type

    def get_strength(self):
        return self.strength
    
    def set_on_board(self):
        self.on_board = True
    
    def take_off_board(self):
        self.on_board = False

    def get_name(self):
        return self.name

    def set_strength(self, new_strength):
        self.strength = new_strength