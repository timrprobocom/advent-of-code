package main

import (
	"fmt"
	"strings"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000`[1:]

//go:embed day01.txt
var live string


func part1(data []string) int {
	accum := 0
	maxx := 0
	for _, line := range data {
		if len(line) == 0 {
			maxx = max(maxx, accum)
			accum = 0
		} else {
			accum += tools.StrToInt(line)
		}
	}
	return maxx
}


func part2(data []string) int {
	accum := []int{0}
	for _, line := range data {
		if len(line) == 0 {
			accum = append( accum, 0 )
		} else {
			accum[len(accum)-1] += tools.StrToInt(line)
		}
	}
	slices.Sort(accum);
	return accum[len(accum)-3]+accum[len(accum)-2]+accum[len(accum)-1]
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
