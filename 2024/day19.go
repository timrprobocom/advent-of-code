package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb`[1:]

//go:embed day19.txt
var live string

var towels []string

func possible(need, sofar string) bool {
	if need == sofar {
		return true
	}

	for _, t := range towels {
		if strings.HasPrefix(need, sofar+t) && possible(need, sofar+t) {
			return true
		}
	}

	return false
}

func part1(needs []string) int {
	sum := 0
	for _, need := range needs {
		if possible(need, "") {
			sum++
		}
	}
	return sum
}

type Cache struct {
	need  string
	sofar string
}

var cache map[Cache]int
var hits int = 0

func howmany(need, sofar string) int {
	c := Cache{need, sofar}
	if cache[c] > 0 {
		hits++
		return cache[c]
	}

	if need == sofar {
		return 1
	}

	sum := 0
	for _, t := range towels {
		if strings.HasPrefix(need, sofar+t) {
			sum += howmany(need, sofar+t)
		}
	}

	cache[c] = sum
	return sum
}

func part2(needs []string) int {
	sum := 0
	for _, need := range needs {
		sum += howmany(need, "")
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	parts := strings.Split(input, "\n\n")
	towels = strings.Split(parts[0], ", ")
	needs := strings.Split(parts[1], "\n")
	cache = make(map[Cache]int)

	fmt.Println("Part 1:", part1(needs))
	fmt.Println("Part 2:", part2(needs))
	if DEBUG {
		fmt.Println("Cache:", len(cache), "hits", hits)
	}
}
