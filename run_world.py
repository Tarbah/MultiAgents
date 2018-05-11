import simulator
import UCT
import time
from collections import defaultdict
from copy import deepcopy
import os
import datetime
import pickle

import sys
import numpy as np
import matplotlib.pyplot as plt
import parameter_estimation


iMaxStackSize = 2000
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
PF_add_threshold = None
PF_del_threshold = None
PF_weight = None

now = datetime.datetime.now()
sub_dir = now.strftime("%Y-%m-%d %H:%M")

current_folder = "outputs/"\
                 # + sub_dir + '/'
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

    if 'PF_add_threshold' in k:
        PF_add_threshold = float(v[0][0])

    if 'PF_del_threshold' in k:
        PF_del_threshold = float(v[0][0])

    if 'PF_weight' in k:
        PF_weight = float(v[0][0])

    if 'sim_path' in k:
        sim_path = dir + str(v[0][0]).strip()

    if 'mcts_mode' in k:
        mcts_mode = str(v[0][0]).strip()



uct = UCT.UCT(reuseTree, iteration_max, max_depth, do_estimation, mcts_mode)
main_sim = simulator.Simulator()

main_sim.loader(sim_path)
logfile = main_sim.create_log_file(current_folder + "log.txt")

for i in range(len(main_sim.agents)):
    print 'true values : level :', main_sim.agents[i].level, ' radius: ', main_sim.agents[i].radius, ' angle: ' \
        , main_sim.agents[i].angle

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

polynomial_degree = 4
agants_parameter_estimation = []
for i in range(len(main_sim.agents)):
    param_estim = parameter_estimation.ParameterEstimation()
    param_estim.estimation_initialisation()

    param_estim.estimation_configuration(type_selection_mode, parameter_estimation_mode, generated_data_number,
                                         polynomial_degree, PF_add_threshold, PF_del_threshold, PF_weight)


    agants_parameter_estimation.append(param_estim)


while main_sim.items_left() > 0:

    print 'main run count: ', time_step
    tmp_sim = deepcopy(main_sim)

    for i in range(len(main_sim.agents)):
        main_sim.agents[i].old_direction = main_sim.agents[i].direction
        # main_sim.agents[i].state_history.append(tmp_sim)
        main_sim.agents[i].previous_state = tmp_sim
        main_sim.agents[i] = main_sim.move_a_agent(main_sim.agents[i])

    if main_sim.main_agent is not None:
        main_sim.main_agent.previous_state = tmp_sim
        # tmp_sim = main_sim.copy()
        if not reuseTree:
            main_agent_next_action, search_tree = uct.m_agent_planning(0, None, tmp_sim,agants_parameter_estimation)
        else:
            main_agent_next_action, search_tree = uct.m_agent_planning(time_step, search_tree, tmp_sim,agants_parameter_estimation)

        # print 'main_agent_direction: ', main_agent.get_agent_direction()
        print 'main_agent_next_action: ', main_agent_next_action

        r = uct.do_move(main_sim, main_agent_next_action)

    ## DEBUG
    # for agent_i in range(len(main_sim.agents)):
    #     print "agent " + str(agent_i) + " heading:" + main_sim.agents[agent_i].get_agent_direction()

    main_sim.update_all_A_agents()
    main_sim.do_collaboration()

    if do_estimation:
        for i in range(len(agants_parameter_estimation)):
            p_agent = main_sim.agents[i]
            agants_parameter_estimation[i].process_parameter_estimations(time_step,
                                                                     p_agent.old_direction,
                                                                     p_agent.next_action,
                                                                     p_agent.index,
                                                                     p_agent.actions_history,
                                                                     p_agent.previous_state)

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
#
# for i in range(len(main_sim.agents)):
#     print agants_parameter_estimation['estimated_parameters'][i]

def plot_data_set(main_sim , estimated_parameter):

    d = estimated_parameter.l1_estimation.data_set
    true_level = main_sim.agents[0].level
    true_angle = main_sim.agents[0].angle
    true_radius = main_sim.agents[0].radius
    a_data_set = np.transpose(np.array(d))

    levels = a_data_set[0, :]
    angle = a_data_set[1, :]
    radius = a_data_set[2, :]
    fig = plt.figure(1)
    w = main_sim.agents[0].estimated_parameter.l1_estimation.weight
    N = len(w)

    colors = np.random.rand(N)
    print colors
    area = (10) ** 2  # 0 to 15 point radii

    plt.subplot(3, 1, 1)
    plt.scatter(w, levels, s=area, c='r', alpha=0.5)
    plt.plot([i for i in range(2)], [true_level for i in range(2)], label='PF', linestyle='-', color='cornflowerblue',
             linewidth=1)
    ax = plt.gca()
    ax.set_ylabel('Level dataset')
    ax.legend(loc="upper right", shadow=True, fontsize='x-large')
    plt.subplot(3, 1, 2)
    plt.scatter(w, angle, s=area, c='r', alpha=0.5)
    plt.plot([i for i in range(2)], [true_angle for i in range(2)], label='PF', linestyle='-', color='cornflowerblue',
             linewidth=1)
    ax = plt.gca()
    ax.set_ylabel('Angle dataset')

    plt.subplot(3, 1, 3)
    plt.scatter(w, radius, s=area, c='r', alpha=0.5)
    plt.plot([i for i in range(2)], [true_radius for i in range(2)], label='PF', linestyle='-', color='cornflowerblue',
             linewidth=1)
    ax = plt.gca()
    ax.set_ylabel('radius dataset')
    ax.set_xlabel('weight')

    fig.savefig("./plots/dataset.jpg")


