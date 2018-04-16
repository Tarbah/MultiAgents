import simulator
import UCT
import sys
import gc



# ==============simulator initialisation=====================================================
#
# if (len(sys.argv) < 3):
#     print("Use: run_world.py [scenario file] [re-use tree]")
#     sys.exit()
#
# if (int(sys.argv[2]) == 0):
#     reuseTree = False
# else:
types = ['l1', 'l2', 'f1', 'f2']
reuseTree = False
    
main_sim = simulator.simulator()
# main_sim.loader(sys.argv[1])
main_sim.loader('/home/elnaz/task_assignment_project/simulator/UCT/Test Files/sim_2_agents.csv')
# main_sim.loader('C:\\simulator\UCT\\Test Files\\A Tests\\test5.csv')

print('Simulation Successful')

# ================create unknown agent  ================================================================


true_radius = 0.78
true_angle = 0.72
true_level = 0.5

true_parameters = [true_level, true_radius, true_angle]

main_agent = main_sim.main_agent

# ======================================================================================================

# real_sim.draw_map_with_level()
main_sim.draw_map()

search_tree = None

time_step = 0
while time_step < 100:

    print 'main run count: ', time_step

    previous_sim = main_sim.copy()

    for i in range(len(main_sim.agents)):
        main_sim.agents[i].state_history.append(main_sim)
        main_sim.agents[i] = main_sim.move_a_agent(main_sim.agents[i])

    if main_sim.main_agent is not None:
        main_sim.main_agent.state_history.append(main_sim)
        tmp_sim = main_sim.copy()

        if not reuseTree:
            main_agent_next_action, search_tree = UCT.m_agent_planning(0, None, tmp_sim, true_parameters)
        else:
            main_agent_next_action, search_tree = UCT.m_agent_planning(time_step, search_tree, tmp_sim, true_parameters)

        # print 'main_agent_direction: ', main_agent.get_agent_direction()
        print 'main_agent_next_action: ', main_agent_next_action

        r = UCT.do_move(main_sim, main_agent_next_action)

    ## DEBUG
    for agent_i in range(len(main_sim.agents)):
        print "agent " + str(agent_i) + " heading:" + main_sim.agents[agent_i].get_agent_direction()

    main_sim.update_all_A_agents()

    for agent in main_sim.agents:
        agent.estimate_parameter(previous_sim, time_step)

    ## DEBUG
    for agent_i in range(len(main_sim.agents)):
        print "agent " + str(agent_i) + " next action:" + main_sim.agents[agent_i].next_action
    
    main_sim.do_collaboration()

    time_step = time_step + 1
    print('***********************************************************************************************************')

    # import ipdb; ipdb.set_trace()
    
    main_sim.draw_map()

    # real_sim.draw_map_with_level()

    if main_sim.items_left() == 0:
        break
    print "left items", main_sim.items_left()

print time_step
print "True parameters: ",true_level,true_radius,true_angle
# print "last new_estimated_parameters", new_estimated_parameters










