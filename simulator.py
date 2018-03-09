# Types for agents are 'L1','L2','F1','F2'
import agent
import position
import a_star
import MCTS
import numpy as np

dx = [1, 0, -1, 0]  # 0: left,  1:up, 2:right  3:down
dy = [0, 1, 0, -1]


class simulator:
    def __init__(self,the_map, items, agents, main_agent, n, m):
        self.the_map = the_map
        self.items = items
        self.agents = agents
        self.main_agent = main_agent
        self.memory = position.position(0, 0)
        self.n = n
        self.m = m

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

        agent_index = self.find_agent_index(old_pos)

        self.main_agent.pos = new_pos

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

        for y in range(self.m):
            for x in range(self.n):
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

    ################################################################################################################
    def draw_map_with_level(self):

        for y in range(self.m):

            line_str = ""
            for x in range(self.n):
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
    def set_map(self, the_map):
        self.the_map = the_map

    ################################################################################################################
    def agent_next_item(self, agent_position, item_position):

        (xA, yA) = agent_position
        (xI, yI) = item_position
        if (yI == yA and abs(xA - xI) == 1) or (xI == xA and abs(yA - yI) == 1):
            return True
        else:
            return False

    ################################################################################################################
    def load_item(self, agent, item_index):

        (xA, yA) = agent.get_position()
        (xI, yI) = self.items[item_index].get_position()
        self.items[item_index].loaded = True

        distance_x = xI - xA
        distance_y = yI - yA

        self.the_map[yA][xA] = 0
        self.the_map[yI][xI] = 8

        return (distance_x, distance_y)


    ################################################################################################################
    def run_and_update(self, agent):

        unknown_agent = agent

        location = unknown_agent.position  # Location of main agent
        destination = position.position(0, 0)
        target = position.position(0, 0)

        item_load = False

        # Check if item is collected by other agents so we need to ignore it and change the target.
        (memory_x,memory_y) = self.memory.get_position()
        destination_index = self.find_item_by_location(memory_x, memory_y)
        if destination_index != -1:
            item_load = self.items[destination_index].loaded

            if item_load:
               # and self.memory.get_position() != (0, 0):
               self.memory = position.position(0, 0)

        # If the target is selected before we have it in memory variable and we can use it
        if self.memory.get_position() != (0, 0) and location != self.memory and not item_load:
            # print "Get old Destination"
            destination = self.memory

        else:  # If there is no target we should choose a target based on visible items and agents.

            unknown_agent.visible_agents_items(self.items,self.agents)

            directions = [0 * np.pi / 2,  np.pi / 2,  2 * np.pi / 2,  3 * np.pi / 2]

            while len(directions) > 0:
                target = unknown_agent.choose_target(self.items,self.agents)

                if target.get_position() != (0, 0):
                    destination = target
                    break

                else:  # rotate agent to find an agent
                    unknown_agent.direction = directions.pop()

            self.memory = destination

        if destination.get_position() == (0, 0):  # There is no destination

            unknown_agent.set_actions_probability(0, 0.25, 0.25, 0.25, 0.25)
            # **Select a random action for move
            return unknown_agent

        else:

            (xA, yA) = unknown_agent.get_position()  # Get agent position

            self.remove_old_destination_in_map()  # Remove any destination that set by ~A_star in the previous step

            (xB, yB) = destination.get_position()  # Get the target position

            # If agent is next to the target item, it should load it.
            load = unknown_agent.is_agent_near_destination(xB, yB)

            if load:

                if destination.level <= unknown_agent.level :  # If there is a an item nearby loading process starts

                    loaded_item_position = destination.get_position()
                    # print("Load item in position ", loaded_item_position, " with A star agent")

                    # load item and and update from map  and get the direction of agent when reaching the item.
                    (distance_x, distance_y) = self.load_item(unknown_agent, destination.index)

                    unknown_agent.next_action = 'L'  # Current action is Load

                    # Set the position of agent with the position of the target item. As agent reach it and load it.
                    unknown_agent.set_position(loaded_item_position[0],loaded_item_position[1])

                    unknown_agent.change_direction(distance_x, distance_y)

                    self.agents[unknown_agent.index] = unknown_agent

                    new_position = loaded_item_position

                    # Empty the memory to choose new target
                    self.memory = position.position(0, 0)

            else:
                # print '****** move'

                destination_index = self.find_item_by_location(xB, yB)
                if destination_index != -1:
                    item_load = self.items[destination_index].loaded

                    if item_load:
                        print "item loaded before"
                        # and self.memory.get_position() != (0, 0):
                        # self.memory = position.position(0, 0)

                self.the_map[yB][xB] = 4  # Update map with target position
                a = a_star.a_star(self.the_map)  # Find the whole path  to reach the destination with A Star

                route = a.pathFind(xA, yA, xB, yB)

                # self.mark_route_map(route, xA, yA)

                if len(route) == 0:
                    return unknown_agent

                action = self.get_first_action(route)  # Get first action of the path

                unknown_agent.next_action = action
                unknown_agent.set_probability_main_action()
                new_position = unknown_agent.change_position_direction(self.n,self.m)
                unknown_agent.set_position(new_position[0], new_position[1])
                self.agents[unknown_agent.index] = unknown_agent

                self.update_map((xA, yA), new_position)

            # self.draw_map()
            return unknown_agent



    ################################################################################################################
    def run(self, agent):

        unknown_agent = agent

        location = unknown_agent.position  # Location of main agent
        destination = position.position(0, 0)
        target = position.position(0, 0)

        item_load = False

        # Check if item is collected by other agents so we need to ignore it and change the target.
        (memory_x, memory_y) = self.memory.get_position()
        destination_index = self.find_item_by_location(memory_x, memory_y)
        if destination_index != -1:
            item_load = self.items[destination_index].loaded

            if item_load:
                # and self.memory.get_position() != (0, 0):
                self.memory = position.position(0, 0)

        # If the target is selected before we have it in memory variable and we can use it
        if self.memory.get_position() != (0, 0) and location != self.memory:
            destination = self.memory

        else:  # If there is no target we should choose a target based on visible items and agents.

            unknown_agent.visible_agents_items(self.items, self.agents)

            directions = [0 * np.pi / 2, np.pi / 2, 2 * np.pi / 2, 3 * np.pi / 2]

            while len(directions) > 0:
                target = unknown_agent.choose_target(self.items, self.agents)

                if target.get_position() != (0, 0):
                    destination = target
                    break

                else:  # rotate agent to find an agent
                    unknown_agent.direction = directions.pop()

            self.memory = destination

        if destination.get_position() == (0, 0):

            unknown_agent.set_actions_probability(0, 0.25, 0.25, 0.25, 0.25)
            # **Select a random action for move
            return unknown_agent

        else:

            (xA, yA) = unknown_agent.get_position()  # Get start position

            self.remove_old_destination_in_map()

            (xB, yB) = destination.get_position()  # Get the target position

            load = unknown_agent.is_agent_near_destination(destination)

            if load:  # If there is a an item nearby loading process starts
                if destination.level <= unknown_agent.level:  # If there is a an item nearby loading process starts

                    loaded_item_position = destination.get_position()
                    # print("Load item in position ", loaded_item_position, " with A star agent")

                    # load item and and update from map  and get the direction of agent when reaching the item.
                    (distance_x, distance_y) = self.load_item(unknown_agent, destination.index)

                    unknown_agent.next_action = 'L'  # Current action is Load

                    # Set the position of agent with the position of the target item. As agent reach it and load it.
                    unknown_agent.set_position(loaded_item_position[0], loaded_item_position[1])

                    unknown_agent.change_direction(distance_x, distance_y)

                    self.agents[unknown_agent.index] = unknown_agent

                    new_position = loaded_item_position

                    # Empty the memory to choose new target
                    self.memory = position.position(0, 0)

            else:
                # print '****** move'

                destination_index = self.find_item_by_location(xB, yB)
                if destination_index != -1:
                    item_load = self.items[destination_index].loaded

                    if item_load:
                        print "item loaded before"
                        # and self.memory.get_position() != (0, 0):
                        # self.memory = position.position(0, 0)

                self.the_map[yB][xB] = 4  # Update map with target position
                a = a_star.a_star(self.the_map)  # Find the whole path  to reach the destination with A Star

                route = a.pathFind(xA, yA, xB, yB)

                # self.mark_route_map(route, xA, yA)

                if len(route) == 0:
                    return unknown_agent

                action = self.get_first_action(route)  # Get first action of the path

                unknown_agent.next_action = action
                unknown_agent.set_probability_main_action()
                new_position = unknown_agent.change_position_direction(self.n, self.m)
                unknown_agent.set_position(new_position[0], new_position[1])
                self.agents[unknown_agent.index] = unknown_agent

                self.update_map((xA, yA), new_position)

                # self.draw_map()
            return unknown_agent

    ################################################################################################################
    def mcts_move(self, parameters_estimation):

        # other_agent_status

        # print(" MCTS Begin")
        m_agent = self.main_agent
        next_move = MCTS.move_agent(self.agents, self.items,  self.main_agent,parameters_estimation )

        (xM, yM) = m_agent.get_position()

        m_agent.next_action = next_move
        (xA, yA) = m_agent.change_position_direction(10, 10)

        m_agent.position = (xA, yA)
        # If the other agent is nearby to help

        if self.the_map[yA][xA] == 1 or self.the_map[yA][xA] == 4:  # load item

            nearby_item_index = self.get_item_by_position(xA, yA)
            if m_agent.level >= self.items[nearby_item_index].level:
                self.load_item(m_agent, nearby_item_index)
                (xA, yA) = self.items[nearby_item_index].get_position()

            a_agent = self.agents[0]
            a_load = a_agent.is_agent_near_destination(xA, yA)and a_agent.next_action == 'L'

            if a_load and m_agent.level + a_agent.level >= self.items[nearby_item_index].level:
                self.load_item(m_agent, nearby_item_index)
                (xA, yA) = self.items[nearby_item_index].get_position()

                # a_agent movement
                new_position = (xA, yA)
                self.memory = position.position(0, 0)
                self.update_map(a_agent.position, new_position)

        # else: # Move
        self.update_map_mcts((xM, yM), (xA, yA))

        return