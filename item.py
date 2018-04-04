import position


class item:

    def __init__(self, x,y,level, index):
        self.position = position.position(int(x), int(y))
        self.loaded = False
        self.level = int(level)
        self.index = index
        self.agents_load_item = list()

    def remove_agent(self,agent_x , agent_y):
        for agent_load in self.agents_load_item:
            (al_x , al_y) = agent_load.get_position()
            if al_x == agent_x and al_y == agent_y:
                self.agents_load_item.remove(agent_load)
                return

    def get_position(self):
        return (self.position.x, self.position.y)

    def copy(self):
        (x, y) = self.get_position()

        copy_item = item(x, y, self.level, self.index)

        copy_item.loaded = self.loaded

        return copy_item
        
    def equals(self, other_item):
        (other_x, other_y) = other_item.get_position()
        (x, y) = self.get_position()

        return (other_x == x) and (other_y == y) and\
               other_item.loaded == self.loaded and \
               other_item.level == self.level and \
               other_item.index == self.index
  
