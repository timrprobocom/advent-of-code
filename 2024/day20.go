package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############`[1:]

//go:embed day20.txt
var live string

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

type PointSet = map[Point]bool

var WIDTH int = -1
var HEIGHT int = -1
var start Point
var finish Point
var directions []Point = []Point{{-1, 0}, {0, -1}, {0, 1}, {1, 0}}

// There is only one path through.  Compute the distance from start for each step.

func makemap(grid []string) map[Point]int {
	mapx := make(map[Point]int)
	point := start
	for point != finish {
		mapx[point] = len(mapx) + 1
		for _, dir := range directions {
			npt := point.actuald(dir)
			if grid[npt.y][npt.x] != '#' && mapx[npt] == 0 {
				point = npt
				break
			}
		}
	}

	mapx[finish] = len(mapx) + 1
	return mapx
}

func mandist(pt1, pt2 Point) int {
	return tools.AbsInt(pt2.x-pt1.x) + tools.AbsInt(pt2.y-pt1.y)
}

func part2(path map[Point]int, cheat int, crit int) int {
	sum := 0

	// For each pair of points, how much would be gained by shortcutting them?

	for k1, v1 := range path {
		for k2, v2 := range path {
			if v1 >= v2 {
				continue
			}
			// Compute Manhattan distance.

			manhattan := mandist(k1, k2)
			if manhattan <= cheat {
				actual := v2 - v1
				gain := actual - manhattan
				if gain >= crit {
					sum++
				}
			}
		}
	}
	return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	WIDTH = len(data[0])
	HEIGHT = len(data)

	for y, row := range data {
		for x, c := range row {
			if c == 'S' {
				start = Point{x, y}
			} else if c == 'E' {
				finish = Point{x, y}
			}
		}
	}

	path := makemap(data)

	c1, c2 := 100, 100
	if TEST {
		c1, c2 = 20, 50
	}

	fmt.Println("Part 1:", part2(path, 2, c1))
	fmt.Println("Part 2:", part2(path, 20, c2))
}
