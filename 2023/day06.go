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
Time:      7  15   30
Distance:  9  40  200`[1:]

//go:embed day06.txt
var live string


// So, for the first race, hold time vs distance:
//  0  1  2  3  4  5  6  7
//  0  6 10 12 12 10  6  0
// It's a Pascal's triangle thing

//  0  1  2  3  4  5  6
//  0  5  8  9  8  5  0

func part1( time []int, dist []int ) int {
	res := 1
	for i := 0; i < len(time); i++ {
		res *= part2(time[i], dist[i])
	}
	return res
}

func part2( time int, dist int ) int {
    d := 0
    i := 0
    n := time-1
    for d <= dist {
        i += 1
        d += n
        n -= 2
	}
    return time+1-i-i
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	lines := strings.Split(input, "\n")

    time := tools.SplitInt(lines[0])
    dist := tools.SplitInt(lines[1])
	var time2 int
	var dist2 int

	for _, c := range []byte(lines[0]) {
		if tools.Isdigit(c) {
			time2 = time2 * 10 + int(c) - '0'
		}
	}

	for _, c := range []byte(lines[1]) {
		if tools.Isdigit(c) {
			dist2 = dist2 * 10 + int(c) - '0'
		}
	}

	fmt.Println("Part 1:", part1(time, dist))
	fmt.Println("Part 2:", part2(time2, dist2))
}
