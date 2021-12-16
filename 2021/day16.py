import sys
from heapq import heappush, heappop
import itertools

test = [
"38006F45291200",
"8A004A801A8002F478", # 16
"620080001611562C8802118E34", # 23
"C0015000016115A2E0802F182340", # 23
"A0016C880162017C3686B18A3D4780" # 31
]

test2 = [
"C200B40A82",
"04005AC33890",
"880086C3E88112",
"CE00C43D881120",
"D8005AC2A8F0",
"F600BC2D8F",
"9C005AC2F8F0",
"9C0141080250320F1802104A08"
]

hex2bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test
elif 'test2' in sys.argv:
    data = test2
else:
    data = [open('day16.txt').read()]

class Bitstream:
    def __init__( self, stream, inhex=True ):
        if inhex:
            self.bits = ''.join( hex2bin[k] for k in stream )
        else:
            self.bits = stream
        self.pos = 0

    def get( self, nbits ):
        p = self.bits[ self.pos : self.pos + nbits ]
        self.pos += nbits
        return p

    def consume( self, nbits ):
        self.pos += nbits

    def rest( self, limit = 99999 ):
        return Bitstream(self.bits[self.pos:self.pos+limit], False)

# 3 bits version
# 3 bits type
# type 4 = literal, encoded in 5 bit units
#    top bit set == more to come
#    top bit clear = last packet
# Type != 4 is operator packet
#   1 bit packet type ID
#      type 0 followed by 15 bit length of subpackets to follow
#      type 1 followed by 11 bit number of subpackets to follow


# We return bits consumed AND packet value.

def part2(bits : Bitstream) -> (int,int):
    global vertot

    vertot += int(bits.get(3),2)
    tid = int(bits.get(3),2)

    if tid == 4:

        # This is a literal packet.  Just return the value.

        val = 0
        while True:
            tag = bits.get(1)
            val = val << 4 | (int(bits.get(4),2))
            if tag == '0':
                break

    else:

        # This is an operator packet.  Let's gather up the value of all 
        # the subpackets.

        subs = []

        tag = bits.get(1)
        if tag == '0':
            pktlen = int(bits.get(15),2)
            j = bits.pos + pktlen
            while bits.pos < j:
                bc, val = part2(bits.rest(pktlen))
                bits.consume( bc )
                subs.append(val)
        else:
            pktcnt = int(bits.get(11),2)
            for _ in range(pktcnt):
                bc, val = part2(bits.rest())
                bits.consume( bc )
                subs.append(val)

        # Now operate on those subpacket values.

        if tid == 0:                # sum
            val = sum(subs)
        elif tid == 1:              # product
            val = 1
            for v in subs:
                val *= v
        elif tid == 2:              # minimum
            val = min(subs)
        elif tid == 3:              # maximum
            val = max(subs)
        elif tid == 5:              # greater
            val = int(subs[0] > subs[1])
        elif tid == 6:              # less
            val = int(subs[0] < subs[1])
        elif tid == 7:              # equal
            val = int(subs[0] == subs[1])

    return bits.pos, val

for n in data:
    vertot = 0
    if DEBUG:
        print(n)
    eaten, value = part2(Bitstream(n))
    print( "Part 1:", vertot )
    print( "Part 2:", value )  # 299227020491

