package main

import (
	"fmt"
	"os"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG = false
var TEST = false
var IMAGE = false

var test = ""

//go:embed day15.txt
var live string

// Inputs:
//   1
// 3   4
//   2
//
// Responses:
//   0 = wall ahead
//   1 = moved
//   2 = found home

// start position

// so, at every position:
// Try 1, 2, 3, 4

type Point = tools.Point

var movement = []Point{ Point{0,0}, Point{0,-1},Point{0,1},Point{-1,0},Point{1,0} }
var nextleft  = []int{ 0, 3, 4, 2, 1 }
var nextright = []int{ 0, 4, 3, 1, 2 }
var opposite  = []int{ 0, 2, 1, 4, 3 }


func printmap( walls map[Point]bool, position Point, target Point ) {
	if !IMAGE {
		return
	}
	if len(walls) == 0 {
		return
	}

	// Estblish the bounds.

	xmin := position.X
	xmax := position.X
	ymin := position.Y
	ymax := position.Y
	for pt,_ := range walls {
		xmin = min(xmin, pt.X)
		xmax = min(xmax, pt.X)
		ymin = min(ymin, pt.Y)
		ymin = min(ymax, pt.Y)
	}

	// Create empty grid

	grid := make([][]byte, ymax-ymin)
	for y := ymin; y < ymax; y++ {
		grid[y] = []byte(strings.Repeat(" ", xmax-xmin))
	}

	// Fill in the walls.

	for w,_ := range walls {
		grid[w.Y-ymin][w.X-xmin] = '#'
	}

	// Fill in the base, the droid, and the oxygen.

	/*
	// ??? what is this doing?  What's a "base"?
	grid[-ymin][-xmin] = '@'
	*/
	grid[position.Y-ymin][position.X-xmin] = 'D'
	if target.X != 0 || target.Y != 0 {
		grid[target.Y-ymin][target.X-ymin] = '$'
	}
	for _,row := range grid {
		fmt.Println( string(row) )
	}
}


func run( program []int ) ( map[Point]bool, Point ) {
	pgm := tools.MakeProgram( program )
	position := Point{0,0}
	dir := 1
	pgm.Push( dir )
	walls := make(map[Point]bool)
	target := Point{0,0}
	base := Point{0,0}
	count := 0

	facing := position.Add(movement[dir])

    // We follow the left-hand rule.

	go pgm.Run()

	for pgm.IsAlive() {

        // Get the next result.  If 0, mark a wall, and turn right.
        // Otherwise, turn left.

		code := pgm.Pop()
		count ++
        if code == 0 {
            walls[facing] = true 
            dir = nextright[dir]
        } else {
            position = facing
            dir = nextleft[dir]
            if code == 2 {
                target = facing
			}
		}

        if IMAGE {
            fmt.Println( "Iteration", count )
            printmap( walls, position, target )
		}

        // We're done when return to base (after leaving base).

        if count > 4 && position == base {
            pgm.Push( 5 )
			continue
		}

        // This is the cell we are facing.

        facing = position.Add(movement[dir])
		pgm.Push( dir )
	}
	return walls, target
}
		

// Now, given the maze, we can do a breadth-first search for the oxygen.

// We track a visited list.  From each point, add all the points we can visit
// that haven't been visited.  When we reach the oxygen, we win.

func process( walls map[Point]bool, start Point, target Point ) int {
    visited := make(map[Point]bool)
    upcoming := []Point{start}
    step := -1

	for len(upcoming) > 0 {
        step ++
        more := []Point{}
        for _,cur := range upcoming {
            if (target.X != 0 || target.Y != 0) && cur == target {
                return step
			}
            visited[cur] = true
			for dir := 1; dir <= 4; dir++ {
                facing := cur.Add(movement[dir])
				if !walls[facing] && !visited[facing] {
					more = append( more, facing )
				}
			}
		}
        upcoming = more
	}

    // This comes out one step too large because we count the final
    // step that actually produces nothing.

    return step
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
	}

    // Run the program to produce the maze.

	program := tools.GetRowNumbers[int](input)
	walls, target := run( program )

	fmt.Println( "Part 1:", process(walls, Point{0,0}, target) )
	fmt.Println( "Part 2:", process(walls, target, Point{0,0}) )
}



