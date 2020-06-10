class Province:
    def __init__(self, set_name, set_cap, set_subsec):
        self.name = set_name
        self.capacity = set_cap
        self.subsection = []
        for i in set_subsec:
            self.subsection.append(i)
        self.piece_list = []
        self.rag_status = False
        self.pillage_reward = []

    def get_rag(self):
        return self.rag_status

    def get_piece_list(self):
        return self.piece_list

    def get_cap(self):
        return self.capacity

    def get_name(self):
        return self.name
        
    def get_sub(self):
        return self.subsection

    def set_ragnorok(self):
        self.rag_status = True

    def get_current_cap(self):
        return len(self.piece_list)

    def get_pillage_reward(self):
        return self.pillage_reward

    # 0 = rage
    # 1 = axes
    # 2 = horns
    # 3 = 5 glory
    def set_pillage_reward(self, set_reward):
        self.pillage_reward.append(set_reward)
