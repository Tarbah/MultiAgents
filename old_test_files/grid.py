import sys, pygame, math, heapq
from pygame.locals import *


############   A star  ###########################

def onBoard(node):
    x, y = node
    return x >= 0 and x < num_cells and y >= 0 and y < num_cells

def blocked_diagnol(current,diag):
    x, y = current
    
    N = x-1, y
    E = x, y+1
    S = x+1, y
    W = x, y-1
    NE = x-1, y+1
    SE = x+1, y+1
    SW = x+1, y-1
    NW = x-1, y-1
    
    if diag == NE:
        return cells[N]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
    elif diag == SE:
        return cells[S]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
    elif diag == SW:
        return cells[S]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
    elif diag == NW:
        return cells[N]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
    else:
        return False # Technically, you've done goofed if you arrive here.

def diagonals(current):
    x, y = current
    
    NE = x-1, y+1
    SE = x+1, y+1
    SW = x+1, y-1
    NW = x-1, y-1
    
    directions = [NE, SE, SW, NW]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list and not blocked_diagnol(current,x)]


def processNode(coord, slow, step):
    global goal, open_list, closed_list, pq_dict, board, screen, needs_refresh
    if coord == goal:
        print "Cost %d\n" % cells[goal]['g_score']
        unwind_path(cells[goal]['parent'], slow)
        needs_refresh = True
        return
        
    # l will be a list of walkable adjacents that we've found a new shortest path to
    l = [] 
    
    # Check all of the diagnols for walkable cells, that we've found a new shortest path to
    for x in diagonals(coord):
        # If x hasn't been visited before
        if cells[x]['g_score'] == None:
            update_child(coord, x, cost_to_travel=14)
            l.append(x)
        # Else if we've found a faster route to x
        elif cells[x]['g_score'] > cells[coord]['g_score'] + 14:
            update_child(coord, x, cost_to_travel=14)
            l.append(x)
    
    for x in orthoganals(coord):
        # If x hasn't been visited before
        if cells[x]['g_score'] == None:
            update_child(coord, x, cost_to_travel=10)
            l.append(x)
        # Else if we've found a faster route to x
        elif cells[x]['g_score'] > cells[coord]['g_score'] + 10:
            update_child(coord, x, cost_to_travel=10)
            l.append(x)
    print "llllll"
    print l
    for x in l:
        if x != goal:
            left, top = x
            left = (left*cell_size)+2
            top = (top*cell_size)+2
            r = pygame.Rect(left, top, cell_size-2, cell_size-2)
            pygame.draw.rect(board, orange, r, 0)
            if slow:
                showBoard(screen, board)
        # If we found a shorter path to x
        # Then we remove the old f_score from the heap and dictionary
        if cells[x]['f_score'] in pq_dict:
            if len(pq_dict[cells[x]['f_score']]) > 1:
                pq_dict[cells[x]['f_score']].remove(x)
            else:
                pq_dict.pop(cells[x]['f_score'])
            open_list.remove(cells[x]['f_score'])
        # Update x with the new f and h score (technically don't need to do h if already calculated)
        calc_h(x)
        calc_f(x)
        # Add f to heap and dictionary
        open_list.append(cells[x]['f_score'])
        if cells[x]['f_score'] in pq_dict:
            pq_dict[cells[x]['f_score']].append(x)
        else:
            pq_dict[cells[x]['f_score']] = [x]
    
    heapq.heapify(open_list)
    
    if not step:
        if len(open_list) == 0:
            print 'NO POSSIBLE PATH!'
            return
        f = heapq.heappop(open_list)
        if len(pq_dict[f]) > 1:
            node = pq_dict[f].pop()
        else:
            node = pq_dict.pop(f)[0]
        
        heapq.heapify(open_list)
        closed_list[node]=True
    
        if node != goal:
            left, top = node
            left = (left*cell_size)+2
            top = (top*cell_size)+2
            r = pygame.Rect(left, top, cell_size-2, cell_size-2)
            pygame.draw.rect(board, blue, r, 0)
            if slow:
                showBoard(screen, board)
    
        processNode(node, slow, step)



