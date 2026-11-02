package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2`[1:]


//go:embed day05.txt
var live string

type Point = tools.Point


func sgn(a int) int {
	if a > 0 {
		return 1
	} else if a < 0 {
		return -1
	} else {
		return 0
	}
}


func part1(part int, data [][]int) int {
	grid := make(map[Point]int)

	for _,row := range data {
		xy0 := Point{row[0],row[1]}
		xy1 := Point{row[2],row[3]}

		cnt := tools.AbsInt(xy1.X-xy0.X) | tools.AbsInt(xy1.Y-xy0.Y)
		dxy := Point{ sgn(xy1.X-xy0.X), sgn(xy1.Y-xy0.Y) }

        if part == 1 && dxy.X != 0 && dxy.Y != 0 {
            continue
		}

        for _ = range cnt+1 {
			grid[xy0] ++
			xy0 = xy0.Add(dxy)
		}
	}

	sumx := 0
	for _,v := range grid {
		if v > 1 {
			sumx += 1
		}
	}
    return sumx
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.GetPosNumbers[int](input)

	fmt.Println("Part 1:", part1(1, data)) // 6564
	fmt.Println("Part 2:", part1(2, data)) // 19172
}

