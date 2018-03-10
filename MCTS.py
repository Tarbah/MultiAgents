from math import *
import random
import simulator
import item
import agent
import a_star

map = []


class State:

    def __init__(self, sim):
        self.the_map = sim.the_map  # At the root pretend the player just moved is p2 - p1 has the first move
        self.sim = sim
        self.items = sim.items
        self.agents = sim.agents
        self.sim.agents[0].reward = 0
        self.options = ['N', 'S', 'E', 'W']

    def Clone(self):
        state = State(self.sim)
        return state

    def DoMove(self, move):
        (xM, yM) = self.sim.agents[0].get_position()

        self.sim.agents[0].next_action = move
        (xA, yA) = self.sim.agents[0].change_position_direction(10, 10)
        get_reward = 0
        self.sim.agents[0].position = (xA, yA)

        if self.sim.the_map[yA][xA] == 1:  # load item
            nearby_item_index = self.sim.get_item_by_position(xA, yA)
            self.sim.load_item(self.sim.agents[0], nearby_item_index)
            self.sim.agents[0].reward += 1
            get_reward += 1
            (xA, yA) = self.sim.items[nearby_item_index].get_position()
        # else: # Move
        self.sim.update_map_mcts((xM, yM), (xA, yA))

        ## This should be the team reward, actually
        return get_reward

    def GetMoves(self):
        return self.options

    def GetResult(self):
        return self.sim.agents[0].reward


class Node:

    def __init__(self, level, move=None, parent=None, numItems=0):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.level = level
        self.childNodes = []
        self.cumulativeRewards = 0
        self.immediateReward = 0
        self.visits = 0
        self.expectedReward = 0
        self.numItems = numItems
        self.untriedMoves = ['N', 'S', 'E', 'W']

    def UCTSelectChild(self):
        """
        Runs UCB for all child nodes.
        UCB expects mean between 0 and 1.
        :return: Maximumum UCB Value
        """
        s = \
        sorted(self.childNodes, key=lambda c: c.expectedReward / self.numItems + sqrt(2 * log(self.visits) / c.visits))[
            -1]
        return s

    def AddChild(self, m, s):
        n = Node(move=m, parent=self, level=self.level + 1, numItems=self.numItems)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)

        return n

    def Update(self, result):
        self.visits += 1
        self.cumulativeRewards += result + self.immediateReward

        self.expectedReward = self.cumulativeRewards / self.visits

        return self.expectedReward * 0.95  # discount factor = 0.95


# TODO: Might MCTS be faster if implemented in NumPy rather than lists?
def create_temp_simulator(items, agents):
    """
    Creates an environment representation
    :param items: Item's positions
    :param agents: Agent object
    :return: Simulator object representing the position of the agent and items
    """
    local_map = []
    row = [0] * 10

    # Create a 10x10 array of zeroes - an empty environment
    for i in range(10):
        local_map.append(list(row))

    # Store each item's position in the environment
    local_items = []
    for i in range(len(items)):
        (item_x, item_y) = items[i].get_position()
        local_item = item.item(item_x, item_y, 1, i)
        local_item.loaded = items[i].loaded
        local_items.append(local_item)
        if not local_item.loaded:
            local_map[item_y][item_x] = 1

    # Get the position of the first agent
    local_agents = list()
    (m_agent_x, m_agent_y) = agents[0].get_position()

    # Represent the agent's position as a 9 in the environment
    local_map[m_agent_y][m_agent_x] = 9
    local_agent = agent.Agent(m_agent_x, m_agent_y, 'l1', 1)
    local_agents.append(local_agent)

    # Build a simulator using the previously created lists
    tmp_sim = simulator.simulator(local_map, local_items, local_agents, 10, 10)
    return tmp_sim


