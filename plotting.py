import pickle
import matplotlib.pyplot as plt
import ast
import os
import numpy as np


results = list()

for root, dirs, files in os.walk('outputs'):
    if 'pickleResults.txt' in files:
       # print root
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
            print historyParameters
            for history in historyParameters:
                zip(trueParameters,history)
                difference =[x - y for x, y in zip(trueParameters, history)]
                # print (list(difference))
                estimationHistError.append((list(difference)))
                xaxis.append(i)
                i = i + 1

            # print(estimationHistError)
            estimationDictionary['historyParameters'] = historyParameters
            estimationDictionary['estimationHistError'] = estimationHistError
            # print(estimationDictionary['estimationHistError'])

            estimationDictionary['estimationError'] = estimationError

            estimated_value = [estimationDictionary['last_estimated_value'].level , estimationDictionary['last_estimated_value'].angle,estimationDictionary['last_estimated_value'].radius]

            diff = [x - y for x, y in zip(trueParameters, estimated_value)]

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

AGA_estimationHistError = list()
ABU_estimationHistError = list()
PF_estimationHistError = list()

AGA_estimationHist = list()
ABU_estimationHist = list()
PF_estimationHist = list()

AGA_comp_time = list()
ABU_comp_time = list()
PF_comp_time = list()
max_len_hist = 0

for result in results:
    r = result['estimationHistError']
    p = result['historyParameters']

    arr = np.array(r)

    if max_len_hist < len(result['estimationHistError']):
        max_len_hist = len(result['estimationHistError'])

    if result['estimationMode'] == 'AGA':
        AGA_errors.append(result['estimationError'])
        AGA_estimationHistError.append(r)
        AGA_estimationHist.append(p)
        AGA_timeSteps.append(result['timeSteps'])
        AGA_comp_time.append(result['computationalTime'])

    if result['estimationMode'] == 'ABU':
        ABU_errors.append(result['estimationError'])
        ABU_estimationHistError.append(result['estimationHistError'])
        ABU_estimationHist.append(p)
        ABU_timeSteps.append(result['timeSteps'])
        ABU_comp_time.append(result['computationalTime'])

    if result['estimationMode'] == 'PF':
        PF_errors.append(result['estimationError'])
        PF_estimationHistError.append(result['estimationHistError'])
        PF_timeSteps.append(result['timeSteps'])
        PF_estimationHist.append(p)
        PF_comp_time.append(result['computationalTime'])

#print (AGA_estimationHistError)
# Normalizing history
difference =[x - y for x, y in zip(trueParameters, history)]

for a in AGA_estimationHist:

    last_value = a[len(a)-1]
    diff = max_len_hist - len(a)
    diff_arr = last_value * diff
    for i in range(diff):
        a.append(last_value)
#
aa = np.array(AGA_estimationHist)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
aga_levels = list(a_data_set[0, :])
aga_angle = list(a_data_set[1, :])
aga_radius = list(a_data_set[2, :])


for a in ABU_estimationHist:
    last_value = a[len(a) - 1]
    diff = max_len_hist - len(a)
    for i in range(diff):
        a.append(last_value)


aa = np.array(ABU_estimationHist)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
abu_levels = a_data_set[0, :]
abu_angle = a_data_set[1, :]
abu_radius = a_data_set[2, :]


for a in PF_estimationHist:
    last_value = a[len(a) - 1]
    diff = max_len_hist - len(a)
    for i in range(diff):
        a.append(last_value)


aa = np.array(PF_estimationHist)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
pf_levels = a_data_set[0, :]
pf_angle = a_data_set[1, :]
pf_radius = a_data_set[2, :]


fig = plt.figure(2)

plt.subplot(3,1,1)
plt.plot([i for i in range(len(pf_levels))], pf_levels, label='PF', linestyle='-', color='cornflowerblue',linewidth=1)
plt.plot([i for i in range(len(abu_levels))], abu_levels, label='ABU', linestyle='-', color='red',linewidth=1)
plt.plot([i for i in range(len(aga_levels))], aga_levels, label='AGA', linestyle='-', color='green',linewidth=1)
ax = plt.gca()
ax.set_ylabel('Level ')
ax.legend(loc="upper center", shadow=False, fontsize='x-small')
plt.subplot(3,1,2)
plt.plot([i for i in range(len(pf_angle))], pf_angle, label='PF', linestyle='-', color='cornflowerblue',linewidth=1)
plt.plot([i for i in range(len(abu_angle))], abu_angle, label='ABU', linestyle='-', color='red',linewidth=1)
plt.plot([i for i in range(len(aga_angle))], aga_angle, label='AGA', linestyle='-', color='green',linewidth=1)
ax = plt.gca()
ax.set_ylabel('Angle ')

plt.subplot(3,1,3)
plt.plot([i for i in range(len(pf_radius))], pf_radius, label='PF', linestyle='-', color='cornflowerblue',linewidth=1)
plt.plot([i for i in range(len(abu_radius))], abu_radius, label='ABU', linestyle='-', color='red',linewidth=1)
plt.plot([i for i in range(len(aga_radius))], aga_radius, label='AGA', linestyle='-', color='green',linewidth=1)
ax = plt.gca()
ax.set_ylabel('Level ')
ax.set_xlabel('Step numbers')


