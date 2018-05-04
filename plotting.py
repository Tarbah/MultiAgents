import pickle
import matplotlib.pyplot as plt
import ast
import os
import numpy as np


results = list()

for root, dirs, files in os.walk('outputs'):
    if 'pickleResults.txt' in files:

        with open(os.path.join(root,'pickleResults.txt'),"r") as pickleFile:

            estimationDictionary = {}
            dataList = pickle.load(pickleFile)

            data = dataList[1]
            systemDetails = dataList[0]

            # Simulator Information
            simWidth = systemDetails['simWidth']
            simHeight = systemDetails['simHeight']
            agentsCounts = systemDetails['agentsCounts']
            itemsCounts = systemDetails['itemsCounts']

            estimationDictionary['typeSelectionMode'] = systemDetails['typeSelectionMode']

            beginTime = systemDetails['beginTime']
            endTime = systemDetails['endTime']
            estimationDictionary['computationalTime'] = int(endTime) - int(beginTime)
            estimationDictionary['estimationMode'] = systemDetails['estimationMode']

            estimationDictionary['timeSteps'] = systemDetails['timeSteps']
            iterationMax = systemDetails['iterationMax']
            maxDepth = systemDetails['maxDepth']
            generatedDataNumber = systemDetails['generatedDataNumber']
            reuseTree = systemDetails['reuseTree']

            agentDictionary = data[0]
            correctStep = []
            historyParameters = [[]]

            maxProbability = max(agentDictionary['l1LastProbability'],agentDictionary['l2LastProbability'],
                                 agentDictionary['f1LastProbability'],agentDictionary['f2LastProbability'])

            estimationDictionary['estimatedType'] = maxProbability
            estimationDictionary['last_estimated_value'] = agentDictionary['last_estimated_value']

            if maxProbability == agentDictionary['l1LastProbability']:
                correctStep = agentDictionary['l1']
                historyParameters = ast.literal_eval(agentDictionary['l1EstimationHistory'])

            elif maxProbability == agentDictionary['l2LastProbability']:
                correctStep = agentDictionary['l2']
                historyParameters = ast.literal_eval(agentDictionary['l2EstimationHistory'])

            elif maxProbability == agentDictionary['f1LastProbability']:
                correctStep = agentDictionary['f1']
                historyParameters = ast.literal_eval(agentDictionary['f1EstimationHistory'])

            else:
                correctStep = agentDictionary['f2']
                historyParameters = ast.literal_eval(agentDictionary['f2EstimationHistory'])

            estimationError = list()
            estimationHistError = list()
            meanEstimationError = []
            i = 0
            xaxis = []
            trueParameters = agentDictionary['trueParameters']

            for history in historyParameters:
                zip(trueParameters,history)
                difference =[x - y for x, y in zip(trueParameters, history)]
                estimationHistError.append(difference)

                xaxis.append(i)
                i = i + 1
            estimationDictionary['estimationHistError'] = estimationHistError

            estimationDictionary['estimationError'] = estimationError

            estimated_value = [estimationDictionary['last_estimated_value'].level , estimationDictionary['last_estimated_value'].angle,estimationDictionary['last_estimated_value'].radius]

            diff = [x - y for x, y in zip(trueParameters , estimated_value)]

            estimationDictionary['estimationError'] = diff

            estimationDictionary['l1EstimationHistory'] = ast.literal_eval(agentDictionary['l1EstimationHistory'])
            estimationDictionary['l2EstimationHistory'] = ast.literal_eval(agentDictionary['l2EstimationHistory'])
            estimationDictionary['f1EstimationHistory'] = ast.literal_eval(agentDictionary['f1EstimationHistory'])
            estimationDictionary['f2EstimationHistory'] = ast.literal_eval(agentDictionary['f2EstimationHistory'])

            estimationDictionary['l1TypeProbHistory'] = agentDictionary['l1TypeProbHistory']
            estimationDictionary['l2TypeProbHistory'] = agentDictionary['l2TypeProbHistory']
            estimationDictionary['f1TypeProbHistory'] = agentDictionary['f1TypeProbHistory']
            estimationDictionary['f2TypeProbHistory'] = agentDictionary['f2TypeProbHistory']

            results.append(estimationDictionary)




AGA_errors = list()
ABU_errors = list()
PF_errors = list()

AGA_timeSteps = list()
ABU_timeSteps = list()
PF_timeSteps = list()

AGA_comp_time = list()
ABU_comp_time = list()
PF_comp_time = list()

for result in results:

    if result['estimationMode'] == 'AGA':
        AGA_errors.append(result['estimationError'])
        AGA_timeSteps.append(result['timeSteps'])
        AGA_comp_time.append(result['computationalTime'])

    if result['estimationMode'] == 'ABU':
        ABU_errors.append(result['estimationError'])
        ABU_timeSteps.append(result['timeSteps'])
        ABU_comp_time.append(result['computationalTime'])

    if result['estimationMode'] == 'PF':
        PF_errors.append(result['estimationError'])
        PF_timeSteps.append(result['timeSteps'])
        PF_comp_time.append(result['computationalTime'])

AGA_ave_level = 0
ABU_ave_level = 0
PF_ave_level = 0

if len(AGA_errors):
    AGA_data_set = np.transpose(np.array(AGA_errors))

    AGA_levels = AGA_data_set [0, :]
    AGA_ave_level = np.average(AGA_levels)

    AGA_angle = AGA_data_set[1, :]
    AGA_ave_angle = np.average(AGA_angle)

    AGA_radius = AGA_data_set[2, :]
    AGA_ave_radius = np.average(AGA_radius)

print AGA_ave_level


if len(PF_errors):
    PF_data_set = np.transpose(np.array(PF_errors))

    PF_levels = PF_data_set [0, :]
    PF_ave_level = np.average(PF_levels)

    PF_angle = PF_data_set[1, :]
    PF_ave_angle = np.average(PF_angle)

    PF_radius = PF_data_set[2, :]
    PF_ave_radius = np.average(PF_radius)

print 'PF_ave_level', PF_ave_level

if len(ABU_errors):
    ABU_data_set = np.transpose(np.array(ABU_errors))

    ABU_levels = ABU_data_set [0, :]
    ABU_ave_level = np.average(ABU_levels)

    ABU_angle = ABU_data_set[1, :]
    ABU_ave_angle = np.average(ABU_angle)

    ABU_radius = ABU_data_set[2, :]
    ABU_ave_radius = np.average(ABU_radius)

ABU_ave_level = 0
ABU_ave_angle = 0
ABU_ave_radius =0


N = 3
ind = np.arange(N)  # the x locations for the groups
width = 0.20       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

level_vals = [PF_ave_level, ABU_ave_level, AGA_ave_level]
rects1 = ax.bar(ind, level_vals, width, color='r')
angle_vals = [PF_ave_angle,ABU_ave_angle,AGA_ave_angle]
rects2 = ax.bar(ind+width, angle_vals, width, color='g')
radius_vals = [PF_ave_radius,ABU_ave_radius,AGA_ave_radius]
rects3 = ax.bar(ind+width*2, radius_vals, width, color='b')

ax.set_title('Errors in Last estimation for different methods')
ax.set_ylabel('Error')
ax.set_xlabel('Estimation Method')
ax.set_xticks(ind+width)
ax.set_xticklabels(('PF', 'ABU','AGA'))
ax.legend((rects1[0], rects2[0], rects3[0]), ('level', 'angle', 'radius'))

fig.savefig("./plots/errors_in_last_estimation.jpg")
# fig.savefig("./plots/TotalLandmarks.jpg")
# print estimationDictionary
