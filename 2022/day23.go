package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day23.txt
var live string


var test = `
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..`[1:]

type Point = tools.Point

type Map = map[Point]bool

func parse(data []string) Map {
    elves := Map{}
	for y,row := range data {
		for x,col := range row {
            if col == '#' {
                elves[Point{x,y}] = true
			}
		}
	}
    return elves
}

var directions = [][]Point{
    {Point{-1,-1},Point{0,-1},Point{1,-1}}, // N
    {Point{-1, 1},Point{0, 1},Point{1, 1}}, // S
    {Point{-1,-1},Point{-1,0},Point{-1,1}}, // W
    {Point{ 1,-1},Point{ 1,0},Point{ 1,1}}, // #
}


var neighbors []Point

func makeNeighbors( directions [][]Point ) []Point {
	near := make(map[Point]bool)
	for _,d1 := range directions {
		for _,d2 := range d1 {
			near[d2] = true
		}
	}
	return tools.Keys(near)
}

func closeness( xmap Map, elf Point, dirs []Point ) int {
	sum := 0
	for _,dxy := range dirs {
		e := elf.Add(dxy)
		if xmap[e] {
			sum ++
		}
	}
	return sum
}

func plot( xmap Map ) {
	xmin, xmax, ymin, ymax := tools.Span( tools.Keys(xmap) )
	plt := make([][]byte, ymax-ymin+1)
	for i := range ymax-ymin+1 {
		plt[i] = tools.Repeat( "."[0], xmax-xmin+1 )
	}

    for pt,_ := range xmap {
		plt[pt.Y-ymin][pt.X-xmin] = '#'
	}
	for _,row := range plt {
		fmt.Println( string(row) )
	}
}


func part1( data []string ) int {
    xmap := parse(data)
    if DEBUG {
        plot(xmap)
	}
    for rnd := range 10 {
		proposed := make(map[Point][]Point)
        newmap := make(Map)
        for elf,_ := range xmap {
            if closeness(xmap, elf, neighbors) == 0 {
                // Leave us alone.
                newmap[elf] = true
                continue
			}

			xy0 := Point{0,0}
			found := false
            for _,dirs := range directions {
                if closeness(xmap,elf,dirs) == 0 {
					xy0 = elf.Add(dirs[1])
                    found = true
                    break
				}
			}
            if !found {
                newmap[elf] = true
                continue
			}

            proposed[xy0] = append( proposed[xy0], elf )
		}

        for k,v := range proposed {
            if len(v) == 1 {
                newmap[k] = true
            } else {
				for _,v1 := range v {
					newmap[v1] = true
				}
			}
		}

        xmap = newmap
        if DEBUG {
            fmt.Println("round",rnd+1)
            fmt.Println(xmap)
            plot(xmap)
		}
		directions = append( directions[1:], directions[0] )
	}

	xmin, xmax, ymin, ymax := tools.Span( tools.Keys(xmap) )
    cnt := len(xmap)

	directions = append( directions[2:], directions[0:2]... )

    return (xmax-xmin+1)*(ymax-ymin+1) - cnt
}


func part2( data []string ) int {
    xmap := parse(data)
    if DEBUG {
        plot(xmap)
	}
    for rnd := range 10000 {
        moved := false
		proposed := make(map[Point][]Point)
        newmap := make(Map)
        for elf,_ := range xmap {
            if closeness(xmap, elf, neighbors) == 0 {
                // Leave us alone??
                newmap[elf] = true
                continue
			}
			xy0 := Point{0,0}
			found := false
            for _,dirs := range directions {
                if closeness(xmap,elf,dirs) == 0 {
                    xy0 = elf.Add(dirs[1])
					found = true
                    break
				}
			}
            if !found {
                newmap[elf] = true
                continue
			}

            proposed[xy0] = append(proposed[xy0], elf)
		}

        for k,v := range proposed {
            if len(v) == 1 {
                moved = true
                newmap[k] = true
            } else {
				for _,v1 := range v {
					newmap[v1] = true
                }
			}
		}

        if ! moved {
			if DEBUG {
				plot(xmap)
			}
            return rnd+1
		}
        xmap = newmap
		directions = append(directions[1:], directions[0] )
	}

    return 0
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n") 
	neighbors = makeNeighbors(directions)

	fmt.Println("Part 1:", part1(data) )
	fmt.Println("Part 2:", part2(data) )
}

