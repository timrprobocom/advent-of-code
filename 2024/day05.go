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
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47`[1:]

//go:embed day05.txt
var live string

var before map[int][]int

func compare(a int, b int) int {
	if a == b {
		return 0
	}
	idx := slices.IndexFunc(before[a], func(c int) bool { return c == b })
	if idx > 0 {
		idx = 1
	}
	return idx
}

func part1(cases [][]int) (int, int) {
	sum1 := 0
	sum2 := 0

	for _, casex := range cases {
		order := slices.Clone(casex)
		slices.SortFunc(order, compare)
		if slices.Equal(order, casex) {
			sum1 += casex[len(casex)/2]
		} else {
			sum2 += order[len(order)/2]
		}
	}
	return sum1, sum2
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(input, "\n")
	var cases [][]int
	before = make(map[int][]int)

	for _, row := range data {
		if len(row) == 0 {
			continue
		}
		if row[2] == '|' {
			words := strings.Split(row, "|")
			a, _ := strconv.Atoi(words[0])
			b, _ := strconv.Atoi(words[1])
			before[b] = append(before[b], a)
		} else {
			var newcase []int
			for _, w := range strings.Split(row, ",") {
				a, _ := strconv.Atoi(w)
				newcase = append(newcase, a)
			}
			cases = append(cases, newcase)
		}
	}

	sum1, sum2 := part1(cases)
	fmt.Println("Part 1:", sum1)
	fmt.Println("Part 2:", sum2)
}
