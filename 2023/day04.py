import sys

test = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day04.txt').readlines()

DEBUG = 'debug' in sys.argv

def wins(row):
    parts = row.split()
    n = parts.index('|')
    wins = set(int(k) for k in parts[2:n])
    mine = set(int(k) for k in parts[n+1:])
    return len(mine & wins)

def part1(data):
    sumx = 0
    for row in data:
        cnt = wins(row)
        if cnt:
            sumx += 2**(cnt-1)
    return sumx

def part2(data):
    copies = [1]*len(data)
    sumx = 0
    for row in data:
        this = copies.pop(0)
        sumx += this

        cnt = wins(row)
        for j in range(cnt):
            copies[j] += this
    return sumx

print("Part 1:", part1(data))
print("Part 2:", part2(data))
