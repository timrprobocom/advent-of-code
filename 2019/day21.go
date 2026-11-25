package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG = false
var TEST = false
var IMAGE = false

var test = ""

//go:embed day21.txt
var live string

type Point = tools.Point



// So, we have to probe to find the holes.

func run(program []int, instructions []string) int {
    pgm := tools.MakeProgram(program)
	for _,line := range instructions {
		for _,c := range line {
			pgm.Push(int(c))
		}
		pgm.Push('\n')
	}
    pgm.Run()
    dump := pgm.Dump()
	if DEBUG {
		out := []byte{}
		for _,c := range dump {
			if c < 255 {
				out = append(out, byte(c))
			}
		}
		fmt.Println( string(out))
	}
    if dump[len(dump)-1] > 255 {
        return dump[len(dump)-1]
	}
    return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(live, live)

	program := tools.GetRowNumbers[int](input)

	// Jump spans 4
	// I've seen 
	//  #####...##     
	//   DCBA
	//  #####.#..#
	//   DCBA A
	//        B
	//  #####.####

	part1 := []string {
		"NOT C J",  // if +3 is hole
		"AND D J",  // but +4 is land
		"NOT A T",  // if +1 is hole
		"OR  T J",  // also jump
		"WALK",
	}

	fmt.Println( "Part 1:", run(program, part1) )

	// I like this because it's more general:
	//   A jump is required, a landing spot is 
	// available, and a second jump is also available.
	// ( !1 | !2 | !3 ) & 4 & (8 | (5 & 9))

	part2 := []string {
		"NOT A J",
		"NOT B T",
		"OR  T J",
		"NOT C T",
		"OR  T J",
		"AND D J",
		"NOT E T",
		"NOT T T",
		"OR  H T",
		"AND T J",
		"RUN",
	}

	// Seen

	// ####.#..#
	// ####...#
	// ####.#.##.####
	// ####.##.######

	fmt.Println( "Part 2:", run(program, part2) )
}
