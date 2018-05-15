from random import randint
import random
import csv

agentValues = [1,2,3,4]
gridSize = [10,15,20,25]
directions = ['N','S','E','W']
types = ['l1','l2','f1','f2']

dataFilesNumber = 2 
for i in range(0,dataFilesNumber):
	filename = 'sim %s.csv'%i
	with open(filename,'wb+') as file:
		writer = csv.writer(file,delimiter = ',')

		angleValue = round(random.uniform(0.1,1), 3) # rounds the value upto 3 places

		index = randint(0,3)

		agent =  agentValues[index]
		gridValue = gridSize[index]

		GRID = ['grid',gridValue,gridValue]
		writer.writerows([GRID])


		mainx = randint(0,gridValue)
		mainy = randint(0,gridValue)
		mainDirection = directions[randint(0,3)]
		mainType = types[randint(0,3)]
		mainLevel = round(random.uniform(0,1), 3)
		MAIN = ['main',mainx,mainy,mainDirection,mainType,mainLevel]
		writer.writerows([MAIN])

		for i in range(0,agent):
			while(randint(0,gridValue) != mainx):
				agentx = randint(0,gridValue)
			while(randint(0,gridValue) != mainy):
				agenty = randint(0,gridValue)
			agentDirection = directions[randint(0,3)]
			agentType = types[randint(0,3)]
			agentLevel = round(random.uniform(0,1), 3)
			agentRadius = round(random.uniform(0.1,1), 3)
			agentAngle = angleValue

			AGENT = ['agent',agentx,agenty,agentDirection,agentType,agentLevel,agentRadius,agentAngle]
			writer.writerows([AGENT])

		for i in range(0,gridValue):
			itemx = randint(0,gridValue)
			itemy = randint(0,gridValue)
			ITEM = ['item',itemx,itemy]
			writer.writerows([ITEM])



