package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
0
0
0
100756`[1:]

//go:embed day01.txt
var live string

func fuel1(mass int, sum int) int {
	return mass/3 - 2
}

func fuel2(mass int, sum int) int {
	f := fuel1(mass, 0)
	if f <= 0 {
		return sum
	}
	return fuel2(f, sum+f)
}

func part1( data []int, fuel func(int, int) int ) int {
	sum := 0
	for _,val := range data {
		if val > 0 {
			sum += fuel(val, 0)
		}
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

    data := tools.GetRowNumbers[int](input)

	fmt.Println("Part 1:", part1(data, fuel1))
	fmt.Println("Part 2:", part1(data, fuel2))
}
