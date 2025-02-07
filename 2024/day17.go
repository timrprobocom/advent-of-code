package main

import (
	"fmt"
	"slices"
	"strconv"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `	
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0`[1:]

var test1 string = `
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0`[1:]

var test2 string = `
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0`[1:]

//go:embed day17.txt
var live string

var opcodes []string = []string{
	// 0      1      2      3      4      5      6      7
	"adv", "bxl", "bst", "jnz", "bxc", "out", "bdv", "cdv",
}

type CPU struct {
	A       uint64
	B       uint64
	C       uint64
	P       uint16
	program []uint16
}

func makecpu(data string) CPU {
	var o CPU
	o.P = 0

	for _, line := range strings.Split(data, "\n") {
		if len(line) == 0 {
			continue
		}

		words := strings.Split(line, " ")
		if words[0] == "Register" {
			var val uint64
			val, _ = strconv.ParseUint(words[2], 10, 64)
			switch words[1][0] {
			case 'A':
				o.A = val
			case 'B':
				o.B = val
			case 'C':
				o.C = val
			}
		} else if words[0] == "Program:" {
			for _, c := range words[1] {
				if c != ',' {
					o.program = append(o.program, uint16(c)-'0')
				}
			}
		}
	}
	return o
}

func (o CPU) combo(n uint16) uint64 {
	switch n {
	case 0, 1, 2, 3:
		return uint64(n)
	case 4:
		return o.A
	case 5:
		return o.B
	case 6:
		return o.C
	}
	return 0
}

func (o *CPU) execute(opc uint16, opd uint16) int16 {
	switch opc {
	case 0: // adv
		o.A = o.A >> o.combo(opd)
	case 6: // bdv
		o.B = o.A >> o.combo(opd)
	case 7: // cdv
		o.C = o.A >> o.combo(opd)
	case 1: // bxl
		o.B = o.B ^ uint64(opd)
	case 2: // bst
		o.B = o.combo(opd) & 7
	case 3: // jnz
		if o.A != 0 {
			o.P = opd - 2
		}
	case 4: // bxc
		o.B = o.B ^ o.C
	case 5: // out
		return int16(o.combo(opd) & 7)
	}
	return -1
}

func (o *CPU) run() []uint16 {
	var result []uint16
	for o.P < uint16(len(o.program)) {
		i := o.program[o.P]
		j := o.program[o.P+1]
		if DEBUG {
			fmt.Println(o.P, ":",
				i, opcodes[i], "  ", j, "->", o.combo(j),
				"A=", o.A, "B=", o.B, "C= ", o.C)
		}
		k := o.execute(i, j)
		if k >= 0 {
			result = append(result, uint16(k))
		}
		o.P += 2
	}
	return result
}

func step(A uint64, v []uint16) uint16 {
	B := (A & 7) ^ uint64(v[0])
	return uint16(B ^ (A >> B) ^ uint64(v[1]))
}

func part1(program string) string {
	cpu := makecpu(program)
	result := cpu.run()
	var ret string
	for _, v := range result {
		if len(ret) > 0 {
			ret += ","
		}
		ret += string('0' + v)
	}
	return ret
}

func part2(program string) uint64 {
	cpu := makecpu(program)

	// The two variables here are the operands to the bxl statements.

	var costs []uint16
	for i := 0; i < len(cpu.program); i += 2 {
		if cpu.program[i] == 1 {
			costs = append(costs, cpu.program[i+1])
		}
	}

	// We start from the program, backwards, and find the values that
	// create the instruction for that step.  There might be several.

	var queue []uint64 = []uint64{0, 1, 2, 3, 4, 5, 6, 7}
	var possible []uint64

	for i := len(cpu.program) - 1; i >= 0; i-- {
		match := cpu.program[i]

		// Run the program sequence for each potential A value.  Save the ones
		// that produce the desired value.

		possible = []uint64{}
		for _, q := range queue {
			if step(q, costs)&7 == match {
				possible = append(possible, q)
			}
		}

		// Now produce the possible A values for the next digit.

		queue = []uint64{}
		for _, p := range possible {
			var i uint64
			for i = 0; i < 8; i++ {
				queue = append(queue, p*8+i)
			}
		}
	}

	// Verify.

	mn := slices.Min(possible)
	cpu.A = mn
	if !slices.Equal(cpu.program, cpu.run()) {
		panic("MISMATCH")
	}

	return mn
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	if TEST {
		fmt.Println("Part 1:", part1(test))
		fmt.Println("Part 1:", part1(test1))
		fmt.Println("Part 1:", part1(test2))
	} else {
		fmt.Println("Part 1:", part1(input))
		fmt.Println("Part 2:", part2(input))
	}
}
