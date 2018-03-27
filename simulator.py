# Types for agents are 'L1','L2','F1','F2'
import agent
import position
import a_star
import numpy as np
from numpy.random import choice

dx = [1, 0, -1, 0]  # 0: left,  1:up, 2:right  3:down
dy = [0, 1, 0, -1]
actions = ['L', 'N', 'E', 'S', 'W']


class simulator:
    def __init__(self,the_map, items, agents, main_agent, dim_w, dim_h):
        self.the_map = the_map
        self.items = items
        self.agents = agents
        self.main_agent = main_agent
        self.dim_w = dim_w
        self.dim_h = dim_h

    ###############################################################################################################
    def equals(self, other_simulator):
        ## TODO: Is there a way to make a quicker comparison? Some sort of unique ID, hash table?..

        for i in range(self.dim_h):
            for j in range(self.dim_w):
                if (other_simulator.the_map[i][j] != self.the_map[i][j]):
                    return False
                
        ## If I reached here the maps are equal. Now let's compare the items and agents

        if (len(self.items) != len(other_simulator.items)):
            return False

        ## TODO: Items have an index. Can we assume that they will always be in the same order?
        for i in range(len(self.items)):
            if (not self.items[i].equals(other_simulator.items[i])):
                return False

        if (len(self.agents) != len(other_simulator.agents)):
            return False

        ## TODO: Can we assume that agents will always be in the same order?
        for i in range(len(self.agents)):
            if (not self.agents[i].equals(other_simulator.agents[i])):
                return False

        if (not self.main_agent.equals(other_simulator.main_agent)):
            return False

        ## TODO: Anything else to be compared? If we could reach here the states are the same?

        return True
        
    ###############################################################################################################
    def copy(self):
        copy_map = list()

        ## m rows of n columns each, right?
        ## why the map is addressed as [y][x] instead of [x][y]?
        for i in range(self.dim_h):
            row = list()
            for j in range(self.dim_w):
                row.append(self.the_map[i][j])
            copy_map.append(list(row))

        copy_items = []

        for i in range(len(self.items)):            
            copy_item = self.items[i].copy()

            copy_items.append(copy_item)


        copy_agents = list()
        
        for agent in self.agents:
            copy_agent = agent.copy()
            
            copy_agents.append(copy_agent)


        copy_main_agent = self.main_agent.copy()

        tmp_sim = simulator(copy_map, copy_items, copy_agents, copy_main_agent, self.dim_h, self.dim_w)
        
        return tmp_sim
                            
            
    ###############################################################################################################
    def get_item_by_position(self, x, y):
        for i in range(0, len(self.items)):
            if self.items[i].get_position() == (x,y):
                return i
        return -1

    ###############################################################################################################
    def get_first_action(self,route):

        dir = route[0]

        if dir == '0':
            return 'W'
        if dir == '1':
            return 'N'
        if dir == '2':
            return 'E'
        if dir == '3':
            return 'S'

    ###############################################################################################################
    def items_left(self):
        items_count= 0
        for i in range(0,len(self.items)):
            if not self.items[i].loaded:
                items_count += 1
        return items_count

    ###############################################################################################################
    def update_map(self,old_pos, new_pos):

        (x, y) = old_pos

        self.the_map[y][x] = 0

        agent_index = self.find_agent_index(old_pos)
        self.agents[0].pos = new_pos

        (x, y) = new_pos

        self.the_map[y][x] = 8  # 8 demonstrate the unknown agent on the map

        return

    ###############################################################################################################
    def update_map_mcts(self, old_pos, new_pos):

        (x, y) = old_pos
        self.the_map[y][x] = 0

        (x, y) = new_pos
        self.the_map[y][x] = 9  # 9 demonstrate the main agent on the map

        return

    ###############################################################################################################
    def find_agent_index(self,pos):

        agents_num = len(self.agents)
        for i in range(0, agents_num):
            if self.agents[i].position == pos:
                return i
        return -1

    ###############################################################################################################
    def remove_old_destination_in_map(self):

        for y in range(self.dim_h):
            for x in range(self.dim_w):
                xy = self.the_map[y][x]
                if xy == 4:
                    self.the_map[y][x] = 1

    ###############################################################################################################
    def mark_route_map(self,route, xA, yA, dx, dy):

        x = xA
        y = yA

        if len(route) > 0:
            for i in range(len(route)):
                j = int(route[i])
                x += dx[j]
                y += dy[j]
                self.the_map[y][x] = 3

    ###############################################################################################################
    def draw_map(self):

        for y in range(self.dim_h):
            for x in range(self.dim_w):
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
                    print 'A',  # A Agent
                elif xy == 9:
                    print 'M',  # Main Agent
            print

    ################################################################################################################
    def draw_map_with_level(self):

        for y in range(self.dim_h):

            line_str = ""
            for x in range(self.dim_w):
                item_index = self.find_item_by_location(x,y)

                xy = self.the_map[y][x]

                if xy == 0:
                    line_str += ' . '

                elif xy == 1:
                    line_str += str(self.items[item_index].level)

                elif xy == 2:
                    line_str += ' S '

                elif xy == 3:
                    line_str += ' R '

                elif xy == 4:
                    line_str += ' D '

                elif xy == 8:
                    line_str += ' A '

                elif xy == 9:
                    line_str += ' M '

            print line_str
            print

    ################################################################################################################
    def find_item_by_location(self, x, y):
        for i in range(len(self.items)):
            (item_x, item_y) = self.items[i].get_position()
            if item_x == x and item_y == y:
                return i
        return -1

    ################################################################################################################
