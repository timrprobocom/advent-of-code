import sys

test = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

check = (12,13,14)

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day02.txt').readlines()

def reformat(data):
    record = {}
    for line in data:
        p1,_,p2 = line.strip().partition(': ')
        game = int(p1.split()[1])
        record[game] = []
        games = p2.split('; ')
        for g in games:
            parts = g.split(', ')
            c = {'red':0, 'green':0, 'blue':0}
            for p in parts:
                a,_,b = p.partition(' ')
                c[b] = int(a)
            record[game].append( list(c.values()) )
    return record

def part1(record):
    sumx = 0
    for game,data in record.items():
        for r in data:
            if r[0] > check[0] or r[1] > check[1] or r[2] > check[2]:
                break
        else:
            sumx += game
    return sumx


def part2(record):
    sumx = 0
    for data in record.values():
        cnt = [0,0,0]
        for row in data:
            cnt = [max(c,r) for c,r in zip(cnt,row)]
        power = cnt[0]*cnt[1]*cnt[2]
        sumx += power
    return sumx

data = reformat(data)
print("Part 1:", part1(data))
print("Part 2:", part2(data))
