import pickle
import matplotlib.pyplot as plt
import ast

def Average(lst):
    return sum(lst) / len(lst)

currentFile = "/home/gauri/Desktop/MultiAgents-Pickle-data/outputs/2018-05-01 23:32/pickleResults.txt"
pickleFile = open(currentFile,'r')
dataList = pickle.load(pickleFile)
print dataList
data = dataList[1]
systemDetails = dataList[0]
agentDictionary = data[0]

correctStep = []
historyParameters = [[]]
maxProbability = max(agentDictionary['l1Probability'],agentDictionary['l2Probability'],agentDictionary['f1Probability'],agentDictionary['f2Probability'])

if maxProbability == agentDictionary['l1Probability']:
	correctStep = agentDictionary['l1']
	historyParameters = ast.literal_eval(agentDictionary['l1History'])
elif maxProbability == agentDictionary['l2Probability']:
	correctStep = agentDictionary['l2']
	historyParameters = ast.literal_eval(agentDictionary['l2History'])
elif maxProbability == agentDictionary['f1Probability']:
	correctStep = agentDictionary['f1']
	historyParameters = ast.literal_eval(agentDictionary['f1History'])
else :
	correctStep = agentDictionary['f2']
	historyParameters = ast.literal_eval(agentDictionary['f2History'])

error = [[]] 
meanError = []
i = 0
xaxis = []
trueParameters = agentDictionary['trueParameters'] 
for history in historyParameters:
	print "\n\n"
	print trueParameters
	print "\n\n"
	zip(trueParameters,history)
	difference =[x - y for x, y in zip(trueParameters, history)]
	error.append(difference)
	meanError.append(Average(difference))
	xaxis.append(i) 
	i = i+1

typeSelectionMode = systemDetails['typeSelectionMode']
plt.plot(xaxis,meanError)
plt.ylabel('mean Error values')
plt.xlabel('Type Selection Parameter '+typeSelectionMode)
plt.show()



