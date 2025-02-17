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
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....`[1:]

//go:embed day16.txt
var live string

var WIDTH = -1
var HEIGHT = -1

type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) addi(dx int, dy int) Point {
	return Point{pt.x + dx, pt.y + dy}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}

func (pt Point) left() Point {
	return Point{pt.y, -pt.x}
}

func (pt Point) right() Point {
	return Point{-pt.y, pt.x}
}

func manhattan(pt1, pt2 Point) int {
	return tools.AbsInt(pt2.x-pt1.x) + tools.AbsInt(pt2.y-pt1.y)
}

var N Point = Point{0, -1}
var E Point = Point{1, 0}
var S Point = Point{0, 1}
var W Point = Point{-1, 0}

func change( c byte, dir Point ) Point {
	if c == '/' {
		if dir == N || dir == S {
			return dir.right()
		} else {
			return dir.left()
		}
	} else if c == '\\' {
		if dir == N || dir == S {
			return dir.left()
		} else {
			return dir.right()
		}
	}
	panic("What?")
	return dir
}

type TwoPoint struct {
	pt  Point
	dir Point
}

func printg(seen map[TwoPoint]bool) {
	grid := [][]rune{}
	for range HEIGHT {
		grid = append(grid, tools.Repeat('.', WIDTH))
	}
	for s := range seen {
		grid[s.pt.y][s.pt.x] = '#'
	}
	for _, row := range grid {
		fmt.Println(string(row))
	}
}

func process(grid []string, start TwoPoint) int {
	beams := []TwoPoint{start}
	seen := make(map[TwoPoint]bool)

	for len(beams) > 0 {
		tpt := beams[0]
		beams = beams[1:]

		if seen[tpt] {
			continue
		}
		seen[tpt] = true

		dir := tpt.dir
		c := grid[tpt.pt.y][tpt.pt.x]
		if c == '/' || c == '\\' {
			dir = change(c, dir)
		} else if c == '|' && (dir == E || dir == W) {
			if tpt.pt.y > 0 {
				beams = append(beams, TwoPoint{tpt.pt.add(N), N})
			}
			dir = S
		} else if c == '-' && (dir == N || dir == S) {
			if tpt.pt.x > 0 {
				beams = append(beams, TwoPoint{tpt.pt.add(W), W})
			}
			dir = E
		}
		pt := tpt.pt.add(dir)
		if tools.Between(0, pt.x, WIDTH) && tools.Between(0, pt.y, HEIGHT) {
			beams = append(beams, TwoPoint{pt, dir})
		}
	}
	if DEBUG {
		printg(seen)
	}
	counter := make(map[Point]bool)
	for k, _ := range seen {
		counter[k.pt] = true
	}
	return len(counter)
}

func part1(grid []string) int {
	return process(grid, TwoPoint{Point{0, 0}, E})
}

func part2(grid []string) int {
	ener := 0
	for y := range HEIGHT {
		ener = max(ener,
			process(grid, TwoPoint{Point{0, y}, E}),
			process(grid, TwoPoint{Point{WIDTH - 1, y}, W}),
		)
	}
	for x := range WIDTH {
		ener = max(ener,
			process(grid, TwoPoint{Point{x, 0}, S}),
			process(grid, TwoPoint{Point{x, HEIGHT - 1}, N}),
		)
	}
	return ener
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	grid := strings.Split(input, "\n")

	WIDTH = len(grid[0])
	HEIGHT = len(grid)

	fmt.Println("Part 1:", part1(grid))
	fmt.Println("Part 2:", part2(grid))
}
