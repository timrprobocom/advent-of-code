package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
	"gonum.org/v1/gonum/stat"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3`[1:]

//go:embed day14.txt
var live string

var WIDTH int = -1
var HEIGHT int = -1

func printgrid(data [][]int) {
	grid := make([][]byte, HEIGHT)
	for y := 0; y < HEIGHT; y++ {
		grid[y] = make([]byte, WIDTH)
	}

	for _, bot := range data {
		grid[bot[1]][bot[0]]++
	}

	for _, row := range grid {
		var s string
		for _, c := range row {
			s += string(".1234"[c])
		}
		fmt.Println(s)
	}
}

func move(data [][]int) {
	for _, row := range data {
		row[0] = (row[0] + row[2] + WIDTH) % WIDTH
		row[1] = (row[1] + row[3] + HEIGHT) % HEIGHT
	}
}

// The tree is solid, so the standard deviation of the coordinates goes WAY down.
// Tpyical is 30, tree gets 19.

func detect_tree(data [][]int) bool {
	var x []float64
	var y []float64
	for _, bot := range data {
		x = append(x, float64(bot[0]))
		y = append(y, float64(bot[1]))
	}
	stx := stat.StdDev(x, nil)
	sty := stat.StdDev(y, nil)
	return stx < 20 && sty < 20 
}

func part1(data [][]int) int {
	for range 100 {
		move(data)
	}

	hw := WIDTH / 2
	hh := HEIGHT / 2
	k1, k2, k3, k4 := 0, 0, 0, 0

	for _, bot := range data {
		if bot[0] < hw && bot[1] < hh {
			k1++
		}
		if bot[0] > hw && bot[1] < hh {
			k2++
		}
		if bot[0] < hw && bot[1] > hh {
			k3++
		}
		if bot[0] > hw && bot[1] > hh {
			k4++
		}
	}
	return k1 * k2 * k3 * k4
}

func part2(data [][]int) int {
	var i int
	for i = 100; i < 10000; i++ {
		move(data)
		if detect_tree(data) {
			if DEBUG {
				printgrid(data)
			}
			break
		}
	}
	return i + 1
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.GetNumbers[int](input)

	if TEST {
		WIDTH = 7
		HEIGHT = 11
	} else {
		WIDTH = 101
		HEIGHT = 103
	}

	if DEBUG {
		printgrid(data)
	}

	fmt.Println("Part 1:", part1(data))
	if !TEST {
		fmt.Println("Part 2:", part2(data))
	}
}
