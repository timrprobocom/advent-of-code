import re
import sys
from collections import deque

#   0     1   2    3   4    5     6  7     8   9    10    11   12  13   14   15       16    17   18 19 20   21 22     23   24    25    26   27  28 29 30
test = """\
Blueprint 1: Each ore robot costs 4 ore.  Each clay robot costs 2 ore.  Each obsidian robot costs 3 ore and 14 clay.  Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore.  Each clay robot costs 3 ore.  Each obsidian robot costs 3 ore and 8 clay.  Each geode robot costs 3 ore and 12 obsidian"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day19.txt').readlines()

DEBUG = 'debug' in sys.argv

def parse(data):
    bps = []
    for line in data:
        parts = line.split()
        nums = [int(parts[k]) for k in (6,12,18,21,27,30)]
        bps.append(nums)
    return bps

data = parse(data)

def solve(plan,T):
    # The state is ore inventory, robot inventory, time
    state = (0, 0, 0, 0, 1, 0, 0, 0, T)
    q = deque([state])
    seen = set()
    best = 0
    core = max(plan[0],plan[1],plan[2],plan[4])
    while q:
        state = q.popleft()
        ox,cl,ob,ge,r1,r2,r3,r4,t = state
        best = max(best,ge)
        if not t:
            continue

# What is this doing?  It produces the correct results without this, 
# but much slower.  It's saying we should never have more ore robots
# than the largest need.  Doesn't this discard bots we already bought?
# Does this just prune useless branches?

        r1 = min(r1, core)
        r2 = min(r2, plan[3])
        r3 = min(r3, plan[5])
        ox = min(ox, t*core - r1*(t-1))
        cl = min(cl, t*plan[3] - r2*(t-1))
        ob = min(ob, t*plan[5] - r3*(t-1))

        state = (ox,cl,ob,ge,r1,r2,r3,r4,t)
        if state in seen:
            continue
        seen.add(state)

        if len(seen) % 1000000 == 0:
            print(t,best,len(seen))

        q.append((ox+r1,cl+r2,ob+r3,ge+r4,r1,r2,r3,r4,t-1))
        if ox >= plan[0]:
            q.append((ox-plan[0]+r1,cl+r2,ob+r3,ge+r4,r1+1,r2,r3,r4,t-1))
        if ox >= plan[1]:
            q.append((ox-plan[1]+r1,cl+r2,ob+r3,ge+r4,r1,r2+1,r3,r4,t-1))
        if ox >= plan[2] and cl >= plan[3]:
            q.append((ox-plan[2]+r1,cl-plan[3]+r2,ob+r3,ge+r4,r1,r2,r3+1,r4,t-1))
        if ox >= plan[4] and ob >= plan[5]:
            q.append((ox-plan[4]+r1,cl+r2,ob-plan[5]+r3,ge+r4,r1,r2,r3,r4+1,t-1))
    return best

def part1(data):
    result = 0
    for idm,plan in enumerate(data):
        ans = solve(plan, 24)
        if DEBUG:
            print("===",idm+1,ans)
        result += (idm+1) * ans
    return result

def part2(data):
    result = 1
    for idm,plan in enumerate(data[:3]):
        ans = solve(plan, 32)
        if DEBUG:
            print("===",idm+1,ans)
        result *= ans
    return result

print("Part 1:", part1(data))
print("Part 2:", part2(data))
