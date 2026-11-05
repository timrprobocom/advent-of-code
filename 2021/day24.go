package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day24.txt
var live string
var test = live


type Machine struct {
	regs	map[byte]int
}

func (self *Machine) reset() {
	self.regs = map[byte]int{ 'w': 0, 'x': 0, 'y': 0, 'z': 0 }
}

func (self *Machine) fetch(c string) int {
	if len(c) == 1 && c >= "w" && c <= "z" {
		return self.regs[c[0]]
	} else {
		return tools.StrToInt(c)
	}
}

func (self *Machine) store( c byte, v int ) {
	self.regs[c] = v
}

func (self *Machine) run( program []string, inp []int) int {
	self.reset()
// clone
	inputs := inp[:]
	for _,line := range program {
		if len(line) < 2 {
			continue
		}
		parts := strings.Fields( line )
		opc := parts[0]
		res := parts[1][0]
		if opc == "inp" {
			self.regs[res] = inputs[0]
			inputs = inputs[1:]
		} else if opc == "add" {
			self.regs[res] += self.fetch(parts[2])
		} else if opc == "mul" {
			self.regs[res] *= self.fetch(parts[2])
		} else if opc == "div" {
			self.regs[res] /= self.fetch(parts[2])
		} else if opc == "mod" {
			self.regs[res] %= self.fetch(parts[2])
		} else if opc == "eql" {
			if self.regs[res] == self.fetch(parts[2]) {
				self.regs[res] = 1
			} else {
				self.regs[res] = 0
			}
		}
	}
	return len(inp)-len(inputs)
}


//  We get these constraints from the code itself.
// So dig[0]+14- 7 == dig[13]  +7 0 is 1,2
// So dig[1]+ 2-10 == dig[12]  -8 1 is 9
// So dig[2]+ 1- 5 == dig[11]  -4 2 is 5-9
// So dig[3]+13-12 == dig[6]   +1 3 is 1-8
// So dig[4]+ 5-12 == dig[5]   -7 4 is 8 9
// So dig[7]+ 9- 7 == dig[8]   +2 7 is 1-7
// So dig[9]+13- 8 == dig[10]  +5 9 is 1-4

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")

	valid := [][]int{}
	machine := Machine{}
	machine.reset()
	d1 := 9
	d12 := 1
	for d0 := 1; d0 <= 2; d0++ {
		for d2 := 5; d2 <= 9; d2++ {
			for d3 := 1; d3 < 9; d3++ {
				for d4 := 8; d4 <= 9; d4++ {
					for d7 := 1; d7 < 8; d7++ {
						for d9 := 1; d9 <= 4; d9++ {
							d13 := d0+7
							d11 := d2-4
							d6 := d3+1
							d5 := d4-7
							d8 := d7+2
							d10 := d9+5
							code := []int{d0,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13}
							machine.run(data, code)
							if machine.regs['z'] == 0 {
								valid = append( valid, code )
							}
						}
					}
				}
			}
		}
	}
	if DEBUG {
		fmt.Println(len(valid), "keys")
	}
	nums := "0123456789"
	last := []byte{}
	first := []byte{}
	n := len(valid) - 1
	for i := 0; i < len(valid[0]); i++ {
		last = append( last, nums[valid[n][i]] )
		first = append( first, nums[valid[0][i]] )
	}
	fmt.Println( "Part 1:", string(last) )
	fmt.Println( "Part 2:", string(first) )
}
