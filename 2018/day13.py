test = open('day13test.txt').readlines()
live = open('day13.txt').readlines()
data = live

import sys
import copy
import itertools


dirs = {
    '<': (-1,0),
    'v': (0,1),
    '>': (1,0),
    '^': (0,-1)
}

# Go left:

# < -1,0 left is 0,1
# < -1,0 right is 0,-1
# v 0,1 left is 1,0
# v 0,1 right is -1,0
# > 1,0 left is 0,-1
# > 1,0 right is 0,1
# ^ 0,-1 left is -1,0
# ^ 0,-1 right is 0,1

def left(x,y):
    if y == 0:
        return 0,-x
    else:
        return y,0

def straight(x,y):
    return x, y

def right(x,y):
    if y == 0:
        return 0,x
    else:
        return -y,0


moves = ( left, straight, right )

cartcounter = itertools.count()
class Cart( object ):
    def __init__(self,cart,x,y):
        self.cart = cartcounter.next()
        self.delta = dirs[cart]
        self.x = x
        self.y = y
        self.intersection = 0
    def forward(self):
        self.x += self.delta[0]
        self.y += self.delta[1]
    def coord(self):
        return (self.x, self.y)
    def turn(self,corner):
        if corner == '+':
            self.delta = moves[self.intersection](*self.delta)
            self.intersection = (self.intersection + 1) % 3
        elif corner == '/':
            self.delta = (-self.delta[1],-self.delta[0])
        elif corner == '\\':
            self.delta = (self.delta[1],self.delta[0])

    def __repr__(self):
        return "Cart at %d,%d moving %d,%d" % (self.x, self.y, self.delta[0], self.delta[1])

def parse( grid ):
    corners = {}
    carts = []
    for y,ln in enumerate(grid):
        for x,ch in enumerate(ln):
            if ch in '>^<v':
                carts.append( Cart( ch, x, y ) )
            elif ch in '\\/+':
                corners[(x,y)] = ch
    return corners, carts

def advance1( corners, carts ):
    for cart in carts:
        cart.forward()
        for other in carts:
            if cart != other and cart.coord() == other.coord():
                print "Collision at ", cart.coord()
                return False
        if cart.coord() in corners:
            cart.turn( corners[cart.coord()] )
    return True

def advance2( corners, carts ):
    remove = []
    for cart in carts:
        cart.forward()
        for other in carts:
            if cart != other and cart.coord() == other.coord():
                print "Collision at ", cart.coord()
                remove.append( cart )
                remove.append( other )
        if cart.coord() in corners:
            cart.turn( corners[cart.coord()] )
    for cart in remove:
        carts.remove( cart )
    return True

advance = advance2

corners, carts = parse( data )
print carts
print corners
while advance( corners, carts ):
    print carts
    print "***"
    if len(carts) == 1:
        break


