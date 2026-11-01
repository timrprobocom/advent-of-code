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
199
200
208
210
200
207
240
269
260
263`[1:]

//go:embed day01.txt
var live string


func part1(data []int) int {
	accum := 0
	for i := range len(data)-1 {
		if data[i+1] > data[i] {
			accum ++
		}
	}
	return accum
}


func part2(data []int) int {
	accum := 0
	for i := range len(data)-3 {
		if data[i+3] > data[i] {
			accum ++
		}
	}
	return accum
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := []int{}
	for _,row := range strings.Fields(input) {
		data = append(data, tools.StrToInt(row))
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
