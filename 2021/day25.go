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
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>`[1:]

//go:embed day25.txt
var live string

type Point = tools.Point

type Grid = map[Point]bool

var WIDTH int
var HEIGHT int


func printgrid(c_right, c_down Grid ) {
	grid := make([][]byte, HEIGHT)
	for i := range HEIGHT {
		grid[i] = tools.Repeat[byte]('.', WIDTH)
	}
    for pt,_ := range c_right {
        grid[pt.Y][pt.X] = '>'
	}
	for pt,_ := range c_down {
        grid[pt.Y][pt.X] = 'v'
	}
    for _,row := range grid {
		fmt.Println(string(row))
	}
}


func generation(c_right, c_down Grid ) (int, Grid, Grid) {
    changes := 0
    new_right := make(Grid)
    new_down := make(Grid)
	for pt,_ := range c_right {
		dx := (pt.X+1) % WIDTH
		tpt := Point{dx,pt.Y}
		if c_right[tpt] || c_down[tpt] {
            new_right[pt] = true
        } else {
            changes ++
            new_right[tpt] = true
		}
	}
    for pt,_ := range c_down {
		dy := (pt.Y+1) % HEIGHT
		tpt := Point{pt.X,dy}
		if new_right[tpt] || c_down[tpt] {
            new_down[pt] = true
        } else {
            changes ++
            new_down[tpt] = true
		}
	}

    return changes, new_right, new_down
}


func part1( c_right Grid, c_down Grid ) int {
	if DEBUG {
		printgrid(c_right,c_down)
		print("\n")
	}
	for gen := range(999) {
		n,right,down := generation(c_right,c_down)
		c_right = right
		c_down = down
		if DEBUG {
			printgrid(c_right,c_down)
			fmt.Println(n)
		}
		if n == 0 {
		    return gen+1
		}
	}
	return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := strings.Split(input, "\n")

	WIDTH = len(data[0])
	HEIGHT = len(data)

	// Convert the map to a set of coordinates.

	c_right := make(Grid)
	c_down := make(Grid)

	for y,row := range data {
		for x := range len(row) {
			pt := Point{x,y}
			if row[x] == '>' {
				c_right[pt] = true
			} else if row[x] == 'v' {
				c_down[pt] = true
			}
		}
	}

	fmt.Println("Part 1:", part1(c_right, c_down) )
}


