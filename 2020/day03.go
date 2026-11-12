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
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#`[1:]

//go:embed day03.txt
var live string

var WIDTH int
var HEIGHT int

func counttrees( data []string, dx, dy int ) int {
	x := 0
	y := 0
	sum := 0
	for y < HEIGHT {
		if data[y][x] == '#' {
			sum ++
		}
		x = (x + dx) % WIDTH
		y += dy
	}
	return sum
}

func part1(data []string) int {
	return counttrees(data, 3, 1)
}

func part2(data []string) int {
	pairs := [][]int{
		{1, 1}, {3, 1}, {5, 1}, {7,1 }, {1,2},
	}
	sumx := 1
	for _,pair := range pairs {
		sumx *= counttrees(data, pair[0], pair[1] )
	}
	return sumx
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	if len(data[len(data)-1]) == 0 {
		data = data[:len(data)-1]
	}

	WIDTH = len(data[0])
	HEIGHT = len(data)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}