fig.savefig("./plots/history_of_estimation.jpg")


for a in ABU_estimationHistError:
    last_value = a[len(a) - 1]
    diff = max_len_hist - len(a)
    diff_arr = last_value * diff
    for i in range(diff):
        a.append(last_value)

aa = np.array(ABU_estimationHistError)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
abu_levels_err = a_data_set[0, :]
abu_angle_err = a_data_set[1, :]
abu_radius_err = a_data_set[2, :]


for a in AGA_estimationHistError:
    last_value = a[len(a) - 1]
    diff = max_len_hist - len(a)
    diff_arr = last_value * diff
    for i in range(diff):
        a.append(last_value)

aa = np.array(AGA_estimationHistError)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
aga_levels_err = a_data_set[0, :]
aga_angle_err = a_data_set[1, :]
aga_radius_err = a_data_set[2, :]

for a in PF_estimationHistError:
    last_value = a[len(a) - 1]
    diff = max_len_hist - len(a)
    for i in range(diff):
        a.append(last_value)


aa = np.array(PF_estimationHistError)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
pf_levels_err = a_data_set[0, :]
pf_angle_err = a_data_set[1, :]
pf_radius_err = a_data_set[2, :]


for a in AGA_estimationHistError:

    last_value = a[len(a)-1]
    diff = max_len_hist - len(a)
    diff_arr = last_value * diff
    for i in range(diff):
        a.append(last_value)

aa = np.array(AGA_estimationHistError)
ave = aa.mean(0)
a_data_set = np.transpose(ave)
pf_levels = list (a_data_set[0, :])
pf_angle = list( a_data_set[1, :])
pf_radius = list(a_data_set[2, :])


fig = plt.figure(1)

plt.subplot(3,1,1)
plt.plot([i for i in range(len(pf_levels_err))], pf_levels, label='PF', linestyle='-', color='cornflowerblue',linewidth=1)
plt.plot([i for i in range(len(abu_levels_err))], abu_levels, label='ABU', linestyle='-', color='red',linewidth=1)
plt.plot([i for i in range(len(aga_levels_err))], aga_levels, label='AGA', linestyle='-', color='green',linewidth=1)
ax = plt.gca()
ax.set_ylabel('Level Error')
ax.legend(loc="upper right", shadow=True, fontsize='x-large')
plt.subplot(3,1,2)
plt.plot([i for i in range(len(pf_angle_err))], pf_angle, label='PF', linestyle='-', color='cornflowerblue',linewidth=1)
plt.plot([i for i in range(len(abu_angle_err))], abu_angle, label='ABU', linestyle='-', color='red',linewidth=1)
plt.plot([i for i in range(len(aga_angle_err))], aga_angle, label='AGA', linestyle='-', color='green',linewidth=1)
ax = plt.gca()
ax.set_ylabel('Angle Error')

plt.subplot(3,1,3)
plt.plot([i for i in range(len(pf_radius))], pf_radius, label='PF', linestyle='-', color='cornflowerblue',linewidth=1)
plt.plot([i for i in range(len(abu_radius))], abu_radius, label='ABU', linestyle='-', color='red',linewidth=1)
plt.plot([i for i in range(len(aga_radius))], aga_radius, label='AGA', linestyle='-', color='green',linewidth=1)
ax = plt.gca()
ax.set_ylabel('Level Error')
ax.set_xlabel('Step numbers')


fig.savefig("./plots/errors_in_history_estimation.jpg")


AGA_ave_level = 0
ABU_ave_level = 0
PF_ave_level = 0

if len(AGA_errors):
    AGA_data_set = np.transpose(np.array(AGA_errors))

    AGA_levels = AGA_data_set[0, :]
    AGA_ave_level = np.average(AGA_levels)

    AGA_angle = AGA_data_set[1, :]
    AGA_ave_angle = np.average(AGA_angle)

    AGA_radius = AGA_data_set[2, :]
    AGA_ave_radius = np.average(AGA_radius)

if len(PF_errors):
    PF_data_set = np.transpose(np.array(PF_errors))

    PF_levels = PF_data_set[0, :]
    PF_ave_level = np.average(PF_levels)

    PF_angle = PF_data_set[1, :]
    PF_ave_angle = np.average(PF_angle)

    PF_radius = PF_data_set[2, :]
    PF_ave_radius = np.average(PF_radius)


if len(ABU_errors):
    ABU_data_set = np.transpose(np.array(ABU_errors))

    ABU_levels = ABU_data_set [0, :]
    ABU_ave_level = np.average(ABU_levels)

    ABU_angle = ABU_data_set[1, :]
    ABU_ave_angle = np.average(ABU_angle)

    ABU_radius = ABU_data_set[2, :]
    ABU_ave_radius = np.average(ABU_radius)




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
#plt.show()
fig.savefig("./plots/errors_in_last_estimation.jpg")



# fig.savefig("./plots/TotalLandmarks.jpg")
# print estimationDictionary
