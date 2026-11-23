package main

import (
	"fmt"
	"os"
	"strings"
	"time"

	"aoc/tools"
	_ "embed"
)

var DEBUG = false
var TEST = false
var IMAGE = false
var SLOW = false

var test = ""

//go:embed day13.txt
var live string

func run(program []int) []int {
	out := []int{}
    pgm := tools.MakeProgram(program)
    go pgm.Run()
	for pgm.IsAlive() {
		out = append( out, pgm.Pop() )
		out = append( out, pgm.Pop() )
		out = append( out, pgm.Pop() )
	}
    return out
}

func display( grid [][]byte ) {
	if IMAGE {
		tools.Gotoxy( 0, 5 )
		for _,row := range grid {
			fmt.Println( string(row) )
		}
		if SLOW {
			time.Sleep( 50 * time.Millisecond )
		}
	}
}

func run2(grid [][]byte, program []int) int {
	pgm := tools.MakeProgram(program)
	xball :=0
	xpaddle := 0
	score := 0

    go pgm.Run()
	for pgm.IsAlive() {
		x := pgm.Pop()
		y := pgm.Pop()
		t := pgm.Pop()

		if x == -1 {
			score = t
			if DEBUG {
				fmt.Println( "Score:", t, "   " )
			}
			continue
		} 
		if t > 4 {
			fmt.Println( "error", x, y, t )
			continue
		}

		grid[y][x] = " #x-o"[t]

		if t == 3 { //&& xpaddle == 0 {
			xpaddle = x
		}
		if t == 4 {
			xball = x
			display(grid)

			if xball == 0 || xpaddle == 0 {
				pgm.Push(0)
			} else if xball < xpaddle {
				xpaddle --
				pgm.Push(-1)
			} else if xball > xpaddle {
				xpaddle ++
				pgm.Push(1)
			} else {
	 			pgm.Push(0)
			}
		}
	}
	queue := pgm.Dump()
	for i := 0; i < len(queue); i += 3 {
		if queue[i] == -1 {
			score = queue[i+2]
		}
	}
	return score
}


func part1(program []int) int {
    queue := run(program)
	twos := 0
	for i := 0; i < len(queue); i += 3 {
		if queue[i+2] == 2 {
			twos ++
		}
	}
    return twos // 228
}


func part2(program []int) int {
	queue := run(program)

	// Determine bounds.

    maxx := 0
	maxy := 0
	for i := 0; i < len(queue); i += 3 {
		maxx = max(maxx, queue[i]+1)
		maxy = max(maxy, queue[i+1]+1)
	}

    // Make grid.

	grid := make([][]byte, maxy)
	for i := range maxy {
		grid[i] = []byte(strings.Repeat(" ", maxx))
	}

    // Populate with the part 1 result.

	for i := 0; i < len(queue); i += 3 {
		x := queue[i]
		y := queue[i+1]
		t := queue[i+2]
        grid[y][x] = " #x-o"[t]
	}

	if IMAGE {
		tools.Cls()
		display(grid)
	}

    // Insert a quarter.

    program[0] = 2
    
    // Go run the app.

    score := run2( grid, program )

    // Pop any unfinished output.

	display(grid)

    return score   // 10776
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup("", live)
	if TEST {
		fmt.Println("No test for this one.")
		return
	}
	for _, arg := range os.Args {
		IMAGE = IMAGE || (arg == "image")
		SLOW = SLOW || (arg == "slow")
	}

	program := tools.GetRowNumbers[int](input)

	fmt.Println("Part 1:", part1(program))
	fmt.Println("Part 2:", part2(program))
}
