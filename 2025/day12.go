package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2`[1:]

//go:embed day12.txt
var live string

func part1(data [][]int) int {
	count := 0
	for _, row := range data {
		if len(row) < 2 {
			continue
		}
		need := tools.Sum(row[2:]) * 8
		if need < row[0]*row[1] {
			count++
		}
	}
	return count
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.GetNumbers[int](input)
	fmt.Println("Part 1:", part1(data))
}