## todo: delete it
    # def set_map(self, the_map):
    #     self.the_map = the_map

    ################################################################################################################
    def agent_next_item(self, agent_position, item_position):

        (xA, yA) = agent_position
        (xI, yI) = item_position
        if (yI == yA and abs(xA - xI) == 1) or (xI == xA and abs(yA - yI) == 1):
            return True
        else:
            return False

    ################################################################################################################
    def load_item(self, agent, destinantion_item_index):

        (x_agent, y_agent) = agent.get_position()
        (x_item, y_item) = self.items[destinantion_item_index].get_position()
        self.items[destinantion_item_index].loaded = True

        distance_x = x_item - x_agent
        distance_y = y_item - y_agent

        self.the_map[y_item][x_item] = 0

        agent.change_direction(distance_x, distance_y)
        agent.item_to_load = -1

       # self.remove_old_destination_in_map()

        return agent


    ################################################################################################################
    def run_and_update(self, a_agent):

        a_agent = self.move_a_agent(a_agent)

        next_action = choice(actions, p=a_agent.get_actions_probabilities())  # random sampling the action

        a_reward = self.update(a_agent, next_action)

        return self.agents[a_agent.index]

    ################################################################################################################
    def update(self, a_agent, action):

        if a_agent.next_action == 'L':
            destination = a_agent.item_to_load
            if destination.level <= a_agent.level:  # If there is a an item nearby loading process starts

                # load item and and remove it from map  and get the direction of agent when reaching the item.
                a_agent = self.load_item(a_agent, destination.index)

                self.agents[a_agent.index] = a_agent

                # Empty the memory to choose new target
                self.agents[a_agent.index].memory = position.position(0, 0)
                return 1

        # if a_agent.item_to_load == -1:
        else:
            # If there is no item to collect just move A agent
            (old_position_x , old_position_y) = a_agent.get_position()

            (new_position_x , new_position_y) = a_agent.change_position_direction(self.dim_h,self.dim_w)

            if self.the_map[new_position_y][new_position_x] == 0:
                self.the_map[old_position_y][old_position_x] = 0
                a_agent.set_position(new_position_x, new_position_y)
                self.agents[a_agent.index] = a_agent
                self.the_map[new_position_y][new_position_x] = 8
        return 0

    ################################################################################################################
    def destination_loaded_by_other_agents(self,agent):
        # Check if item is collected by other agents so we need to ignore it and change the target.

        (memory_x, memory_y) = agent.memory.get_position()
        destination_index = self.find_item_by_location(memory_x, memory_y)

        item_loaded = False

        if destination_index != -1:
            item_loaded = self.items[destination_index].loaded

        return item_loaded
    ################################################################################################################
    def move_a_agent(self, a_agent):

        location = a_agent.position  # Location of main agent
        destination = position.position(0, 0)
        target = position.position(0, 0)

        if self.destination_loaded_by_other_agents(a_agent):  # item is loaded by other agents so reset the memory to choose new target.
            a_agent.reset_memory()

        # If the target is selected before we have it in memory variable and we can use it
        if a_agent.memory.get_position() != (0, 0) and location != a_agent.memory: #here
            destination = a_agent.memory

        else:  # If there is no target we should choose a target based on visible items and agents.

            directions = [0 * np.pi / 2, np.pi / 2, 2 * np.pi / 2, 3 * np.pi / 2]

            while len(directions) > 0:
                a_agent.visible_agents_items(self.items, self.agents)
                target = a_agent.choose_target(self.items, self.agents)

                if target.get_position() != (0, 0):
                    destination = target
                    break

                else:  # rotate agent to find an agent
                    a_agent.direction = directions.pop()

            a_agent.memory = destination

        # If there is no destination the probabilities for all of the actions are same.
        if destination.get_position() == (0, 0): #here
            a_agent.set_actions_probability(0, 0.25, 0.25, 0.25, 0.25)
            a_agent.set_random_action()
            return a_agent
        else:

            (x_destination, y_destination) = destination.get_position()  # Get the target position
            destination_index = self.find_item_by_location(x_destination, y_destination)

            load = a_agent.is_agent_near_destination(x_destination, y_destination)

            ## TODO: It does not look like we are treating Load correctly yet
            if load:  # If there is a an item nearby loading process starts
                a_agent.item_to_load = self.items[destination_index]

                a_agent.set_actions_probabilities('L')
                a_agent.next_action = 'L'

            else:

                self.the_map[y_destination][x_destination] = 4  # Update map with target position

                a = a_star.a_star(self.the_map)  # Find the whole path  to reach the destination with A Star
                (x_agent, y_agent) = a_agent.get_position()  # Get agent's current position

                route = a.pathFind(x_agent, y_agent, x_destination, y_destination)

                if len(route) == 0:
                    a_agent.set_actions_probability(0, 0.25, 0.25, 0.25, 0.25)
                    a_agent.set_random_action()
                    return a_agent

                action = self.get_first_action(route)  # Get first action of the path
                a_agent.next_action = action

                a_agent.set_actions_probabilities(action)

            return a_agent

