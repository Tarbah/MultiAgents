import pickle
import matplotlib.pyplot as plt
import ast
import os
import numpy as np


results = list()
i = 0

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
            PF_add_threshold = systemDetails['PF_add_threshold']
            PF_del_threshold = systemDetails['PF_del_threshold']
            PF_weight = systemDetails['PF_weight']


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

            a_data_set = np.transpose(np.array(estimationHistError))

            levels = a_data_set[0, :]
            angle = a_data_set[1, :]
            radius = a_data_set[2, :]

            fig, ax = plt.subplots()
            ax.plot([i for i in range(len(levels))], levels, linestyle='-', color='cornflowerblue',linewidth=1)
            ax.plot([i for i in range(len(angle))], angle, linestyle='-', color='red',linewidth=1)
            ax.plot([i for i in range(len(radius))], radius, linestyle='-', color='green',linewidth=1)
            title = ''
            title = title + 'Estimation method is ' + estimationDictionary['estimationMode']
            if ( estimationDictionary['estimationMode'] == 'PF'):
                title += "Data number :"+ str(generatedDataNumber) + 'PF_add_threshold'+ str(PF_add_threshold)\
                         + 'PF_del_threshold' + str(PF_del_threshold) + 'PF_weight' + str(PF_weight)


            ax.set_title(title)

            ax.set_ylabel('Error')
            ax.set_xlabel('Step numbers')
            fig.savefig('./plots/plotResult' + str(i)+ '.jpg')
            i+=1
            #
        # plt.show()