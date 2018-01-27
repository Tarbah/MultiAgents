import sys, pygame, math, heapq
from pygame.locals import *


# Function to Draw the initial board.

def initBoard(board):
    background = pygame.Surface(board.get_size())
    background = background.convert()
    background.fill (gray)
    
    # Draw Grid lines
    for i in range(0,(cell_size*num_cells)+1)[::cell_size]:
        pygame.draw.line(background, black, (i, 0), (i, cell_size*num_cells), 2)
        pygame.draw.line(background, black, (0, i), (cell_size*num_cells, i), 2)
    return background

def draw_cell(x, y, size, color):
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(board, color, r, 0)


def draw_agent(x, y, size):  
    pygame.draw.circle(board, dark_blue, (x, y), size/2, 0)


def showBoard(screen, board):
    screen.blit(board, (0,0))
    pygame.display.flip()


###################################initialisation####################################################
# Colors
black = (0,0,0)             # Wall Cells
gray = (112, 128, 144)      # Default Cells
bright_green = (0, 204, 102) # Start Cell
red = (255, 44, 0)          # Goal Cell
orange = (255, 175, 0)      # Open Cells
blue = (0, 124, 204)        # Closed Cells
white = (250,250,250)       # Not used, yet
dark_blue = (0,0,255)

# Adjust the size of the board and the cells
cell_size = 40
num_cells = 10

cells = {}   # Dictionary of Cells where a tuple (immutable set) of (x,y) coordinates is used as keys



############################screen Set up ############################################################

def initialize_world(screen):    
    print num_cells
    for x in range(num_cells):
	for y in range(num_cells):
	    cells[(x,y)]= { 'state':None,'f_score':None,'h_score':None,'g_score':None,'parent':None}   

    board = initBoard(screen)
    return board


pygame.init()
size = width, height = (cell_size * num_cells) + 2, (cell_size * num_cells) + 2
screen = pygame.display.set_mode(size)
board = initialize_world(screen)
pygame.display.set_caption = ('World')

#print cells 

while True:
    showBoard(screen, board)

    left = ((200/cell_size)*cell_size)+2
    top = ((200/cell_size)*cell_size)+2
    x_index = (left-2)/cell_size+1
    y_index = (top-2)/cell_size+1
    start = (x_index, y_index)
   
    draw_cell(left,top, cell_size-2, bright_green)
    left = ((300/cell_size)*cell_size) + cell_size/2 + 1
    top = ((300/cell_size)*cell_size) + cell_size/2 + 1
    x_index = (left)/cell_size+1
    y_index = (top)/cell_size+1
    goal = (x_index, y_index)
    draw_agent (left,top, cell_size-2)
   





