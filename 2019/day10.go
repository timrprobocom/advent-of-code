package main

import (
	"cmp"
	"fmt"
	"math"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = [][]int{
	{109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99}, //# takes no input and produces a copy of itself as output.
	{1102,34915192,34915192,7,4,7,99,0}, //# should output a 16-digit number.
	{104,1125899906842624,99}, // should output the large number in the middle.
}

// 3,4 with 8

var t1 = `
.#..#
.....
#####
....#
...##`[1:]

// 5,6 with 33

var t2 = `
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####`[1:]


// 1,2 with 35

var t3 = `
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.`[1:]

// 6,3 with 41

var t4 = `
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..`[1:]

// 11,13 with 210

var t5 = `
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##`[1:]

//go:embed day10.txt
var live string

type Point = tools.Point

type Graph = [][]byte

// Is this line completely visible?
func visible (graph Graph, pt0, pt1 Point ) bool {
    // Get the slope of the line.
	delta := pt1.Sub(pt0)
    
    // Compute the GCD.  If they are relatively prime, then this star is visible.
	div := tools.Gcd(tools.AbsInt(delta.X), tools.AbsInt(delta.Y))
    if div == 1 {
        return true
	}

    // Compute the steps at which stars will interfere.
	step := Point{delta.X/div, delta.Y/div}

    // until we reach the target (which we always will), check for blocks.
	pt0 = pt0.Add(step)
	for pt0 != pt1 {
        if graph[pt0.Y][pt0.X] == '#' {
            return false
		}
		pt0 = pt0.Add(step)
	}
    return true
}


func check( graph Graph, t Point ) map[Point]bool {
    if DEBUG {
        fmt.Println( "Checking", t )
	}
    dim := len(graph)
    found := make(map[Point]bool)
    for y1 := range dim {
        for x1 := range dim {
			pt := Point{x1,y1}
			if DEBUG {
				fmt.Println( "   ", pt )
			}
            if pt == t {
                continue
			}
            if graph[pt.Y][pt.X] != '#' {
                continue
			}
            if visible( graph, t, pt ) {
                found[pt] = true
			}
		}
	}
    if DEBUG {
        fmt.Println( len(found) )
	}
    return found
}

func scan( graph Graph) (int,Point) {
    maxcount := 0
	maxelem := Point{}
    for y,line := range graph {
        for x,cell := range line {
            if DEBUG {
                fmt.Println( x, y, string(line), cell )
			}
            if cell == '#' {
				pt := Point{x,y}
				count := len(check(graph, pt))
				if count > maxcount {
					maxcount = count
					maxelem = pt
				}
			}
		}
	}
    if DEBUG {
        fmt.Println( maxelem, "sees", maxcount )
	}
    return maxcount, maxelem
}


func laser( graph Graph, pt Point ) int {
    remains := 200
	found := map[Point]bool{}
    for remains > 0 {
        found = check(graph,pt)
        // If we don't catch them all in one round, eliminate these.
		if len(found) > remains {
			break
		}
		for pt1,_ := range found {
			graph[pt1.Y][pt1.X] = '.'
		}
		remains -= len(found)
	}

    type Hold struct {
		angle float64
		point Point
	}

	// Compute the angle from north.
	angles := []Hold{}
	for pt1,_ := range found {
	    delta := pt1.Sub(pt)
	    angle := math.Pi/4 - math.Atan2(float64(delta.X),float64(delta.Y))
		angles = append( angles, Hold{angle, pt1} )
    }

	// Sort by the angle, pick the 200th.
	slices.SortFunc( angles, func(a,b Hold) int { return cmp.Compare[float64](a.angle,b.angle) } )
    if DEBUG {
        fmt.Println( "Number 200 is", angles[remains-1] )
	}
    return angles[remains-1].point.X * 100 + angles[remains-1].point.Y
}

func convert( data []string ) Graph {
	graph := Graph{}
	for _,row := range data {
		graph = append( graph, []byte(row) )
	}
	return graph
}

func part1t() {
    a,_ := scan(convert(strings.Split(t1,"\n")))
    fmt.Println("Part 1:", a)
    a,_ = scan(convert(strings.Split(t2,"\n")))
    fmt.Println("Part 1:", a)
    a,_ = scan(convert(strings.Split(t3,"\n")))
    fmt.Println("Part 1:", a)
    a,_ = scan(convert(strings.Split(t4,"\n")))
    fmt.Println("Part 1:", a)
    a,_ = scan(convert(strings.Split(t5,"\n")))
    fmt.Println("Part 1:", a)
}

func part1(data Graph) int {
	a,_ := scan(data)
    return a
}

// Answer was 26, 29.
        
func part2(data Graph) int {
    _,best := scan(data)
    return laser(data, best)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(t5, live)
	graph := convert( strings.Split(strings.TrimSpace(input), "\n" ) )

	if TEST {
		part1t()
	}

	fmt.Println("Part 1:", part1(graph))
	fmt.Println("Part 2:", part2(graph))
}

