import agent
import item
import random
import simulator
import UCT


radius_max = 1
radius_min = 0.1
angle_max = 1
angle_min = 0.1
level_max = 1
level_min = 0


items = []
agents = []



def initialize_items_agents_notrandom(n, m):
    # generating choices for random selection

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

        # tmp_item = item.item(x, y, (10 - i) / 10.0, i)
        #tmp_item = item.item(x, y, ( i) / 10.0, i)
        tmp_item = item.item(x, y, 1, i)
        items.append(tmp_item)

    # creating agent
    (x, y) = (4,4)
    unknown_agent = agent.Agent(x, y, 0,'l1', 0)
    agents.append(unknown_agent)

    (x, y) = (1, 1)
    main_agent = agent.Agent(x, y,0,'l1', 1)
    main_agent.level = 1
    #agents.append(main_agent)


    return main_agent

def initialize_items_agents(n, m):
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
    unknown_agent = agent.Agent(x, y,0, 'l1', 0)
    the_map[x][y] = 8

    agents.append(unknown_agent,1)
    sf.remove((x, y))
    the_map[x][y] = 9

    (x, y) = random.choice(sf)
    main_agent = agent.Agent(x, y, 0, 'l1', -1)
    main_agent.level = 1
    main_agent.direction = 0

    sf.remove((x, y))

    return main_agent



def create_tmp_map(items, agents, main_agent):
    local_map = []
    row = [0] * 10

    for i in range(10):
        local_map.append(list(row))

    local_items = []
    for i in range(len(items)):
        (item_x, item_y) = items[i].get_position()
        local_item = item.item(item_x, item_y, 1, i)
        local_item.loaded = items[i].loaded
        local_items.append(local_item)
        if not local_item.loaded:
            local_map[item_y][item_x] = 1

    local_agents = list()

    (a_agent_x, a_agent_y) = agents[0].get_position()
    local_map[a_agent_y][a_agent_x] = 8
    local_agent = agent.Agent(a_agent_x, a_agent_y,agents[0].direction, 'l1', 0)
    local_agents.append(local_agent)

    (m_agent_x, m_agent_y) = main_agent.get_position()
    local_map[m_agent_y][m_agent_x] = 9
    local_main_agent = agent.Agent(m_agent_x, m_agent_y,main_agent.direction, 'l1', -1)
    local_main_agent.level = main_agent.level

    return local_agents,local_items,local_map,local_main_agent

# ========== main part  ====== ===========

# Map creation

# ==============simulator initialisation=====================================================


n = 10  # horizontal size ,column
m = 10  # vertical size ,row

# initialize_items_agents(n, m)
main_agent = initialize_items_agents_notrandom(n, m)

real_sim = simulator.simulator([], items, agents, main_agent,n,m)
real_sim.update_the_map()



# ================create unknown agent  ================================================================

# true parameters
true_radius = 0.78
true_angle = 0.72
true_level = 1

true_parameters = [true_level, true_radius, true_angle]

unknown_agent = agents[0]
unknown_agent.set_parameters(true_level, true_radius, true_angle)

# ======================================================================================================

real_sim.draw_map()
# real_sim.draw_map_with_level()
main_agent.direction = 0

time_step = 0
while time_step < 100:

    print 'main run count: ', time_step

    # Initializing the simulator
    local_agents, local_items, local_map, local_main_agent = create_tmp_map(items, agents, main_agent)
    prev_sim = simulator.simulator(local_map, local_items, local_agents, local_main_agent, 10, 10)

    unknown_agent = real_sim.run_and_update(unknown_agent)
    main_agent_next_action = UCT.move_agent(real_sim.agents, real_sim.items,  real_sim.main_agent, true_parameters)

    r = UCT.do_move(real_sim, main_agent_next_action)

    time_step = time_step + 1

    real_sim.draw_map()
    # real_sim.draw_map_with_level()

    if real_sim.items_left() == 0:
        break
    print "left items", real_sim.items_left()


print  time_step
print "True parameters: ",true_level,true_radius,true_angle
#print "last new_estimated_parameters", new_estimated_parameters


