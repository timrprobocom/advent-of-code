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
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11`[1:]

//go:embed day04.txt
var live string

func intersect[T comparable](m1 map[T]bool, m2 map[T]bool) map[T]bool {
	newx := make(map[T]bool)
	for k := range m1 {
		if m2[k] {
			newx[k] = true
		}
	}
	return newx
}

func wins(row string) int {
	phase := 0
	wins := make(map[int]bool)
	mine := make(map[int]bool)
	for _, w := range strings.Split(row, " ") {
		if len(w) == 0 {
			continue
		} else if w[len(w)-1] == ':' {
			phase = 1
		} else if w == "|" {
			phase = 2
		} else if phase == 1 {
			wins[tools.StrToInt(w)] = true
		} else if phase == 2 {
			mine[tools.StrToInt(w)] = true
		}
	}
	return len(intersect(mine, wins))
}

func part1(data []string) int {
	sum := 0
	for _, row := range data {
		cnt := wins(row)
		if cnt > 0 {
			sum += 1 << (cnt - 1)
		}
	}
	return sum
}

func part2(data []string) int {
	sum := 0
	copies := tools.Repeat(1, len(data))
	for _, row := range data {
		this := copies[0]
		copies = copies[1:]
		sum += this

		for j := range wins(row) {
			copies[j] += this
		}
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
