from math import *
import random


class State:

    def __init__(self, sim):
        self.the_map = sim.the_map  # At the root pretend the player just moved is p2 - p1 has the first move
        self.sim = sim
        self.items = sim.items
        self.agents = sim.agents
        self.mcts_agent = sim.agents[1]
        self.astar_agent = sim.agents[0]
        self.mcts_agent.reward = 0
        self.options = ['N', 'S', 'E', 'W']

    def Clone(self):
        state = State(self.sim)
        return state

    def DoMove(self, move):

        (xM, yM) = self.mcts_agent.get_position()

        self.mcts_agent.next_action = move
        nearby_item_index = self.mcts_agent.is_item_nearby(self.items)

        if nearby_item_index == -1:

            (xA, yA) = self.mcts_agent.change_position_direction(10, 10)

        else:

            self.sim.load_item(self.mcts_agent,nearby_item_index)
            self.mcts_agent.position = self.sim.items[nearby_item_index].get_position()
            self.mcts_agent.reward +=1
            (xA, yA) = self.sim.items[nearby_item_index].get_position()

        self.sim.update_map((xM, yM), (xA, yA))

        #self.sim.draw_map()

    def GetMoves(self):
        return self.options

    def GetResult(self):
        return self.mcts_agent.reward


class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.rewards = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves()  # future child nodes


    def UCTSelectChild(self):

        s = sorted(self.childNodes, key=lambda c: c.rewards / c.visits + sqrt(2 * log(self.visits) / c.visits))[-1]
        return s

    def AddChild(self, m, s):

        n = Node(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):

        self.visits += 1
        self.rewards += result

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, parameters_estimation):

    rootnode = Node(state=rootstate)

    for i in range(itermax):

        node = rootnode
        state = rootstate.Clone()
        agent = state.sim.agents[0]

        # Select
       # print "********** UCT select ", i
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        #print "********** UCT Expand ", i
        #print(node.untriedMoves )
        if node.untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
           # print "In if of Expand ", i
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree
       # print(state.GetMoves())

       # print "********** UCT Rollout ", i
        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function

        while state.GetMoves() != []:  # while state is non-terminal
            move = random.choice(state.GetMoves())
            state.DoMove(move)
            state.options.remove(move)
            state.astar_agent.set_parameters(parameters_estimation[0], parameters_estimation[1], parameters_estimation[2])
            state.sim.run_and_update(state.astar_agent)

       # print "********** UCT Backpropagate ", i
        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult())
            node = node.parentNode



    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited


def move_agent(sim,parameters):

    state = State(sim)
   # print(parameters)
    m = UCT(rootstate=state, itermax=10, parameters_estimation =parameters  )
  #  print "Best Move: " + str(m) + "\n"

    state.DoMove(m)
    return state.sim
