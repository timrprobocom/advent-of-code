package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
..F7.
.FJ|.
SJ.L7
|F--J
LJ...`[1:]

var test1 = `
.....
.S-7.
.|.|.
.L-J.
.....`[1:]

var test2 = `
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........`[1:]

//go:embed day10.txt
var live string

type Point = tools.Point

var N = Point{0, -1}
var W = Point{-1, 0}
var S = Point{0, 1}
var E = Point{1, 0}

type TwoPoint struct {
	p0 Point
	p1 Point
}

var dirs map[byte]TwoPoint

var start Point
var WIDTH = -1
var HEIGHT = -1

func Initialize(lines [][]byte) {
	dirs = make(map[byte]TwoPoint)
	dirs['|'] = TwoPoint{N, S}
	dirs['-'] = TwoPoint{E, W}
	dirs['F'] = TwoPoint{S, E}
	dirs['L'] = TwoPoint{N, E}
	dirs['J'] = TwoPoint{N, W}
	dirs['7'] = TwoPoint{S, W}

	WIDTH = len(lines[0])
	HEIGHT = len(lines)

	// Find the S.

	X := 0
	Y := 0

	for Y = 0; Y < HEIGHT; Y++ {
		X = slices.Index(lines[Y], 'S')
		if X >= 0 {
			break
		}
	}

	// What's below the S?

	var possx []Point
	if Y > 1 {
		c := lines[Y-1][X]
		if dirs[c].p0 == S || dirs[c].p1 == S {
			possx = append(possx, N)
		}
	}
	if Y < HEIGHT-1 {
		c := lines[Y+1][X]
		if dirs[c].p0 == N || dirs[c].p1 == N {
			possx = append(possx, S)
		}
	}
	if X < WIDTH-1 {
		c := lines[Y][X+1]
		if dirs[c].p0 == W || dirs[c].p1 == W {
			possx = append(possx, E)
		}
	}
	if X > 1 {
		c := lines[Y][X-1]
		if dirs[c].p0 == E || dirs[c].p1 == E {
			possx = append(possx, W)
		}
	}

	poss := TwoPoint{possx[0], possx[1]}

	base := byte('?')
	for k, v := range dirs {
		if v == poss {
			base = k
			break
		}
	}

	start = Point{X, Y}
	if DEBUG {
		fmt.Println(X, ",", Y)
	}

	// Replace the 'S' with whatever character completes the loop.

	lines[Y][X] = base
}

func print_data(lines [][]byte) {
	fmt.Println()
	for _, s := range lines {
		fmt.Println(string(s))
	}
}

// This contains the coordinates of the loop path.

type PointElem struct {
	pt   Point
	cost int
}

func part1(lines [][]byte) (int, map[Point]int) {
	pending := []PointElem{PointElem{start, 1}}
	found := make(map[Point]int)

	// This is a BFS, visiting all the cells on the loop path.

	for len(pending) > 0 {
		p := pending[0]
		pending = pending[1:]
		found[p.pt] = p.cost
		ch := lines[p.pt.Y][p.pt.X]

		for _, d := range []Point{dirs[ch].p0, dirs[ch].p1} {
			npt := p.pt.Add(d)
			if npt.InRange(WIDTH, HEIGHT) &&
				found[npt] == 0 {
				pending = append(pending, PointElem{npt, p.cost + 1})
			}
		}
	}
	if DEBUG {
		fmt.Println(found)
	}
	maxx := 0
	for _, v := range found {
		maxx = max(maxx, v-1)
	}

	return maxx, found
}

// Erase all cells that are not part of the loop path.

func blank_path(data [][]byte, found map[Point]int) {
	for y := 0; y < HEIGHT; y++ {
		for x := 0; x < WIDTH; x++ {
			if found[Point{x, y}] == 0 {
				data[y][x] = '.'
			}
		}
	}
}

func part2(lines [][]byte, found map[Point]int) int {
	blank_path(lines, found)
	if DEBUG {
		print_data(lines)
	}

	// Use the winding rule.  Scanning from the left, if we have
	// encountered an odd number of edges, then the point is inside.

	cells := 0
	for _, row := range lines {
		inside := false
		for _, c := range row {
			if c == 'J' || c == 'L' || c == '|' {
				inside = !inside
			}
			if inside && c == '.' {
				cells++
			}
		}
	}
	return cells
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test2, live)

	lines := [][]byte{}
	for _, l := range strings.Split(input, "\n") {
		lines = append(lines, []byte(l))
	}

	Initialize(lines)

	p1, found := part1(lines)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", part2(lines, found))
}
