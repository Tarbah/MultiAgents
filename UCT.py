from math import *
from numpy.random import choice

iteration_max = 100
max_depth = 100

totalItems = 0 ## TODO: Adding as a global variable for now

actions = ['L', 'N', 'E', 'S', 'W']

root = None


class Q_table_row:
    def __init__(self, action, QValue, sumValue, trials):
        self.action = action
        self.QValue = QValue
        self.sumValue = sumValue
        self.trials = trials


class State:

    def __init__(self, simulator):

        self.simulator = simulator

    def equals(self, state):
        return self.simulator.equals(state.simulator)

################################################################################################################


class Node:

    def __init__(self, depth, state,  parent=None):

        self.parentNode = parent  # "None" for the root node
        self.depth = depth

        self.state = state
        self.Q_table = self.create_empty_table()

        self.untriedMoves = self.create_possible_moves()
        self.childNodes = []

        self.visits = 0

        self.numItems = state.simulator.items_left()

    @staticmethod
    def create_empty_table():

        Qt = list()
        Qt.append(Q_table_row('L', 0, 0, 0))
        Qt.append(Q_table_row('N', 0, 0, 0))
        Qt.append(Q_table_row('E', 0, 0, 0))
        Qt.append(Q_table_row('S', 0, 0, 0))
        Qt.append(Q_table_row('W', 0, 0, 0))
        return Qt

    def update(self, action, result):

        ## TODO: We should change the table to a dictionary, so that we don't have to find the action
        for i in range(len(self.Q_table)):
            if self.Q_table[i].action == action:
                self.Q_table[i].trials += 1
                self.Q_table[i].sumValue += result
                self.Q_table[i].QValue = self.Q_table[i].sumValue/self.Q_table[i].trials
                return

    def uct_select_action(self):

        maxUCB = -1
        maxA = None
        
        for a in range(len(self.Q_table)):
            if self.valid(self.Q_table[a].action):
                currentUCB = self.Q_table[a].QValue + sqrt(2.0 * log(float(self.visits)) / float(self.Q_table[a].trials))

                if currentUCB > maxUCB:
                    maxUCB = currentUCB
                    maxA = self.Q_table[a].action

        return maxA

    def add_child(self, state):

        n = Node(parent=self, depth=self.depth + 1, state=state)
        self.childNodes.append(n)

        return n

    def valid(self, action):
        (x, y) = self.state.simulator.main_agent.get_position()
        ## TODO: We should get from the map/simulator here the correct dimension
        m = 10

        # Check in order to avoid moving out of board.
        if x == 0:
            if action == 'E':
                return False

        if y == 0:
            if action == 'S':
                return False

        ## TODO: There is a bug here. It will only work for squared scenarios
        if x == m - 1:
            if action == 'W':
                return False

        if y == m - 1:
            if action == 'N':
                return False

        return True

    def create_possible_moves(self):

        (x, y) = self.state.simulator.main_agent.get_position()
        ## TODO: We should get from the map/simulator here the correct dimension
        m = 10

        untriedMoves = ['L', 'N', 'E', 'S', 'W']

        # Check in order to avoid moving out of board.
        if x == 0:
            untriedMoves.remove('E')

        if y == 0:
            untriedMoves.remove('S')

        ## TODO: There is a bug here. It will only work for squared scenarios
        if x == m - 1:
            untriedMoves.remove('W')

        if y == m - 1:
            untriedMoves.remove('N')

        return untriedMoves

################################################################################################################


def do_move(sim, move):

    get_reward = 0

    tmp_m_agent = sim.main_agent

    if move == 'L':
        load_item, (item_position_x,  item_position_y) = tmp_m_agent.is_agent_face_to_item(sim)
        if load_item:
            destinantion_item_index = sim.find_item_by_location(item_position_x, item_position_y)
            if sim.items [destinantion_item_index].level <= tmp_m_agent.level:
                sim.items[destinantion_item_index].loaded = True
                get_reward += float(1.0)
            else:
                sim.items[destinantion_item_index].agents_load_item.append(tmp_m_agent)

    else:
        (x_new, y_new) = tmp_m_agent.new_position_with_given_action(sim.dim_w, sim.dim_h, move)

        # If there new position is empty
        if sim.position_is_empty(x_new, y_new):
            tmp_m_agent.next_action = move
            tmp_m_agent.change_position_direction(sim.dim_w, sim.dim_h)

        else:
            tmp_m_agent.change_direction_with_action(move)

        sim.main_agent = tmp_m_agent

    sim.update_the_map()

    return get_reward


