# Types for agents are 'L1','L2','F1','F2'
import agent
import item
import position
import a_star
import numpy as np
from numpy.random import choice
import csv
import random
from collections import defaultdict

dx = [1, 0, -1, 0]  # 0: left,  1:up, 2:right  3:down
dy = [0, 1, 0, -1]
actions = ['L', 'N', 'E', 'S', 'W']


radius_max = 1
radius_min = 0.1
angle_max = 1
angle_min = 0.1
level_max = 1
level_min = 0


class simulator:
    def __init__(self):
        self.the_map = []
        self.items = []
        self.agents = []
        self.main_agent = None
        self.dim_w = None  # Number of columns
        self.dim_h = None  # Number of rows

        ###############################################################################################################

    def initialisation_fixed_values(self):
        # generating choices for random selection
        sf = list()
        sf.append((1, 2))
        sf.append((1, 5))
        sf.append((3, 4))
        # sf.append((0, 4))
        sf.append((5, 8))
        sf.append((8, 1))
        sf.append((6, 2))
        sf.append((5, 4))
        sf.append((9, 4))
        sf.append((2, 6))
        sf.append((9, 9))

        # creating items
        for i in range(0, 10):
            (x, y) = sf[i]

            # tmp_item = item.item(x, y, (10 - i) / 10.0, i)
            # tmp_item = item.item(x, y, ( i) / 10.0, i)
            tmp_item = item.item(x, y, 1, i)

            ## DEBUG: If you start M at (1,4) and A at (2,4), this creates an interesting case for testing A agent
            # tmp_item.loaded = True

            # if (x == 0 and y == 4):
            #     tmp_item.loaded = False

            # if (x == 1 and y == 5):
            #     tmp_item.loaded = False

            self.items.append(tmp_item)

        # creating agent
        (x, y) = (4, 4)
        # (x, y) = (2, 4)
        a_agent = agent.Agent(x, y, 0, 'l1', 0)
        self.agents.append(a_agent)

        # (x, y) = (4, 4)
        (x, y) = (6, 5)
        a_agent = agent.Agent(x, y, np.pi / 2, 'l1', 0)
        self.agents.append(a_agent)

        (x, y) = (1, 1)
        # (x, y) = (1, 4)
        ##self.main_agent = agent.Agent(x, y, np.pi/2, 'l1', 1)
        self.main_agent = agent.Agent(x, y, 0, 'l1', 1)
        self.main_agent.level = 1
        self.dim_w = 10
        self.dim_h = 10

        self.update_the_map()

        return

    # ###############################################################################################################

    def loader(self, path):
        """
        Takes in a csv file and stores the necessary instances for the simulation object. The file path referenced
        should point to a file of a particular format - an example of which can be found in utils.py txt_generator().
        The exact order of the file is unimportant - the three if statements will extract the needed information.
        :param path: File path directory to a .csv file holding the simulation information
        :return:
        """
        # Load and store csv file
        # info = defaultdict(list)
        # Load and store csv file
        # Load and store csv file
        info = defaultdict(list)
        with open(path) as info_read:
            for line in info_read:
                data = line.strip().split(', ')
                key, val = data[0], data[1:]
                info[key].append(val)

        # with open(path) as info_read:
        #     csv_reader = csv.reader(info_read, delimiter=',')
        #     for row in csv_reader:
        #         key, value = row[0], row[1]
        #         info[key].append(value)

        # Extract grid dimensions
        self.dim_w = int(info['grid'][0][0])
        self.dim_h = int(info['grid'][0][1])

        # Add items and agents to the environment
        i = 0
        j = 0
        l = 0
        for k, v in info.items():
            if 'item' in k:
                self.items.append(item.item(v[0][0], v[0][1], v[0][2], i))
                i += 1
            elif 'agent' in k:
                self.agents.append(agent.Agent(v[0][0], v[0][1], v[0][4], 'l1', j))
                j += 1
            elif 'main' in k:
                # x-coord, y-coord, direction, type, index
                self.main_agent = agent.Agent(v[0][0], v[0][1], v[0][4], 'l1', l)
                self.main_agent.level = v[0][2]
                l += 1

        # Run Checks
        assert len(self.items) == i, 'Incorrect Item Loading'
        assert len(self.agents) == j, 'Incorrect Ancillary Agent Loading'

        # Print Simulation Description
        print('Grid Size: {} \n{} Items Loaded\n{} Agents Loaded'.format(self.dim_w, len(self.items), len(self.agents)))

        # Update the map
        self.update_the_map()

    ################################################################################################################

    def is_there_item_in_position(self, x, y):

        for i in range(len(self.items)):
            if not self.items[i].loaded:
                (item_x, item_y) = self.items[i].get_position()
                if (item_x, item_y) == (x, y):
                    return i

        return -1

    ###############################################################################################################
    def create_empty_map(self):

        self.the_map = list()

        row = [0] * self.dim_w

        for i in range(self.dim_h):
            self.the_map.append(list(row))

    ###############################################################################################################
    def equals(self, other_simulator):

        ## If I reached here the maps are equal. Now let's compare the items and agents

        if len(self.items) != len(other_simulator.items):
            return False

        for i in range(len(self.items)):
            if not self.items[i].equals(other_simulator.items[i]):
                return False

        if len(self.agents) != len(other_simulator.agents):
            return False

        for i in range(len(self.items)):
            if not self.items[i].equals(other_simulator.items[i]):
                return False

        for i in range(len(self.agents)):
            if not self.agents[i].equals(other_simulator.agents[i]):
                return False

        if not self.main_agent.equals(other_simulator.main_agent):
            return False

        return True
        
    ###############################################################################################################
    def copy(self):

        copy_items = []

        for i in range(len(self.items)):
            copy_item = self.items[i].copy()
            copy_items.append(copy_item)

        copy_agents = list()

        for agent in self.agents:
            copy_agent = agent.copy()
            copy_agents.append(copy_agent)

        copy_main_agent = self.main_agent.copy()

        tmp_sim = simulator()
        tmp_sim.dim_h = self.dim_h
        tmp_sim.dim_w = self.dim_w
        tmp_sim.agents = copy_agents
        tmp_sim.items = copy_items
        tmp_sim.main_agent = copy_main_agent
        tmp_sim.update_the_map()

        return tmp_sim

    ###############################################################################################################
    def get_first_action(self,route): #todo: change for multiple agents
        #  This function is to find the first action afte finding the path by  A Star

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
    def update_the_map(self):

        self.create_empty_map()

        for i in range(len(self.items)):
            (item_x, item_y) = self.items[i].get_position()
            if self.items[i].loaded :
                self.the_map[item_y][item_x] = 0
            else:
                self.the_map[item_y][item_x] = 1

        for i in range(len(self.agents)):
            (agent_x, agent_y) = self.agents[i].get_position()
            self.the_map[agent_y][agent_x] = 8

            (memory_x, memory_y) = self.agents[i].get_memory()
            if (memory_x, memory_y) != (-1, -1):
                self.the_map[memory_y][memory_x] = 4

        (m_agent_x, m_agent_y) = self.main_agent.get_position()
        self.the_map[m_agent_y][m_agent_x] = 9

    ###############################################################################################################
    def find_agent_index(self,pos):

        agents_num = len(self.agents)
        for i in range(0, agents_num):
            if self.agents[i].position == pos:
                return i
        return -1

    ###############################################################################################################
    def remove_old_destination_in_map(self): #todo: check to delete

        for y in range(self.dim_h):
            for x in range(self.dim_w):
                xy = self.the_map[y][x]
                if xy == 4:
                    self.the_map[y][x] = 1

    ###############################################################################################################
    def mark_route_map(self,route, xA, yA, dx, dy): #todo: check to  delete

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
                item_index = self.find_item_by_location(x, y)

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
    def load_item(self, agent, destinantion_item_index):

        self.items[destinantion_item_index].loaded = True
        (agent_x , agent_y) = agent.get_position()
        self.items[destinantion_item_index].remove_agent(agent_x , agent_y)
        agent.item_to_load = -1

        # Empty the memory to choose new target
        agent.reset_memory()

        return agent

    ################################################################################################################
    def run_and_update(self, a_agent):


        a_agent = self.move_a_agent(a_agent)

        next_action = choice(actions, p=a_agent.get_actions_probabilities())  # random sampling the action

        a_agent.next_action = next_action

        self.update(a_agent)

        return self.agents[a_agent.index]

    ################################################################################################################
    def update_all_A_agents(self):
        reward = 0

        for i in range (len(self.agents)):
            next_action = choice(actions, p=self.agents[i].get_actions_probabilities())  # random sampling the action

            self.agents[i].next_action = next_action

            reward += self.update(i)

        return reward

    ################################################################################################################
    def update(self, a_agent_index):
        reward = 0
        a_agent = self.agents[a_agent_index]
        if a_agent.next_action == 'L' and a_agent.item_to_load != -1:
            destination = a_agent.item_to_load

            if destination.level <= a_agent.level:  # If there is a an item nearby loading process starts

                # load item and and remove it from map  and get the direction of agent when reaching the item.
                a_agent = self.load_item(a_agent, destination.index)
                reward += 1
            else:
                self.items[destination.index].agents_load_item.append(a_agent)

        else:
            # If there is no item to collect just move A agent
            (new_position_x, new_position_y) = a_agent.new_position_with_given_action(self.dim_h,self.dim_w
                                                                                      , a_agent.next_action)

            if self.position_is_empty(new_position_x, new_position_y):
                a_agent.position = (new_position_x, new_position_y)
            else:
                a_agent.change_direction_with_action(a_agent.next_action)

        self.agents[a_agent_index] = a_agent
        self.update_the_map()
        return reward

    ################################################################################################################
    def destination_loaded_by_other_agents(self, agent):
        # Check if item is collected by other agents so we need to ignore it and change the target.

        (memory_x, memory_y) = agent.get_memory()
        destination_index = self.find_item_by_location(memory_x, memory_y)

        item_loaded = False

        if destination_index != -1:
            item_loaded = self.items[destination_index].loaded

        return item_loaded

    ################################################################################################################
    def position_is_empty(self, x, y):

        for i in range(len(self.items)):
            (item_x, item_y) = self.items[i].get_position()
            if (item_x, item_y) == (x,y) and not self.items[i].loaded:
                return False

        for i in range(len(self.agents)):
            (agent_x, agent_y) = self.agents[i].get_position()
            if (agent_x, agent_y) == (x, y):
                return False

        (m_agent_x, m_agent_y) =self.main_agent.get_position()
        if (m_agent_x, m_agent_y) == (x, y):
            return False

        return True

    ################################################################################################################
    def do_collaboration(self):
        c_reward = 0

        for item in self.items:
            agents_total_level = 0
            for agent in item.agents_load_item:
                agents_total_level += agent.level
            if agents_total_level >= item.level and item.agents_load_item !=[]:
                item.loaded = True
                item.agents_load_item = list()
                c_reward += 1

        return

    ################################################################################################################

    def move_a_agent(self, a_agent):

        location = a_agent.position  # Location of main agent
        destination = position.position(-1, -1)
        target = position.position(-1, -1)

        if self.destination_loaded_by_other_agents(a_agent):  # item is loaded by other agents so reset the memory to choose new target.
            a_agent.reset_memory()

        # If the target is selected before we have it in memory variable and we can use it
        if a_agent.memory.get_position() != (-1, -1) and location != a_agent.memory: #here
            destination = a_agent.memory

        else:  # If there is no target we should choose a target based on visible items and agents.

            directions = [0 * np.pi / 2, np.pi / 2, 2 * np.pi / 2, 3 * np.pi / 2]

            while len(directions) > 0:

                a_agent.visible_agents_items(self.items, self.agents)
                target = a_agent.choose_target(self.items, self.agents)

                if target.get_position() != (-1, -1):
                    destination = target
                    break

                else:  # rotate agent to find an agent
                    a_agent.direction = directions.pop()

            a_agent.memory = destination

        # If there is no destination the probabilities for all of the actions are same.
        if destination.get_position() == (-1, -1):

            a_agent.set_actions_probability(0, 0.25, 0.25, 0.25, 0.25)
            a_agent.set_random_action()
            return a_agent
        else:

            (x_destination, y_destination) = destination.get_position()  # Get the target position
            destination_index = self.find_item_by_location(x_destination, y_destination)

            load = a_agent.is_agent_near_destination(x_destination, y_destination)

            if load:  # If there is a an item nearby loading process starts
                a_agent.item_to_load = self.items[destination_index]

                a_agent.set_actions_probabilities('L')
            else:

                self.the_map[y_destination][x_destination] = 4  # Update map with target position

                a = a_star.a_star(self)  # Find the whole path  to reach the destination with A Star
                (x_agent, y_agent) = a_agent.get_position()  # Get agent's current position

                route = a.pathFind(x_agent, y_agent, x_destination, y_destination)

                if len(route) == 0:
                    a_agent.set_actions_probability(0, 0.25, 0.25, 0.25, 0.25)
                    a_agent.set_random_action()
                    return a_agent

                action = self.get_first_action(route)  # Get first action of the path
                a_agent.set_actions_probabilities(action)

            return a_agent

