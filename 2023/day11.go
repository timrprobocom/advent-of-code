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
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....`[1:]

//go:embed day11.txt
var live string

type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) addi(dx int, dy int) Point {
	return Point{pt.x + dx, pt.y + dy}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}

func (pt Point) left() Point {
	return Point{pt.y, -pt.x}
}

func (pt Point) right() Point {
	return Point{-pt.y, pt.x}
}

func manhattan(pt1, pt2 Point) int {
	return tools.AbsInt(pt2.x-pt1.x) + tools.AbsInt(pt2.y-pt1.y)
}

var nogrow map[int]bool
var nogcol map[int]bool

func expand(data []string, delta int) []Point {
	stars := []Point{}
	dy := 0
	for y, row := range data {
		if nogrow[y] {
			dy += delta
			continue
		}
		dx := 0
		for x, col := range row {
			if nogcol[x] {
				dx += delta
			} else if col == '#' {
				stars = append(stars, Point{x + dx, y + dy})
			}
		}
	}
	return stars
}

func part1(data []string, delta int) int {
	stars := expand(data, delta-1)
	mandist := 0
	for i := 0; i < len(stars)-1; i++ {
		for j := i; j < len(stars); j++ {
			mandist += manhattan(stars[i], stars[j])
		}
	}
	return mandist
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	// Find the rows without galaxies.

	nogrow = make(map[int]bool)
	for n, row := range data {
		if !strings.Contains(row, "#") {
			nogrow[n] = true
		}
	}

	// Find the columns without galaxies.

	counts := tools.Repeat(0, len(data[0]))
	for _, row := range data {
		for n, col := range row {
			if col == '#' {
				counts[n] += 1
			}
		}
	}

	nogcol = make(map[int]bool)
	for n, val := range counts {
		if val == 0 {
			nogcol[n] = true
		}
	}

	fmt.Println("Part 1:", part1(data, 2))
	if TEST {
		fmt.Println("Test 10:", part1(data, 10))
		fmt.Println("Test 100:", part1(data, 100))
	}
	fmt.Println("Part 2:", part1(data, 1000000))
}
