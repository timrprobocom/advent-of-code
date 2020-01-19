from hashlib import md5
from itertools import count

ctr = count(1)

test = b'abcdef'
real = b'ckczppom'

data = real

for c in ctr:
    o = md5( data + str(c).encode() ).hexdigest()
    if o[:6] == '000000':
        print( 'Part 2:', c, o )
        break
    if o[:5] == '00000':
        print( 'Part 1:', c, o )


