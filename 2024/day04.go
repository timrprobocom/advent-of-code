package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX`

//go:embed day04.txt
var live string

var WIDTH int = -1
var HEIGHT int = -1

// Find all occurrances of c.

type Point struct {
	x int
	y int
}

func findall(data []string, c rune) []Point {
	var result []Point
	for y, row := range data {
		for x, col := range row {
			if col == c {
				result = append(result, Point{x, y})
			}
		}
	}
	return result
}

var directions []Point

func part1(data []string) int {
	winner := 0
	for _, point := range findall(data, 'X') {
		for _, dir := range directions {
			var pt = point
			winner++
			for _, c := range []byte("MAS") {
				pt.x += dir.x
				pt.y += dir.y
				if !(tools.Between(0, pt.x, WIDTH-1) && tools.Between(0, pt.y, HEIGHT-1) && data[pt.y][pt.x] == c) {
					winner--
					break
				}
			}
		}
	}
	return winner
}

func part2(data []string) int {
	winner := 0
	for _, pt := range findall(data, 'A') {
		if tools.Between(1, pt.x, WIDTH-2) &&
			tools.Between(1, pt.y, HEIGHT-2) &&
			((data[pt.y-1][pt.x-1] == 'M' && data[pt.y+1][pt.x+1] == 'S') ||
				(data[pt.y-1][pt.x-1] == 'S' && data[pt.y+1][pt.x+1] == 'M')) &&
			((data[pt.y-1][pt.x+1] == 'M' && data[pt.y+1][pt.x-1] == 'S') ||
				(data[pt.y-1][pt.x+1] == 'S' && data[pt.y+1][pt.x-1] == 'M')) {
			winner++
		}
	}
	return winner
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	var data = strings.Split(input, "\n")
	WIDTH = len(data[0])
	HEIGHT = len(data)
	directions = []Point{
		{-1, -1}, {-1, 0}, {-1, 1},
		{0, -1}, {0, 1},
		{1, -1}, {1, 0}, {1, 1}}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
