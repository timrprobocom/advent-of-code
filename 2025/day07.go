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
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............`[1:]

//go:embed day07.txt
var live string

func part1(data []string) (int, int) {
	beams := make(map[int]int)
	count := 0
	for _, row := range data {
		c := strings.Index(row, "S")
		if c >= 0 {
			beams[c] = 1
			continue
		}
		nbeams := make(map[int]int)
		for i, c := range beams {
			if row[i] == '.' {
				nbeams[i] += c
			} else {
				count++
				if i > 0 {
					nbeams[i-1] += c
				}
				if i < len(row)-1 {
					nbeams[i+1] += c
				}
			}
		}
		beams = nbeams
		if DEBUG {
			fmt.Println(row, beams)
		}
	}
	return count, tools.Sum(tools.Values(beams))
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	p1, p2 := part1(data)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}
