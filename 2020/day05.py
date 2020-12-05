import sys

#BFFFBBFRRR: row 70, column 7, seat ID 567.
#FFFBBBFRRR: row 14, column 7, seat ID 119.
#BBFFBBFRLL: row 102, column 4, seat ID 820.

test = (
'BFFFBBFRRR',
'FFFBBBFRRR',
'BBFFBBFRLL'
)

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
else:
    data = open('day05.txt').read().split('\n')[:-1]

def xlate(n):
    return int(n.replace('B','1').replace('F','0').replace('R','1').replace('L','0'),2)

#def xlate(n):
#    x = int(n[:7].replace('B','1').replace('F','0'),2)
#    y = int(n[7:].replace('R','1').replace('L','0'),2)
#    if DEBUG:
#        print( n, x, y, x*8+y )
#    return x*8+y

ids = [xlate(i) for i in data]
print( "Part 1:", max( ids ) )
ids.sort()
if DEBUG:
    print(ids)
last = 0
for i in ids:
    if last and i != last+1:
        print( "Part 2:", i-1 )
        break
    last = i

