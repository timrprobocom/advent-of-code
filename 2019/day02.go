package main

import (
	"Fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
1,9,10,3,2,3,11,0,99,30,40,50",
1,0,0,0,99",
2,3,0,3,99",
2,4,4,5,99,0",
1,1,1,4,99,5,6,0,99`[1:]

//go:embed day02.txt
var live string

// This program computes 466644 + 216000 x [1] + [2];

func run(pgm []int) []int {
    pc := 0
    for true {
        opcode := pgm[pc]
        if opcode == 1 {
            pgm[pgm[pc+3]] = pgm[pgm[pc+1]] + pgm[pgm[pc+2]]
            pc += 4
        } else if opcode == 2 {
            pgm[pgm[pc+3]] = pgm[pgm[pc+1]] * pgm[pgm[pc+2]]
            pc += 4
        } else if opcode == 99 {
            break
		}
	}
	return pgm
}

func testrun( pgm []int, p1, p2 int ) int {
    base := append(pgm[:0:0], pgm...)
    base[1] = p1
    base[2] = p2
    return run(base)[0]
}

// Part 1.

func part1( data []int ) int {
	if TEST {
		return run(data)[0] 
	}
    return testrun(data, 12, 2)
}

// Part 2, brute force.
// Answer 8976.
// (19690720 - 466644) // 216000 == 89
// (19690720 - 466644 - 216000 * 89) == 76.

func part2( data []int ) int {
    for i := range 100 {
        for j := range 100 {
            k := testrun(data,i,j)
            if DEBUG {
                fmt.Println(i, j, k )
			}
            if k == 19690720 {
                return i * 100 + j
			}
		}
	}
	return 0
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	for _,line := range strings.Split(input,"\n") {
		data := tools.GetRowNumbers[int](line)

		fmt.Println("Part 1:", part1(data))
		if ! TEST {
			fmt.Println("Part 2:", part2(data))
		}
	}
}
