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
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82`[1:]

//go:embed day01.txt
var live string

func part1(data []string) int {
	pos := 50
	count := 0
	for _, line := range data {
		v := tools.StrToInt(line[1:len(line)])
		if line[0] == 'L' {
			pos = (pos - v + 100) % 100
		} else {
			pos = (pos + v) % 100
		}
		if pos == 0 {
			count++
		}
		if DEBUG {
			fmt.Println(line, pos, count)
		}
	}
	return count
}

func part2(data []string) int {
	pos := 50
	count := 0
	for _, line := range data {
		v := tools.StrToInt(line[1:len(line)])
		if line[0] == 'L' {
			if pos == 0 {
				count--
			}
			pos -= v
			for pos < 0 {
				pos += 100
				count++
			}
			if pos == 0 {
				count++
			}
		} else {
			pos += v
			count += pos / 100
			pos %= 100
		}
		if DEBUG {
			fmt.Println(line, pos, count)
		}
	}
	return count
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
