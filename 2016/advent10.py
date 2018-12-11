data = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""".splitlines()

data = open('../Downloads/day10.txt').readlines()

class Bot(object):
    def __init__(self, i):
        self.bot = i+0
        self.lowrule = None
        self.highrule = None
        self.chips = []

    def give( self, chip ):
        self.chips.append( chip )
        if len(self.chips) == 2:
            print self.bot, self.chips
            low = min(self.chips)
            high = max(self.chips)
            if low==17 and high==61:
                print "****"
            if self.lowrule[0]:
                output[self.lowrule[1]] = low
            else:
                bot[self.lowrule[1]].give( low )
            if self.highrule[0]:
                output[-self.highrule[1]] = high
            else:
                bot[self.highrule[1]].give( high )

output = [0 for i in range(250)]
bot = [Bot(i) for i in range(250)]

gives = []

# We parse the rules first.

for ln in data:
    parts = ln.split()
    if parts[0] == 'value':
        gives.append( (int(parts[1]), int(parts[5])) )
    else:
        tgt = int(parts[1])
        assert parts[3] == 'low'
        assert parts[8] == 'high'
        lowd = int(parts[6])
        if parts[5] == 'bot':
            bot[tgt].lowrule = (0,lowd)
        elif parts[5] == 'output':
            bot[tgt].lowrule = (1,lowd)
        highd = int(parts[11])
        if parts[10] == 'bot':
            bot[tgt].highrule = (0,highd)
        elif parts[10] == 'output':
            bot[tgt].highrule = (1,highd)

# Now feed the gives.
print gives

for tok,dst in gives:
    bot[dst].give( tok )
print output
print output[0]*output[1]*output[2]
