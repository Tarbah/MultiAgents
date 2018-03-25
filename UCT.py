from math import *
from numpy.random import choice
import simulator
import item
import agent
import position

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

## TODO: I think this method is not necessary. What we want is to use the copy method inside simulator class, right?
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

        ## TODO: Does not seem necessary. Also looks like our State is just a wrapper for Simulator
        ##self.action_probabilities = [0, 0, 0, 0]  # ['N','E','S','W']


    def equals(self, state):
        return self.simulator.equals(state.simulator)

################################################################################################################
class Node:

    def __init__(self, depth, state, action=None, parent=None):

        self.parentNode = parent  # "None" for the root node
        self.depth = depth

        self.state = state
        self.Q_table = self.create_empty_table()

        ## It is better to not have that. Different actions could lead to the same s'
        #self.action = action  # the move that got us to this node - "None" for the root node

        self.untriedMoves = self.create_possible_moves()
        self.childNodes = []

        #self.cumulativeRewards = 0
        #self.immediateReward = 0
        self.visits = 0
        #self.expectedReward = 0
        self.numItems = state.simulator.items_left()


    def create_empty_table(self):
        Qt = list()
        Qt.append ( Q_table_row('L', 0, 0, 0))
        Qt.append ( Q_table_row('N', 0, 0, 0))
        Qt.append ( Q_table_row('E', 0, 0, 0))
        Qt.append ( Q_table_row('S', 0, 0, 0))
        Qt.append ( Q_table_row('W', 0, 0, 0))
        return Qt

        
    def uct_select_action(self):
        #Q_table = self.Q_table

        #action = sorted(Q_table, key=lambda c: c.QValue + sqrt(2 * log(self.visits) / c.trials))[-1]
        # for a in range(len(self.Q_table)):
        #     if (self.Q_table[a].trials == 0):
        #         import ipdb; ipdb.set_trace()

        
        maxUCB = -1
        maxA = None

        #if (self == root):
        #    import ipdb; ipdb.set_trace()
        
        for a in range(len(self.Q_table)):
            if (self.valid(self.Q_table[a].action)):            
                currentUCB = self.Q_table[a].QValue + sqrt(2.0 * log(float(self.visits)) / float(self.Q_table[a].trials))

                if (currentUCB > maxUCB):
                    maxUCB = currentUCB
                    maxA = self.Q_table[a].action

        return maxA
        
    # def uct_select_child(self):

    #     ## UCB expects mean between 0 and 1.
    #     s = \
    #     sorted(self.childNodes, key=lambda c: c.expectedReward / self.numItems + sqrt(2 * log(self.visits) / c.visits))[
    #         -1]
    #     return s

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
            if (action == 'E'):
                return False

        if y == 0:
            if (action == 'S'):
                return False

        ## TODO: There is a bug here. It will only work for squared scenarios
        if x == m - 1:
            if (action == 'W'):
                return False

        if y == m - 1:
            if (action == 'N'):
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

    def update(self, action, result):
        ## TODO: We should change the table to a dictionary, so that we don't have to find the action
        for i in range(len(self.Q_table)):
            if (self.Q_table[i].action == action):        
                self.Q_table[i].trials += 1
                self.Q_table[i].sumValue += result
                self.Q_table[i].QValue = self.Q_table[i].sumValue/self.Q_table[i].trials
                return


################################################################################################################

def do_move(sim, move):
    get_reward = 0

    # get the position of main agent
    tmp_m_agent = sim.main_agent
    (x_m_agent, y_m_agent) = tmp_m_agent.get_position()

    # assign unknown agent
    tmp_a_agent = sim.agents[0]

    (x_new, y_new) = tmp_m_agent.new_position_with_given_action(10, 10, move)

    ### TODO: Something is weird here. I should only load an item if the action was "load"
    ### TODO: Also, only M agent should be moving here, not A agent

    ## TODO: M shouldn't move to the item position if the action was Load... But keeping it for now to be similar to previous version
    if (move == 'L'):