def UCT(local_sim, itermax, num_items):
    """
    Runs UCB for the Monte Carlo Tree
    :param local_sim: Simulation object containing information on the agent's and item's positions
    :param itermax: Number of iterations to make
    :param num_items: The number of items left in the environment
    :return: N, S, E, W. The direction for the agent to move in
    """
    rootnode = Node(level=0, numItems=num_items)
    node = rootnode

    # import ipdb; ipdb.set_trace()

    for i in range(itermax):

        # Create simulation of current state and store in a State object
        tmp_sim = create_temp_simulator(local_sim.items, local_sim.agents)
        tmp_state = State(tmp_sim)

        # Get first moves
        while node.untriedMoves == [] and node.childNodes != [] and node.numItems > 0:
            # node is fully expanded and non-terminal
            # if we try all possible moves and current node has a child then select a node to expand
            # We will move till reaching a leaf which don't have any child and we don't
            node = node.UCTSelectChild()

            # Moves down the tree to the node of highest UCB Value
            tmp_state.DoMove(node.move)

        # Expand
        if node.untriedMoves != [] and node.numItems > 0:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            get_reward = tmp_state.DoMove(m)
            node = node.AddChild(m, tmp_state)  # add child and descend tree
            node.immediateReward = get_reward
            node.numItems -= get_reward  # I assume get_reward is the number of collected boxes, so we can use it to decrease the number of boxes available

            # Nothing to do if the scenario is cleared, we created a terminal node
            if (node.numItems == 0):
                continue

        node_reward = 0

        if node.numItems > 0:
            # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
            rollout_max = 100
            # rollout_max = 10
            rollout_count = 0

            rollout_sim = create_temp_simulator(tmp_state.sim.items, tmp_state.sim.agents)
            rollout_state = State(rollout_sim)

            while rollout_count < rollout_max:  # while state is non-terminal
                move = random.choice(rollout_state.GetMoves())
                get_reward = rollout_state.DoMove(move)
                if get_reward:
                    node_reward += 1 * (0.95 ** rollout_count)

                rollout_count += 1

        # Backpropagate
        # TO CHECK: Are we handling the "no items" case correctly?

        while 1 == 1:  # backpropagate from the expanded node and work back to the root node
            node_reward = node.Update(node_reward)

            node = node.parentNode
            # it is root node and iteration should stop here and just update the root node
            if node.level == 0:
                node.Update(node_reward)
                break

    # N is going South, and S is going North
    # Prints UCT details
    for n in rootnode.childNodes:
        print ('Direction: {}'.format(n.move)) # N, S, E, or W
        print('Expected Reward: {}'.format(n.expectedReward / 10))
        print('Cumulative Rewards: {}'.format(n.cumulativeRewards))
        print('Number of Visits: {}\n'.format(n.visits))

    # import ipdb; ipdb.set_trace()
    result = sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited
    print('UCT Result: {}'.format(result))
    return result


def move_agent(agents, items):
    """
    Returns the direction for which the agent will move after this simulation. Essentially generates the lists for the
    map, agents and map, simulates them and passes it to a UCB algortihm
    :param agents: Agent(s) for which the simulation should occur for
    :param items: Item's position in the environment
    :return: N, S, E, W. The direction for the agent to move in
    """
    local_map = []
    row = [0] * 10

    # Builds a 10x10 array of 0s np.zeros
    for i in range(10):
        local_map.append(list(row))

    # Append local item's position to map
    local_items = []
    num_items = 0
    for i in range(len(items)):
        (item_x, item_y) = items[i].get_position()
        local_item = item.item(item_x, item_y, 1, i)
        local_item.loaded = items[i].loaded
        local_items.append(local_item)
        if not local_item.loaded:
            local_map[item_y][item_x] = 1
            num_items += 1

    # Gets the position of the first agent of the method's argument
    local_agents = list()
    for i in range(len(agents)):
        (m_agent_x, m_agent_y) = agents[i].get_position()
        # Appends a 9 to the map for the position of that agent
        local_map[m_agent_y][m_agent_x] = 9
        # Calls an Agent object with position passed to method and type 'l1'
        local_agent = agent.Agent(m_agent_x, m_agent_y, 'l1', 1)
        local_agents.append(local_agent)

    print('Number of Local Agents: {}\n'.format(len(local_agents)))

    # Creates simulation object with aforementioned objects
    real_sim = simulator.simulator(local_map, local_items, local_agents, 10, 10)

    # Uses UCT to determine the next move
    # Decides based upon the move that was visited most
    next_move = UCT(real_sim, itermax=10000, num_items=num_items)

    return next_move
