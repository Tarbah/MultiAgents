
import simulator
import UCT
import sys

# ========== main part  ====== ===========

# Map creation

# ==============simulator initialisation=====================================================


main_sim = simulator.simulator()


main_sim.loader(sys.argv[1])

# main_sim.loader('/home/elnaz/task_assignment_project/simulator/UCT/Test Files/M Tests/test2.csv')
# main_sim.loader('C:\simulator\UCT\Test Files\sim2 - level.csv')

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

time_step = 0
while time_step < 100:

    print 'main run count: ', time_step

    for i in range(len(main_sim.agents)):
        main_sim.agents[i] = main_sim.move_a_agent(main_sim.agents[i])

    if main_sim.main_agent is not None:
        tmp_sim = main_sim.copy()
        main_agent_next_action = UCT.m_agent_planning(tmp_sim, true_parameters)

        print 'main_agent_direction: ', main_agent.get_agent_direction()
        print 'main_agent_next_action: ', main_agent_next_action

        r = UCT.do_move(main_sim, main_agent_next_action)

    ## DEBUG
    for agent_i in range(len(main_sim.agents)):
        print "agent " + str(agent_i) + " heading:" + main_sim.agents[agent_i].get_agent_direction()
        
    main_sim.update_all_A_agents()

    ## DEBUG
    for agent_i in range(len(main_sim.agents)):
        print "agent " + str(agent_i) + " next action:" + main_sim.agents[agent_i].next_action
    
    main_sim.do_collaboration()

    time_step = time_step + 1
    print('*******************************************************************************************************************')


    # import ipdb; ipdb.set_trace()
    
    main_sim.draw_map()

    # real_sim.draw_map_with_level()

    if main_sim.items_left() == 0:
        break
    print "left items", main_sim.items_left()

print  time_step
print "True parameters: ",true_level,true_radius,true_angle
#print "last new_estimated_parameters", new_estimated_parameters


