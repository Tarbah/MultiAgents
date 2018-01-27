#Types for agents are 'L1','L2','F1','F2'

import agent
import item
import position
import sys, pygame, math, heapq
import matplotlib.pyplot as plt
import numpy as np
import shutil,os

red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

start = None
goal = None

cells = {}      # Dictionary of Cells where a tuple (immutable set) of (x,y) coordinates is used as keys

open_list = []
pq_dict = {}
closed_list = {}
heuristic = 'crow'

items = []
agents = []

# Adjust the size of the board and the cells
cell_size = 40
num_cells = 10


def initialize_world():
    
        
    pygame.init()    
    size = width, height = (cell_size * num_cells) + 2, (cell_size * num_cells) + 2
    screen = pygame.display.set_mode(size)    
 
    background = pygame.Surface(screen .get_size())
    background = background.convert()
    background.fill (white)
    
    # Draw Grid lines
    for i in range(0,(cell_size*num_cells)+1)[::cell_size]:
        pygame.draw.line(background, black, (i, 0), (i, cell_size*num_cells), 2)
        pygame.draw.line(background, black, (0, i), (cell_size*num_cells, i), 2) 

  
    screen.blit(background, (0,0))
  
    return screen


def initialize_items_agents():
    item1= item.item(2,2,1)
    items.append(item1) 	
    item2 = item.item(3,5,2)
    items.append(item2) 
    unknown_agent = agent.agent(5,8,0.5, 0.2, 0.1,0.3,'L1')  
    agents.append(unknown_agent)
    
    main_agent = agent.agent(7,4,0.75, 0.2, 0.1,0.3,'L1') 	
    agents.append(main_agent)
    

def draw_world(screen):
    
    for i in range (0,len(items)):
#	if not tasks[i].done :
             x = (items[i].position.x - 1 ) * cell_size + 2
             y = (items[i].position.y - 1 ) * cell_size + 2
             r = pygame.Rect(x, y, cell_size-2, cell_size-2)
             pygame.draw.rect(screen, green, r, 0)
    
    x = (agents[0].position.x - 1 ) * cell_size + cell_size/2 + 1
    y = (agents[0].position.y - 1 ) * cell_size + cell_size/2 + 1   	    
    pygame.draw.circle(screen, blue, (x, y), cell_size/2, 0)
   
    x = (agents[1].position.x - 1 ) * cell_size + cell_size/2 + 1
    y = (agents[1].position.y - 1 ) * cell_size + cell_size/2 + 1   	    
    pygame.draw.circle(screen, red, (x, y), cell_size/2, 0)
	  
def draw_cell(screen,x, y, size, color):
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, color, r, 0)



########################################################
def main():
   global start, goal
   screen = initialize_world()
   initialize_items_agents()
   mem = position.position(0,0)
   
   unknown_agent = agents[0]
   main_agent = agents[1]

   start = unknown_agent.get_position()
   goal = main_agent.get_position()


   while True:
       draw_world(screen)
       pygame.display.flip()

       loc = main_agent.position # main agent

   #     print loc.x

       # dest =  position.position(0,0)
       # if mem.get_position() != (0,0) and loc != mem :
	  # dest = mem
       # else:
       #    main_agent.visible_agents_items(items)
       #    targ = main_agent.choose_target ()
       #    if targ.get_position() != (0,0):
	  #    dest = targ
       # mem = dest
      #
       # if mem.get_position() == (0,0) :
	  #  unknown_agent.set_actions_probability ( 0, 0.25,0.25,0.25,0.25)
        #else:
    

main()
