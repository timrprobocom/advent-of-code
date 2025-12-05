package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
3-5
10-14
16-20
12-18

1
5
8
11
17
32`[1:]

//go:embed day05.txt
var live string

func part1(ranges [][]int, codes []int) int {
	count := 0
	for _, c := range codes {
		for _, r := range ranges {
			if r[0] <= c && c <= r[1] {
				count += 1
				break
			}
		}
	}
	return count
}

func part2(ranges [][]int) int {
	slices.SortFunc(ranges, func(a, b []int) int {
		return a[0] - b[0]
	})
	total := 0
	high := 0
	for _, r := range ranges {
		if high < r[0] {
			total += r[1] - r[0] + 1
			high = r[1] + 1
		} else if high <= r[1] {
			total += r[1] - high + 1
			high = r[1] + 1
		}
	}
	return total
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	var ranges [][]int
	var codes []int

	for _, line := range strings.Split(input, "\n") {
		if len(line) == 0 {
			continue
		}
		var parts []int
		for _, p := range strings.Split(line, "-") {
			parts = append(parts, tools.StrToInt(p))
		}
		if len(parts) == 1 {
			codes = append(codes, parts[0])
		} else {
			ranges = append(ranges, parts)
		}
	}
	if DEBUG {
		fmt.Println(codes)
		fmt.Println(ranges)
	}

	fmt.Println("Part 1:", part1(ranges, codes))
	fmt.Println("Part 2:", part2(ranges))
}
