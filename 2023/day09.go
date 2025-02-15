package main

import (
	"fmt"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45`[1:]

//go:embed day09.txt
var live string

func allequal(row []int) bool {
	for i := 0; i < len(row)-1; i++ {
		if row[i] != row[i+1] {
			return false
		}
	}
	return true
}

func part1(part int, data [][]int) int {
	sum := 0
	for _, row := range data {
		stack := [][]int{row}

		// Determine differences.

		for !allequal(row) {
			var newrow []int
			for i := 0; i < len(row)-1; i++ {
				newrow = append(newrow, row[i+1]-row[i])
			}
			row = newrow
			stack = append(stack, row)
		}

		slices.Reverse(stack)
		incr := 0
		for _, row := range stack {
			if part == 1 {
				incr = row[len(row)-1] + incr
			} else {
				incr = row[0] - incr
			}
		}
		sum += incr
	}

	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.GetNumbers[int](input)

	fmt.Println("Part 1:", part1(1, data))
	fmt.Println("Part 2:", part1(2, data))
}
