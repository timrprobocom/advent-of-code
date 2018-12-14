test = (
    ( 5, 124515891 ),
    ( 9, 5158916779 ),
    ( 18, 9251071085 ),
    ( 2018, 594142982 ),
    ( 260321, 9276422810 )
)


class Recipe(object):
    def __init__(self,score):
        self.score = score
        self.next = self
        self.prev = self

    def link( self, new ):
        new.prev = self
        new.next = self.next
        self.next = new
        return new

class State():
    def __init__(self):
        self.head = self.elf1 = Recipe( 3 )
        self.tail = self.elf2 = self.elf1.link( Recipe( 7 ) )
        self.length = 2

    def round( self ):
        xsum = self.elf1.score + self.elf2.score
        if xsum >= 10:
            self.length += 1
            self.tail = self.tail.link( Recipe( xsum // 10 ) )
        self.length += 1
        self.tail = self.tail.link( Recipe( xsum % 10 ) )
        e1 = self.elf1.score + 1
        for _ in range(e1):
            self.elf1 = self.elf1.next
        e2 = self.elf2.score + 1
        for _ in range(e2):
            self.elf2 = self.elf2.next

    def printlist( self, n=0 ):
        start = self.head
        if n == 0:
            print start.score,
            start = start.next
        for _ in range(n):
            start = start.next
        while start != self.head:
            print start.score,
            start = start.next
        print

    def printback5( self, n=0 ):
        start = self.head
        if n == 0:
            print start.score,
            start = start.next
        for _ in range(n-5):
            start = start.next
        while start != self.head:
            print start.score,
            start = start.next
        print

state = State()

state.printlist( )
for n, master in test:
    while state.length < n+11:
        state.round( )
    state.printlist( n )
    print n, master
