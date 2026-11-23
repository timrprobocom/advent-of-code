package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG = false
var TEST = false
var IMAGE = false

var test = ""

//go:embed day17.txt
var live string

type Point = tools.Point


func printmap(walls map[Point]bool, position Point, target Point) {
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
	for pt, _ := range walls {
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

	for w, _ := range walls {
		grid[w.Y-ymin][w.X-xmin] = '#'
	}

	// Fill in the base, the droid, and the oxygen.

	grid[-ymin][-xmin] = '@'
	grid[position.Y-ymin][position.X-xmin] = 'D'
	if target.X != 0 || target.Y != 0 {
		grid[target.Y-ymin][target.X-ymin] = '$'
	}
	for _, row := range grid {
		fmt.Println(string(row))
	}
}

var WIDTH int
var HEIGHT int

func run(program []int) []string {
	pgm := tools.MakeProgram(program)
	s := ""

	go pgm.Run()

	for pgm.IsAlive() {
		code := pgm.Pop()
		s += string(byte(code))
	}

	for _,code := range pgm.Dump() {
		s += string(byte(code))
	}

	maze := strings.Split(strings.TrimSpace(s),"\n")
	WIDTH = len(maze[0])
	HEIGHT = len(maze)

	return maze
}

func getpt( maze []string, pt Point ) byte {
	if !tools.Between( 0, pt.X, WIDTH) || !tools.Between( 0, pt.Y, HEIGHT) {
		return '.'
	}
	return maze[pt.Y][pt.X]
}

func part1( maze []string ) int {
    // Find the robot.

    robot := Point{strings.Index(maze[HEIGHT-1], "^"), HEIGHT-1}
    lastturn := robot

    // Robot starts facing north.

    facing := Point{0,-1}

    crossings := make(map[Point]bool)
    turns := ""
    for true {
        //  If we are facing empty space, turn.
        if getpt(maze, robot.Add(facing)) == '.' {
            if robot != lastturn {
                turns += fmt.Sprintf("%d", tools.Mandist(robot,lastturn) )
			}
            if getpt(maze, robot.Add(facing.Left())) == '#' {
                facing = facing.Left()
                turns += "L"
            } else if getpt(maze, robot.Add(facing.Right())) == '#' {
                facing = facing.Right()
                turns += "R"
            } else {
                // End of the scaffold.
                break
			}
            lastturn = robot
            robot = robot.Add(facing)

        // Otherwise, look for a crossing.
        } else {
			if getpt(maze, robot.Add(facing.Left())) == '#' && getpt(maze, robot.Add(facing.Right())) == '#' {
                crossings[robot] = true
			}
            robot = robot.Add(facing)
		}

        if DEBUG {
           fmt.Println( robot )
			fmt.Println( string(turns) )
		}
	}
    // We return the set of crossings and the record of turns.

    sum := 0
	for pt,_ := range crossings {
		sum += pt.X * pt.Y
	}
	return sum
}

func part2( program []int ) int {
	program[0] = 2
    pgm := tools.MakeProgram(program)

    instructions := []string{
        "A,B,A,C,C,A,B,C,B,B\n",
        "L,8,R,10,L,8,R,8\n",
        "L,12,R,8,R,8\n",
        "L,8,R,6,R,6,R,10,L,8\n",
        "n\n",
    }
    go pgm.Run()
	for _,ln := range instructions {
		for _,c := range ln {
			pgm.Push( int(c) )
		}
	}
    d := pgm.Dump()
	s := ""
	for _,ch := range d[:len(d)-1] {
		s += string(byte(ch))
	}
	if DEBUG {
		fmt.Println(s)
	}
    return d[len(d)-1]
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup("", live)
	if TEST {
		fmt.Println("No test for this one.")
		return
	}

	// Run the program to produce the maze.

	program := tools.GetRowNumbers[int](input)
	maze := run(program)

	fmt.Println("Part 1:", part1(maze))
	fmt.Println("Part 2:", part2(program))
}


