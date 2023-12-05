import sys

test = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open('day05.txt').readlines()

DEBUG = 'debug' in sys.argv

# Convert the input into a list of seed numbers, and a
# list of maps.  Each map is a list of tuples, (dest,src,len).

def process(data):
    seeds = []
    maps = []
    lastmap = []
    for row in data:
        if row.startswith('seeds'):
            seeds = list(int(k) for k in row.split()[1:])
        elif len(row) < 2:
            if lastmap:
                lastmap.sort(key=lambda k: k[1])
                maps.append(lastmap)
                lastmap = []
        elif row[0].isdigit():
            lastmap.append( tuple(int(k) for k in row.split()) )
    lastmap.sort(key=lambda k: k[1])
    maps.append(lastmap)
    return seeds, maps

# Map a single value through a single map.

def mapping(mapx, inval):
    for a,b,n in mapx:
        if b <= inval <= b+n:
            return inval-b+a
    return inval

# Map a single value through all of the maps.

def domapping(i):
    for m in maps:
        i = mapping(m, i)
    return i

# We need to intersect these ranges.
#  So given 79,14  against 50,98,2 and 52,50,48
#    We get 79,14 had a delta of +2
#  Given 40,70  against 50,98,2 and 52,50,48
#    We get 40,10 with delta 0
#           50,48 with a delta of +2
#           98,2 with a delta of -48
#           100,10 with a delta of 0

# Map a single range through a single map.

def maprange(mapx, rnglo, size):
    if DEBUG:
        print("doing",rnglo,size)
    rnghi = rnglo + size
    a,b,n = mapx[0]
    if rnglo < b:
        take = min(rnghi, b) - rnglo
        yield rnglo, take
        rnglo += take
    if rnglo == rnghi:
        return 
    # At this point, rnglo is at or beyond the first map.
    if DEBUG:
        print('mapx',mapx)
    for a,b,n in mapx:
        if DEBUG:
            print("===",b+n,rnghi,rnglo)
        if rnglo <= b+n:
            take = min(b+n, rnghi)-rnglo
            yield rnglo+a-b, take
            rnglo += take
        if rnglo == rnghi:
            return
    if rnglo < rnghi:
        yield rnglo, rnghi-rnglo

# Map a set of ranges through a single map.

def domapranges(mapx, rngs):
    for a,b in rngs:
        yield from maprange(mapx, a, b)

def part1(seeds,maps):
    m = [domapping(seed) for seed in seeds]
    return min(m)

def part2(seeds,maps):
    # Convert the list to a set of ranges.
    myseeds = zip(seeds[0::2],seeds[1::2])
    # Run the set of ranges through all of the maps.
    for m in maps:
        myseeds = domapranges(m, myseeds)
    # Find the smallest resulting range.
    return min(a[0] for a in myseeds)


seeds, maps = process(data)
if DEBUG:
    print(seeds,maps)
    print(list(domapranges(maps[0], [(79, 14)] )))
    print(list(domapranges(maps[0], [(40, 70)] )))
    exit(0)

print("Part 1:", part1(seeds,maps))
print("Part 2:", part2(seeds,maps))
