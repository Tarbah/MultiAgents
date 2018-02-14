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
    sf.append((9, 9))

    # creating items
    for i in range(0, 10):
        (x, y) = sf[i]
        tmp_item = item.item(x, y, 1, i)
        items.append(tmp_item)
        the_map[y][x] = 1


    (x, y) = (1,1)
    main_agent = agent.Agent(x, y,'l1',1)
    agents.append(main_agent)
    the_map[y][x] = 9


def create_empty_map(n,m):
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

real_sim = simulator.simulator(the_map, items, agents,n,m)


# ======================================================================================================
real_sim.draw_map()

t = 0
while t < 35:

    print 'main run count: ', t

    t = t + 1

    real_sim.mcts_move()
    real_sim.draw_map()

    if real_sim.items_left() == 0:
        break
    print "left items", real_sim.items_left()


