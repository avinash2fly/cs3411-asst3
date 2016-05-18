#!/usr/bin/python

# agent.py
# By Sean Batongbacal
# Agent for Text-Based Adventure Game
# COMP3411 Artificial Intelligence
# UNSW Session 1, 2016

import sys, os, socket, heapq, random

# tile types?
# 'T' tree
# '.' off map
# '-' door
# '~' water
# '*' wall
# 'a' axe
# 'k' key
# 'o' stepping stone
# 'O' placed stone
# 'g' gold

# commands
# L left
# R right
# F forward
# C chop
# U unlock

class compass_class:
    def __init__(self, start = 'n'):
        self.directions = ['n', 'e', 's', 'w']
        if start in self.directions:
            self.i = self.directions.index(start)
        else:
            self.i = 0 # "north" is default starting direction
    def left(self):
        self.i = (self.i-1) % len(self.directions)
    def right(self):
        self.i = (self.i+1) % len(self.directions)
    def curr(self):
        return self.directions[self.i]

def get_action(env):
    # action = raw_input('Action: ')
    # if action:
    #     env.moves = []
    #     return action # for debugging

    # new_poi essentially means needs to recalculate path
    # maybe should be renamed
    # maybe there should be an if not new_poi at beginning so only does
    # rest if necessary

    if env.has_gold:
        if not env.moves:
            env.moves = env.pathfind((0,0)) # since ?s are assumed traversable may provide a path which doesnt work
        else:
            for step in env.path: # maybe should make method to check if current path is traversable
                if not env.valid(step):
                    env.moves = env.pathfind((0,0))
                    break
        return env.moves.pop(0)

    # pois are sorted in order of interestingness: gold first, then tools (closest first), then removable obstacles
    #if env.gold:
        # first search with current tools
        #path = env.pathfind(env.gold)
        # if not path:
            # then figure out if stones required and how many
            # for i in range(0, 5):
            #     path = env.pathfind(env.gold, num_stones = i)
            #     if path:
            #         break
        #if path:
        #    env.moves = path
    
    pois = []
    if env.gold:
        pois.append(env.gold)
    if not env.has_key:
        pois += list(env.key)
    if not env.has_axe:
        pois += list(env.axe)
    # dont go for stones if would use two to get
    pois += sorted(pois + list(env.stone), key = lambda pos: abs(pos[0] - env.x) + abs(pos[1] - env.y))

    if env.has_key:
        pois += sorted(env.doors, key = lambda pos: abs(pos[0] - env.x) + abs(pos[1] - env.y))
    if env.has_axe:
        pois += sorted(env.trees, key = lambda pos: abs(pos[0] - env.x) + abs(pos[1] - env.y))

    # search if higher priority pois are found
    # print('pois: '+str(pois))
    while pois:
        # should remove new_poi variable
        # instead, manually check i.e. check all pois of higher priority, or check if a path now has obstacles
        # ^ still may take a long time? only check other pois if current path is bad or if gold so doesnt take ages searching on every stepk

        # if no path or is new highest priority thing
        # get list of pois in priority order i.e. gold first, then by dist?
        pos = pois.pop(0)
        print('env.path: '+str(env.path))
        if env.path and pos == env.path[-1]:
            # no path to any poi of higher priority than current target
            valid = True
            for step in env.path:
                print(step)
                if not env.valid(step):
                    # print(str(step) + ' is invalid since its a "' + env.rep[step]+'"')
                    valid = False
                    break
            if valid:
                break # current path is still valid, just continue with it
            else:
                env.moves = []
                env.path = []
        path = env.pathfind(pos) # put in pathfind?
        if path:
            env.moves = path
            break

    if not env.moves: # use default behaviour
        # hug borders
        # bad strat for large empty space in middle
        # go forward and turn left
        # if cant go forward, turn right until can go forward then go forward and turn left
        direction = env.compass.curr()
        x = None
        y = None
        if direction == 'n': # # maybe should have a function to return adjacent pos given a pos and direction?
            x = env.x
            y = env.y + 1
        elif direction == 'e':
            x = env.x + 1
            y = env.y
        elif direction == 's':
            x = env.x
            y = env.y - 1
        elif direction == 'w':
            x = env.x - 1
            y = env.y
        if env.valid((x,y)) and not env.hug_start:
            return 'f'
        else:
            env.hug_start = (env.x,env.y)

    if env.hug_start and not env.moves:
        direction = env.compass.curr()
        # if reached hug_start again, need to change strat
        x = None
        y = None
        if direction == 'n': # # maybe should have a function to return adjacent pos given a pos and direction?
            x = env.x
            y = env.y + 1
        elif direction == 'e':
            x = env.x + 1
            y = env.y
        elif direction == 's':
            x = env.x
            y = env.y - 1
        elif direction == 'w':
            x = env.x - 1
            y = env.y
        if env.valid((x,y)):
            env.moves = ['f','l']
        else:
            env.moves = ['r']

    env.new_poi = False

    # else continue with prior path
    print('env.moves:')
    print(env.moves)
    action = env.moves.pop(0)

    return action # action must be a single char string

    # when you see a poi, immediately search for a path to it and store the path. now update the path each time you move to counter the move. if you move in a certain way e.g. u turns you should search for a new path with your updated env

    # targets of opportunity
    # if see a poi which is trivial to obtain (and the gold is not trivial to obtain), immediately go for the poi in order to avoid backtracking for it later

    # first, try to map env, noting pois, taking targets of opportunity, etc.
    # when see gold, search for path w/ current items
    # if succeeds, go for gold and return to start
    # if fails, search for path w/ each other item
    # note required items and either search for them if not known or path to them if known

    # map env by searching e.g. grid type search(?)
    # grab pois if path (but not if path needs stone); if part of a path would be unknown, assume you can go through them.
    # only use stones if necessary to get gold or to be able to search more (i.e. nowhere else to go unless use stone)
    # remove any obstacles if possible
    # when gold found, search for path

    # search env for points of interest in priority order (priority queue; lists for each type of poi, append to appropriate list, then search lists in order of type by priority)
    # ^only search newly added bits?
    # search for path to appropriate pois
    # if no path, try next poi
    # maybe store previously planned path and just continue if same poi is highest priority still

