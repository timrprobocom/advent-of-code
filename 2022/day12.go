package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day12.txt
var live string

var test = `
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi`[1:]

type Point = tools.Point

type Visit struct {
	XY Point
	Depth int
}

var directions = []Point {
	Point{-1,0},
	Point{1,0},
	Point{0,-1},
	Point{0,1},
}

func part1(data []string, pick string) int {
    w := len(data[0])
    h := len(data)
    visited := make(map[Point]bool)
	q := []Visit{}

    for y,row := range data {
        for x,c := range row {
            if strings.ContainsRune(pick, c) {
				xy := Point{x,y}
                visited[xy] = true
				q = append( q, Visit{xy, 0} )
			}
		}
	}
	for len(q) > 0 {
		v := q[0]
		q = q[1:]

        if data[v.XY.Y][v.XY.X] == 'E' {
            return v.Depth
		}
        c := data[v.XY.Y][v.XY.X]
        if c == 'S' {
            c = 'a'
		}
		for _,dxy := range directions {
			xy0 := v.XY.Add( dxy )
			if xy0.X < 0 || xy0.X >= w || xy0.Y < 0 || xy0.Y >= h || visited[xy0] {
                continue
			}
			m := data[xy0.Y][xy0.X]
			if (m == 'E' && c >= 'y') || (m != 'E' && m <= (c+1)) {
                visited[xy0] = true
				q = append( q, Visit{xy0, v.Depth+1} )
		    }
		}
	}
    return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data, "S"))
	fmt.Println("Part 2:", part1(data, "Sa"))
}
