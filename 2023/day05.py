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
            seeds = tuple(int(k) for k in row.split()[1:])
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

# We need to intersect the ranges.
# There are 3 cases to consider:
#   * The range starts before any map
#   * The range intersects one or more maps
#   * The range extends beyond the last map
#
#  So given 79,14  against 50,98,2 and 52,50,48
#    We get 79,14 had a delta of +2
#  Given 40,70  against 50,98,2 and 52,50,48
#    We get 40,10 with delta 0
#           50,48 with a delta of +2
#           98,2 with a delta of -48
#           100,10 with a delta of 0

# Map a single range through a single map.

def maprange(mapx, rnglo, size):
    rnghi = rnglo + size
    a,b,n = mapx[0]
    if rnglo < b:
        take = min(rnghi, b) - rnglo
        yield rnglo, take
        rnglo += take
    if rnglo == rnghi:
        return 
    # We now know that rnglo is at or beyond the first map.
    for a,b,n in mapx:
        if rnglo <= b+n:
            take = min(rnghi, b+n)-rnglo
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

# Map a set of ranges through all of the maps.

def doallmapranges(rngs):
    for m in maps:
        rngs = domapranges(m, rngs)
    return rngs

def part1(seeds,maps):
    m = map(domapping, seeds)
    return min(m)

def part1(seeds,maps):
    ranges = [(s,1) for s in seeds]
    ranges = doallmapranges(ranges)
    return min(a[0] for a in ranges)

def part2(seeds,maps):
    ranges = zip(seeds[0::2],seeds[1::2])
    ranges = doallmapranges(ranges)
    return min(a[0] for a in ranges)


seeds, maps = process(data)
if DEBUG:
    print(seeds,maps)
    print(list(domapranges(maps[0], [(79, 14)] )))
    print(list(domapranges(maps[0], [(40, 70)] )))
    exit(0)

print("Part 1:", part1(seeds,maps))
print("Part 2:", part2(seeds,maps))
