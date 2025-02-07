package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0`[1:]

//go:embed day18.txt
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
var start Point
var finish Point
var directions []Point = []Point{{-1, 0}, {0, -1}, {0, 1}, {1, 0}}

type Queue struct {
	point Point
	score int
}

func makeset(points []Point) PointSet {
	ps := make(PointSet)
	for _, pt := range points {
		ps[pt] = true
	}
	return ps
}

func shortest(points []Point) int {
	walls := makeset(points)
	queue := []Queue{{start, 0}}
	visited := make(PointSet)
	visited[start] = true
	for len(queue) > 0 {
		q := queue[0]
		queue = queue[1:]

		if q.point == finish {
			return q.score
		}
		for _, dir := range directions {
			pt0 := q.point.add(dir)
			if tools.Between(0, pt0.x, WIDTH) && tools.Between(0, pt0.y, WIDTH) && !walls[pt0] && !visited[pt0] {
				visited[pt0] = true
				queue = append(queue, Queue{pt0, q.score + 1})
			}
		}
	}
	return -1
}

func part1(walls []Point) int {
	limit := 1024
	if TEST {
		limit = 12
	}
	return shortest(walls[:limit])
}

// Binary search.

func part2(walls []Point) string {
	minx := 1024
	if TEST {
		minx = 12
	}
	maxx := len(walls)
	var mid int

	for minx < maxx {
		mid = (maxx + minx) / 2
		if shortest(walls[:mid]) < 0 {
			maxx = mid
			if DEBUG {
				fmt.Println(mid, "fails")
			}
		} else {
			minx = mid + 1
			if DEBUG {
				fmt.Println(mid, "passes")
			}
		}
	}
	return fmt.Sprintf("%d,%d", walls[mid-1].x, walls[mid-1].y)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.Parse[int](input)

	if TEST {
		WIDTH = 7
	} else {
		WIDTH = 71
	}
	start = Point{0, 0}
	finish = Point{WIDTH - 1, WIDTH - 1}

	var points []Point
	for _, row := range data {
		points = append(points, Point{row[0], row[1]})
	}

	fmt.Println("Part 1:", part1(points))
	fmt.Println("Part 2:", part2(points))
}
