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
987654321111111
811111111111119
234234234234278
818181911112111`[1:]

//go:embed day03.txt
var live string

func part2(data []string, n int) int {
	count := 0
	for _, line := range data {
		row := []rune(line)

		// In each loop, we take the largest number that still leave enough room.

		var poss []rune
		ix := 0
		for len(poss) < n {
			px := n - len(poss)
			m := slices.Max(row[ix : len(row)-px+1])
			poss = append(poss, m)
			ix = slices.Index(row[ix:], m) + ix + 1
		}

		count += tools.StrToInt(string(poss))
		if DEBUG {
			fmt.Println(row, poss)
		}
	}
	return count
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part2(data, 2))
	fmt.Println("Part 2:", part2(data, 12))
}
