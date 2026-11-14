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
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL`[1:]

//go:embed day11.txt
var live string

type Point = tools.Point

var deltas = []Point{
    Point{-1,-1},Point{-1,0},Point{-1,1},
    Point{ 0,-1},            Point{ 0,1},
    Point{ 1,-1},Point{ 1,0},Point{ 1,1},
}


func count(grid []string) int {
	sum := 0
	for _,ln := range grid {
		sum += strings.Count(ln, "#")
	}
	return sum
}


func pass1step(grid []string) []string {
    xlen := len(grid[0])
    ylen := len(grid)
    newgrid := []string{}
    for y,oline := range grid {
        line := []byte{}
		for x := range len(oline) {
			c := oline[x]
			point := Point{x,y}
            adjacent := 0
            if c != '.' {
                for _,pt := range deltas {
					pt = point.Add(pt)
					if tools.Between(0, pt.X, xlen) && tools.Between(0, pt.Y, ylen) && grid[pt.Y][pt.X] == '#' {
                        adjacent ++
					}
				}
			}
            if c == 'L' && adjacent == 0 {
                line = append(line, '#')
			} else if c == '#' && adjacent >= 4 {
                line = append(line, 'L')
            } else {
                line = append(line, c)
			}
		}
        newgrid = append(newgrid, string(line))
	}
    return newgrid
}


func pass2step(grid []string) []string {
    xlen := len(grid[0])
    ylen := len(grid)
    newgrid := []string{}
    for y,oline := range grid {
        line := []byte{}
		for x := range len(oline) {
			c := oline[x]
            adjacent := 0
            if c != '.' {
				for _,dxy := range deltas {
                    xy0 := Point{x,y}
                    for true {
						xy0 = xy0.Add(dxy)
						if !tools.Between(0, xy0.X, xlen) || !tools.Between(0, xy0.Y, ylen) || grid[xy0.Y][xy0.X] == 'L' {
                            break
						}
                        if grid[xy0.Y][xy0.X] == '#' {
                            adjacent ++
                            break
						}
					}
				}
			}
            if c == 'L' && adjacent == 0 {
                line = append(line, '#')
			} else if c == '#' && adjacent >= 5 {
                line = append(line, 'L')
            } else {
                line = append(line, c)
			}
		}
        newgrid = append(newgrid, string(line))
	}
    return newgrid
}


func process( grid []string, passfunc func([]string) []string ) int {
    for true {
        if DEBUG {
            fmt.Println( grid )
		}
        grid2 := passfunc(grid)
        if DEBUG {
            fmt.Println( count(grid) )
		}
        if slices.Equal(grid, grid2) {
            break
		}
        grid = grid2
	}
	return count(grid)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	grid := strings.Split(strings.TrimSpace(input), "\n")

	fmt.Println("Part 1:", process(grid, pass1step))
	fmt.Println("Part 2:", process(grid, pass2step))
}



