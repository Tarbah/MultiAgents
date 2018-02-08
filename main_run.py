import agent
import item
import random
import simulator
import parameter_estimation


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

    # creating agent
    (x, y) = (4,4)
    unknown_agent = agent.Agent(x, y,'l1',0)
    the_map[y][x] = 8
    agents.append(unknown_agent)

    (x, y) = (1,1)
    main_agent = agent.Agent(x, y,'l1',1)
    agents.append(main_agent)
    the_map[y][x] = 9


def initialize_items_agents( n, m):
    # generating choices for random selection
    global the_map

    sf = []
    for i in range(0, n):
        for j in range(0, m):
            sf.append((i, j))

    # creating items
    for i in range(1, 11):
        (x, y) = random.choice(sf)
        item_level = round(random.uniform(level_min, level_max), 2)
        tmp_item = item.item(x, y, item_level,i)
        items.append(tmp_item)
        sf.remove((x, y))
        the_map[x][y] = 1

    # creating agent
    (x, y) = random.choice(sf)
    unknown_agent = agent.Agent(x, y,'l1',0)
    the_map[x][y] = 8

    agents.append(unknown_agent,1)
    sf.remove((x, y))
    the_map[x][y] = 9

    (x, y) = random.choice(sf)
    main_agent = agent.Agent(x, y,'l1',1)
    agents.append(main_agent)
    sf.remove((x, y))


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
sim_history = list()
sim_history.append(the_map)

# ==============parameter estimation initialisation=====================================================

param_estim = parameter_estimation.ParameterEstimation()
param_estim.estimation_initialisation()

# ================create unknown agent  ================================================================

# true parameters
true_radius = 0.48
true_angle = 0.42
true_level = 1

true_parameters = [true_level, true_radius, true_angle]

unknown_agent = agents[0]
unknown_agent.set_parameters(true_level, true_radius, true_angle)

# ======================================================================================================
real_sim.draw_map()

t = 0
while t < 100:

    print 'main run count: ', t

    local_map = []
    row = [0] * 10

    for i in range(10):
        local_map.append(list(row))

    local_items = []
    for i in range(len(items)):
        (item_x,item_y) = items[i].get_position()
        local_item = item.item(item_x, item_y, 1, i)
        local_item.loaded = items[i].loaded
        local_items.append(local_item)
        if not local_item.loaded:
            local_map[item_y][item_x] = 1

    local_agents = list()

    (a_agent_x,a_agent_y) = agents[0].get_position()
    local_map[a_agent_y][a_agent_x] = 8
    local_agent = agent.Agent(a_agent_x, a_agent_y, 'l1', 0)
    local_agents.append(local_agent)

    (m_agent_x, m_agent_y) = agents[1].get_position()
    local_map[m_agent_y][m_agent_x] = 9
    local_agent = agent.Agent(m_agent_x, m_agent_y, 'l1', 1)
    local_agents.append(local_agent)

    prev_sim = simulator.simulator(local_map, local_items, local_agents, 10, 10)

    prev_position = unknown_agent.get_position()

    # moving the unknown agent with true parameters
    unknown_agent = real_sim.run_and_update(unknown_agent)

    # map changes after move of unknown agent
    sim_history.append(real_sim)
    t = t + 1
    #real_sim.draw_map()
    #print("----------------------------------------")
    unknown_action_prob = unknown_agent.get_action_probability(unknown_agent.next_action)
    #prev_sim.draw_map()

    new_estimated_parameters = param_estim.process_parameter_estimations(t, prev_sim, prev_position, unknown_agent.next_action)

    real_sim.mcts_move(new_estimated_parameters)
    real_sim.draw_map()

    if real_sim.items_left() == 0:
        break
    print "left items", real_sim.items_left()

#real_sim.draw_map()
print  t
print "True parameters: ",true_level,true_radius,true_angle
print "last new_estimated_parameters", new_estimated_parameters


