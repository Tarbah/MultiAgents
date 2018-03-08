import agent
import item
import simulator



radius_max = 1
radius_min = 0.1
angle_max = 1
angle_min = 0.1
level_max = 1
level_min = 0

# ============ Creating the map ==========================

items = []
agents = []
the_map = []


def initialize_items_agents_notrandom(n,m):
    # generating choices for random selection
    global the_map

    sf = list()
    sf.append((1, 2))
    sf.append((1, 5))
    sf.append((3, 4))
    sf.append((5, 8))
    sf.append((8, 1))
    sf.append((6, 2))
    sf.append((5, 4))
    sf.append((9, 4))
    sf.append((2, 6))
    sf.append((8, 8))

    # creating items
    for i in range(0, 10):
        (x, y) = sf[i]
        tmp_item = item.item(x, y, 1, i)
        items.append(tmp_item)
        the_map[y][x] = 1


    (x, y) = (1,1)
    main_agent = agent.Agent(x, y,'l2',1)
    unknown_agent = agent.Agent(9,9, 'l1',1)
    agents.append(main_agent)
    agents.append(unknown_agent)
    the_map[y][x] = 9
    the_map[8][8] = 8


def create_empty_map(n, m):
    # create the map

    row = [0] * n

    for i in range(m):
        the_map.append(list(row))


# ========== main part  ====== ===========

# Map creation


# ==============simulator initialisation=====================================================
n = 10  # horizontal size ,column
m = 10  # vertical size ,row

create_empty_map(n,m)

# initialize_items_agents(n, m)
initialize_items_agents_notrandom(n, m)
print('Agents: '.format(agents))
# Creates
real_sim = simulator.simulator(the_map, items, agents, n, m)


# ======================================================================================================
# Prints map to console
real_sim.draw_map()

t = 0
while t < 5:

    print 'main run count: ', t

    t = t + 1

    # Run's MCTS for the environment, moves agent forward one state and will grab an item if necessary
    real_sim.mcts_move()
    real_sim.draw_map()

    if real_sim.items_left() == 0:
        break
    print "left items", real_sim.items_left()

# TODO: Add new unknown agent to the map.
