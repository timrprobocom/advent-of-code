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

data = [k.strip() for k in open('../Downloads/day6.txt').readlines()]

class Counter(object):
    def __init__(self):
        self.counts = [0]*26
    def register(self,c):
        self.counts[ord(c)-ord('a')] += 1
    def debug(self):
        for c in self.counts:
            print "%d" % c,
        print
    def getmax(self):
        mc = '-'
        mx = 999
        for i,t in enumerate(self.counts):
            if t < mx:
                mc = chr(i+97)
                mx = t
        return mc

counters = []
for i in range(len(data[0])):
    counters.append( Counter() )

for line in data:
    print line
    for i,c in enumerate(line):
        counters[i].register(c)
    counters[0].debug()

print '------'
print ''.join(c.getmax() for c in counters)
