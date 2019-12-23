import sys
import time
import queue
from intcode import Program
from tools import Point

TRACE = 'trace' in sys.argv

progs = []
nat = None

class Prog23(Program):
    def read_input(self):
        if self.nextin is not None:
            self.idle = False
            i, self.nextin = self.nextin, None
            return i
        if not self.input.empty():
            self.idle = False
            a,self.nextin = self.input.get()
            if TRACE:
                print( f"{self.id}: read {a} {self.nextin}" )
            return a
        time.sleep( 0.1 )
        if TRACE:
            sys.stdout.flush()
        self.idle = True
        return -1

    def send_output(self,p):
        global nat
        if self.output.qsize() > 1:
            ad = self.output.get()
            x = self.output.get()
            if TRACE:
                print( f"{self.id}: send {x} {p} to {ad}" )
            pkt = (x,p)
            if ad == 255:
                if TRACE:
                    print( "Sending", pkt )
                nat = pkt
                return
            progs[ad].push( pkt )
        else:
            self.output.put( p )

real = list(eval(open('day23.txt').read()))

for i in range(50):
    progs.append( Prog23(real) )
    progs[-1].nextin = i

for i in range(50):
    progs[i].start()

lastnat = None
while 1:
    # Wait for idle.
    time.sleep( 0.1 )
    if nat and all(p.idle for p in progs):
        if not lastnat:
            print( "Part 1:", nat )
        if nat == lastnat:
            print( "Part 2:", nat )
            break
        if TRACE:
            print( "Delivering", nat )
        progs[0].push( nat )
        nat,lastnat = None,nat

for p in progs:
    p.die = True

time.sleep( 0.5 )
