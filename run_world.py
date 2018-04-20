import simulator
import UCT
import sys
import gc
from collections import defaultdict


types = ['l1', 'l2', 'f1', 'f2']

iteration_max = None
type_selection_mode = None
parameter_estimation_mode = None
generated_data_number = None
reuseTree = None
max_depth = None
sim_path = None
do_estimation = True


def print_result(main_sim):
    for i in range(len(main_sim.agents)):
        print 'true values : level :', main_sim.agents[i].level, ' radius: ', main_sim.agents[i].radius, ' angle: '\
            , main_sim.agents[i].angle

        print 'l1', main_sim.agents[i].estimated_parameter.l1_estimation.get_last_type_probability()
        estimated_value = main_sim.agents[i].estimated_parameter.l1_estimation.get_last_estimation()
        print 'estimated values : level :', estimated_value.level, ' radius: ', estimated_value.radius, ' angle: '\
             , estimated_value.angle

        print 'l2', main_sim.agents[i].estimated_parameter.l2_estimation.get_last_type_probability()
        estimated_value = main_sim.agents[i].estimated_parameter.l2_estimation.get_last_estimation()
        print 'estimated values : level :', estimated_value.level, ' radius: ', estimated_value.radius, ' angle: ' \
            , estimated_value.angle

        print 'f1', main_sim.agents[i].estimated_parameter.f1_estimation.get_last_type_probability()
        estimated_value = main_sim.agents[i].estimated_parameter.f1_estimation.get_last_estimation()
        print 'estimated values : level :', estimated_value.level, ' radius: ', estimated_value.radius, ' angle: ' \
            , estimated_value.angle

        print 'f2', main_sim.agents[i].estimated_parameter.f2_estimation.get_last_type_probability()
        estimated_value = main_sim.agents[i].estimated_parameter.f2_estimation.get_last_estimation()
        print 'estimated values : level :', estimated_value.level, ' radius: ', estimated_value.radius, ' angle: '\
            , estimated_value.angle
        selected_type = main_sim.agents[i].estimated_parameter.get_highest_probability()
        estimated_value = main_sim.agents[i].estimated_parameter.get_properties_for_selected_type(selected_type)

        print 'estimated values for highes property : level :', estimated_value.level, ' radius: ', estimated_value.radius, ' angle: '\
             , estimated_value.angle

path = 'config.csv'
info = defaultdict(list)
with open(path) as info_read:
    for line in info_read:
        data = line.strip().split(',')
        key, val = data[0], data[1:]
        info[key].append(val)


for k, v in info.items():
    print k

    if 'type_selection_mode' in k:
        type_selection_mode = str(v[0][0]).strip()

    if 'parameter_estimation_mode' in k:
        parameter_estimation_mode = str(v[0][0]).strip()

    if 'generated_data_number' in k:
        generated_data_number = int(v[0][0])

    if 'reuseTree' in k:
        reuseTree = v[0][0]

    if 'iteration_max' in k:
        iteration_max = int(v[0][0])

    if 'max_depth' in k:
        max_depth = int(v[0][0])

    if 'sim_path' in k:
        sim_path = str(v[0][0]).strip()

uct = UCT.UCT(reuseTree, iteration_max, max_depth, do_estimation)
main_sim = simulator.simulator()
main_sim.loader(sim_path)
for i in range(len(main_sim.agents)):
    print 'true values : level :', main_sim.agents[i].level, ' radius: ', main_sim.agents[i].radius, ' angle: ' \
        , main_sim.agents[i].angle

for i in range(len(main_sim.agents)):
    main_sim.agents[i].initialise_parameter_estimation(type_selection_mode, parameter_estimation_mode, generated_data_number)

if main_sim.main_agent is not None:
    main_sim.main_agent.initialise_parameter_estimation(type_selection_mode, parameter_estimation_mode, generated_data_number)

for i in range(len(main_sim.agents)):
        print 'true values : level :', main_sim.agents[i].level, ' radius: ', main_sim.agents[i].radius, ' angle: ' \
            , main_sim.agents[i].angle
main_agent = main_sim.main_agent

# ======================================================================================================

# real_sim.draw_map_with_level()
main_sim.draw_map()

search_tree = None

time_step = 0
while time_step < 200:

    print 'main run count: ', time_step

    previous_sim = main_sim.copy()

    for i in range(len(main_sim.agents)):
        main_sim.agents[i].state_history.append(main_sim)
        main_sim.agents[i] = main_sim.move_a_agent(main_sim.agents[i])

    if main_sim.main_agent is not None:
        main_sim.main_agent.state_history.append(main_sim)
        tmp_sim = main_sim.copy()

        if not reuseTree:
            main_agent_next_action, search_tree = uct.m_agent_planning(0, None, tmp_sim)
        else:
            main_agent_next_action, search_tree = uct.m_agent_planning(time_step, search_tree, tmp_sim)

        # print 'main_agent_direction: ', main_agent.get_agent_direction()
        print 'main_agent_next_action: ', main_agent_next_action

        r = uct.do_move(main_sim, main_agent_next_action)

    ## DEBUG
    # for agent_i in range(len(main_sim.agents)):
    #     print "agent " + str(agent_i) + " heading:" + main_sim.agents[agent_i].get_agent_direction()

    main_sim.update_all_A_agents()
    main_sim.do_collaboration()

    if do_estimation:
        print_result(main_sim)
        estimate_sim = main_sim.copy()

        for i in range(len(estimate_sim.agents)):
            estimate_sim.agents[i].estimate_parameter(previous_sim, time_step)

    # ## DEBUG
    # for agent_i in range(len(main_sim.agents)):
    #     print "agent " + str(agent_i) + " next action:" + main_sim.agents[agent_i].next_action

    time_step = time_step + 1
    print('***********************************************************************************************************')

    # import ipdb; ipdb.set_trace()
    
    main_sim.draw_map()

    # real_sim.draw_map_with_level()

    if main_sim.items_left() == 0:
        break
    print "left items", main_sim.items_left()

