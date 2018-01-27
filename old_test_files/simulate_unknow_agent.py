# Types for agents are 'L1','L2','F1','F2'

import simulator.agent
import simulator.item
import simulator.position
import simulator.a_star
import sys, pygame, math, heapq
import matplotlib.pyplot as plt
import numpy as np
import random , time


items = []
agents = []
the_map = []


def initialize_items_agents(n,m):
    global the_map

    sf = []
    for i in range(0, n):
        for j in range(0, m):
            sf.append((i, j))



    for  i in range (1,10):
        (x, y) = random.choice(sf)
        tmp_item = simulator.item.item(x, y, 1)
        items.append(tmp_item)
        sf.remove((x, y))
        the_map[x][y] = 1



    (x, y) = random.choice(sf)
    unknown_agent = simulator.agent.agent(x, y)
    agents.append(unknown_agent)
    the_map[x][y] = 4
    sf.remove((x, y))

    (x, y) = random.choice(sf)
    main_agent = simulator.agent.agent(x, y)
    agents.append(main_agent)
    the_map[x][y] = 2
    sf.remove((x, y))



################################################################################################################
def main():
    global the_map

    directions = 4  # number of possible directions to move on the map

    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    # map matrix
    n = 30  # horizontal size
    m = 30  # vertical size

    row = [0] * n



    for i in range(m):
        the_map.append(list(row))

    initialize_items_agents(n,m)

    unknown_agent = agents[0]
    main_agent = agents[1]

    (xA, yA) = unknown_agent.get_position()
    (xB, yB) = main_agent.get_position()

    print 'Start: ', xA, yA
    print 'Finish: ', xB, yB

    a = simulator.a_star.a_star(the_map, n, m, directions, dx, dy)
    route = a.pathFind( xA, yA, xB, yB)
    if len(route) > 0:
        x = xA
        y = yA
        the_map[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            the_map[y][x] = 3
        the_map[y][x] = 4

    # mark the route on the map
    # if len(route) > 0:
    #     x = xA
    #     y = yA
    #     the_map[y][x] = 2
    #     for i in range(len(route)):
    #         j = int(route[i])
    #         x += dx[j]
    #         y += dy[j]
    #         the_map[y][x] = 3
    #     the_map[y][x] = 4
    #
    # # display the map with the route
    # print 'Map:'
    for y in range(m):
        for x in range(n):
            xy = the_map[y][x]
            if xy == 0:
                print '.',  # space
            elif xy == 1:
                print 'O',  # obstacle
            elif xy == 2:
                print 'S',  # start
            elif xy == 3:
                print 'R',  # route
            elif xy == 4:
                print 'F',  # finish
        print

    #raw_input('Press Enter...')


        #loc = main_agent.position  # main agent

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
        # else:


main()
