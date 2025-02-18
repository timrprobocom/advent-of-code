package main

import (
	"fmt"
	"strings"
	"strconv"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)`[1:]

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

func (pt Point) backward() Point {
	return Point{-pt.x, -pt.y}
}

func manhattan(pt1, pt2 Point) int {
	return tools.AbsInt(pt2.x-pt1.x) + tools.AbsInt(pt2.y-pt1.y)
}

var N Point = Point{0, -1}
var E Point = Point{1, 0}
var S Point = Point{0, 1}
var W Point = Point{-1, 0}

var directions map[byte]Point

func part1(part int, data []string) int64 {

// This implements Gauss's "shoelace formula" for computing the area of
// a polygon described by its vertex coordinates.  "Shoelace" would 
// normally accumulate both x*dy and y*dx, but since the side are all
// horizontal and vertical, the sums are the same.

    var area int64 = 0
    var perim int64 = 0
	pt := Point{0,0}

    for _, row := range data {
		parts := strings.Fields(row)
		var dist int64
		var dir Point
		clr := parts[2]
        if part == 1 {
            dist,_ = strconv.ParseInt( parts[1], 10, 32)
            dir = directions[parts[0][0]]
        } else {
			dist,_ = strconv.ParseInt( clr[2:7], 16, 32)
            dir = directions[clr[7]]
		}
		delta := Point{dir.x*int(dist), dir.y*int(dist)}
        area += int64(pt.x) * int64(delta.y)
        perim += int64(dist)
		pt = pt.add(delta)
	}
    if DEBUG {
        fmt.Println(area,perim)
	}
    return area + perim / 2 + 1
}
       

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	directions = make(map[byte]Point)
	directions['R'] = E
	directions['L'] = W
	directions['U'] = N
	directions['D'] = S
	directions['0'] = E
	directions['1'] = S
	directions['2'] = W
	directions['3'] = N

	fmt.Println("Part 1:", part1(1, data))
	fmt.Println("Part 2:", part1(2, data))
}

