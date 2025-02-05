package main

import (
	"fmt"
	"strconv"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20`[1:]

//go:embed day07.txt
var live string

// Yes, I use a goto here.  I need to break out of three levels of for loop.
// It can be done with extra "if win", but this reads OK.

func part1(data [][]int) int64 {
	var sumx int64 = 0
	for _, row := range data {
		var k int64 = -1
		win := false
		var maybe []int64
		for _, v0 := range row {
			v1 := int64(v0)
			if k < 0 {
				k = v1
			} else if len(maybe) == 0 {
				maybe = append(maybe, v1)
			} else {
				var next []int64
				for _, m := range maybe {
					p := m + v1
					win = p == k
					if win {
						goto win
					}
					next = append(next, p)

					p = m * v1
					win = p == k
					if win {
						goto win
					}
					next = append(next, p)
				}
				maybe = next
			}
		}
	win:
		if win {
			sumx += k
		}
	}
	return sumx
}

func part2(data [][]int) int64 {
	var sumx int64 = 0
	for _, row := range data {
		var k int64 = -1
		win := false
		var maybe []int64
		for _, v0 := range row {
			v1 := int64(v0)
			if k < 0 {
				k = v1
			} else if len(maybe) == 0 {
				maybe = append(maybe, v1)
			} else {
				var next []int64
				for _, m := range maybe {
					p := m + v1
					win = p == k
					if win {
						goto win
					}
					next = append(next, p)

					p = m * v1
					win = p == k
					if win {
						goto win
					}
					next = append(next, p)

					p, _ = strconv.ParseInt(strconv.FormatInt(m, 10)+strconv.FormatInt(v1, 10), 10, 0)
					win = p == k
					if win {
						goto win
					}
					next = append(next, p)
				}
				maybe = next
			}
		}
	win:
		if win {
			sumx += k
		}
	}
	return sumx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.Parse(input)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