def print_result(main_sim,  time_steps,  begin_time, end_time,mcts_mode,estimated_parameter):

    file = open(current_folder + "/results.txt", 'w')
    pickleFile = open(current_folder + "/pickleResults.txt", 'wb')

    dataList = []

    systemDetails = {}

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

    systemDetails['simWidth'] = main_sim.dim_w
    systemDetails['simHeight'] = main_sim.dim_h
    systemDetails['agentsCounts'] = len(main_sim.agents)
    systemDetails['itemsCounts'] = len(main_sim.items)
    systemDetails['timeSteps'] = time_steps
    systemDetails['beginTime'] = begin_time
    systemDetails['endTime'] = end_time
    systemDetails['estimationMode'] = parameter_estimation_mode
    systemDetails['typeSelectionMode'] = type_selection_mode
    systemDetails['iterationMax'] = iteration_max
    systemDetails['maxDepth'] = max_depth
    systemDetails['generatedDataNumber'] = generated_data_number
    systemDetails['reuseTree'] = reuseTree
    systemDetails['mcts_mode'] = mcts_mode
    systemDetails['PF_del_threshold'] = PF_del_threshold
    systemDetails['PF_add_threshold'] = PF_add_threshold
    systemDetails['PF_weight'] = PF_weight


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
        # L1 ******************************

        estimated_value = estimated_parameter[i].l1_estimation.get_last_estimation()

        # Result
        file.write('l1:' + str(estimated_parameter[i].l1_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ',' + str(estimated_value.angle)
                   + '\n')
        file.write(str(estimated_parameter[i].l1_estimation.type_probabilities) + '\n')
        file.write(str(estimated_parameter[i].l1_estimation.get_estimation_history()) + '\n')

        # pickleResults
        agentData['l1LastProbability'] = estimated_parameter[i].l1_estimation.get_last_type_probability()
        l1 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['l1'] = l1

        l1EstimationHistory = estimated_parameter[i].l1_estimation.get_estimation_history()
        agentData['l1EstimationHistory'] = l1EstimationHistory
        agentData['l1TypeProbHistory'] = estimated_parameter[i].l1_estimation.type_probabilities
        agentData['last_estimated_value'] = estimated_value

        # L2  ******************************

        estimated_value = estimated_parameter[i].l2_estimation.get_last_estimation()

        # Result
        file.write('l2:' + str(estimated_parameter[i].l2_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ','
                       + str(estimated_value.angle) + '\n')
        file.write(str(estimated_parameter[i].l2_estimation.type_probabilities) + '\n')
        file.write(str(estimated_parameter[i].l2_estimation.get_estimation_history()) + '\n')

        # pickleResults
        agentData['l2LastProbability'] = estimated_parameter[i].l2_estimation.get_last_type_probability()
        l2 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['l2'] = l2
        l2EstimationHistory = estimated_parameter[i].l2_estimation.get_estimation_history()
        agentData['l2EstimationHistory'] = l2EstimationHistory
        agentData['l2TypeProbHistory'] = estimated_parameter[i].l2_estimation.type_probabilities
        agentData['last_estimated_value'] = estimated_value

        # F1  ******************************

        estimated_value = estimated_parameter[i].f1_estimation.get_last_estimation()

        # Result
        file.write('f1:' + str(estimated_parameter[i].f1_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ','
                       + str(estimated_value.angle) + '\n')
        file.write(str(estimated_parameter[i].f1_estimation.type_probabilities) + '\n')
        file.write(str(estimated_parameter[i].f1_estimation.get_estimation_history()) + '\n')

        # pickleResults

        agentData['f1LastProbability'] = estimated_parameter[i].f1_estimation.get_last_type_probability()
        f1 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['f1'] = f1
        f1EstimationHistory = estimated_parameter[i].f1_estimation.get_estimation_history()
        agentData['f1EstimationHistory'] = f1EstimationHistory
        agentData['f1TypeProbHistory'] = estimated_parameter[i].f1_estimation.type_probabilities
        agentData['last_estimated_value'] = estimated_value

        # F2  ******************************

        estimated_value = estimated_parameter[i].f2_estimation.get_last_estimation()

        # Result
        file.write('f2:' + str(estimated_parameter[i].f2_estimation.get_last_type_probability()))
        file.write(',' + str(estimated_value.level) + ',' + str(estimated_value.radius) + ','
                       + str(estimated_value.angle) + '\n')
        file.write(str(estimated_parameter[i].f2_estimation.type_probabilities) + '\n')
        file.write(str(estimated_parameter[i].f2_estimation.get_estimation_history()) + '\n')

        # pickleResults

        agentData['f2LastProbability'] = estimated_parameter[i].f2_estimation.get_last_type_probability()
        f2 = [estimated_value.level,estimated_value.radius,estimated_value.angle]
        agentData['f2'] = f2
        f2EstimationHistory = estimated_parameter[i].f2_estimation.get_estimation_history()
        agentData['f2EstimationHistory'] = f2EstimationHistory
        agentData['f2TypeProbHistory'] = estimated_parameter[i].f2_estimation.type_probabilities
        agentData['last_estimated_value'] = estimated_value

        agentDictionary[i]=agentData

    dataList.append(systemDetails)
    dataList.append(agentDictionary)
    print "writing to pickle file."
    pickle.dump(dataList,pickleFile)
    print "writing over "

#plot_data_set(main_sim)
print_result(main_sim, time_step, begin_time, end_time,mcts_mode,agants_parameter_estimation)


# selected_type = estimated_parameter[i].get_highest_probability()
# estimated_value = estimated_parameter[i].get_properties_for_selected_type(selected_type)
#
# file.write('highest property :' + str(selected_type) + ' level :' + str(estimated_value.level) + ', radius: ' +
#            str(estimated_value.radius) + ' angle: ' + str(estimated_value.angle) + '\n')
#

