package main

import (
	"fmt"
	"os"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var IMAGE = false

var test = ""

//go:embed day11.txt
var live string

type Point = tools.Point

// NWSE
var directions = []Point{Point{0, -1}, Point{-1, 0}, Point{0, 1}, Point{1, 0}}

// 0 is left, N -> W -> S -> E
// 1 is right, N -> E -> S -> W

type Grid = map[Point]bool

func run(live []int, base Point, blacks Grid, whites Grid) {
	pgm := tools.MakeProgramNo(live)
	loc := base
	facing := 0
	go pgm.Run()

	for pgm.IsAlive() {
		if whites[loc] {
			pgm.Push(1)
		} else {
			pgm.Push(0)
		}

		color := pgm.Pop()
		newdir := pgm.Pop()
		if DEBUG {
			fmt.Println("pop", color, newdir)
		}
		whites[loc] = color != 0
		blacks[loc] = color == 0
		facing = (facing + 1 + 2*newdir) % 4
		loc = loc.Add(directions[facing])
		if DEBUG {
			fmt.Println(facing, loc)
		}
	}
}

func bounds(blacks Grid, whites Grid) (int, int, int, int) {
	lowx := 9999
	lowy := 9999
	highx := -9999
	highy := -9999

	for k, _ := range blacks {
		lowx = min(lowx, k.X)
		lowy = min(lowy, k.Y)
		highx = max(highx, k.X)
		highy = max(highy, k.Y)
	}
	return lowx, lowy, highx, highy
}

func count(grid Grid) int {
	count := 0
	for _, v := range grid {
		if v {
			count++
		}
	}
	return count
}

func makeimage(blacks Grid, whites Grid, use string) string {
	lowx, lowy, highx, highy := bounds(blacks, whites)
	array := [][]byte{}
	for y := lowy; y <= highy; y++ {
		array = append(array, []byte(strings.Repeat(" ", highx-lowx+1)))
	}
	for pt, v := range blacks {
		if v {
			array[pt.Y-lowy][pt.X-lowx] = use[1]
		}
	}
	for pt, v := range whites {
		if v {
			array[pt.Y-lowy][pt.X-lowx] = use[0]
		}
	}
	str := ""
	for _, row := range array {
		if len(str) > 0 {
			str += "\n"
		}
		str += string(row)
	}
	return str
}

func part1(program []int) int {
	blacks := make(Grid)
	whites := make(Grid)
	run(program, Point{0, 0}, blacks, whites)

	if DEBUG {
		fmt.Println(count(blacks), count(whites))
	}

	if IMAGE {
		fmt.Println(makeimage(blacks, whites, "#."))
	}

	return count(blacks) + count(whites)
}

func part2(program []int) string {
	blacks := make(Grid)
	whites := make(Grid)
	whites[Point{0, 0}] = true
	run(program, Point{0, 0}, blacks, whites)
	if DEBUG {
		fmt.Println(count(blacks), count(whites))
	}

	return makeimage(blacks, whites, "X ")
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
	program := tools.GetRowNumbers[int](input)

	fmt.Println("Part 1:", part1(program))
	fmt.Println("Part 2:")
	fmt.Println(part2(program))
}
