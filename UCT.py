from math import *
from numpy.random import choice
import simulator
import item
import agent
import position

iteration_max = 100
max_depth = 100

actions = ['N', 'E', 'S', 'W']


class q_table_row:
    def __init__(self, action, value, visited_number):
        action = action
        value = value
        visited_number = visited_number


def create_temp_simulator(items, agents, main_agent):
    local_map = []
    row = [0] * 10

    for i in range(10):
        local_map.append(list(row))

    local_items = []
    for i in range(len(items)):
        (item_x, item_y) = items[i].get_position()
        local_item = item.item(item_x, item_y, items[i].level, i)
        local_item.loaded = items[i].loaded
        local_items.append(local_item)
        if not local_item.loaded:
            local_map[item_y][item_x] = 1

    local_agents = list()

    (a_agent_x, a_agent_y) = agents[0].get_position()
    local_map[a_agent_y][a_agent_x] = 8
    local_agent = agent.Agent(a_agent_x, a_agent_y, 'l1', 0)
    local_agents.append(local_agent)

    (m_agent_x, m_agent_y) = main_agent.get_position()
    local_map[m_agent_y][m_agent_x] = 9
    local_main_agent = agent.Agent(m_agent_x, m_agent_y, 'l1', 1)
    local_main_agent.set_level(main_agent.level)

    tmp_sim = simulator.simulator(local_map, local_items, local_agents, local_main_agent, 10, 10)
    return tmp_sim


class State:

    def __init__(self, simulator):
        # At the root pretend the player just moved is p2 - p1 has the first move

        self.simulator = simulator
        self.q_table = self.create_empty_table()
        self.action_probabilities = [0, 0, 0, 0]  # ['N','E','S','W']

    def create_empty_table(self):
        qt = list()
        qt.append ( q_table_row('N', 0, 0))
        qt.append ( q_table_row('E', 0, 0))
        qt.append ( q_table_row('S', 0, 0))
        qt.append ( q_table_row('W', 0, 0))
        return qt


################################################################################################################
class Node:

    def __init__(self, depth, state, action=None, parent=None):

        self.parentNode = parent  # "None" for the root node
        self.depth = depth

        self.state = state
        self.action = action  # the move that got us to this node - "None" for the root node

        self.untriedMoves = self.create_possible_moves()
        self.childNodes = []

        self.cumulativeRewards = 0
        self.immediateReward = 0
        self.visits = 0
        self.expectedReward = 0
        self.numItems = state.simulator.items_left()

    def uct_select_child(self):

        ## UCB expects mean between 0 and 1.
        s = \
        sorted(self.childNodes, key=lambda c: c.expectedReward / self.numItems + sqrt(2 * log(self.visits) / c.visits))[
            -1]
        return s

    def add_child(self, a):

        n = Node(action=a, parent=self, depth=self.depth + 1,  state= self.state )
        self.untriedMoves.remove(a)
        self.childNodes.append(n)

        return n

    def create_possible_moves(self):

        (x, y) = self.state.simulator.main_agent.get_position()
        m = 10

        untriedMoves = ['N', 'E', 'S', 'W']

        # Check in order to avoid moving out of board.
        if x == 0:
            untriedMoves.remove('E')

        if y == 0:
            untriedMoves.remove('S')

        if x == m - 1:
            untriedMoves.remove('W')

        if y == m - 1:
            untriedMoves.remove('N')

        return untriedMoves

    def update(self, result):

        self.visits += 1
        self.cumulativeRewards += result + self.immediateReward
        self.expectedReward = self.cumulativeRewards / self.visits
        return self.expectedReward * 0.95  # discount factor = 0.95


################################################################################################################

