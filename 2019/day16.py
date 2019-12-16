import itertools
import sys
import time

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

real = """\
59791911701697178620772166487621926539855976237879300869872931303532122404711706813176657053802481833015214226705058704017099411284046473395211022546662450403964137283487707691563442026697656820695854453826690487611172860358286255850668069507687936410599520475680695180527327076479119764897119494161366645257480353063266653306023935874821274026377407051958316291995144593624792755553923648392169597897222058613725620920233283869036501950753970029182181770358827133737490530431859833065926816798051237510954742209939957376506364926219879150524606056996572743773912030397695613203835011524677640044237824961662635530619875905369208905866913334027160178"""

#print( "My input length is ", len(real) )

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
    nextx.append( abs(sumx) % 10 )
    for n in digits[:-1]:
        sumx -= n
        nextx.append( abs(sumx) % 10 )
    return nextx

def make(s):
    return list(int(k) for k in s)

def do100(pat,process,rep=1,ofs=0):
    base = (make(pat)*rep)[ofs:]
    for i in range(100):
        base = process(base,ofs)
    return ''.join(str(k) for k in base[:8])

if "tests" in sys.argv:
    for s in tests:
        print( do100(s, onepass) )

print( "Part 1:", do100(real, onepass) )

def part2(seq):
    offset = int(seq[:7])
    assert( len(seq) < 2 * offset )
    return do100( seq, offsetpass, 10000, offset )

if "tests" in sys.argv:
    for seq in test2:
        before = time.time()
        print( part2(seq) )
        print( "Elapsed", time.time() - before )

before = time.time()
print( "Part 2:", part2( real ) )
print( "Elapsed", time.time() - before )
