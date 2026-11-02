package main

import (
	"fmt"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
2199943210
3987894921
9856789892
8767896789
9899965678`[1:]

//go:embed day09.txt
var live string

var WIDTH int
var HEIGHT int

type Point = tools.Point

var directions = []Point{ Point{-1,0}, Point{1,0}, Point{0,1}, Point{0,-1} }

func nextto( pt Point ) []Point {
	out := []Point{}
	for _,dir := range directions {
		pt0 := pt.Add( dir )
		if tools.Between(0, pt0.X, WIDTH) && tools.Between(0, pt0.Y, HEIGHT) {
			out = append( out, pt0 )
		}
	}
	return out
}

func printgrid(grid [][]byte) {
	for _,row := range grid {
		for _,cell := range row {
            fmt.Printf( "%5d", cell)
		}
        fmt.Println()
	}
}


func part1( data [][]byte ) int {
    risk := 0
    for y0 := range HEIGHT {
        for x0 := range WIDTH {
            fail := false
            this := data[y0][x0]
            for _,pt := range nextto(Point{x0,y0}) {
                if data[pt.Y][pt.X] <= this {
                    fail = true
                    break
				}
			}
            if ! fail {
                risk += int(this) + 1
                if DEBUG {
                    fmt.Println( x0, y0, this )
				}
			}
		}
	}
    return risk
}


func part2( data [][]byte ) int {
    region := 0
    counts := make(map[int]int)

    // Find all regions surrounded by 9s.

    for y0 := range HEIGHT {
        for x0 := range WIDTH {
            if data[y0][x0] == 9 {
                continue
			}

            // This cell is not part of a region.  Spread to its neighbors
            // and count them.

            counts[region] = 1
            data[y0][x0] = 9
			unchecked := tools.Stack[Point]{}
			unchecked.Push( Point{x0,y0} )
            for unchecked.Size() > 0 {
                xy1,_ := unchecked.PopFront()
				for _,pt := range nextto(xy1) {
                    if data[pt.Y][pt.X] < 9 {
                        counts[region] += 1
                        data[pt.Y][pt.X] = 9
                        unchecked.Push( pt )
					}
				}
			}
            region += 1
		}
	}

    // Grab the top three.

	counts[-1] = 0
   // delete( counts, -1 )
    if DEBUG {
        fmt.Println((counts))
	}
	countx := tools.Values(counts)
	slices.Sort(countx)
	n := len(countx)
    return countx[n-1]*countx[n-2]*countx[n-3]
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := [][]byte{}
	row := []byte{}
	for _,c := range input {
		if c == '\n' {
			data = append(data, row)
			row = []byte{}
		} else {
			row = append(row, byte(c)-'0')
		}
	}
	data = append(data, row)

	WIDTH = len(data[0])
	HEIGHT = len(data)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}


