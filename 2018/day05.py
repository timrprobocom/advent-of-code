import sys

test = 'dabAcCaCBAcCcaDA'
live = open('day05.txt').read().strip()

data = live

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
        sys.stdout.write( str(len(old))+'   \r')
        sys.stdout.flush()
    return len(new)


# Part 1.
print analyze(data)

# Part 2.

track = []
for i in range(26):
    uc = chr(65+i)
    lc = chr(97+i)

    knt = analyze( data.replace(uc,'').replace(lc,'') )
    print '\n', uc, lc, knt
    track.append( knt )

mx = min(track)
print track,mx, track.index(mx), chr(65+track.index(mx))

