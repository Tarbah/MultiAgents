
import position
import numpy as np
from math import sqrt


class Agent:
    def __init__(self, x, y, agent_type, index):
        # TODO: what is self.index for?
        self.position = (x, y)
        self.level=1
        self.visible_agents = []
        self.visible_items = []
        self.direction = np.pi / 2
        self.actions_probability = {'L': 0, 'N': 0, 'E': 0, 'S': 0, 'W': 0}
        self.next_action = None
        self.index = index
        self.agent_type = agent_type

    def get_position(self):
        return self.position[0], self.position[1]

    def set_position(self, x, y):

        self.position = (x, y)
        return

    def set_type(self, atype):
        self.atype = atype

    def is_item_nearby(self, items):

        pos = self.position

        for i in range(0, len(items)):
            if not items[i].loaded:
                item = items[i]
                (xI, yI) = item.position.get_position()
                if (yI == pos[1] and abs(pos[0] - xI) == 1) or (xI == pos[0] and abs(pos[1] - yI) == 1):
                    return i
        return -1

    def find_nearest_item(self, items):

        pos = self.position
        minimum_distance = 10000
        nearest_item_index = -1

        for i in range(0, len(items)):
            if not items[i].loaded:
                item = items[i]
                (xI, yI) = item.position.get_position()
                if self.distance(item) < minimum_distance:
                    minimum_distance = self.distance(item)
                    nearest_item_index = i

        return nearest_item_index

    def if_see_other_agent(self, agent):
        if self.distance(agent) < self.radius:
            print(11)
            print self.direction
            if self.direction - self.angle / 2 <= self.angle_of_gradient(agent) <= self.direction + self.angle / 2:
              return True
        return False

    def is_agent_near_destination(self, item):

        pos = self.position

        (xI, yI) = item.position.get_position()
        if (yI == pos[1] and abs(pos[0] - xI) == 1) or (xI == pos[0] and abs(pos[1] - yI) == 1):
            return True
        else:
            return False

    def set_parameters(self, level, radius, angle):

        width, hight = 10, 10
        self.level = level
        self.radius = radius * sqrt(width ** 2 + hight ** 2)
        self.angle = 2 * np.pi * angle

    def set_direction(self, direction):
        self.direction = direction

    def set_probability_main_action(self):

        if self.next_action == 'L':
            self.actions_probability['L'] = 0.96
            self.actions_probability['N'] = 0.01
            self.actions_probability['E'] = 0.01
            self.actions_probability['S'] = 0.01
            self.actions_probability['W'] = 0.01
            return

        if self.next_action == 'N':
            self.actions_probability['L'] = 0.01
            self.actions_probability['N'] = 0.96
            self.actions_probability['E'] = 0.01
            self.actions_probability['S'] = 0.01
            self.actions_probability['W'] = 0.01
            return

        if self.next_action == 'W':
            self.actions_probability['L'] = 0.01
            self.actions_probability['N'] = 0.01
            self.actions_probability['E'] = 0.01
            self.actions_probability['S'] = 0.01
            self.actions_probability['W'] = 0.96
            return

        if self.next_action == 'S':
            self.actions_probability['L'] = 0.01
            self.actions_probability['N'] = 0.01
            self.actions_probability['E'] = 0.01
            self.actions_probability['S'] = 0.96
            self.actions_probability['W'] = 0.01
            return

        if self.next_action == 'E':
            self.actions_probability['L'] = 0.01
            self.actions_probability['N'] = 0.01
            self.actions_probability['E'] = 0.96
            self.actions_probability['S'] = 0.01
            self.actions_probability['W'] = 0.01
            return

    def get_action_probability(self, action):
        if action == 'W':
            return self.actions_probability['W']

        if action == 'L':
            return self.actions_probability['L']

        if action == 'N':
            return self.actions_probability['N']

        if action == 'E':
            return self.actions_probability['E']

        if action == 'S':
            return self.actions_probability['S']

    def change_direction(self, dx, dy):
        if dx == -1 and dy == 0:  # 'E':
            self.direction = 0 * np.pi / 2

        if dx == 0 and dy == 1:  # 'N':
            self.direction = np.pi / 2

        if dx == 1 and dy == 0:  # 'W':
            self.direction = 2 * np.pi / 2

        if dx == 0 and dy == -1:  # 'S':
            self.direction = 3 * np.pi / 2

    def change_position_direction(self, n, m):
        dx = [1, 0, -1, 0]  # 0:W ,  1:N , 2:E  3:S
        dy = [0, 1, 0, -1]

        x_diff = 0
        y_diff = 0

        if self.next_action == 'W':
            x_diff = dx[0]
            y_diff = dy[0]
            self.direction = 0 * np.pi / 2

        if self.next_action == 'N':
            x_diff = dx[1]
            y_diff = dy[1]
            self.direction = np.pi / 2

        if self.next_action == 'E':
            x_diff = dx[2]
            y_diff = dy[2]
            self.direction = 2 * np.pi / 2

        if self.next_action == 'S':
            x_diff = dx[3]
            y_diff = dy[3]
            self.direction = 3 * np.pi / 2

        x, y = self.get_position()

        if x + x_diff < n and x + x_diff >= 0 and y + y_diff < m and y + y_diff >= 0:
            self.position = (x + x_diff, y + y_diff)

        return self.position

    def set_actions_probability(self, l, n, e, s, w):
        self.actions_probability['L'] = l
        self.actions_probability['N'] = n
        self.actions_probability['E'] = e
        self.actions_probability['S'] = s
        self.actions_probability['W'] = w

    def angle_of_gradient(self, point):

        point_position = point.get_position()
        my_position = self.get_position()
        if my_position[0] - point_position[0] == 0:
            return np.pi / 2
        else:
            return np.arctan((my_position[1] - point_position[1]) * 1.0 / (my_position[0] - point_position[0]))

    def distance(self, point):
        point_position = point.get_position()
        my_position = self.get_position()
        return sqrt((point_position[0] - my_position[0]) ** 2 + (point_position[1] - my_position[1]) ** 2)

    def number_visible_items(self):

        return len(self.visible_items)

    def visible_agents_items(self, items, agents):

        self.visible_agents = list()
        self.visible_items = list()

        for i in range(0, len(items)):

            if not items[i].loaded:
                if self.distance(items[i]) < self.radius:
                    if self.direction - self.angle / 2 <= self.angle_of_gradient(
                            items[i]) <= self.direction + self.angle / 2:
                        self.visible_items.append(items[i])

        for i in range(0, len(agents)):
            if self.distance(agents[i]) < self.radius:
                if self.direction - self.angle / 2 <= self.angle_of_gradient(
                        agents[i]) <= self.direction + self.angle / 2:
                    self.visible_agents.append(agents[i])


        return self.visible_items

    def choose_target(self, items, agents):

        #print 'number of visible items: ' , len(self.visible_items)

        if len(self.visible_items) == 0:
            return position.position(0, 0)

        max_index = -1
        max_distanse = 0
        # if items visible, return furthest one;
        # else, return 0
        if self.agent_type == "l1":

            for i in range(0, len(self.visible_items)):
                if self.distance(self.visible_items[i]) > max_distanse:
                    max_distanse = self.distance(self.visible_items[i])
                    max_index = i

            return self.visible_items[max_index]

        # if items visible, return item with highest level below own level,
        # or item with highest level if none are below own level;
        # else, return 0

        if self.agent_type == "l2":
            max_level = -1
            for i in range(0, len(self.visible_items)):
                if self.visible_items[i].level > max_level:
                    if self.visible_items[i].level < self.level:
                        max_level = self.visible_items[i].level
                        max_index = i

            if max_index == -1:
                return (0, 0)
            else:
                return self.visible_items[max_index]

        # if agents visible but no items visible, return furthest agent;
        # if agents and items visible, return item that furthest agent would choose if it had type L1;
        #  else, return 0
        if self.agent_type == "f1":
            if len(self.visible_items) == 0 and len(self.visible_agents) > 0:

                for i in range(0, len(self.visible_agents)):
                    if self.distance(self.visible_agents[i]) > max_distanse:
                        max_distanse = self.distance(self.visible_agents[i])
                        max_index = i

                return self.visible_items[max_index]

            if len(self.visible_items) > 0 and len(self.visible_agents) > 0:

                for i in range(0, len(self.visible_agents)):
                    if self.distance(self.visible_agents[i]) > max_distanse:
                        max_distanse = self.distance(self.visible_agents[i])
                        max_index = i

                furthest_agent = self.visible_agents[max_index]
                if furthest_agent.agent_type == "l1":

                    furthest_agent.visible_agents_items(items, agents)

                    return furthest_agent.choose_target()
                else:
                    return (0, 0)

        # if agents visible but no items visible, return agent with highest level above own level,
        # or furthest agent if none are above own level;
        # if agents and items visible, select agent as  before and return item that this agent would choose if it had type L2;
        # else, return 0
        if self.agent_type == "f2":
            if len(self.visible_items) == 0 and len(self.visible_agents) > 0:
                max_level = -1
                for i in range(0, len(self.visible_agents)):
                    if self.visible_agents[i].level > max_level:
                        if self.visible_agents[i].level > self.level:
                            max_level = self.visible_agents[i].level
                            max_index = i
                if max_index == -1:
                    for i in range(0, len(self.visible_items)):
                        if self.distance(self.visible_items[i]) > max_distanse:
                            max_distanse = self.distance(self.visible_items[i])
                            max_index = i

                return self.visible_items[max_index]

            if len(self.visible_items) > 0 and len(self.visible_agents) > 0:
                max_distanse = 0

                for i in range(0, len(self.visible_agents)):
                    if self.distance(self.visible_agents[i]) > max_distanse:
                        max_distanse = self.distance(self.visible_agents[i])
                        max_index = i

                furthest_agent = self.visible_agents[max_index]
                if furthest_agent.agent_type == "l2":

                    furthest_agent.visible_agents_items(items, agents)

                    return furthest_agent.choose_target()
                else:
                    return (0, 0)



