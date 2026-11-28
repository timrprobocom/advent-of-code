import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

test = 'dabAcCaCBAcCcaDA'
live = open('day05.txt').read().strip()

data = test if TEST else live

def analyze(data):
    old = list(ord(c) for c in data)
    new = []
    while old:
        if len(old) > 1 and old[0] ^ old[1] == 0x20:
            old.pop(0)
            if new:
                old[0] = new.pop()
            else:
                old.pop(0)
        else:
            new.append(old.pop(0))
        if DEBUG:
            sys.stdout.write( str(len(old))+'   \r')
            sys.stdout.flush()
    return len(new)


# Part 1.
def part1(data):
    return analyze(data)

# Part 2.

def part2(data):
    track = []
    for i in range(26):
        uc = chr(65+i)
        lc = chr(97+i)

        knt = analyze( data.replace(uc,'').replace(lc,'') )
        if DEBUG:
            print( '\n', uc, lc, knt)
        track.append( knt )
    mx = min(track)
    if DEBUG:
        print( track,mx, track.index(mx), chr(65+track.index(mx)))
    return mx

print( "Part 1:", part1(data))
print( "Part 2:", part2(data))
