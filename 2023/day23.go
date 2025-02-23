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
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#`[1:]

//go:embed day23.txt
var live string


type Point = tools.Point

var directions []Point = []Point{
	Point{0,-1},	// U
	Point{-1,0},	// L
	Point{0,1},		// D
	Point{1,0},		// R
}

var WIDTH = -1
var HEIGHT = -1

const UU = 1
const LL = 2
const DD = 4
const RR = 8

var START Point
var TARGET Point

type ValidMap map[Point]byte 

// Construct a map of the valid directions from any given point.

func parse( grid []string ) (ValidMap, ValidMap) {
	valid1 := make(ValidMap)
	valid2 := make(ValidMap)
	for y, line := range grid {
		for x,c := range line {
			pt := Point{x,y}
			if c != '#' {
				valid2[pt] = UU|RR|DD|LL
			}
			if c == '.' {
				valid1[pt] = UU|RR|DD|LL
			} else if c == '>' {
				valid1[pt] = RR
			} else if c == 'v' {
				valid1[pt] = DD
			}
		}
	}
	WIDTH = len(grid[0])
	HEIGHT = len(grid)
	START = Point{1,0}
	TARGET = Point{WIDTH-2, HEIGHT-1}
	return valid1, valid2
}


// Make an adjacency graph.

type PathMap		map[Point]int
type AdjacencyGraph map[Point]PathMap

func make_graph( data []string, valid ValidMap ) AdjacencyGraph {
	graph := make(AdjacencyGraph)
	for y := range HEIGHT {
		for x := range WIDTH {
			pt := Point{x,y}
			if valid[pt] > 0 {
				possible := valid[pt]
				adj := make(PathMap)
				for i := range 4 {
					if possible & (1<<i) > 0 {
						pt1 := pt.Add(directions[i])
						if valid[pt1] > 0 {
							adj[pt1] = 1
						}
					}
				}
				graph[pt] = adj
			}
		}
	}
	return graph
}


type Tracking struct {
	pt      Point
	length  int
}

// Optimize the graph by just connecting the places where multiple paths join.

func optimize_graph( graph AdjacencyGraph ) AdjacencyGraph {
	hubs := make(map[Point]bool)
	hubs[START] = true
	hubs[TARGET] = true
	for k, v := range graph {
		if len(v) > 2 {
			hubs[k] = true
		}
	}

	if DEBUG {
		fmt.Println( "Found", len(hubs), "hubs")
	}

	// For each hub, find the next hubs in line.

	newgraph := make(AdjacencyGraph)
	for hub := range hubs {
		adj := make(PathMap)
		queue := []Tracking{}
		queue = append( queue, Tracking{hub,1} )
		seen := make(map[Point]bool)

		for len(queue) > 0 {
			t := queue[0]
			queue = queue[1:]

			seen[t.pt] = true
			for pt2,_ := range graph[t.pt] {
				if !seen[pt2] {
					if hubs[pt2] {
						adj[pt2] = t.length
					} else {
						queue = append( queue, Tracking{pt2,t.length+1} )
					}
				}
			}
		}
		newgraph[hub] = adj
	}
	return newgraph
}


type Traverse struct {
	pt Point
	cost int64
}

func traverse(graph AdjacencyGraph ) int64 {
	queue := []Traverse{Traverse{START,0}}
	var maxsize int64 = 0
	seen := make(map[Point]bool)
	for len(queue) > 0 {
		t := queue[len(queue)-1]
		queue = queue[:len(queue)-1]
		if t.cost < 0 {
			seen[t.pt] = false
		} else if t.pt == TARGET {
			if t.cost > maxsize  {
				maxsize = t.cost
				if DEBUG {
					fmt.Println( len(queue), maxsize )
				}
			}
		} else if !seen[t.pt] {
			seen[t.pt] = true
			queue = append( queue, Traverse{t.pt, -1} )
			for k,v := range graph[t.pt] {
				queue = append( queue, Traverse{k, t.cost+int64(v)} )
			}
		}
	}
	return maxsize
}




func part1( grid []string, valid ValidMap ) int64 {
	graph := make_graph(grid,valid)
	graph = optimize_graph(graph);
	return traverse(graph)
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	grid := strings.Split(input, "\n")

	valid1, valid2 := parse(grid)

	fmt.Println("Part 1:", part1(grid,valid1)) // 2154
	fmt.Println("Part 2:", part1(grid,valid2)) // 6654
}



