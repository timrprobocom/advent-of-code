package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day04.txt
var live string

var test = `
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8`[1:]

// Is one completely contained within the other?

func part1(data [][]int) int {
    total := 0
	for _,row := range data {
		if row[0] <= row[2] && row[1] >= row[3] ||
			row[2] <= row[0] && row[3] >= row[1] {
			total += 1
		}
	}
    return total
}

// Is there any overlap at all?

func part2(data [][]int) int {
    total := 0
	for _,row := range data {
		if row[2] >= row[0] && row[2] <= row[1] ||
			row[0] >= row[2] && row[0] <= row[3] {
			total += 1
		}
	}
    return total
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	input = strings.ReplaceAll(input, "-", ",")
	data := tools.GetNumbers[int](input)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
