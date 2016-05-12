#!/usr/bin/python

# agent.py
# By Sean Batongbacal
# Agent for Text-Based Adventure Game
# COMP3411 Artificial Intelligence
# UNSW Session 1, 2016

import sys, os, socket

has_axe = False
has_key = False

# tile types?

# curr location relative to start
curr_x = 0
curr_y = 0

# poi locations relative to start (as tuples)
axe = False
key = False
stone = False
gold = False
# but are these unique (besides gold)?
# use lists of tuples for each if not?

env = {} # dict mapping relative co-ordinates to tile types
last_move = ''
direction = 'n'

class compass_class:
    def __init__(self):
        self.directions = ['n', 'e', 's', 'w']
        self.i = 0 # "north" is the starting direction
    def left(self):
        self.i = (self.i-1) % len(self.directions)
    def right(self):
        self.i = (self.i+1) % len(self.directions)
    def curr(self):
        return self.directions[self.i]
compass = compass_class()

def get_action(view):
    return 'f' # placeholder
    # view is a 5 x 5 array
    if not env: # just spawned
        # for x in range(5):
        #     for y in range(5):
        #         env[(x-2, y+2)] = view[x][y]
        env = view
    else:
        # add new stuff to env if moved; note, must account for direction as view rotates with agent
        if last_move == 'f':
            new = []
            if direction == 'n':
                # top row is new
                for x in range(5):
                    env[(curr_x)] = view[x,0]
            elif direction == 'e':
                # right col is new
                pass
            elif direction == 's':
                # bottom row is new
                pass
            elif direction == 'w':
                # left col is new
                pass

    # return action # action must be a single char string

    # when you see a poi, immediately search for a path to it and store the path. now update the path each time you move to counter the move. if you move in a certain way e.g. u turns you should search for a new path with your updated env

    # targets of opportunity
    # if see a poi which is trivial to obtain (and the gold is not trivial to obtain), immediately go for the poi in order to avoid backtracking for it later

    # first, try to map env, noting pois, taking targets of opportunity, etc.
    # when see gold, search for path w/ current items
    # if succeeds, go for gold and return to start
    # if fails, search for path w/ each other item
    # note required items and either search for them if not known or path to them if known

    # may need to move naively since might take too long to search every possible path
    # timer?

    # add new env info to memory (but how big can envs get? might only be able to store parts; answer: 80 x 80 is max size, may start in any location)
    # search env for points of interest in priority order (priority queue; lists for each type of poi, append to appropriate list, then search lists in order of type by priority)
    # ^only search newly added bits?
    # search for path to appropriate pois
    # if no path, try next poi
    # maybe store previously planned path and just continue if same poi is highest priority still

def print_view(view):
    print("+-----+")
    for y in range(2, -3, -1):
        line = '|'
        for x in range(-2, 3):
            if not (x == 0 and y == 0): # skip agent location
                line += view[(x, y)]
            else:
                line += '^'
        line += '|'
        print(line)
    print("+-----+")

if len(sys.argv) < 3:
    print("Usage: %s -p <port>" % sys.argv[0])
    sys.exit()

# open socket to Game Engine
sd = socket.create_connection(('localhost', sys.argv[2]))
in_stream = sd.makefile('r')
out_stream = sd.makefile('w')

while True:
    # scan 5-by-5 window around curr loc
    view = {}
    for y in range(2, -3, -1):
        for x in range(-2, 3):
            if not (x == 0 and y == 0): # skip agent location
                ch = in_stream.read(1) # read 1 char at a time
                if ch == -1:
                    exit()
                view[(x, y)] = ch
    print_view(view)
    action = get_action(view)
    print action
    out_stream.write(action)
    out_stream.flush()
