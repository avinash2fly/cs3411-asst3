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
# 'T' tree
# '.' off map
# '-' door
# '~' water
# '*' wall
# 'a' axe
# 'k' key
# 'o' stepping stone
# 'g' gold

# commands
# L left
# R right
# F forward
# C chop
# U unlock

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

# env borders (mainly for print_env)
border_n = 0
border_e = 0
border_s = 0
border_w = 0

env = {} # dict mapping relative co-ordinates to tile types
last_move = ''

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

def get_action(env):
    action = 'f' # placeholder
    return action # action must be a single char string

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

# maybe stick env stuff in its own module?

def update_env(env, view): # turn this into a method
    if not env: # just spawned
        env = view
        border_n =  2 # probs should be attributes
        border_e =  2
        border_s = -2
        border_w = -2
    else:
        # add new stuff to env if moved; note, must account for direction as view rotates with agent
        if last_move == 'f':
            new = []
            direction = compass.curr()
            if direction == 'n':
                # top row is new
                for x in range(5):
                    env[(curr_x - 2 + x, curr_y + 2)] = view[x,0]
            elif direction == 'e':
                # right col is new
                pass
            elif direction == 's':
                # bottom row is new
                pass
            elif direction == 'w':
                # left col is new
                pass
    return env

def print_env(env):
    for y in range(border_n, border_s - 1, -1):
        line = ''
        for x in range(border_w, border_e + 1):
            if not (x == 0 and y == 0): # skip agent location
                if (x,y) in env:
                    line += env[(x, y)]
                else:
                    line += '?' # unmapped
                # line += env[(x,y)] if (x,y) in env else '?' # ternary alt
            else:
                line += 'A' # TODO: agent direction
        print(line)


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
    env = update_env(env, view)
    print_view(view)
    print_env(env)
    action = get_action(env)
    print action
    out_stream.write(action)
    out_stream.flush()
