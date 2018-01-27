
import agent
import item
import task
import pygame
import cv2
import matplotlib.pyplot as plt
import numpy as np
import shutil,os

red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
black = (0,0,0)

tasks = []


def initialize_world(screen,robot):
    
    for i in range (0,len(tasks)):
	if not tasks[i].done :
	    pygame.draw.rect(screen, red, (tasks[i].position.x, tasks[i].position.y, 20, 20))

    pygame.draw.rect(screen, (10, 20, 200), (robot.position.x, robot.position.y, robot.size, robot.size), 4)		
   
	  
def tasks_finished():
    
    for i in range (0,len(tasks)):
	if not tasks[i].done :
	   return False
	  
    return True	


def main():
    # initialization of screen and background
    pygame.init()

    screen = pygame.display.set_mode((1000, 500))
    p1= point.point(100,100)
    task1 = task.task(p1)
    p2 = point.point(400,100)
    task2 = task.task(p2) 	
    tasks.append (task1)
    tasks.append (task2)
  
    # initializing robots 
    start_point = point.point(2,3)   
    robot1 = robot.robot(start_point, 10, 0.1)  
    current_task_index = robot1.do_task(tasks)
    current_task = tasks[current_task_index]	
    end_point = current_task.position

    while True:
        screen.fill(white)
        initialize_world(screen,robot1)        
	   
        robot1.move_it(screen,end_point)

        if robot1.isStopped():
	   
            current_task.done = True
	    tasks[current_task_index] = current_task
        		
	    current_task_index = robot1.do_task(tasks)
            current_task = tasks[current_task_index]
          
            end_point = current_task.position
            
        if  tasks_finished():
	   
	    break
 	
        pygame.display.flip()
   
   
    

main()