# Display the shortest path found

def unwind_path(coord, slow):
    if cells[coord]['parent'] != None:
        left, top = coord
        left = (left*cell_size)+2
        top = (top*cell_size)+2
        r = pygame.Rect(left, top, cell_size-2, cell_size-2)
        pygame.draw.rect(board, white, r, 0)
        if slow:
            showBoard(screen, board)
        unwind_path(cells[coord]['parent'], slow)

def update_child(parent, child, cost_to_travel):
    cells[child]['g_score'] = cells[parent]['g_score'] + cost_to_travel
    cells[child]['parent'] = parent

def orthoganals(current):
    x, y = current
    
    N = x-1, y
    E = x, y+1
    S = x+1, y
    W = x, y-1
    
    directions = [N, E, S, W]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list]

def calc_f(node):
    cells[node]['f_score'] = cells[node]['h_score'] + cells[node]['g_score']


def calc_h(node):
    global heuristic
    x1, y1 = goal
    x0, y0 = node
    if heuristic == 'manhattan':
        cells[node]['h_score'] = (abs(x1-x0)+abs(y1-y0))*10#
    elif heuristic == 'crow':
        cells[node]['h_score'] = math.sqrt( (x1-x0)**2 + (y1-y0)**2 )*10
    else:
        cells[node]['h_score'] = 0

def findPath(slow, step):
   # print start
    if start != None and goal != None:
        cells[start]['g_score'] = 0

        calc_h(start)
        calc_f(start)
        
        if step:
            open_list.append(cells[start]['f_score'])
            pq_dict[cells[start]['f_score']] = [start]
            if len(open_list) == 0:
                print 'NO POSSIBLE PATH!'
                return
            f = heapq.heappop(open_list)
            if len(pq_dict[f]) > 1:
                node = pq_dict[f].pop()
            else:
                node = pq_dict.pop(f)[0]
                
            heapq.heapify(open_list)
          # print open_list
            closed_list[node]=True
            
            if node != goal and node != start:
                left, top = node
                left = (left*cell_size)+2
                top = (top*cell_size)+2
                r = pygame.Rect(left, top, cell_size-2, cell_size-2)
                pygame.draw.rect(board, blue, r, 0)
                if slow:
                    showBoard(screen, board)
                    
            processNode(node, slow, step)
        else:
            closed_list[start]=True
            processNode(start, slow, step)

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
cell_size = 50
num_cells = 20

cells = {}   # Dictionary of Cells where a tuple (immutable set) of (x,y) coordinates is used as keys


start_placed = goal_placed = needs_refresh = step_started = False
last_wall = None
start = None
goal = None

open_list = []  
pq_dict = {} 
closed_list = {}  
heuristic = 'crow'
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

    #left = ((100/cell_size)*cell_size)+2
    #top = ((100/cell_size)*cell_size)+2
  
 #   draw_cell(left,top, cell_size-2, bright_green)
    left = ((200/cell_size)*cell_size)+2
    top = ((200/cell_size)*cell_size)+2
    x_index = (left-2)/cell_size+1
    y_index = (top-2)/cell_size+1
    start = (x_index, y_index)
    print "start "
    print start 

    draw_cell(left,top, cell_size-2, bright_green)
    left = ((300/cell_size)*cell_size) + cell_size/2 + 1
    top = ((300/cell_size)*cell_size) + cell_size/2 + 1
    x_index = (left)/cell_size+1
    y_index = (top)/cell_size+1
    goal = (x_index, y_index)
    print "goal "
    print goal 
    draw_agent (left,top, cell_size-2)
    findPath(slow = True, step = True)
     #  start = (x_index, y_index)





