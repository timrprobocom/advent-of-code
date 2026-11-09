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
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###`[1:]

//go:embed day20.txt
var live string

type Point = tools.Point
type Grid = map[Point]bool

// Convert to a set of coordinates.

func convert(data []string) Grid {
    coords := make(Grid)
    for y,row := range data[2:] {
        for x,cell := range row {
            if cell == '#' {
                coords[Point{x,y}] = true
			}
		}
	}
    return coords
}


type Mapper struct {
	algo	string
	coords	Grid
	infinite int
	minx	int
	maxx	int
	miny	int
	maxy	int
}

func (self *Mapper) find_extrema() {
	self.minx, self.maxx, self.miny, self.maxy = tools.Span( tools.Keys(self.coords) )
}

func makeMapper( data []string ) *Mapper {
	mmm := Mapper{}
	mmm.algo = data[0]
	mmm.coords = convert(data)
	mmm.find_extrema()
	mmm.infinite = 0
	return &mmm
}

func (self *Mapper) getval( xy Point ) int {
	num := 0
	for dy := -1; dy <= 1; dy++ {
		for dx := -1; dx <= 1; dx++ {
			pt := xy.Add( Point{dx,dy} )
			num <<= 1
			if self.outside(pt) || self.coords[pt] {
				num ++
			}
		}
	}
	return num
}

// In an evil twist, I (like many) did not realize that the entire infinite
// background blinks with the live data, because algo[0] == '#' and algo[511] == '.'.
// So, if a cell is out of bounds, return the state of the void.

func (self *Mapper) outside( pt Point ) bool {
	return (self.infinite == 1) && (!tools.Between(self.minx, pt.X, self.maxx+1) || !tools.Between(self.miny, pt.Y, self.maxy+1))
}


func (self *Mapper) printit() {
	print("Grid:\n")
	for y := self.miny; y <= self.maxy; y++ {
		row := make([]byte, self.maxx-self.minx+1)
		for x := self.minx; x <= self.maxx; x++ {
			if self.coords[Point{x,y}] {
				row[x] = '#'
			} else {
				row[x] = '.'
			}
		}
		fmt.Printf("%3d %s", y, string(row))
	}
}

func (self *Mapper) generation() {
	newcoords := make(Grid)
	for y := self.miny-1; y <= self.maxy+1; y++ {
		for x := self.minx-1; x <= self.maxx+1; x++ {
			pt := Point{x,y}
			if self.algo[self.getval(pt)] == '#' {
				newcoords[pt] = true
			}
		}
	}
	if self.algo[self.infinite*511] == '#' {
		self.infinite = 1
	}
	self.coords = newcoords
	self.find_extrema()
}

func (self *Mapper) length() int {
	return len(self.coords)
}



func part1( coords *Mapper, n int ) int {
    if DEBUG {
        coords.printit()
	}

    for _ = range n {
        coords.generation()
        if DEBUG {
            coords.printit()
		}
	}

    return coords.length()
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	coords := makeMapper(strings.Split(input, "\n"))

	fmt.Println( "Part 1:", part1(coords,2) )
	fmt.Println( "Part 2:", part1(coords,48) )
}

