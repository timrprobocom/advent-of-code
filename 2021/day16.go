package main

import (
	"fmt"
	"strconv"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
38006F45291200
8A004A801A8002F478
620080001611562C8802118E34
C0015000016115A2E0802F182340
A0016C880162017C3686B18A3D4780`[1:]

var test2 = `
C200B40A82
04005AC33890
880086C3E88112
CE00C43D881120
D8005AC2A8F0
F600BC2D8F
9C005AC2F8F0
9C0141080250320F1802104A08`[1:]

var hex2bin = map[byte]string {
    '0': "0000",
    '1': "0001",
    '2': "0010",
    '3': "0011",
    '4': "0100",
    '5': "0101",
    '6': "0110",
    '7': "0111",
    '8': "1000",
    '9': "1001",
    'A': "1010",
    'B': "1011",
    'C': "1100",
    'D': "1101",
    'E': "1110",
    'F': "1111",
}

//go:embed day16.txt
var live string

type Bitstream struct {
	bits	string
	pos		int
}

func makeBitstream( stream string, inhex bool ) *Bitstream {
	bs := Bitstream{"",0}
	if inhex {
		for i := range len(stream) {
			bs.bits += hex2bin[stream[i]]
		}
	} else {
		bs.bits = stream
	}
	return &bs
}

func (self *Bitstream) get( nbits int ) int {
	p := self.bits[ self.pos : self.pos + nbits ]
	self.pos += nbits
	val,_ := strconv.ParseInt(p,2,64)
	return int(val)
}

func (self *Bitstream) consume( nbits int ) {
	self.pos += nbits
}

func (self *Bitstream) rest(limit int) *Bitstream {
	if limit == 0 {
		limit = len(self.bits) - self.pos
	}
	return &Bitstream{self.bits[self.pos:self.pos+limit], 0}
}



// 3 bits version
// 3 bits type
// type 4 = literal, encoded in 5 bit units
//    top bit set == more to come
//    top bit clear = last packet
// Type != 4 is operator packet
//   1 bit packet type ID
//      type 0 followed by 15 bit length of subpackets to follow
//      type 1 followed by 11 bit number of subpackets to follow


// We return bits consumed AND packet value.

var vertot int

func part2( bits *Bitstream ) (int,int) {
    vertot += bits.get(3)
    tid := bits.get(3)
	val := 0

    if tid == 4 {

        // This is a literal packet.  Just return the value.

		tag := 99
        for tag != 0 {
            tag = bits.get(1)
            val = (val << 4) | bits.get(4)
		}

    } else {

        // This is an operator packet.  Let's gather up the value of all 
        // the subpackets.

        subs := []int{}

        tag := bits.get(1)
        if tag == 0 {
            pktlen := bits.get(15)
            //j := bits.pos + pktlen
            for pktlen > 0 {
                bc, val := part2(bits.rest(pktlen))
                bits.consume( bc )
				pktlen -= bc
				subs = append( subs, val )
			}
        } else {
            pktcnt := bits.get(11)
            for _ = range pktcnt {
                bc, val := part2(bits.rest(0))
                bits.consume( bc )
				subs = append( subs, val )
			}
		}

        // Now operate on those subpacket values.

        if tid == 0 {                     // sum
            val = tools.Sum(subs)
        } else if tid == 1 {              // product
            val = 1
            for _, v := range subs {
                val *= v
			}
        } else if tid == 2 {              // minimum
            val = tools.Min(subs)
        } else if tid == 3 {              // maximum
            val = tools.Max(subs)
        } else if tid == 5 {              // greater
            if subs[0] > subs[1] {
				val = 1
			}
        } else if tid == 6 {              // less
            if subs[0] < subs[1] {
				val = 1
			}
        } else if tid == 7 {              // equal
            if subs[0] == subs[1] {
				val = 1
			}
		}
	}

    return bits.pos, val
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	for _,line := range strings.Split(input, "\n") {
		bs := makeBitstream( line, true )
		_, p2 := part2(bs)
		fmt.Println("Part 1:", vertot )
		fmt.Println("Part 2:", p2 )
	}
}

