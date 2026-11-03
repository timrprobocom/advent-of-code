package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526`[1:]

var xtest = `
11111
19991
19191
19991
11111`[1:]

var live = `
1443582148
6553734851
1451741246
8835218864
1662317262
1731656623
1128178367
5842351665
6677326843
7381433267`[1:]

type Point = tools.Point

var WIDTH int
var HEIGHT int

func makegrid(input string) [][]byte {
    data := [][]byte{}
	row := []byte{}
	for i := range len(input) {
		c := input[i]
		if c == '\n' {
			data = append(data, row)
			row = []byte{}
		} else {
			row = append(row, c - '0' )
		}
	}
	data = append(data, row)
    return data
}


func printgrid( grid [][]byte ) {
	print("\n")
    for _,row := range grid {
		for _,c := range row {
			fmt.Print(c)
		}
		fmt.Println()
	}
}


var directions = []Point{
    Point{-1,-1},Point{0,-1},Point{1,-1},
    Point{-1, 0},            Point{1, 0},
	Point{-1, 1},Point{0, 1},Point{1, 1}, 
}


func nextto( pt Point ) []Point {
	out := []Point{}
	for _,dir := range directions {
		xy0 := pt.Add(dir)
		if tools.Between(0, xy0.X, WIDTH) && tools.Between(0, xy0.Y, HEIGHT) {
			out = append( out, xy0 )
		}
	}
	return out
}


// Steps:
// Each +1
// Each 9 causes +1 for all neighbors
// Repeat until no more pass 9.
// Any that get to >= 9 reset to 0


func generation( data [][]byte ) int {
    // This modifies data in place.
    flashes := 0
    for y := range HEIGHT {
        for x := range WIDTH {
            data[y][x] ++
		}
	}
    more := true
    for more {
        more = false
        for y := range HEIGHT {
            for x := range WIDTH {
                if data[y][x] >= 10 {
                    flashes ++
                    data[y][x] = 0
                    for _,xy := range nextto(Point{x,y}) {
                        if data[xy.Y][xy.X] > 0 {
                            more = true
                            data[xy.Y][xy.X] ++
						}
					}
				}
			}
		}
	}
    return flashes
}


// How many flashes in the first 100 generations?

func part1( data [][]byte ) int {
	sum := 0
	for _ = range 100 {
		sum += generation(data)
	}
	return sum
}


// How many generations until they all flash at once?

func part2( data [][]byte ) int {
    for gen := range 1000 {
        if generation(data) == WIDTH*HEIGHT {
            return gen+1
		}
	}
	return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	grid := makegrid(input)
	WIDTH = len(grid[0])
	HEIGHT = len(grid)
	fmt.Println("Part 1:", part1(grid))
	grid = makegrid(input)
	fmt.Println("Part 2:", part2(grid))
}

