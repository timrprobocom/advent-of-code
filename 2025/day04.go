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
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.`[1:]

//go:embed day04.txt
var live string

type Point = tools.Point

type PointSet = map[Point]bool

var directions []Point = []Point{{-1, -1}, {-1, 0}, {-1, 1}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1}}

func makeset(grid []string) PointSet {
	rolls := make(PointSet)
	for y, row := range grid {
		for x, col := range row {
			if col == '@' {
				rolls[Point{x, y}] = true
			}
		}
	}
	return rolls
}

func part1(rolls PointSet) int {
	total := 0
	for pt := range rolls {
		count := 0
		for _, dpt := range directions {
			if rolls[pt.Add(dpt)] {
				count += 1
			}
		}
		if count < 4 {
			total++
		}
	}
	return total
}

func part2(rolls PointSet) int {
	removed := 0
	for true {
		nrolls := make(PointSet)
		for pt := range rolls {
			count := 0
			for _, dpt := range directions {
				if rolls[pt.Add(dpt)] {
					count += 1
				}
			}
			if count >= 4 {
				nrolls[pt] = true
			}
		}
		if len(rolls) == len(nrolls) {
			break
		}
		removed += len(rolls) - len(nrolls)
		rolls = nrolls
	}
	return removed
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := makeset(strings.Split(input, "\n"))

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
