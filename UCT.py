from math import *
from numpy.random import choice
import gc

## TODO: Perhaps we should have a configuration file, besides the scenario file
iteration_max = 1000
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

########################################################################################################################

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

    #@staticmethod
    #def create_empty_table():
    # Not sure if this needs to be a static method. I removed static for now, because re-using tree is leaking memory...
    def create_empty_table(self):
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

    def uct_select_child(self):

        ## UCB expects mean between 0 and 1.
        s = \
        sorted(self.childNodes, key=lambda c: c.expectedReward / self.numItems + sqrt(2 * log(self.visits) / c.visits))[
            -1]
        return s
    def uct_select_action(self):

        maxUCB = -1
        maxA = None
        
        for a in range(len(self.Q_table)):
            if self.valid(self.Q_table[a].action):

                #currentUCB = self.Q_table[a].QValue + sqrt(2.0 * log(float(self.visits)) / float(self.Q_table[a].trials))
                
                ## TODO: The exploration constant could be set up in the configuration file
                currentUCB = self.Q_table[a].QValue + 0.5*sqrt(log(float(self.visits)) / float(self.Q_table[a].trials))

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

        m = self.state.simulator.dim_w
        n = self.state.simulator.dim_h

        # Check in order to avoid moving out of board.
        if x == 0:
            if action == 'W':
                return False

        if y == 0:
            if action == 'S':
                return False
        if x == m - 1:
            if action == 'E':
                return False

        if y == n - 1:
            if action == 'N':
                return False

        return True

    def create_possible_moves(self):

        (x, y) = self.state.simulator.main_agent.get_position()

        m = self.state.simulator.dim_w
        n = self.state.simulator.dim_h

        untriedMoves = ['L', 'N', 'E', 'S', 'W']

        # Check in order to avoid moving out of board.
        if x == 0:
            untriedMoves.remove('W')

        if y == 0:
            untriedMoves.remove('S')

        if x == m - 1:
            untriedMoves.remove('E')

        if y == n - 1:
            untriedMoves.remove('N')

        return untriedMoves


########################################################################################################################

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


################################################################################################################
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


################################################################################################################
def terminal(state):
    if state.simulator.items_left() == 0:
        return True

    return False


################################################################################################################
def leaf(main_time_step ,node):
    if node.depth == main_time_step + max_depth + 1:
        return True
    return False


################################################################################################################
def evaluate(node):
    return node.expectedReward


################################################################################################################
def select_action(node):
    # If all *actions* of the current node have been tried at least once, then Select Child based on UCB

    if node.untriedMoves == []:
        return node.uct_select_action()

    # If there is some untried moves we will select a random move from the untried ones
    if node.untriedMoves != []:
        move = choice(node.untriedMoves)
        node.untriedMoves.remove(move)
        return move


################################################################################################################
def simulate_action(state, action, current_estimated_parameters):

    sim = state.simulator.copy()
    next_state = State(sim)

    # Run the A agent to get the actions probabilities

    for i in range(len(sim.agents)):
        sim.agents[i].set_parameters_array(sim,current_estimated_parameters)
        sim.agents[i] = sim.move_a_agent(sim.agents[i])

    m_reward = do_move(sim, action)

    a_reward = sim.update_all_A_agents()

    if sim.do_collaboration():
        c_reward = float(1)
    else:
        c_reward = 0

    total_reward = float(m_reward + a_reward + c_reward) / totalItems

    return next_state, total_reward


################################################################################################################

def find_new_root(previous_root,current_state):

    ## Initialise with new node, just in case the child was not yet expanded
    root_node = Node(depth=previous_root.depth+1,state=current_state)

    for child in previous_root.childNodes:
        if child.state.equals(current_state):
            root_node = child
            break

    return root_node


################################################################################################################
def search(main_time_step,node, current_estimated_parameters):

    state = node.state

    if terminal(state):
        return 0

    if leaf(main_time_step,node):
        return 0

    action = select_action(node)
    # print ('---action:',action)
    # print_Q_table(node)

    (next_state, reward) = simulate_action(node.state, action, current_estimated_parameters)

    # next_state.simulator.draw_map()
    next_node = None
    for child in node.childNodes:
        if child.state.equals(next_state):
            next_node = child
            break

    if next_node is None:
        next_node = node.add_child(next_state)

    discount_factor = 0.95
    q = reward + discount_factor * search(main_time_step, next_node, current_estimated_parameters)

    node.update(action, q)
    node.visits += 1

    return q


########################################################################################################################
def monte_carlo_planning(main_time_step, search_tree, simulator, current_estimated_parameters):
    global root

    current_state = State(simulator)

    if search_tree is None:
        root_node = Node(depth=0, state=current_state)
    else:
        root_node = find_new_root(search_tree , current_state)
        print "----- Beginning of monte_carlo_planning ---- "
        print "root node children:", len(root_node.childNodes)
        
    #print_Q_table(root_node)
    time_step = 0

    node = root_node
    root = node

    while time_step < iteration_max:
        tmp_sim = simulator.copy()
        node.state.simulator = tmp_sim
        # print('monte_carlo_planning', time_step)
        # print_Q_table(node)
        # print_nodes(node.childNodes)
        # print('=================================================================')
        search(main_time_step, node, current_estimated_parameters)
        
        time_step += 1

    # print_search_tree(main_time_step)
    # print('_________________________________________________________________________________________________________')
    print "----- End of monte_carlo_planning ---- "
    print_Q_table(node)

    best_selected_action = best_action(node)
    print "Selected Action: ", best_selected_action

    return best_selected_action, node


########################################################################################################################
def m_agent_planning(time_step,search_tree,sim,current_estimated_parameters):
    global totalItems

    tmp_sim = sim.copy()
    
    ## We need total items, because the QValues must be between 0 and 1
    ## If we are re-using the tree, I think we should use the initial number of items, and not update it
    if (search_tree is None):
        totalItems = tmp_sim.items_left()

    next_move , search_tree = monte_carlo_planning(time_step, search_tree,tmp_sim, current_estimated_parameters)

    return next_move , search_tree


########################################################################################################################
def print_search_tree(main_time_step):

    node = root

    for i in range(max_depth + main_time_step ):
        print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
        print node.depth
        print_nodes(node.childNodes)
        if len(node.childNodes)>0 :
            node = node.childNodes[0]
        else:
            break


########################################################################################################################
def print_nodes(childNodes):
    print('Total number of children:', len(childNodes))
    for i in range(len(childNodes)):
        print 'Node: ', i
        print_Q_table(childNodes[i])
        # print childNodes[i].state.simulator.draw_map()

################################################################################################################
def print_Q_table(node):
    for a in range(len(node.Q_table)):
        print "Action: ", node.Q_table[a].action, "QValue:", node.Q_table[a].QValue, "sumValue:", node.Q_table[a].sumValue, "trials:", node.Q_table[a].trials