# maybe stick env stuff in its own module?
# this is really a rep of whole game now... maybe rename rep to env and env_class to game?
class env_class:
    """Representation of known game environment"""
    def __init__(self):
        self.rep = {} # dict mapping relative co-ordinates to tile types

        # env borders (mainly for show())
        self.border_n = 0
        self.border_e = 0
        self.border_s = 0
        self.border_w = 0

        self.compass = compass_class()

        # poi locations relative to start (as tuples)
        self.axe = set()
        self.key = set()
        self.stone = set()
        self.gold = False
        self.trees = set()
        self.doors = set()

        # need to store what agent has
        self.has_axe = False
        self.has_key = False
        self.num_stones = 0
        self.has_gold = False

        self.path = []
        self.moves = []
        self.new_poi = False

        # agent loc
        self.x = 0
        self.y = 0

        # border hug active
        self.hug_start = None

        # maybe store path tiles so know if a ? is updated to an obstacle, which means a path recalculation is required
        # since otherwise may recalculate even when unnecessary

    def pathfind(self, pos):
        # search towards pos from current xy
        path = []
        for num_stones in range(0, self.num_stones + 1):
            path = self.astar((self.x, self.y), pos, num_stones)
            if path:
                break
        path = [(self.x, self.y)] + path
        self.path = path
        print(path)
        if len(path) == 1:
            self.path = []
            return [] # no path
        compass = compass_class(self.compass.curr())

        # convert path to sequence of moves
        moves = []
        for i, curr_tile in enumerate(path):
            if i + 1 >= len(path):
                break # end of path
            next_tile = path[i+1]
            # compare direction and relative positions
            x, y = curr_tile
            a, b = next_tile
            direction = compass.curr()
            if a == x and b == y + 1:
                # go north
                if direction == 'e':
                    compass.left()
                    moves.append('l')
                elif direction == 's':
                    compass.left()
                    compass.left()
                    moves.append('l')
                    moves.append('l')
                elif direction == 'w':
                    compass.right()
                    moves.append('r')
            elif a == x + 1 and b == y:
                # go east
                if direction == 's':
                    compass.left()
                    moves.append('l')
                elif direction == 'w':
                    compass.left()
                    compass.left()
                    moves.append('l')
                    moves.append('l')
                elif direction == 'n':
                    compass.right()
                    moves.append('r')
            elif a == x and b == y - 1:
                # go south
                if direction == 'w':
                    compass.left()
                    moves.append('l')
                elif direction == 'n':
                    compass.left()
                    compass.left()
                    moves.append('l')
                    moves.append('l')
                elif direction == 'e':
                    compass.right()
                    moves.append('r')
            elif a == x - 1 and b == y:
                # go west
                if direction == 'n':
                    compass.left()
                    moves.append('l')
                elif direction == 'e':
                    compass.left()
                    compass.left()
                    moves.append('l')
                    moves.append('l')
                elif direction == 's':
                    compass.right()
                    moves.append('r')
            else:
                # bad path
                print('Bad path')
                return []
            if self.rep[next_tile] == '-' and self.has_key:
                moves.append('u')
            elif self.rep[next_tile] == 'T' and self.has_axe:
                moves.append('c')
            moves.append('f')
        return moves

    def astar(self, start, end, num_stones):

        # astar search may be less useful since no weights, every node is equal distance to neighbours

        # prev is previous pos
        # cost cost to get to pos for each pos in a tuple dict
        c, d = end

        # seen set ensures positions are only checked once, with the shortest prev path
        seen = set([start])

        # minimize stone usage
        # use a for loop
        # i.e. search for a path using 0 stones, then using 1 stones, etc. up to actual amount of stones

        queue = [(0, start, [], num_stones)]
        # insert nodes into queue based on mdist + prev cost
        # first val is est cost to goal, third is list of prior nodes i.e. path ending in pos
        # first being 0 is dummy since will immediately be popped

        # steps:
        # take first node from queue
        # expand nodes from that node
        # add them to queue based on cost
        # repeat

        while len(queue) > 0:
            # pop queue
            _ , pos, path, num_stones = heapq.heappop(queue)
            # if pos in seen: # maybe? prolly not, since means unnecessary adding and checking of queue
            #      continue

            if pos == end:
                return path

            prev = len(path)
            a, b = pos
            
            # expand n
            x = a
            y = b + 1
            if (x,y) not in seen and self.valid((x,y), num_stones): # this bit prolly can be a function
                dist = abs(x - c) + abs(y - d) + prev # manhattan distance + cost to get to (x,y) from (a,b)
                # insert into priority queue
                heapq.heappush(queue, (dist, (x,y), path + [(x,y)], num_stones if self.rep[(x,y)] != '~' else num_stones - 1))
                seen.add((x,y)) # means that if tried later i.e. by something with higher prior cost, is skipped

            # expand e
            x = a + 1
            y = b
            if (x,y) not in seen and self.valid((x,y), num_stones):
                dist = abs(x - c) + abs(y - d) + prev
                # insert into priority queue
                heapq.heappush(queue, (dist, (x,y), path + [(x,y)], num_stones if self.rep[(x,y)] != '~' else num_stones - 1))
                seen.add((x,y))

            # expand s
            x = a
            y = b - 1
            if (x,y) not in seen and self.valid((x,y), num_stones):
                dist = abs(x - c) + abs(y - d) + prev
                # insert into priority queue
                heapq.heappush(queue, (dist, (x,y), path + [(x,y)], num_stones if self.rep[(x,y)] != '~' else num_stones - 1))
                seen.add((x,y))

            # expand w
            x = a - 1
            y = b
            if (x,y) not in seen and self.valid((x,y), num_stones):
                dist = abs(x - c) + abs(y - d) + prev
                # insert into priority queue
                heapq.heappush(queue, (dist, (x,y), path + [(x,y)], num_stones if self.rep[(x,y)] != '~' else num_stones - 1))
                seen.add((x,y))

        return [] # no path


    def valid(self, pos, num_stones = 0):
        if pos not in self.rep:
            return False # out of borders
        tile = self.rep[pos]
        if tile == '*':
            return False
        elif tile == '.':
            return False
        elif tile == 'T' and self.has_axe == False:
            return False
        elif tile == '-' and self.has_key == False:
            return False
        elif tile == '~' and num_stones == 0:
            return False
        else:
            return True

    def check(self, pos):
        if self.rep[pos] == 'a' and pos not in self.axe:
            self.axe.add(pos)
            self.new_poi = True
        elif self.rep[pos] == 'k' and pos not in self.key:
            self.key.add(pos)
            self.new_poi = True
        elif self.rep[pos] == 'o' and pos not in self.stone:
            self.stone.add(pos)
            self.new_poi = True
        elif self.rep[pos] == 'g'and self.gold != pos:
            self.gold = pos
            self.new_poi = True
        elif self.rep[pos] == 'T' and pos not in self.trees:
            self.trees.add(pos)
            self.new_poi = True
        elif self.rep[pos] == '-' and pos not in self.doors:
            self.doors.add(pos)
            self.new_poi = True

    def on_poi(self):
        pos = (self.x, self.y)
        if self.rep[pos] == 'a':
            self.axe.remove(pos)
            self.has_axe = True
        elif self.rep[pos] == 'k':
            self.key.remove(pos)
            self.has_key = True
        elif self.rep[pos] == 'o':
            self.stone.remove(pos)
            self.num_stones += 1
        elif self.rep[pos] == 'g':
            self.gold = False
            self.has_gold = True
        elif self.rep[pos] == '~':
            # place stone
            self.rep[pos] = 'O'
            self.num_stones -= 1
            # if self.num_stones < 0:
            #     ded

    def update(self, view, action):
        direction = self.compass.curr()
        if not self.rep: # just spawned
            self.rep = view
            self.rep[(0,0)] = ' '
            self.border_n =  2
            self.border_e =  2
            self.border_s = -2
            self.border_w = -2
            for y in range(2, -3, -1):
                for x in range(-2, 3):
                    self.check((x,y))
        elif action == 'f':
            # add new stuff to env if moved; note, must account for direction as view rotates with agent
            # need to deal with increasing borders
            if direction == 'n':
                self.y += 1
                # top row is new
                for x in range(-2, 3):
                    if (self.x + x, self.y + 2) in self.rep and self.rep[(self.x + x, self.y + 2)] == '?' and view[(x,2)] != ' ':
                        self.new_poi = True
                    self.rep[(self.x + x, self.y + 2)] = view[(x,2)]
                    self.check((self.x + x, self.y + 2))
                # update tile you just stepped off
                self.rep[(self.x, self.y - 1)] = view[(0,-1)]
                if self.y + 2 > self.border_n:
                    self.border_n = self.y + 2
                    for x in range(self.border_w, self.border_e + 1):
                        if (x, self.border_n) not in self.rep:
                            self.rep[(x, self.border_n)] = '?'
            elif direction == 'e':
                self.x += 1
                # right col is new
                for x in range(-2, 3):
                    if (self.x + 2, self.y - x) in self.rep and self.rep[(self.x + 2, self.y - x)] == '?' and view[(x,2)] != ' ':
                        self.new_poi = True
                    self.rep[(self.x + 2, self.y - x)] = view[(x,2)]
                    self.check((self.x + 2, self.y - x))
                # update tile you just stepped off
                self.rep[(self.x - 1, self.y)] = view[(0,-1)]
                if self.x + 2 > self.border_e:
                    self.border_e = self.x + 2
                    for y in range(self.border_s, self.border_n + 1):
                        if (self.border_e, y) not in self.rep:
                            self.rep[(self.border_e, y)] = '?'
            elif direction == 's':
                self.y -= 1
                # bottom row is new
                for x in range(-2, 3):
                    if (self.x - x, self.y - 2) in self.rep and self.rep[(self.x - x, self.y - 2)] == '?' and view[(x,2)] != ' ':
                        self.new_poi = True
                    self.rep[(self.x - x, self.y - 2)] = view[(x,2)]
                    self.check((self.x - x, self.y - 2))
                # update tile you just stepped off
                self.rep[(self.x, self.y + 1)] = view[(0,-1)]
                if self.y - 2 < self.border_s:
                    self.border_s = self.y - 2
                    for x in range(self.border_w, self.border_e + 1):
                        if (x, self.border_s) not in self.rep:
                            self.rep[(x, self.border_s)] = '?'
            elif direction == 'w':
                self.x -= 1
                # left col is new
                for x in range(-2, 3):
                    if (self.x - 2, self.y + x) in self.rep and self.rep[(self.x - 2, self.y + x)] == '?' and view[(x,2)] != ' ':
                        self.new_poi = True
                    self.rep[(self.x - 2, self.y + x)] = view[(x,2)]
                    self.check((self.x - 2, self.y + x))
                # update tile you just stepped off
                self.rep[(self.x + 1, self.y)] = view[(0,-1)]
                if self.x - 2 < self.border_w:
                    self.border_w = self.x - 2
                    for y in range(self.border_s, self.border_n + 1):
                        if (self.border_w, y) not in self.rep:
                            self.rep[(self.border_w, y)] = '?'
            self.on_poi()
        elif action == 'l':
            self.compass.left()
        elif action == 'r':
            self.compass.right()
        elif action == 'c' or action == 'u':
            # update right in front since tree or door gone
            x = None
            y = None
            if direction == 'n':
                x = self.x
                y = self.y + 1
            elif direction == 'e':
                x = self.x + 1
                y = self.y
            elif direction == 's':
                x = self.x
                y = self.y - 1
            elif direction == 'w':
                x = self.x - 1
                y = self.y
            self.rep[(x, y)] = view[(0,1)]
            self.trees.discard((x,y))
            self.doors.discard((x,y))

    def show(self):
        # print(self.border_n)
        # print(self.border_e)
        # print(self.border_s)
        # print(self.border_w)
        line = '+'
        for x in range(self.border_w, self.border_e + 1):
            line += '-'
        line += '+'
        print(line)
        for y in range(self.border_n, self.border_s - 1, -1):
            line = '|'
            for x in range(self.border_w, self.border_e + 1):
                if (x == self.x and y == self.y):
                    line += 'A' # TODO: Agent direction
                elif (x == 0 and y == 0):
                    line += 'X' # Start/End
                elif (x,y) in self.rep:
                    line += self.rep[(x, y)]
                else:
                    line += '/' # should never be printed
            line += '|'
            print(line)
        line = '+'
        for x in range(self.border_w, self.border_e + 1):
            line += '-'
        line += '+'
        print(line)
        print('axe: ' + str(self.axe))
        print('key: ' + str(self.key))
        print('stone: ' + str(self.stone))
        print('gold: ' + str(self.gold))
        print('has_axe: ' + str(self.has_axe))
        print('has_key: ' + str(self.has_key))
        print('num_stones: ' + str(self.num_stones))
        print('has_gold: ' + str(self.has_gold))
        print('trees: ' + str(self.trees))
        print('doors: ' + str(self.doors))
env = env_class()

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

action = ''

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
    env.update(view, action)
    env.show()
    action = get_action(env)
    out_stream.write(action)
    out_stream.flush()
