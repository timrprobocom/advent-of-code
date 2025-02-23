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
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732`[1:]

//go:embed day10.txt
var live string

var WIDTH = -1
var HEIGHT = -1

type Point = tools.Point

func part1(data [][]int) (int, int) {
	// Find the zeros.
	var zeros []Point
	for y, row := range data {
		for x, c := range row {
			if c == 0 {
				zeros = append(zeros, Point{x, y})
			}
		}
	}

	type Entry struct {
		pt   Point
		cost int
	}

	directions := []Point{{-1, 0}, {0, -1}, {0, 1}, {1, 0}}

	var queue []Entry
	part1 := 0
	part2 := 0
	for _, zpt := range zeros {
		queue = append(queue, Entry{zpt, 0})
		solutions := make(map[Point]bool)
		for len(queue) > 0 {
			next := queue[0]
			queue = queue[1:]
			c := next.cost + 1
			for _, dxy := range directions {
				pxy := next.pt.Add(dxy)
				if pxy.InRange(WIDTH, HEIGHT) && data[pxy.Y][pxy.X] == c {
					if c == 9 {
						part2++
						solutions[pxy] = true
					} else {
						queue = append(queue, Entry{pxy, c})
					}
				}
			}
		}
		part1 += len(solutions)
	}
	return part1, part2
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	var data [][]int
	for _, line := range strings.Split(input, "\n") {
		var row []int
		for _, c := range line {
			row = append(row, int(byte(c)-'0'))
		}
		data = append(data, row)
	}

	WIDTH = len(data[0])
	HEIGHT = len(data)

	p1, p2 := part1(data)

	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}
