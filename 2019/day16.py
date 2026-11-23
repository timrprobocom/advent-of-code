import sys
import time

TEST = 'test' in sys.argv
TIMING = "timing" in sys.argv

tests = (
"80871224585914546619083218645595", # becomes 24176176.
"19617804207202209144916044189917", # becomes 73745418.
"69317163492948606335995924319873"  # becomes 52432133.
)

test2 = (
"03036732577212944063491565474664", # becomes 84462026.
"02935109699940807407585447034323", # becomes 78725270.
"03081770884921959731165446850517"  # becomes 53553731.
)

live = open('day16.txt').read().strip()
#print( "My input length is ", len(live) )

# This works for pass 1 but is way too slow for pass 2.

def onepass(digits,offset):
    nextx = []
    for n in range(len(digits)):
        sumx = 0
        np1 = n+offset+1
# For n=0:  0, 4, 8, 12.    0 + 4x
# For n=1:  1, 9, 17, 25    1 + 8x
# for n=2:  2, 14, 26, 38   2 + 12x
        for i in range(n, len(digits), 4*np1):
            sumx += sum(digits[i:i+np1]) - sum(digits[i+2*np1:i+3*np1])
        nextx.append( abs(sumx) % 10)
    return nextx

# This works for pass 2.

def offsetpass(digits,offset):
    nextx = []
    sumx = sum(digits)
    nextx.append( sumx % 10 )
    for n in digits[:-1]:
        sumx += 10 - n
        nextx.append( sumx % 10 )
    return nextx

def make(s):
    return list(int(k) for k in s)

def do100(pat,process,rep=1,ofs=0):
    if rep == 1:
        base = pat
    else:
        # Since we throw away almost all of the resulting string, don't 
        # compute all of it.
        # Example: 32 10000 303673
        # So we keep 320000-303673 = 16327.
        # So repeat (16327/32 + 1) times and skip 303673 % 32 = 25
        need = (len(pat) * rep - ofs) // len(pat) + 1
        base = (pat * need)[ofs % len(pat):]
    base = make(base)
    for _ in range(100):
        base = process(base,ofs)
    return ''.join(str(k) for k in base[:8])

def part2(seq):
    offset = int(seq[:7])
    assert( len(seq) < 2 * offset )
    return do100( seq, offsetpass, 10000, offset )

if TEST:
    for seq in tests:
        print( "Test 1:", do100(seq, onepass) )
    for seq in test2:
        before = time.time()
        print( "Test 2:", part2(seq) )
        print( "Elapsed", time.time() - before )
else:
    print( "Part 1:", do100(live, onepass) )
    before = time.time()
    print( "Part 2:", part2( live ) )
    if TIMING:
        print( "Elapsed", time.time() - before )
