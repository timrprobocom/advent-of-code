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
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  `[1:]

//go:embed day06.txt
var live string

// Prep for part 1 by transposing the matrix.

func transpose(data []string, ops []string) [][]int {
	cols := tools.Repeat([]int{}, len(ops))
	for _, line := range data {
		row := tools.SplitInt(line)
		for i := 0; i < len(row); i++ {
			cols[i] = append(cols[i], row[i])
		}
	}
	return cols
}

// Prep for part 2 by handling column by column.

func transform(data []string, ops []string) [][]int {
	ml := len(data[0])
	cols := [][]int{}
	col := []int{}
	for i := 0; i < ml; i++ {
		n := 0
		for _, line := range data {
			if line[i] != ' ' {
				n = n*10 + int(line[i]) - '0'
			}
		}
		if n > 0 {
			col = append(col, n)
		} else if len(col) > 0 {
			cols = append(cols, col)
			col = []int{}
		}
	}
	if len(col) > 0 {
		cols = append(cols, col)
	}
	return cols
}

func part2(nums [][]int, ops []string) int {
	result := 0
	for i := 0; i < len(ops); i++ {
		if ops[i] == "*" {
			result += tools.Prod(nums[i])
		} else {
			result += tools.Sum(nums[i])
		}
	}
	return result
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	ops := strings.Fields(data[len(data)-1])
	data = data[:len(data)-1]

	fmt.Println("Part 1:", part2(transpose(data, ops), ops))
	fmt.Println("Part 2:", part2(transform(data, ops), ops))
}
