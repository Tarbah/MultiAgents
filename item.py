import position


class item:

    def __init__(self, x,y,level, index):
         self.position = position.position(x,y)
         self.loaded = False
         self.level = level
         self.index = index

    def get_position(self):
        return (self.position.x, self.position.y)

     

  
