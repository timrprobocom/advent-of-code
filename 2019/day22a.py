import sys


# I know I will regret this, but I'll do it with a real list.
#
# I'm sure I will need a "remap" type function, then apply 100 times.

test1 = """\
deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""
# Result: 9 2 5 8 1 4 7 0 3 6

# Equivalent:
test1 = """\
deal with increment 3
cut -3
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""

class Deck(object):
    def __init__(self,n):
        self.n = n
        self.deck = list(range(n))
    def reverse(self):
        self.deck.reverse()
    def cut(self,n):
    # -2 means
    #  [-2:] plus :-2
    # +2 means
    # [2:] plus [:2]
#        if n > 0:
#            n = self.n - 1 - n
        self.deck = self.deck[n:]+self.deck[:n]
    def increment(self,n):
        new = [0]*self.n
        for i in range(self.n):
            new[(i*n)%self.n] = self.deck[i]
        self.deck = new




# Pre-parse the input.


def run( src, count ):
    deck = Deck(count)
    if not isinstance(src,str):
        src = src.read()
    for ln in src.splitlines():
        words = ln.strip().split()
        if words[0] == 'cut':
            deck.cut( int(words[1]) )
        if words[1] == 'with':
            deck.increment( int(words[3]) )
        if words[1] == 'into':
            deck.reverse();
#        print(deck.deck)
    return deck

deck = run( test1, 10 )
print(deck.deck)

deck = run( open("day22.txt"), 10007 )
print(deck.deck)
print(deck.deck.index(2019))
sys.exit(0)

# Run the program.

program = []
def no():
    print( program )
    deck = []
    for card in range(TOTAL):
        for act,val in program:
            card = act(val,card)
            print( "Now", card )
        print( "Saved", card )
        deck.append( card )

    print( deck )
    print( deck[2019] )
