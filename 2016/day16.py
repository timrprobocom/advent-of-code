import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv


def dragoncurve( seq, n ):
    while len(seq) < n:
        s2 = seq[:]
        s2.reverse()
        s2 = [ 1-k for k in s2 ]
        seq = seq + [0] + s2
    return seq[:n]

def checksum( seq ):
    if len(seq) & 1:
        return seq
    newseq = []
    for i in range(0, len(seq), 2):
        newseq.append( 1 - seq[i] ^ seq[i+1] )
    return checksum(newseq)

def strtoseq(s):
    return [ord(c)-48 for c in s]

def seqtostr(s):
    return ''.join( chr(c+48) for c in s)

if DEBUG:
    print( dragoncurve([1],3) )
    print( dragoncurve([0],3) )
    print( dragoncurve([1,1,1,1,1],9) )
    print( seqtostr(dragoncurve(strtoseq('111100001010'),25)) )

    print( seqtostr(checksum([1,1,0,0,1,0,1,1,0,1,0,0])) )

data = strtoseq('11101000110010100')
curve = dragoncurve(data,272)
print( 'Part 1:', seqtostr(checksum(curve)) )
curve = dragoncurve(data,35651584)
print( 'Part 2:', seqtostr(checksum(curve)) )

