package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day14.txt
var live string

var test = `
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9`[1:]


type Point = tools.Point

func cmp(s, t int) int {
	if s < t {
		return -1
	} else if s > t {
		return 1
	}
	return 0
}

// Directly below first, then left, then right.

var directions = []Point {
	Point{0,1},
	Point{-1,1},
	Point{1,1},
}

func plot( xmap map[Point]bool ) {
	points := tools.Keys(xmap)
	minx, maxx, miny, maxy := tools.Span( points )
	miny = 0
	themap := make( [][]byte, maxy-miny+1 )
	for i := range maxy-miny+1 {
		themap[i] = tools.Repeat( "."[0], maxx-minx+1 )
	}
	for _, xy := range points {
		themap[xy.Y-miny][xy.X-minx] = '#'
	}
    for _,row := range themap {
		fmt.Println( string(row) )
	}
}

func fillsegment( xmap map[Point]bool, segment []Point ) {
	xy := segment[0]
	xmap[xy] = true

	for _,nxy := range segment[1:] {
        dxy := Point{cmp(nxy.X, xy.X), cmp(nxy.Y, xy.Y)}
		for xy != nxy {
			xy = xy.Add(dxy)
            xmap[xy] = true
		}
	}
}

func fill( xmap map[Point]bool, line string) {
	segment := []Point{}
	for _,point := range strings.Split(line, " -> ") {
		xy := strings.Split( point, "," )
		x := tools.StrToInt(xy[0])
		y := tools.StrToInt(xy[1])
		segment = append( segment, Point{x,y} )
	}
    fillsegment(xmap,segment)
}


func part1(part int, data []string) int {
    xmap := make(map[Point]bool)
	for _,line := range data {
		fill(xmap,line)
	}
	_,_,_,maxy := tools.Span(tools.Keys(xmap))

    if part == 2 {
        maxy += 2
        fillsegment(xmap,[]Point{Point{0,maxy},Point{699,maxy}})
	}

    sand := 0
	base := Point{500,0}
	for !xmap[base] {
		sxy := base
		for sxy.Y <= maxy {
			blocked := true
            for _,dxy := range directions {
				sxy0 := sxy.Add(dxy)
                if ! xmap[sxy0] {
                    sxy = sxy0
					blocked = false
                    break
				}
			}
            if blocked {
                sand ++
				xmap[sxy] = true
                if DEBUG {
                    fmt.Println("placed",sxy.X,sxy.Y)
					plot(xmap)
				}
				break
			}
		}
		if sxy.Y > maxy {
			break
		}
	}
    if DEBUG {
        plot(xmap)
	}
    return sand
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(1,data))
	fmt.Println("Part 2:", part1(2,data))
}

