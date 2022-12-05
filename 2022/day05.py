import sys

test = """\
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = [s.rstrip() for s in open('day05.txt').readlines()]

DEBUG = 'debug' in sys.argv

columns = [[] for _ in range(9)]
commands = []
for row in data:
    # Parse the columns.
    if '[' in row:
        for col in range((len(row)+1)//4):
            if row[4*col+1] != ' ':
                columns[col].insert(0, row[4*col+1])
    # Parse the commands.
    elif len(row) > 4 and row[:4] == 'move':
        parts = row.split()
        commands.append( tuple(int(parts[k]) for k in (1,3,5)) )

if DEBUG:
    print(columns)

def part1(cols,commands):
    for cnt,frm,to in commands:
        for _ in range(cnt):
            cols[to-1].append(cols[frm-1].pop())
    return ''.join(c[-1] for c in cols)

def part2(cols,commands):
    for cnt,frm,to in commands:
        to -= 1
        frm -= 1
        cols[to].extend( cols[frm][-cnt:] )
        cols[frm] = cols[frm][:-cnt]
    return ''.join(c[-1] for c in cols)

def copy(columns):
    return [c[:] for c in columns if c ]

print("Part 1:", part1(copy(columns),commands))
print("Part 2:", part2(copy(columns),commands))
