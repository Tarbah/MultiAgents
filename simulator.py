# Types for agents are 'L1','L2','F1','F2'
import agent
import position
import a_star
import MCTS
import numpy as np

dx = [1, 0, -1, 0]  # 0: left,  1:up, 2:right  3:down
dy = [0, 1, 0, -1]


class simulator:
    def __init__(self,the_map ,items ,agents,n,m):
        self.the_map = the_map
        self.items = items
        self.agents = agents
        self.memory = position.position(0, 0)
        self.n = n
        self.m = m

    def get_item_by_position(self, x, y):
        for i in range(0, len(self.items)):
            if self.items[i].get_position() == (x,y):
                return i
        return -1

    def get_first_action(self,route):
        # print '~~~~~~~~~~~~~~~~~~~~~~~  route : ' , route
        dir = route[0]
        # print 'dir: ' + dir
        if dir == '0':
            return 'W'
        if dir == '1':
            return 'N'
        if dir == '2':
            return 'E'
        if dir == '3':
            return 'S'

    def items_left(self):
        items_count= 0
        for i in range(0,len(self.items)):
            if not self.items[i].loaded:
                items_count += 1
        return items_count

    def update_map(self,old_pos, new_pos):

        (x, y) = old_pos

        self.the_map[y][x] = 0

        agent_index = self.find_agent_index(old_pos)
        self.agents[0].pos = new_pos

        (x, y) = new_pos

        self.the_map[y][x] = 8  # 8 demonstrate the unknown agent on the map

        return

    def update_map_mcts(self, old_pos, new_pos):

        (x, y) = old_pos

        self.the_map[y][x] = 0

        agent_index = self.find_agent_index(old_pos)
        self.agents[0].pos = new_pos

        (x, y) = new_pos

        self.the_map[y][x] = 9  # 9 demonstrate the main agent on the map

        return

    def find_agent_index (self,pos):
        agents_num = len(self.agents)
        for i in range (0, agents_num):

            if self.agents[i].position == pos :
                return i
        return -1

    def remove_old_destination_in_map(self):

        for y in range(self.m):
            for x in range(self.n):
                xy = self.the_map[y][x]
                if xy == 4:
                    self.the_map[y][x] = 1

    def mark_route_map(self,route,xA,yA,dx,dy):
        x = xA
        y = yA

        if len(route) > 0:
            for i in range(len(route)):
                j = int(route[i])
                x += dx[j]
                y += dy[j]
                self.the_map[y][x] = 3


    def draw_map(self):
      #  print(self.the_map)
        for y in range(self.m):
            for x in range(self.n):
                xy = self.the_map[y][x]
                if xy == 0:
                    print '.',  # space
                elif xy == 1:
                    print 'I',  # Items
                elif xy == 2:
                    print 'S',  # start
                elif xy == 3:
                    print 'R',  # route
                elif xy == 4:
                    print 'D',  # finish
                elif xy == 8:
                    print 'A',  # Unnown Agent
                elif xy == 9:
                    print 'M',  # Main Agent
            print

    def set_map(self, the_map):
        self.the_map = the_map

    def agent_next_item(self, agent_position, item_position):

        (xA, yA) = agent_position
        (xI, yI) = item_position
        if (yI == yA and abs(xA - xI) == 1) or (xI == xA and abs(yA - yI) == 1):
            return True
        else:
            return False

    def load_item(self, agent, item_index):

        (xA, yA) = agent.get_position()
        (xI, yI) = self.items[item_index].get_position()
        self.items[item_index].loaded = True

        dx = xI - xA
        dy = yI - yA

        self.the_map[yA][xA] = 0
        self.the_map[yI][xI] = 8

        return (dx, dy)


################################################################################################################
    def mcts_move(self):

        # print(" MCTS Begin")

        next_move = MCTS.move_agent(self.agents,self.items)

        (xM, yM) = self.agents[0].get_position()

        self.agents[0].next_action = next_move
        (xA, yA) = self.agents[0].change_position_direction(10, 10)

        self.agents[0].position = (xA, yA)
        if self.the_map[yA][xA] == 1:  # load item

            print("Load item in position ", xA, yA, " with MCTS agent")
            nearby_item_index = self.get_item_by_position(xA, yA)
            if self.agents[0].level >= self.items[nearby_item_index].level:
                self.load_item(self.agents[0], nearby_item_index)
#
                (xA, yA) = self.items[nearby_item_index].get_position()
        # else: # Move
        self.update_map_mcts((xM, yM), (xA, yA))


        return

