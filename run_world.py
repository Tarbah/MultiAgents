import simulator
import UCT
import time
from collections import defaultdict
from copy import deepcopy
import os
import datetime
import pickle

import sys

iMaxStackSize = 5000
sys.setrecursionlimit(iMaxStackSize)
types = ['l1', 'l2', 'f1', 'f2']

iteration_max = None
type_selection_mode = None
parameter_estimation_mode = None
generated_data_number = None
reuseTree = None
max_depth = None
sim_path = None
do_estimation = True
# Multiple State Per Action (MSPA)/ One State Per Action (OSPA)
mcts_mode = None

now = datetime.datetime.now()
sub_dir = now.strftime("%Y-%m-%d %H:%M")

current_folder = "outputs/"+ sub_dir + '/'
if not os.path.exists(current_folder):
    os.mkdir(current_folder, 0755)

dir = ""
if len(sys.argv) > 1 :
    dir = str(sys.argv[1])

path = dir + 'config.csv'

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
        sim_path = dir + str(v[0][0]).strip()

    if 'mcts_mode' in k:
        mcts_mode = str(v[0][0]).strip()

uct = UCT.UCT(reuseTree, iteration_max, max_depth, do_estimation, mcts_mode)
main_sim = simulator.Simulator()
print 'simulator path:' + sim_path
main_sim.loader(sim_path)
logfile = main_sim.create_log_file(current_folder + "log.txt")

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
main_sim.log_map(logfile)

search_tree = None

time_step = 0
begin_time = time.time()

while main_sim.items_left() > 0:

    print 'main run count: ', time_step

    for i in range(len(main_sim.agents)):
        main_sim.agents[i].state_history.append(main_sim)
        main_sim.agents[i] = main_sim.move_a_agent(main_sim.agents[i])

    if main_sim.main_agent is not None:
        main_sim.main_agent.state_history.append(main_sim)
        # tmp_sim = main_sim.copy()
        tmp_sim = deepcopy(main_sim)

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
        for i in range(len(main_sim.agents)):

            main_sim.agents[i].estimate_parameter(main_sim, time_step)


    # ## DEBUG
    # for agent_i in range(len(main_sim.agents)):
    #     print "agent " + str(agent_i) + " next action:" + main_sim.agents[agent_i].next_action
    time_step += 1

    print('***********************************************************************************************************')

    # import ipdb; ipdb.set_trace()
    
    main_sim.draw_map()
    main_sim.log_map(logfile)

    # real_sim.draw_map_with_level()

    if main_sim.items_left() == 0:
        break
    print "left items", main_sim.items_left()

end_time = time.time()

for i in range(len(main_sim.agents)):
    print main_sim.agents[i].estimated_parameter.l1_estimation.data_set

def print_result(main_sim,  time_steps,  begin_time, end_time):

    file = open(current_folder + "/results.txt", 'w')
    pickleFile = open(current_folder + "/pickleResults.txt", 'wb')

    file.write('sim width:' + str(main_sim.dim_w) + '\n')
    file.write('sim height:' + str(main_sim.dim_h) + '\n')
    file.write('agents counts:' + str(len(main_sim.agents)) + '\n')
    file.write('items counts:' + str(len(main_sim.items)) + '\n')
    file.write('time steps:' + str(time_steps) + '\n')
    file.write('begin time:' + str(begin_time) + '\n')
    file.write('end time:' + str(end_time) + '\n')
    file.write('estimation mode:' + str(parameter_estimation_mode) + '\n')
    file.write('type selection mode:' + str(type_selection_mode) + '\n')
    file.write('iteration max:' + str(iteration_max) + '\n')
    file.write('max depth:' + str(max_depth) + '\n')
    file.write('generated data number:' + str(generated_data_number) + '\n')
    file.write('reuseTree:' + str(reuseTree) + '\n')

    agentDictionary = {}

    for i in range(len(main_sim.agents)):
        agentData = {}
        file.write('#level,radius,angle\n')
        file.write('true type:' + str(main_sim.agents[i].agent_type) + '\n')
        file.write('true parameters:' + str(main_sim.agents[i].level) + ',' + str(main_sim.agents[i].radius)+ ',' +
                   str(main_sim.agents[i].angle) + '\n')
        agentData['trueType'] = main_sim.agents[i].agent_type
        trueParameters = [main_sim.agents[i].level,main_sim.agents[i].radius,main_sim.agents[i].angle]
        agentData['trueParameters'] = trueParameters

        file.write('#probability of type ,level,radius,angle\n')
        estimated_value = main_sim.agents[i].estimated_parameter.l1_estimation.get_last_estimation()
        file.write('l1:' + str(main_sim.agents[i].estimated_parameter.l1_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ',' + str(estimated_value.angle)
                   + '\n')
        agentData['l1Probability'] = main_sim.agents[i].estimated_parameter.l1_estimation.get_last_type_probability()
        l1 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['l1'] = l1

        file.write( str(main_sim.agents[i].estimated_parameter.l1_estimation.type_probabilities) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.l1_estimation.get_estimation_history()) + '\n')
        l1History = main_sim.agents[i].estimated_parameter.l1_estimation.get_estimation_history()
        agentData['l1History'] = l1History

        estimated_value = main_sim.agents[i].estimated_parameter.l2_estimation.get_last_estimation()
        file.write('l2:' + str(main_sim.agents[i].estimated_parameter.l2_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ','
                   + str(estimated_value.angle) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.l2_estimation.type_probabilities) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.l2_estimation.get_estimation_history()) + '\n')
        agentData['l2Probability'] = main_sim.agents[i].estimated_parameter.l2_estimation.get_last_type_probability()
        l2 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['l2'] = l2
        l2History = main_sim.agents[i].estimated_parameter.l2_estimation.get_estimation_history()
        agentData['l2History'] = l2History

        estimated_value = main_sim.agents[i].estimated_parameter.f1_estimation.get_last_estimation()
        file.write('f1:' + str(main_sim.agents[i].estimated_parameter.f1_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ','
                   + str(estimated_value.angle) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.f1_estimation.type_probabilities) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.f1_estimation.get_estimation_history()) + '\n')
        agentData['f1Probability'] = main_sim.agents[i].estimated_parameter.f1_estimation.get_last_type_probability()
        f1 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['f1'] = f1
        f1History = main_sim.agents[i].estimated_parameter.f1_estimation.get_estimation_history()
        agentData['f1History'] = f1History

        estimated_value = main_sim.agents[i].estimated_parameter.f2_estimation.get_last_estimation()
        file.write('f2:' + str(main_sim.agents[i].estimated_parameter.f2_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ','
                   + str(estimated_value.angle) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.f2_estimation.type_probabilities) + '\n')
        file.write(str(main_sim.agents[i].estimated_parameter.f2_estimation.get_estimation_history()) + '\n')
        agentData['f2Probability'] = main_sim.agents[i].estimated_parameter.f2_estimation.get_last_type_probability()
        f2 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['f2'] = f2
        f2History = main_sim.agents[i].estimated_parameter.f2_estimation.get_estimation_history()
        agentData['f2History'] = f2History

        agentDictionary[i]=agentData

    pickle.dump(agentDictionary,pickleFile)    


print_result(main_sim, time_step, begin_time, end_time)


# selected_type = main_sim.agents[i].estimated_parameter.get_highest_probability()
# estimated_value = main_sim.agents[i].estimated_parameter.get_properties_for_selected_type(selected_type)
#
# file.write('highest property :' + str(selected_type) + ' level :' + str(estimated_value.level) + ', radius: ' +
#            str(estimated_value.radius) + ' angle: ' + str(estimated_value.angle) + '\n')
#

