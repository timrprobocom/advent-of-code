import sys
from collections import Counter
from statistics import median

test = "16,1,2,0,4,2,7,1,2,14"


DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day07.txt').read()

# This is actually n*(n+1)/2
cost = [0]
for i in range(1,2000):
    cost.append( cost[-1] + i )

data = eval(data)

def cost1(k):
    return k
def cost2(k):
    return cost[k]

# avg = 4 med = 2
# avg = 479 med = 339
# Part 1 answer is the median.

def part1(data):
    med = int(median(data))
    if DEBUG:
        print("med",med)
    return sum(abs(k-med) for k in data)

def part2(data,cost):
    mf = 1e10
    for avg in range(max(data)):
        f = sum(cost(abs(k-avg)) for k in data)
        if f > mf:
            return mf
        mf = f

print("Part 1:", part1(data) )
print("Part 1:", part2(data, cost1) )
print("Part 2:", part2(data, cost2) )

