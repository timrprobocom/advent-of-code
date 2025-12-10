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
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3`[1:]

//go:embed day09.txt
var live string

type Point = tools.Point

func part1(data []Point) int {
    best := 0
	for i, a := range data {
		for _, b := range data[i+1:] {
			area := (tools.AbsInt(b.X-a.X)+1) * (tools.AbsInt(b.Y-a.Y)+1)
			if area > best {
				best = area
			}
		}
	}
    return best
}

func part2(data []Point) int {
    best := 0
	for i, a := range data {
		for _, b := range data[i+1:] {
			area := (tools.AbsInt(b.X-a.X)+1) * (tools.AbsInt(b.Y-a.Y)+1)
			if area < best {
				continue
			}
			x1 := a.X
			x2 := b.X
			if x1 > x2 {
				x1, x2 = x2, x1
			}
			y1 := a.Y
			y2 := b.Y
			if y1 > y2 {
				y1, y2 = y2, y1
			}
			
			maybe := true
			for i := 0; i < len(data)-1; i++ {
				p1 := data[i];
				p2 := data[i+1];
				if p1.X == p2.X {
					// Vertical.
					py0 := p1.Y
					py1 := p2.Y
					if py0 > py1 {
						py0, py1 = py1, py0
					}
					if x1 <  p1.X && p1.X < x2 && py0 <= y2 && py1 >= y1 {
						maybe = false
						break
					}
				} else {
					// Horizontal.
					px0 := p1.X;
					px1 := p2.X;
					if px0 > px1 {
						px0, px1 = px1, px0
					}
					if y1 < p1.Y && p1.Y < y2 && px0 <= x2 && px1 >= x1 {
						maybe = false
						break
					}
				}
			}
			if maybe {
				if DEBUG {
					fmt.Println( area, a, b )
				}
				best = area
			}
		}
	}
	return best
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := []Point{}
	for _, row := range strings.Split(input, "\n") {
		p := strings.Split(row, ",")
		data = append(data, Point{
			tools.StrToInt(p[0]),
			tools.StrToInt(p[1])})
	}

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
