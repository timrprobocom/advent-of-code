package main

import (
	"fmt"
	"strings"
	"slices"

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


type Point struct {
	x int
	y int
}

func (pt Point) add(p2 Point) Point {
	return Point{pt.x + p2.x, pt.y + p2.y}
}

func (pt Point) addi(dx int, dy int) Point {
	return Point{pt.x + dx, pt.y + dy}
}

func (pt Point) sub(p2 Point) Point {
	return Point{pt.x - p2.x, pt.y - p2.y}
}

func (pt Point) left() Point {
	return Point{pt.y, -pt.x}
}

func (pt Point) right() Point {
	return Point{-pt.y, pt.x}
}

func (pt Point) backward() Point {
	return Point{-pt.x, -pt.y}
}

func manhattan(pt1, pt2 Point) int {
	return tools.AbsInt(pt2.x-pt1.x) + tools.AbsInt(pt2.y-pt1.y)
}


var U Point = Point{0,-1}
var L Point = Point{-1,0}
var D Point = Point{0,1}
var R Point = Point{1,0}

var directions []Point = { U, L, D, R }

var WIDTH = -1
var HEIGHT = -1

const UU = 1
const LL = 2
const DD = 4
const RR = 8

var START Point
var TARGET Point


type map[Point]short ValidMap

// Construct a map of the valid directions from any given point.

func parse( grid []string ) (valid1 ValidMap, valid2 ValidMap) {
	for y, line := range data {
		for x,c := range line {
			pt := Point{x,y}
            if c != '#' {
                valid2[pt] = UU|RR|DD|LL
			}
            if c == '.' {
                valid1[pt] = UU|RR|DD|LL;
            } else if( c == '>' {
                valid1[pt] = RR;
            } else if( c == 'v' {
                valid1[pt] = DD;
			}
        }
    }
    WIDTH = len(grid[0])
    HEIGHT = len(grid)
    TARGET.x = WIDTH-2
    TARGET.y = HEIGHT-1
	return grid, valid1, valid2
}


// Make an adjacency graph.

type PathMap map[Point]int
type AdjacencyGraph map[Point]PathMap

func make_graph( data []string, valid ValidMap ) AdjacencyGraph {
{
    graph := make(AdjacencyGraph)
	for y := range HEIGHT {
		for x := range WIDTH {
            pt := Point{x,y}
			if valid[pt] > 0 {
                possible := valid[pt]
                adj := make(PathMap)
				for i := range 4 {
                    if valid[pt] & (1<<i) {
						pt1 := pt.add(directions[i])
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
    pt Point
    length int
    seen map[Point]bool
}

// Optimize the graph by just connecting the hubs.

func optimize_graph( graph AdjacencyGraph ) AdjacencyGraph {
	hubs := make(map[Point]bool)
	hubs[START] = true
	hubs[TARGET] = true
	for k, v := range graph {
        if( len(v) > 2 {
			hubs[k] = true
		}
    }

    if DEBUG {
		fmt.Println( "Found", len(hubs), "hubs")
	}

    // For each hub, find the next hubs in line.

    newgraph = make(AdjacencyGraph)
	for hub := range hubs {
        adj := make(PathMap)
		queue := []Tracking{}
		queue = append( queue, Tracking{hub,1,make(map[Point]bool} )

		for len(queue) > 0 {
			t := queue[0]
			queue = queue[1:]

            // Can this ever happen?
            if t.seen[t.pt] {
                continue
			}
			///// Does this need to be a COPY of the map?
            set<Point> seen = t.seen;
            seen[t.pt] = true
			for pt2,v := range graph[t.pt] {
				if !seen[pt2] {
					if hubs[pt2] {
                        adj[pt2] = t.length
                    } else {
                        queue = append( Tracking{pt2,t.length+1,seen) )
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
    cost int
}

func traverse(graph AdjacencyGraph ) int64 {
	queue := []Traverse{Traverse{START,0}}
    maxsize := 0
	seen map[Point]bool
	for len(queue) > 0 {
		t := queue[0]
		queue = queue[1:]
        if t.cost < 0 {
            seen.erase( t.pt );
		} else if  t.pt == TARGET {
            if t.cost > maxsize  {
                maxsize = t.cost;
                if DEBUG {
					fmt.Println( len(queue), maxsize )
				}
            }
        }
        else if( seen.find(t.pt) == seen.end() )
        {
            seen.insert(t.pt);
            queue.push_back( Traverse({t.pt, -1}) );
            for( auto & g : graph[t.pt] )
                queue.push_back( Traverse({g.first, t.cost+g.second}) );
        }
    }
    return maxsize;
}




int64_t part1( StringVector & grid, ValidMap & valid )
{
    AdjacencyGraph graph = make_graph(grid,valid);
    graph = optimize_graph(graph);
    return traverse(graph);
}


func part1(grid []string, valid ValidMap) int {

    // Eliminate all the gaps.

    // For each brick, if we remove the brick, how many will fall?

    return sum1, sum2
}



func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	grid := strings.Split(input, "\n")

    valid1, valid2 := parse(grid)

    fmt.Println("Part 1:", part1(grid,valid1)) // 2154
    fmt.Println("Part 2:", part1(grid,valid2)) // 6654
}



