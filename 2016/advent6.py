import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

data = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""".splitlines()

if not TEST:
    data = [k.strip() for k in open('day6.txt').readlines()]

class Counter(object):
    def __init__(self):
        self.counts = [0]*26
    def register(self,c):
        self.counts[ord(c)-ord('a')] += 1
    def debug(self):
        for c in self.counts:
            print( "%d" % c, end='')
        print()
    def getmax(self):
        m = max(self.counts)
        return chr(self.counts.index(m)+97)
    def getmin(self):
        m = min(self.counts)
        return chr(self.counts.index(m)+97)

counters = []
for _ in range(len(data[0])):
    counters.append( Counter() )

for line in data:
    if DEBUG:
        print(line)
    for i,c in enumerate(line):
        counters[i].register(c)
    if DEBUG:
        counters[0].debug()

if DEBUG:
    print(counters)
print( 'Part 1:', ''.join(c.getmax() for c in counters) )
print( 'Part 2:', ''.join(c.getmin() for c in counters) )