def best_action(node):
    Q_table = node.Q_table

    maxA = None
    maxQ = -1
    for a in range(len(Q_table)):
        if Q_table[a].QValue > maxQ:
            maxQ = Q_table[a].QValue
            maxA = Q_table[a].action

    # maxA=node.uct_select_action()
    return maxA


def terminal(state):
    if state.simulator.items_left() == 0:
        return True

    return False


def leaf(node):
    if node.depth == max_depth + 1:
        return True
    return False


def evaluate(node):
    return node.expectedReward


def select_action(node):
    # If all *actions* of the current node have been tried at least once, then Select Child based on UCB
    if node.untriedMoves == []:
        return node.uct_select_action()

    # If there is some untried moves we will select a random move from the untried ones
    if node.untriedMoves != []:
        move = choice(node.untriedMoves)
        node.untriedMoves.remove(move)
        return move


def simulate_action(state, action, current_estimated_parameters):

    sim = state.simulator.copy()
    next_state = State(sim)

    # Run the A agent to get the actions probabilities

    for i in range(len(sim.agents)):
        sim.agents[i].set_parameters_array(current_estimated_parameters)
        sim.agents[i] = sim.move_a_agent(sim.agents[i])

    m_reward = do_move(sim, action)

    a_reward = sim.update_all_A_agents()

    if sim.do_collaboration():
        c_reward = float(1)
    else:
        c_reward = 0
    #
    # print('*********************************************************************')
    # sim.draw_map()

    total_reward = float(m_reward + a_reward + c_reward) / totalItems

    return next_state, total_reward


def search(node, current_estimated_parameters):

    state = node.state

    if terminal(state):
        return 0

    if leaf(node):
        return 0

    action = select_action(node)
    # print ('---action:',action)
    # print_Q_table(node)

    # Agents move at the same time, so the previous action was not performed yet in the point of view of A agent.
    # Hence, we simulate next state from the current node state
    (next_state, reward) = simulate_action(node.state, action, current_estimated_parameters)
    # print '***Search***',node.depth
    # next_state.simulator.draw_map()
    # Now we must either create a new child node or go to an existing node
    # I will assume that different actions a_i could lead to the same s'
    # However, I will assume that the s_i node when coming from parent s
    # will be different than s_i node when coming from a different parent s'.
    # This will make it simpler (i.e., a tree, not a graph), and more efficient
    # print('reward:', reward)
    # print next_state.simulator.draw_map()
    next_node = None
    for child in node.childNodes:
        if child.state.equals(next_state):
            next_node = child
            break

    if next_node == None:
        next_node = node.add_child(next_state)

    discount_factor = 0.95
    q = reward + discount_factor * search(next_node, current_estimated_parameters)

    node.update(action, q)
    node.visits += 1
    return q


def print_Q_table(node):
    for a in range(len(node.Q_table)):
        print "Action: ", node.Q_table[a].action , "QValue:", node.Q_table[a].QValue  , "sumValue:", node.Q_table[a].sumValue , "trials:", node.Q_table[a].trials


def monte_carlo_planning(simulator, current_estimated_parameters):
    global root
    
    time_step = 0
    current_state = State(simulator)

    root_node = Node(depth=0, state=current_state)
    node = root_node
    root = node

    while time_step < iteration_max:
        tmp_sim = simulator.copy()
        node.state.simulator = tmp_sim
        # print('monte_carlo_planning', time_step)
        # print_Q_table(node)
        # # print_nodes(node.childNodes)
        # print('=================================================================')
        search(node, current_estimated_parameters)
        
        time_step += 1

    # print('_____________________________________________________________________________________________________________________')
    # print_Q_table(node)
    return best_action(node)


def print_nodes(childNodes):
    print('Total number of children:',len(childNodes) )
    for i in range(len(childNodes)):
        print 'Node: ' , i
        print childNodes[i].state.simulator.draw_map()


def m_agent_planning(sim,current_estimated_parameters):
    global totalItems

    tmp_sim = sim.copy()
    ## We need total items, because the QValues must be between 0 and 1
    totalItems = tmp_sim.items_left()

    next_move = monte_carlo_planning(tmp_sim, current_estimated_parameters)

    return next_move

