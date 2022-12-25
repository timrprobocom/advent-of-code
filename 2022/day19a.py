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

class Plan:
    def __init__(self,nums):
        self.ore_ore = nums[0]
        self.clay_ore = nums[1]
        self.obsidian_ore = nums[2]
        self.obsidian_clay = nums[3]
        self.geode_ore = nums[4]
        self.geode_obsidian = nums[5]

def parse(data):
    bps = []
    for line in data:
        parts = line.split()
        nums = [int(parts[k]) for k in (6,12,18,21,27,30)]
        bps.append(Plan(nums))
    return bps

data = parse(data)

# This code is quick, but not always right.  It gets part 1 of the sample right, and part 2 of my data right.

def most_geodes(ore_robots, clay_robots, obsidian_robots, geode_robots, ore, clay, obsidian, geodes, minutes, blueprint):
    (next_ore, next_clay, next_obsidian, next_geodes) = (ore + ore_robots, clay + clay_robots, obsidian + obsidian_robots, geodes + geode_robots)
    if minutes == 1:
        return next_geodes

    if ore >= blueprint.geode_ore and obsidian >= blueprint.geode_obsidian:
      return most_geodes(ore_robots, clay_robots, obsidian_robots, geode_robots + 1, next_ore - blueprint.geode_ore, next_clay, next_obsidian - blueprint.geode_obsidian, next_geodes, minutes - 1, blueprint)

    if ore >= blueprint.obsidian_ore and clay >= blueprint.obsidian_clay:
      return most_geodes(ore_robots, clay_robots, obsidian_robots + 1, geode_robots, next_ore - blueprint.obsidian_ore, next_clay - blueprint.obsidian_clay, next_obsidian, next_geodes, minutes - 1, blueprint)

    maybe = []
    if ore < 4:
        maybe.append( most_geodes(ore_robots, clay_robots, obsidian_robots, geode_robots, next_ore, next_clay, next_obsidian, next_geodes, minutes - 1, blueprint) )

    if ore >= blueprint.ore_ore:
        maybe.append( most_geodes(ore_robots + 1, clay_robots, obsidian_robots, geode_robots, next_ore - blueprint.ore_ore, next_clay, next_obsidian, next_geodes, minutes - 1, blueprint))

    if ore >= blueprint.clay_ore:
        maybe.append( most_geodes(ore_robots, clay_robots + 1, obsidian_robots, geode_robots, next_ore - blueprint.clay_ore, next_clay, next_obsidian, next_geodes, minutes - 1, blueprint))

    return max(maybe)

def part1( data ):
    result = 0
    for i,plan in enumerate(data):
        result += (i+1) * most_geodes( 1, 0, 0, 0, 0, 0, 0, 0, 24, plan )
    return result

def part2( data ):
    result = 1
    for i,plan in enumerate(data[:3]):
        ans = most_geodes( 1, 0, 0, 0, 0, 0, 0, 0, 32, plan )
        print("===",i+1,ans)
        result *= ans
    return result

print("Part 1:", part1(data))
print("Part 2:", part2(data))
