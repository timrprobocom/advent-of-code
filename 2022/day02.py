import sys

# 1 rock X A
# 2 paper Y B
# 3 scissors Z C

# win lose draw +6 +0 +3

test = """\
A Y
B X
C Z
"""

score = {
    "AX": 3,
    "BY": 3,
    "CZ": 3,
    "AY": 6,
    "BZ": 6,
    "CX": 6,
    "AZ": 0,
    "BX": 0,
    "CY": 0
}

# "ldw" which is XYZ
need = {
    'A': 'ZXY',
    'B': 'XYZ',
    'C': 'YZX'
}


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day02.txt').readlines()

def part1(data):
    count = 0
    for game in data:
        count += score[game[0]+game[2]] + ord(game[2])-ord('W')
    return count

def part2(data):
    count = 0
    for game in data:
        choice = ord(game[2]) - ord('X')
        mypick = need[game[0]][choice]
        count += score[game[0]+mypick] + ord(mypick)-ord('W')
    return count

def part(data):
    count1 = 0
    count2 = 0
    for game in data:
        mypick = game[2]
        count1 += score[game[0]+mypick] + ord(mypick)-ord('W')
        choice = ord(game[2]) - ord('X')
        mypick = need[game[0]][choice]
        count2 += score[game[0]+mypick] + ord(mypick)-ord('W')
    return count1,count2

results = part(data)
print("Part 1:", results[0])
print("Part 1:", results[1])