#        import ipdb; ipdb.set_trace()
        
        # If there is any item near main agent.
        x_item = None
        y_item = None

        if (y_new - 1 > -1) and (sim.the_map[y_new - 1][x_new] == 1 or sim.the_map[y_new - 1][x_new] == 4):
            y_item = y_new - 1
            x_item = x_new

        ## TODO: Check: self.n or self.m?
        if (y_new + 1 < sim.n) and (sim.the_map[y_new + 1][x_new] == 1 or sim.the_map[y_new + 1][x_new] == 4):
            y_item = y_new + 1
            x_item = x_new
        
        if (x_new - 1 > -1) and (sim.the_map[y_new][x_new - 1] == 1 or sim.the_map[y_new][x_new - 1] == 4):
            y_item = y_new
            x_item = x_new - 1

        ## TODO: Check: self.n or self.m?            
        if (x_new + 1 < sim.m) and (sim.the_map[y_new][x_new + 1] == 1 or sim.the_map[y_new][x_new + 1] == 4):
            y_item = y_new
            x_item = x_new + 1

            
        if (x_item != None):

            item_loaded = False

            # Find the index and position of item that should be loaded.
            loaded_item_index = sim.get_item_by_position(x_item, y_item)



            # load the item.
            # for now the agent will assume the item position if loaded
            tmp_m_agent.position = (x_item, y_item)
            sim.load_item(tmp_m_agent, loaded_item_index)


            sim.update_map_mcts((x_m_agent, y_m_agent), (x_item, y_item))
                 
            get_reward += float(1)/totalItems
            item_loaded = True

           ## TODO: The level test is not working yet 
            # if tmp_m_agent.level >= sim.items[loaded_item_index].level:

            #      # load the item.
            #      # for now the agent will assume the item position if loaded
            #      tmp_m_agent.position = (x_item, y_item)
            #      sim.load_item(tmp_m_agent, loaded_item_index)


            #      sim.update_map_mcts((x_m_agent, y_m_agent), (x_item, y_item))
                 
            #      get_reward += float(1)/totalItems
            #      item_loaded = True
            # else:

            #      # (x_a_agent, y_a_agent) = tmp_a_agent.get_position()

            #      # If unknown agent is in the loading position of the same item that main agent wants to collect.
            #      a_load = tmp_a_agent.is_agent_near_destination(x_new, y_new) and tmp_a_agent.next_action == 'L'

            #      # Check if two agents can load the item together
            #      if a_load and tmp_m_agent.level + tmp_a_agent.level >= sim.items[loaded_item_index].level:
            #          tmp_m_agent.position = (x_item, y_item)
            #          sim.load_item(tmp_m_agent, loaded_item_index)

            #          get_reward += float(1)/totalItems

            #          # move a agent
            #          new_position = (x_item, y_item)
            #          sim.memory = position.position(0, 0)
            #          sim.update_map(tmp_a_agent.position, new_position)

            #          item_loaded = True

            #          # Update the map

            #          if item_loaded:
            #              tmp_m_agent.next_action = 'L'
            #              sim.main_agent = tmp_m_agent
            #              sim.update_map_mcts((x_m_agent, y_m_agent), (x_item, y_item))

    else:
        hasItem = True
        testItem = sim.get_item_by_position(x_new,y_new) 
        if (testItem != -1):
            if (sim.items[testItem].loaded):
                hasItem = False
        else:
            hasItem = False
                
        if ((x_new, y_new) != tmp_a_agent.get_position() and (not hasItem)):
            # Set the new action to the main agent.
            tmp_m_agent.next_action = move

            # Get new action of main agent and set it to the main agent.
            (x_new, y_new) = tmp_m_agent.change_position_direction(10, 10)
            sim.main_agent = tmp_m_agent
            sim.update_map_mcts((x_m_agent, y_m_agent), (x_new, y_new))


    return get_reward


def best_action(node):
    Q_table = node.Q_table

    maxA = None
    maxQ = -1
    for a in range(len(Q_table)):
        if (Q_table[a].QValue > maxQ):
            maxQ = Q_table[a].QValue
            maxA = Q_table[a].action

    return maxA


