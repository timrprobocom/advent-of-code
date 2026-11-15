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
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12`[1:]

var test2 = `
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9`[1:]

//go:embed day16.txt
var live string

type SeatSet [1000]int8

// rules should be a map of string to 4 ints
// mytix is a list of int
// nearby is a list of list of int

func parse(chunks []string) (map[string]SeatSet, []int, [][]int) {
	// There are three parts to the input.

	rules := make(map[string]SeatSet)
	for _, line := range strings.Split(chunks[0], "\n") {
		keyword, rest, _ := strings.Cut(line, ": ")
		parts := strings.Fields(rest)
		i := strings.IndexByte(parts[0], '-')
		i1 := tools.StrToInt(parts[0][:i])
		i2 := tools.StrToInt(parts[0][i+1:])
		i = strings.IndexByte(parts[2], '-')
		j1 := tools.StrToInt(parts[2][:i])
		j2 := tools.StrToInt(parts[2][i+1:])
		// Let's make an array of 1000 int8s.
		var seats SeatSet
		for i = i1; i <= i2; i++ {
			seats[i] = 1
		}
		for i = j1; i <= j2; i++ {
			seats[i] = 1
		}
		rules[keyword] = seats
	}

	// Now my ticket.
	mytix := tools.GetNumbers[int](chunks[1])[1]

	// Now nearby tickets.
	nearby := tools.GetNumbers[int](chunks[2])[1:]
	return rules, mytix, nearby
}

func makevalid(rules map[string]SeatSet) SeatSet {
	// Combine all ranges.
	var seats SeatSet
	for _, v := range rules {
		for i := range 1000 {
			seats[i] += v[i]
		}
	}
	return seats
}

func part1(rules map[string]SeatSet, nearby [][]int) int {
	valid := makevalid(rules)
	sum := 0
	for _, tix := range nearby {
		for _, t := range tix {
			if valid[t] == 0 {
				sum += t
			}
		}
	}

	return sum
}

// OK, we have N fields.
// We need to know which fields each can be.

func part2(rules map[string]SeatSet, mytix []int, nearby [][]int) int {
	possible := make(map[string][]int)
	for k, _ := range rules {
		possible[k] = tools.Repeat(1, len(rules))
	}
	if DEBUG {
		fmt.Println(possible)
	}

	valid := makevalid(rules)

	for _, tix := range nearby {
		whole := 1
		for _, t := range tix {
			whole *= int(valid[t])
		}
		if whole == 0 {
			continue
		}
		for name, valid := range rules {
			for i, t := range tix {
				if possible[name][i] > 0 && valid[t] == 0 {
					possible[name][i] = 0
				}
			}
		}
	}

	// Pull out the certains.  It takes 7 passes for the full list.
	// The "possible" lists have about 20 elements, so Index is way
	// quicker than a map.

	certain := make(map[string]int)
	removed := true
	for removed {
		removed = false
		for k, poss := range possible {
			if tools.Sum(poss) == 1 && certain[k] == 0 {
				value := slices.Index(poss, 1)
				certain[k] = value
				for k1, poss1 := range possible {
					if k != k1 && poss1[value] > 0 {
						removed = true
						poss1[value] = 0
					}
				}
			}
		}
	}

	if DEBUG {
		fmt.Println("Final:", possible)
	}

	factor := 1
	for k, value := range certain {
		if DEBUG {
			fmt.Println(k, value)
		}
		if tools.StartsWith(k, "departure") {
			factor *= mytix[value]
		}
	}
	return factor
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	rules, mytix, nearby := parse(strings.Split(input, "\n\n"))

	fmt.Println("Part 1:", part1(rules, nearby))
	fmt.Println("Part 2:", part2(rules, mytix, nearby))
}
