package main

import (
	"fmt"
	"slices"
	"strconv"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL`[1:]

// BFFFBBFRRR: row 70, column 7, seat ID 567.
// FFFBBBFRRR: row 14, column 7, seat ID 119.
// BBFFBBFRLL: row 102, column 4, seat ID 820.

//go:embed day05.txt
var live string


func mapper(c rune) rune {
	if c == 'B' || c == 'R' {
		return '1'
	} else if c == 'F' || c == 'L' {
		return '0'
	}
	return 'X'
}

func xlate(n string) int {
	t := strings.Map( mapper, n)
	v,_ := strconv.ParseInt(t, 2, 64)
	return int(v)
}


func part1(data []int) int {
    return tools.Max(data)
}


func part2(data []int) int {
	slices.Sort(data)

	last := 0
	for _, i := range data {
		if last > 0 && i != last+1 {
			return i - 1
		}
		last = i
	}

    return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := []int{}
	for _,line := range strings.Split(strings.TrimSpace(input), "\n") {
		data = append(data, xlate(line))
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