def do_move(sim, move):
    get_reward = 0

    # get the position of main agent
    tmp_m_agent = sim.main_agent
    (x_m_agent, y_m_agent) = tmp_m_agent.get_position()

    # assign unknown agent
    tmp_a_agent = sim.agents[0]

    (x_new, y_new) = tmp_m_agent.new_position_with_given_action(10, 10, move)

    # If there is any item near main agent.
    if sim.the_map[y_new][x_new] == 1 or sim.the_map[y_new][x_new] == 4:

        item_loaded = False

        # Find the index and position of item that should be loaded.
        loaded_item_index = sim.get_item_by_position(x_new, y_new)

        (x_item, y_item) = (x_new, y_new)

        if tmp_m_agent.level >= sim.items[loaded_item_index].level:

            # load the item.
            tmp_m_agent.position = (x_item, y_item)
            sim.load_item(tmp_m_agent, loaded_item_index)

            get_reward += 1
            item_loaded = True
        else:

            # (x_a_agent, y_a_agent) = tmp_a_agent.get_position()

            # If unknown agent is in the loading position of the same item that main agent wants to collect.
            a_load = tmp_a_agent.is_agent_near_destination(x_new, y_new) and tmp_a_agent.next_action == 'L'

            # Check if two agents can load the item together
            if a_load and tmp_m_agent.level + tmp_a_agent.level >= sim.items[loaded_item_index].level:
                tmp_m_agent.position = (x_item, y_item)
                sim.load_item(tmp_m_agent, loaded_item_index)

                get_reward += 1

                # move a agent
                new_position = (x_item, y_item)
                sim.memory = position.position(0, 0)
                sim.update_map(tmp_a_agent.position, new_position)

                item_loaded = True

                # Update the map

        if item_loaded:
            tmp_m_agent.next_action = 'L'
            sim.main_agent = tmp_m_agent
            sim.update_map_mcts((x_m_agent, y_m_agent), (x_item, y_item))

    else:
        if (x_new, y_new) != tmp_a_agent.get_position():
            # Set the new action to the main agent.
            tmp_m_agent.next_action = move

            # Get new action of main agent and set it to the main agent.
            (x_new, y_new) = tmp_m_agent.change_position_direction(10, 10)
            sim.main_agent = tmp_m_agent
            sim.update_map_mcts((x_m_agent, y_m_agent), (x_new, y_new))

    return get_reward, sim


def best_action(node):
    node= node.uct_select_child()

    return node.action


def terminal(state):
    if state.simulator.items_left() == 0:
        return True

    return False


def leaf(node):
    if node.depth == max_depth:
        return True
    return False


def evalute(node):
    return node.expectedReward


def select_action(node):
    # If all childeren of the current node is expanded then Select Child based on UCB
    while node.untriedMoves == [] and node.childNodes != [] and node.numItems > 0:
        node = node.uct_select_child()
        return node.action, node

    # If there is some untried moves we will select a random move from the untried ones
    if node.untriedMoves != [] and node.numItems > 0:
        m = choice(node.untriedMoves)

        node = node.add_child(m)
        return m, node


def simulate_action(node, current_estimated_parameters):
    state = node.state
    sim = state.simulator
    a_agent = sim.agents[0]
    a_agent.set_parameters_array(current_estimated_parameters)
    # print('111111*********************************************************************')
    # sim.draw_map()
    # Run the agent to get the actions probabilities
    a_agent = sim.move_a_agent(a_agent)

    node.state.action_probabilities = a_agent.get_actions_probabilities()

    # print node.state.action_probabilities

    next_action = choice(actions, p=node.state.action_probabilities)  # random sampling the action

    a_reward = sim.update(a_agent, next_action)
    # print(node.action, '*********************************************************************')
    # sim.draw_map()

    m_reward , sim = do_move(sim, node.action)
    # print('33333333*********************************************************************')
    # sim.draw_map()

    state.simulator = sim
    return state, a_reward + m_reward


def update_value(node,  q):
    while 1 == 1:
        node_reward = node.update(q)
        # it is root node and iteration should stop here and just update the root node
        if node.depth == 0:
            node.update(node_reward)
            break
        node = node.parentNode

    return 0


def search(node, current_estimated_parameters):

    state = node.state

    if terminal(state):
        return 0

    if leaf(node):
        return evalute(node)

    action, child_node = select_action(node)
    # add a child with action but parents state. State will be update in simulate_action

    (next_state, reward) = simulate_action(child_node, current_estimated_parameters)
    child_node.state = next_state

    discount_factor = 0.95
    q = reward + discount_factor * search(child_node, current_estimated_parameters)
    update_value(node,  q)
    return q


def monte_carlo_planning(simulator, current_estimated_parameters):
    time_step = 0
    m_agent_position = simulator.main_agent.get_position()
    current_state = State(simulator)

    root_node = Node(depth=0, state=current_state)

    node = root_node

    while time_step < iteration_max:
         tmp_sim = create_temp_simulator(simulator.items, simulator.agents, simulator.main_agent)
         node.state.simulator = tmp_sim
         # print_nodes(node.childNodes)
         search(node, current_estimated_parameters)
         time_step += 1

    return best_action(node)


def move_agent(agents, items, main_agent, current_estimated_parameters):
    real_sim = create_temp_simulator(items, agents, main_agent)

    next_move = monte_carlo_planning(real_sim, current_estimated_parameters)

    return next_move

def print_nodes(childNodes):
    for i in range(len(childNodes)):
        print childNodes[i].action , ", Visits:",childNodes[i].visits , ", Rewards: ",    childNodes[i].expectedReward
