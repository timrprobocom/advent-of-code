package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day09.txt
var live string

var test = `
test = """\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2`[1:]

var test2 = `
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20`[1:]

type Point = tools.Point

var dirs = map[byte]Point{
	'L': Point{-1, 0},
	'U': Point{0, -1},
	'R': Point{1, 0},
	'D': Point{0, 1},
}

func move(h Point, t Point) Point {
	if tools.AbsInt(h.X-t.X) <= 1 && tools.AbsInt(h.Y-t.Y) <= 1 {
		return t
	}
	tail := Point{}
	if h.X == t.X {
		tail = Point{t.X, (h.Y + t.Y) / 2}
	} else if h.Y == t.Y {
		tail = Point{(h.X + t.X) / 2, t.Y}

		// So one of them is off by 2.
		// For part 2, both can be off by 2.
	} else if tools.AbsInt(h.X-t.X) == 2 {
		if tools.AbsInt(h.Y-t.Y) == 2 {
			tail = Point{(h.X + t.X) / 2, (h.Y + t.Y) / 2}
		} else {
			tail = Point{(h.X + t.X) / 2, h.Y}
		}
	} else {
		tail = Point{h.X, (h.Y + t.Y) / 2}
	}
	return tail
}

func plot(visit map[Point]bool) {
	minx, maxx, miny, maxy := tools.Span(tools.Keys(visit))
	w := maxx - minx + 1
	h := maxy - miny + 1
	mapx := make([][]byte, h)
	for i := range h {
		mapx[i] = tools.Repeat("."[0], w)
	}
	for pt, _ := range visit {
		mapx[pt.Y-miny][pt.X-minx] = '#'
	}
	mapx[-miny][-minx] = 's'
	for _, row := range mapx {
		fmt.Println(string(row))
	}
}

func part1(data []string, n int) int {
	ropes := make([]Point, n)
	visited := make(map[Point]bool)
	visited[ropes[len(ropes)-1]] = true
	for _, line := range data {
		delta := dirs[line[0]]
		nnn := tools.StrToInt(line[2:])
		for range nnn {
			ropes[0] = ropes[0].Add(delta)
			for i := range len(ropes) - 1 {
				ropes[i+1] = move(ropes[i], ropes[i+1])
			}
			visited[ropes[len(ropes)-1]] = true
		}
	}
	if DEBUG {
		plot(visited)
	}
	return len(visited)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	data2 := data
	if TEST {
		data2 = strings.Split(test2, "\n")
	}

	fmt.Println("Part 1:", part1(data, 2))
	fmt.Println("Part 2:", part1(data2, 10))
}
