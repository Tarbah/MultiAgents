import simulator
import UCT
import sys
import gc

# ===========Configuration Values====================================================================================
# ======== Estimation Configuration=================

# type_selection_mode are: all types selection 'AS', Posterior Selection 'PS' , Bandit Selection 'BS'
type_selection_mode = 'AS'

# Parameter estimation mode is AGA if it is Approximate Gradient Ascent , ABU if it is Approximate Bayesian Updating
parameter_estimation_mode = 'AGA'


# ======== MCTS Configuration=================
# If it is False we recreate the search tree for MCTS in each time step and
# if it is True we will reuse the created tree from previous steps.
reuseTree = False

iteration_max = 10
max_depth = 10
# ==============simulator initialisation=====================================================
#
# if (len(sys.argv) < 3):
#     print("Use: run_world.py [scenario file] [re-use tree]")
#     sys.exit()
#
# if (int(sys.argv[2]) == 0):
#     reuseTree = False
# else:

uct = UCT.UCT(reuseTree, iteration_max, max_depth)
types = ['l1', 'l2', 'f1', 'f2']

    
main_sim = simulator.simulator()
# main_sim.loader(sys.argv[1])
main_sim.loader('/home/elnaz/task_assignment_project/simulator/UCT/Test Files/sim1.csv')
# main_sim.loader('C:\\simulator\UCT\\Test Files\\sim1.csv')

print('Simulation Successful')

# ================create unknown agent  ================================================================

for i in range(len(main_sim.agents)):
    main_sim.agents[i].initialise_parameter_estimation(type_selection_mode, parameter_estimation_mode)

main_sim.main_agent.initialise_parameter_estimation(type_selection_mode, parameter_estimation_mode)

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

    for agent in main_sim.agents:
        agent.estimate_parameter(previous_sim, time_step)

    # ## DEBUG
    # for agent_i in range(len(main_sim.agents)):
    #     print "agent " + str(agent_i) + " next action:" + main_sim.agents[agent_i].next_action
    
    main_sim.do_collaboration()

    time_step = time_step + 1
    print('***********************************************************************************************************')

    # import ipdb; ipdb.set_trace()
    
    main_sim.draw_map()

    # real_sim.draw_map_with_level()

    if main_sim.items_left() == 0:
        break
    print "left items", main_sim.items_left()


for i in range(len(main_sim.agents)):
    print main_sim.agents[i].estimated_parameter.l1_estimation.type_probabilities
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













