package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
.#.
..#
###`[1:]

//go:embed day17.txt
var live string

type Node struct {
	x int
	y int
	z int
	w int
}

type Grid = map[Node]bool

func (self Node) add(other Node) Node {
	return Node{
		self.x + other.x,
		self.y + other.y,
		self.z + other.z,
		self.w + other.w,
	}
}

var adjacent []Node

func translate(data []string) Grid {
	grid := make(Grid)
	for y, ln := range data {
		for x, c := range ln {
			if c == '#' {
				grid[Node{x, y, 0, 0}] = true
			}
		}
	}
	return grid
}

func countneighbors(cell Node, state map[Node]bool) int {
	sum := 0
	for _, delta := range adjacent {
		if state[cell.add(delta)] {
			sum++
		}
	}
	return sum
}

func minmax(state Grid) (Node, Node) {
	mins := Node{99, 99, 99, 99}
	maxs := Node{-99, -99, -99, -99}
	for k, _ := range state {
		mins.x = min(mins.x, k.x)
		mins.y = min(mins.y, k.y)
		mins.z = min(mins.z, k.z)
		mins.w = min(mins.w, k.w)
		maxs.x = max(maxs.x, k.x)
		maxs.y = max(maxs.y, k.y)
		maxs.z = max(maxs.z, k.z)
		maxs.w = max(maxs.w, k.w)
	}
	return mins, maxs
}

func printgrid(state Grid) {
	mins, maxs := minmax(state)
	for z := mins.z; z <= maxs.z; z++ {
		fmt.Println("Layer", z)
		for y := mins.y; y <= maxs.y; y++ {
			line := []byte(strings.Repeat(".", maxs.x-mins.x+1))
			for x := mins.x; x <= maxs.x; x++ {
				if state[Node{x, y, z, 0}] {
					line[x-mins.x] = '#'
				}
			}
			fmt.Println(string(line))
		}
	}
}

func nextstate(state Grid, part int) Grid {
	mins, maxs := minmax(state)
	wlow := 0
	whigh := 0
	if part == 2 {
		wlow = mins.w - 1
		whigh = maxs.w + 1
	}

	newgrid := make(Grid)
	for w := wlow; w <= whigh; w++ {
		for z := mins.z - 1; z <= maxs.z+1; z++ {
			for y := mins.y - 1; y <= maxs.y+1; y++ {
				for x := mins.x - 1; x <= maxs.x+1; x++ {
					cell := Node{x, y, z, w}
					neighbors := countneighbors(cell, state)
					if neighbors == 3 || (state[cell] && neighbors == 2) {
						newgrid[cell] = true
					}
				}
			}
		}
	}
	return newgrid
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n")

	for x := -1; x < 2; x++ {
		for y := -1; y < 2; y++ {
			for z := -1; z < 2; z++ {
				for w := -1; w < 2; w++ {
					if x != 0 || y != 0 || z != 0 || w != 0 {
						adjacent = append(adjacent, Node{x, y, z, w})
					}
				}
			}
		}
	}

	state := translate(data)
	if DEBUG {
		printgrid(state)
	}
	for range 6 {
		state = nextstate(state, 1)
		if DEBUG {
			printgrid(state)
		}
	}

	fmt.Println("Part 1:", len(state))

	state = translate(data)
	for range 6 {
		state = nextstate(state, 2)
	}

	fmt.Println("Part 2:", len(state))
}
