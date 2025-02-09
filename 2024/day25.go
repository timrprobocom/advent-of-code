package main

import (
	"fmt"
	"strconv"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####`[1:]

//go:embed day25.txt
var live string

func tobinary(pat string) int64 {
	val, _ := strconv.ParseInt(pat, 2, 64)
	return val
}

func part1(locks, keys []int64) int {
	sum := 0
	for _, k := range keys {
		for _, l := range locks {
			if l&k == 0 {
				sum++
			}
		}
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	input = strings.ReplaceAll(strings.ReplaceAll(input, "#", "1"), ".", "0")

	// Convert the input into locks and keys.

	var locks []int64
	var keys []int64
	for _, chunk := range strings.Split(input, "\n\n") {
		if chunk[0] == '0' {
			keys = append(keys, tobinary(strings.ReplaceAll(chunk, "\n", "")))
		} else {
			locks = append(locks, tobinary(strings.ReplaceAll(chunk, "\n", "")))
		}
	}

	// Any #/# invalidates.

	fmt.Println("Part 1:", part1(locks, keys))
}
