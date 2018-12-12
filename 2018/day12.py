test = "#..#.#..##......###...###"

test1 = (
"...##",
"..#..",
".#...",
".#.#.",
".#.##",
".##..",
".####",
"#.#.#",
"#.###",
"##.#.",
"##.##",
"###..",
"###.#",
"####."
)

live = "##.#.####..#####..#.....##....#.#######..#.#...........#......##...##.#...####..##.#..##.....#..####"

live1 = (
"#..#.",
"#.#.#",
"#.#..",
".#...",
".#.##",
"..#..",
"..###",
"##.#.",
"##.##",
".##.#",
"...##",
"##...",
".#..#",
"####.",
".##.."
)

data = "."*5 + live + "."*30
data1 = live1

def printsum( base ):
    sumx = 0
    for i,c in enumerate(data):
        if c == '#':
            sumx += i - 5
    return sumx

def generate( base, gen ):
    new = ""
    for i in range(len(base)-5):
        if base[i:i+5] in gen:
            new += '#'
        else:
            new += '.'
    return '..' + new + '....'

print data

last = printsum(data)
print last
for i in range(200):
    data = generate( data, data1)
    print data
    nxt = printsum(data)
    print i+1, nxt, nxt-last
    last = nxt

# It repeats -- 78 more per iteration.

print (50000000000-200) * 78 + nxt

