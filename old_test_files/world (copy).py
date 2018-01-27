#Types for agents are 'L1','L2','F1','F2'

import agent
import item
import position
import pygame
import matplotlib.pyplot as plt
import numpy as np
import shutil,os

red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

items = []
agents = []


def initialize_world():
    
    width = 500
    hight = 500
    
    pygame.init()    
    screen = pygame.display.set_mode((width, hight))
    
    
    item1= item.item(10,10,1)
    items.append(item1) 	
    item2 = item.item(40,50,2)
    items.append(item2) 	

    unknown_agent = agent.agent(50,50,0.5, 0.2, 0.1,0.3,'L1')  
    agents.append(agent1)
    return screen

def draw_world(screen):
    
    for i in range (0,len(items)):
#	if not tasks[i].done :
	    pygame.draw.rect(screen, red, (items[i].position.x, items[i].position.y, 20, 20))

    pygame.draw.circle(screen, blue, (agents[0].position.x, agents[0].position.y), 10, 0)
   
	  
def tasks_finished():
    
    for i in range (0,len(tasks)):
	if not tasks[i].done :
	   return False
	  
    return True	


def main():
    main_agent = agent.agent(100,100,0.75, 0.2, 0.1,0.3,'L1')  
    # initialization of screen and background
#    screen = initialize_world()
    mem = position.position(0,0)
    while True:
        loc = m_agent.position
	dest =  position.position(0,0)
        if mem != 0 and loc != mem :
	   dest = mem
        else:
           m_agent.visible_agents_items(agents,items)
           targ = m_agent.choose_target () 
           if targ != 0:
	      dest = targ
        mem = dest
        if dest == 0 :
	   p = 0.25
        else:
            

        print "ccc"
        #screen.fill(white)
       # draw_world(screen)        
	   
    #    robot1.move_it(screen,end_point)

        
      #  pygame.display.flip()
   
   
    

main()
