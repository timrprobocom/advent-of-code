package main

import (
	"crypto/md5"
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....`[1:]

//go:embed day14.txt
var live string

var WIDTH = -1
var HEIGHT = -1

func tilt_n(grid [][]byte) {
	for x := range WIDTH {
		dy := 0
		for y := range HEIGHT {
			switch grid[y][x] {
			case '.':
				dy++
			case '#':
				dy = 0
			case 'O':
				grid[y][x] = '.'
				grid[y-dy][x] = 'O'
			}
		}
	}
}

func tilt_s(grid [][]byte) {
	for x := range WIDTH {
		dy := 0
		for y := HEIGHT - 1; y >= 0; y-- {
			switch grid[y][x] {
			case '.':
				dy++
			case '#':
				dy = 0
			case 'O':
				grid[y][x] = '.'
				grid[y+dy][x] = 'O'
			}
		}
	}
}

func tilt_w(grid [][]byte) {
	for y := range HEIGHT {
		dx := 0
		for x := range WIDTH {
			switch grid[y][x] {
			case '.':
				dx++
			case '#':
				dx = 0
			case 'O':
				grid[y][x] = '.'
				grid[y][x-dx] = 'O'
			}
		}
	}
}

func tilt_e(grid [][]byte) {
	for y := range HEIGHT {
		dx := 0
		for x := WIDTH - 1; x >= 0; x-- {
			switch grid[y][x] {
			case '.':
				dx++
			case '#':
				dx = 0
			case 'O':
				grid[y][x] = '.'
				grid[y][x+dx] = 'O'
			}
		}
	}
}

func weight(grid [][]byte) int {
	sum := 0
	for y, row := range grid {
		for _, col := range row {
			if col == 'O' {
				sum += HEIGHT - y
			}
		}
	}
	return sum
}

func unique(grid [][]byte) [16]byte {
	hasher := md5.New()
	for _, row := range grid {
		hasher.Write(row)
	}
	var res [16]byte
	copy(res[:], hasher.Sum(nil))
	return res
}

// This is one case where the fancy data structure did not help.  I converted
// the grid to a list of coordinate pairs.  69 seconds vs 0.5 seconds.

func makegrid(data []string) [][]byte {
	var grid [][]byte
	for _, row := range data {
		grid = append(grid, []byte(row))
	}
	return grid
}

func printgrid(grid [][]byte) {
	for _, row := range grid {
		fmt.Println(string(row))
	}
	fmt.Println()
}

func part1(data []string) int {
	grid := makegrid(data)
	tilt_n(grid)
	return weight(grid)
}

func part2(data []string) int {
	grid := makegrid(data)
	seen := make(map[[16]byte]int)
	scores := []int{0}
	var cur [16]byte
	for {
		tilt_n(grid)
		tilt_w(grid)
		tilt_s(grid)
		tilt_e(grid)
		cur = unique(grid)
		scores = append(scores, weight(grid))
		if DEBUG {
			fmt.Println(len(scores)-1, scores[len(scores)-1])
		}
		if seen[cur] > 0 {
			break
		}
		seen[cur] = len(scores) - 1
	}
	pat0 := seen[cur]
	cycle := len(scores) - 1 - pat0
	want := (1000000000-pat0)%cycle + pat0
	return scores[want]
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(input, "\n")

	WIDTH = len(data[0])
	HEIGHT = len(data)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
