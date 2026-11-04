package main

import (
	"fmt"

	"aoc/tools"
	pq "gopkg.in/dnaeon/go-priorityqueue.v1"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581`[1:]

//go:embed day15.txt
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


// Grow the grid by 5x.

func expandgrid( grid [][]byte ) [][]byte {
	newgrid := make([][]byte, HEIGHT )
    for i := range 5 {
        for y,row := range grid {
			newgrid[y] = make([]byte, WIDTH)
            for j := range 5 {
                for x,cell := range row {
                    newgrid[y][x] = (cell+byte(i+j)-1) % 9 + 1
				}
			}
		}
	}
    return newgrid
}


// This is Dijkstra's algorithm.
//
// We use priority queue so the lowest cost path is always on top.

func part1( grid [][]byte ) int64 {
    untried := pq.New[Point, int64](pq.MinHeap)
	untried.Put( Point{0,0}, 0 )
    costs := make( map[Point]int64 )
    for !untried.IsEmpty() {
        item := untried.Get()
		xy := item.Value
		cost := item.Priority
		if xy.X == WIDTH-1 && xy.Y == HEIGHT-1 {
            return cost
		}
        for _,pt := range nextto(xy) {
            nc := cost + int64(grid[pt.Y][pt.X])
			if nc > costs[pt] {
				costs[pt] = nc
				untried.Put( pt, nc )
			}
		}
	}
    return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	grid := [][]byte{}
	row := []byte{}
	for _,c := range input {
		if c == '\n' {
			grid = append( grid, row )
			row = []byte{}
		} else {
			row = append( row, byte(c)-'0' )
		}
	}
	grid = append( grid, row )
	WIDTH = len(grid[0])
	HEIGHT = len(grid)

	fmt.Println("Part 1:", part1(grid))
	fmt.Println("Part 2:", part1(expandgrid(grid)))
}