def terminal(state):
    if state.simulator.items_left() == 0:
        return True

    return False


def leaf(node):
    if node.depth == max_depth + 1:
        return True
    return False


def evalute(node):
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
    ## We have to be careful, all objects and lists in Python are actually pointers
    next_state = State(state.simulator.copy())
    #next_state.simulator = state.simulator.copy()
    
    sim = next_state.simulator
    a_agent = sim.agents[0]
    a_agent.set_parameters_array(current_estimated_parameters)
    # print('111111*********************************************************************')
    # sim.draw_map()
    # Run the agent to get the actions probabilities
    ## TODO: CHECK: There are no side-effects here?
    a_agent = sim.move_a_agent(a_agent)

    action_probabilities = a_agent.get_actions_probabilities()

    # print node.state.action_probabilities

    next_action = choice(actions, p=action_probabilities)  # random sampling the action

    a_reward = sim.update(a_agent, next_action)
    ## Dividing here because the simulator does not know the number of total items that we started with
    if (a_reward > 0):
        a_reward = float(a_reward)/totalItems
    # print(node.action, '*********************************************************************')
    # sim.draw_map()

    ## TODO: Check side-effects
    m_reward = do_move(sim, action)
    # print('33333333*********************************************************************')
    # sim.draw_map()

    #state.simulator = sim

    return next_state, a_reward + m_reward

## The recursive update is already in the search method
# def update_value(node, action, q):    
#     # while 1 == 1:
#     #     node_reward = node.update(q)
#     #     # it is root node and iteration should stop here and just update the root node
#     #     if node.depth == 0:
#     #         node.update(node_reward)
#     #         break
#     #     node = node.parentNode

    
    
#     return 0


def search(node, current_estimated_parameters):

    state = node.state

    if terminal(state):
        return 0

    if leaf(node):
        return 0#evalute(node)

    action = select_action(node)
    
    # Agents move at the same time, so the previous action was not performed yet in the point of view of A agent.
    # Hence, we simulate next state from the current node state
    (next_state, reward) = simulate_action(node.state, action, current_estimated_parameters)

    # Now we must either create a new child node or go to an existing node
    # I will assume that different actions a_i could lead to the same s'
    # However, I will assume that the s_i node when coming from parent s
    # will be different than s_i node when coming from a different parent s'.
    # This will make it simpler (i.e., a tree, not a graph), and more efficient

    next_node = None
    for child in node.childNodes:
        if (child.state.equals(next_state)):
            next_node = child
            break

    if (next_node == None):
        next_node = node.add_child(next_state)
    
    discount_factor = 0.95
    q = reward + discount_factor * search(next_node, current_estimated_parameters)

#    if (q > 0):
#        import ipdb; ipdb.set_trace()
    
    node.update(action, q)
    node.visits += 1
    return q


def monte_carlo_planning(simulator, current_estimated_parameters):
    global root
    
    time_step = 0
    m_agent_position = simulator.main_agent.get_position()
    current_state = State(simulator)

    root_node = Node(depth=0, state=current_state)

    node = root_node

    root = node
    
    while time_step < iteration_max:
         tmp_sim = create_temp_simulator(simulator.items, simulator.agents, simulator.main_agent)
         node.state.simulator = tmp_sim
         # print_nodes(node.childNodes)
         search(node, current_estimated_parameters)
         time_step += 1

    #import ipdb; ipdb.set_trace()
    
    return best_action(node)


def move_agent(agents, items, main_agent, current_estimated_parameters):
    global totalItems
    
    real_sim = create_temp_simulator(items, agents, main_agent)

    ## We need total items, because the QValues must be between 0 and 1
    totalItems = real_sim.items_left()
    
    next_move = monte_carlo_planning(real_sim, current_estimated_parameters)

    return next_move

def print_nodes(childNodes):
    for i in range(len(childNodes)):
        print childNodes[i].action , ", Visits:",childNodes[i].visits , ", Rewards: ",    childNodes[i].expectedReward
