package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day01.txt
var live string

func fuel1(mass int, sum int) int {
	return mass/3 - 2
}

func part1( data []int ) int {
	return tools.Sum(data)
}

func part2( data []int ) int {
	cnts := make(map[int]bool)
	found := -1
	sum := 0
	for found < 0 {
		for _,num := range data {
			sum += num
			if cnts[sum] {
				found = sum
				break
			}
			cnts[sum] = true
		}
	}
	return found
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(live, live)

    data := tools.GetRowNumbers[int](input)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
