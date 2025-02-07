package main

import (
	"fmt"
)

import _ "embed"

import "aoc/tools"

var DEBUG bool = false
var TEST bool = false

var test = `
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`[1:]

//go:embed day02.txt
var live string

func is_safe(row []int) bool {
	for i := 0; i < len(row)-1; i++ {
		x := row[i]
		y := row[i+1]
		if (y-x)*(row[1]-row[0]) < 0 {
			return false
		}
		if tools.AbsInt(y-x) < 1 || tools.AbsInt(y-x) > 3 {
			return false
		}
	}
	return true
}

func part1(data [][]int) int {
	sumx := 0
	for _, row := range data {
		if is_safe(row) {
			sumx++
		}
	}
	return sumx
}

func part2(data [][]int) int {
	safe := 0
	for _, row := range data {
		if is_safe(row) {
			safe++
		} else {
			for i := 0; i < len(row); i++ {
				if is_safe(tools.Remove(row, i)) {
					safe++
					break
				}
			}
		}
	}
	return safe
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := tools.Parse[int](input)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
