import random
import math

# Need a tree class ? Or maybe dont :/ 
#class Tree()

board=[[0,0,0.1],[0.3,0.5,0],[0,0,0.2]]
nodecount = 0 # keeps a count of nodes 
reward = 4 # count of rewards

class Node:
	def __init__(self,t,n,x,y):
		self.t = t 
		self.n = n # how many times it has been visited
		self.childArray = [] 
		self.parent = None # for root it is none, have to see the other values
		self.parentArray = [] # keep a track of the path 
		self.xpos = x
		self.ypos = y #Position of our agent
		self.direction = None # None for the root
		self.reward = 0 # rewards at this current state
		self.board = board

	
def addChild(parent,parentArray,ops,x,y):
	child = Node(0,0,x,y)
	child.parent = parent
	child.parentArray = parentArray
	child.parentArray.append(child.parent)
	child.direction = ops
	#child.reward = getreward(child.board)
	if(board[child.xpos][child.ypos]!=0):
		# take reward and change the board
		child.reward = parent.reward -1 
		tempboard = parent.board
		tempboard[child.xpos][child.ypos] = 0
		child.board = tempboard
	else:
		child.board = parent.board
		child.reward = parent.reward
	child.parent.childArray.append(child)
	print("\n")
	print(child.direction)
	print(child.board)
	#return child 


def getreward(board): # returns the number of rewards remaining
	rewards = 0
	for i in range(len(board[0])):
		for j in range(len(board)):
			if (board[i][j] != 0):
				rewards = rewards+1 

def displayChild(node):
	print 'Child t = ',node.t
	print "Node dir = ", node.direction
	print "Node n = ",node.n
	print "Node parent = ",node.parent
	print "Node x = ",node.xpos
	print "Node y = ",node.ypos
	print "Node children = ",len(node.childArray)
	print "Node reward = ",node.reward







def UCB(node):
	if(node.n==0):
		ucbValue = 99999
	else : 
		c = 2 # check this value, can be 1.4
		ucbValue = node.t + c*math.sqrt(math.log(node.parent.n)/node.n) # check if this works or we have to make seperate functions to return the values?
	#upgrade the visited value


	print "UCB value of node ",node.direction," value = ",ucbValue
	return ucbValue

def rollout(node):
	# check if node is a terminal state or not
	print "Rollout"
	disc = 0.95
	if(node.reward == 0):
		print "rollout if"
		val = node.t # this is the value that is to be passed on to parents
		for parents in reversed(node.parentArray): #update parents visited count and t value
			parents.n = parents.n + 1
			parents.t = parents.t + disc*val # included discount factor
			val = parents.t # gets discounted all along !

		node.n = node.n + 1 #node has been visited
	else :
		print "rollout else"
		# have to have a random walk? 
		# looking a 100 steps forward
		tempboard = board # make changes in a temporary board
		node.t = 0
		for i in range(5):
			x,y = random_walk(node.xpos,node.ypos,True)
			if(tempboard[x][y]!=0):
				# there is a reward at this position
				print " rollout reward"
				node.t = node.t + tempboard[x][y]
				tempboard[x][y]=0 # reward taken, assign it 0
				node.reward = node.reward-1 #decrement number of rewards
		val = node.t
		for parents in node.parentArray: # update parents visited value and t value
			parents.n = parents.n + 1
			parents.t = parents.t + disc*val
			val = parents.t
		node.n = node.n +1 #node has been visited






def MonteCarlo(node):
	# if it is Leaf node and visited, expand it
	# if it is not visited, go for simulation 
	current = node
	# if current is not a leaf node
	while(len(current.childArray)!=0): # contains children
		print('Going in while')
		MaxUcb = -1 
		for TempNode in current.childArray:
			if (UCB(TempNode) > MaxUcb):
				MaxUcb = UCB(TempNode)
				print('Max ucb = ',MaxUcb)
				current = TempNode


	print('Exit while')
	if(len(current.childArray) == 0):
#		if(current.n == 0): # condition for root checking?
#			rollout(current)
		if(current.n != 0):
			print('In if')
			# add new child for each available state
			availableOptions = PossibleOptions(3,current.xpos,current.ypos)
			chk = 0 
			for ops in availableOptions:
				x,y = random_walk(current.xpos,current.ypos,ops,False)
				print "Adding child at x = ",x,"y = ",y
				addChild(current,current.parentArray,ops,x,y) # check 
				#have not changed current till yet
			current = current.childArray[0] # assign it to the first child 
	displayChild(current)
	rollout(current) # check this part




def random_walk(x,y,step,ran=True):
	#Pass in arguments
	#x=0
	#y=0
	size = 3 # check to make it an argument !
	#for i in range(n):
	options = PossibleOptions(size,x,y)
	step = random.choice(options)
	if(ran!= True):
		step = step
	if step == 'N':
		y = y-1
	elif step == 'S':
		y = y+1
	elif step == 'E':
		x = x + 1
	else : 
		x = x-1

	return (x,y)

def PossibleOptions(size,x,y):
	options = ['N','S','E','W'] 
	if x == size -1 :
		del options[2]
	if x == 0:
		del options[3]
	if y == size-1:
		del options[1]
	if y == 0:
		del options[0]
	return options



#for i in range(25):
#	walk = random_walk(50,0,0)
#	print(walk,"Distance from home = ",abs(walk[0])+abs(walk[1]))

root = Node(0,0,0,0)
root.reward = 4
addChild(root,root.parentArray,'S',0,1)
addChild(root,root.parentArray,'E',1,0)
displayChild(root) # check insertion part
MonteCarlo(root)
#for child in root.childArray:
#	displayChild(child)
#	print "\n"
#	UCB(child)
#	print "\n\n"
#print "\n"
#print "iteration 2"
#MonteCarlo(root)
#print "\n"
#print "iteration 3"
#MonteCarlo(root)
#print "\n"
#print "iteration 4"
#MonteCarlo(root)
#print "\n"
#print "iteration 5"
#MonteCarlo(root)
#print "\n"
#print "iteration 6"
#MonteCarlo(root)
#print "\n"
#print "iteration 7"
#MonteCarlo(root)
