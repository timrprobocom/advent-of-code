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

//go:embed day19.txt
var live string

type Point = tools.Point


// So...
// Beam zero point  (5, 3)
// Top beam ends (1005,352) slope = 349/1000
// Bot beam ends (1005,476) slope = 473/1000
//
// Top beam is y = 349/1000 x + 3
// Bot beam is y = 473/1000 x + 3
// Height is 124x/1000
// To be 100 tall, that's x=806, y=281.

func inside( program []int, x, y int ) bool {
    pgm := tools.MakeProgram(program)
    pgm.Push( x )
    pgm.Push( y )
    pgm.Run()
    return pgm.Pop() != 0
}

func topy(x int) int {
    return 349 * x / 1000 + 3
}

func boty(x int) int {
    return 473 * x / 1000 + 3
}


// Run the program once to get the path.

func part1(program []int) int {
    sumx := 0
    for y := range 25 {
        row := []byte{}
        for x := range 50 {
			var val byte = '.'
            if inside(program, x, y ) {
				sumx++
				val = '#'
			}
			row = append(row, val)
		}
		fmt.Println(string(row))
	}

	return sumx
}

func assert( program []int, x, y int ) {
	if !inside(program,x,y) {
		fmt.Println( "Assertion failed", x, y );
	}
}

func check( program []int, x, y int ) bool {
    return inside(program, x,y)  && inside(program, x+99,y) && inside(program, x,y+99) && inside(program, x+99,y+99)
}

func part2( program []int ) int {
    y0 := 0
    y1 := 0
	for x := 800; true; x++ {
        // Find the top of the beam.
		for !inside(program, x, y0) {
            y0 ++
		}

        // Find the bottom of the beam.
        if y1 < y0 {
            y1 = y0 + 1
		}
        for inside( program, x, y1 ) {
            y1 ++
		}

        if DEBUG {
            fmt.Println( x, y0, y1-y0 )
		}

        // (x,y0) and (x,y1-1) are inside.  (x,y1) is outside.

        y := y1 - 100

        if check(program, x,y) {
            return x * 10000 + y
		}
	}
	return -1
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(live, live)

	// Run the program to produce the maze.

	program := tools.GetRowNumbers[int](input)

	assert( program, 5,2 )
	assert( program, 48,18 )
	assert( program, 48,19 )
	assert( program, 48,20 )
	assert( program, 48,21 )
	assert( program, 48,22 )

	fmt.Println("Part 1:", part1(program))
	fmt.Println("Part 2:", part2(program))
}


