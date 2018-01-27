
import item
import pygame
import position
from math import sqrt
import matplotlib.pyplot as plt

#direction is a gradient  

class agent:

    	
    def __init__(self,  x,y, direction, level, radius, angle,atype):
    
        self.position = position.position(x,y)        
        self.size = 20              
        self.x_vel = 1
	self.y_vel = 0
        self.starting_point = self.position   
        self.stopped = True
        self.level = level
	self.radius = radius
	self.angle = angle
	self.direction = direction
        self.visible_agents = []
	self.visible_items = []
	self.atype = atype

    def do_task(self,task_lists):     

        self.stopped = False   
    	self.current_task_no  = self.find_nearest_task(task_lists)        
	self.current_task = task_lists [ self.current_task_no]
	end_point = self.current_task.position

	self.find_y_vel (end_point)
	
	return self.current_task_no


    def find_nearest_task(self,task_lists):
	min_dist = -1
	min_index = -1
	
        for i in range (0,len(task_lists)):
		if  not task_lists[i].done:
		        task_x = task_lists[i].position.x
			task_y = task_lists[i].position.y
			dist = sqrt( (self.position.x - task_x)**2 + (self.position.y - task_y)**2 )
		else :
         		dist = -1


		if  min_dist == -1 :
			min_index = i	
			min_dist = dist
		else: 
			if  dist < min_dist:
				min_dist = dist
				min_index = i	

	return min_index


    def find_y_vel (self, end_point):
	start_point = self.position
	a = end_point.x - start_point.x 
	b = end_point.y - start_point.y 
	
        self.y_vel = (b * self.x_vel ) / a
    
    def gradient (self,point):
        return ( self.position.y - point.position.y) / ( self.position.x - point.position.x)

    def distance (self, point):
        return sqrt((point.position.x - self.position.x)** 2 + (point.position.y - self.position.y)** 2)

    def visible_agents_items(self,items):
	
       # self.visible_agents = []
	self.visible_items = []

 	for i in range (0,len(items)):
	    if self.distance (items[i]) < self.radius:
	       if self.gradient (items[i]) < self.direction + self.angle/2 and self.gradient (items[i]) > self.direction - self.angle/2 :
		  visible_items.append(items[i])   
				
	#for i in range (0,len(agents)):
	#    if self.distance (agents[i]) < self.radius:
	#       if self.gradient (agents[i]) < self.direction + self.angle/2 and self.gradient (agents[i]) > self.direction - self.angle/2 :
	#	  visible_agents.append(agents[i])   
	
	
	return 	self.visible_items

    def  choose_target(self):
        
	if len(self.visible_items)==0 :
	   return 0;
	if self.atype== "L1" :    
	   max_distanse = 0
           for i in range (0,len(items)):
	      if self.distance (items[i]) > max_distanse :
		 max_distanse = self.distance (items[i])
           return items[i].position

    def move_it(self,screen,end_point):
       
        self.position.x +=  self.x_vel
	self.position.y +=  self.y_vel
	
	if self.position.x <  end_point.x: 
        	pygame.draw.rect(screen, (10, 20, 200), (self.position.x, self.position.y, self.size, self.size), 4)
	else:
		self.stopped = True 
		
        
    
    def isStopped(self):
        return  self.stopped

    def draw_path(self,screen):

        x1 = self.starting_point[0]
        y1 = self.starting_point[1]

        dir_num = -1

        while dir_num < len(self.direction) - 1:
            dir_num += 1
            dir = self.direction[dir_num]
            distance = int(dir[1:])

            if dir[0] == 'r':
                x2 = x1 + distance
                y2 = y1

            elif dir[0] == 'l':
                x2 = x1 - distance
                y2 = y1

            elif dir[0] == 'u':
                x2 = x1
                y2 = y1 - distance

            elif dir[0] == 'd':
                x2 = x1
                y2 = y1 + distance

            pygame.draw.line(screen, (0,0,0), [x1, y1], [x2, y2], 1)
            pygame.display.flip()
            x1 = x2
            y1 = y2

