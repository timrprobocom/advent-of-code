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

//go:embed day22.txt
var live string


var test = `
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5`[1:]

type Point = tools.Point

var BOX int

var R int = 0
var D int = 1
var L int = 2
var U int = 3

var directions = [...]Point{ Point{1,0},Point{0,1},Point{-1,0},Point{0,-1} }

// Discover the layout.

func findLayout( data []string ) []Point {
	boxes := []Point{}
	for y := 0; y < len(data); y += BOX {
		for x := 0; x < len(data[y]); x += BOX {
			if data[y][x] != ' ' {
				boxes = append( boxes, Point{x,y} )
			}
		}
	}
	return boxes
}

// For TEST map, 
//      0
//  1 2 3
//      4 5 

// For DATA map:
//    0 1
//    2
//  3 4
//  5

// Apply rules to find the other connections.  This table says that,
// from a cube at x,y, we can get to cube at x-1,x+1 from our left,
// entering going down.  We can also get to it from our down, 
// entering going left.

var rules = [...][]int {
    {-1, +1, L, D},
    {-1, +1, D, L},
    {-2, +1, U, D},
    {-2, +1, D, U},
    {+1, +1, R, D},
    {+1, +1, D, R},
    {+2, +1, D, U},
    {+3, +1, L, U},
    {+1, +2, R, L},
    {-1, +2, L, R},
    {-1, +2, R, L},
    {-1, +3, U, R},
    {-2, +3, U, U},
}

// Hey, a practical use for goroutines.

func instruct( codes string, instr chan int ) {
	defer close(instr)
    accum := 0
	for i := range len(codes) {
		c := codes[i]
		if c == 'L' || c == 'R' {
            if accum > 0 {
                instr <- accum
                accum = 0
			}
            instr <- int(c)
        } else {
            accum = accum * 10 + int(c - '0')
		}
	}
    if accum > 0 {
		instr <- accum
	}
}

func padlines( mymap []string ) {
	maxw := 0
	for _,row := range mymap {
		maxw = max(maxw,len(row))
	}
	for y := range len(mymap) {
        if len(mymap[y]) < maxw {
            mymap[y] += strings.Repeat( " ", maxw-len(mymap[y]) )
		}
	}
}

func part1( mymap []string, codes string ) int {

	boxes := findLayout(mymap)

    // Pad the rows.
	padlines( mymap )

    direc := 0

    // Find the start.

    xy := boxes[0]

	instr := make(chan int)
	go instruct(codes, instr)

    for code := range instr {
        if DEBUG {
            fmt.Println("---",code)
		}
        if code == 'L' {
            direc = (direc + 3) % 4
        } else if  code == 'R' {
            direc = (direc + 1) % 4
        } else {
            dxdy := directions[direc]
            for _ = range code {
				xy0 := xy.Add(dxdy)

                // Handle wraps.

                if dxdy.X > 0 && (xy0.X >= len(mymap[xy0.Y]) || mymap[xy0.Y][xy0.X] == ' ') {
                    xy0.X = 0
				}
                if dxdy.X < 0 && (xy0.X < 0 || mymap[xy0.Y][xy0.X] == ' ') {
                    xy0.X = len(mymap[xy0.Y])-1
				}
                if dxdy.Y > 0 && (xy0.Y >= len(mymap) || mymap[xy0.Y][xy0.X] == ' ') {
                    xy0.Y = 0
				}
                if dxdy.Y < 0 && (xy0.Y < 0 || mymap[xy0.Y][xy0.X] == ' ') {
                    xy0.Y = len(mymap)-1
				}

                for mymap[xy0.Y][xy0.X] == ' ' {
					xy0 = xy0.Add(dxdy)
				}

                // Check for a wall.

                if mymap[xy0.Y][xy0.X] == '#' {
                    break
				}

				xy = xy0
                if DEBUG {
					fmt.Println(xy)
				}
			}
		}
	}

    if DEBUG {
        fmt.Println("final",xy)
	}
    return 1000*(xy.Y+1)+4*(xy.X+1)+direc
}



// Find the cube structure.

func find_cube(data []string, boxes []Point) map[Point]Point {
    trans := make(map[Point]Point)
	boxint := []Point{}
	for _,bpt := range boxes {
		boxint = append(boxint, Point{bpt.X/BOX,bpt.Y/BOX} )
	}

    // This finds all the direct connections, both directions.

	for n, xy := range boxint {
		for c, dxy := range directions {
			bi := slices.Index(boxint, xy.Add(dxy))
			if bi >= 0 {
				trans[Point{n,c}] = Point{bi,c}
				trans[Point{bi,c^2}] = Point{n,c^2}
			}
		}
	}


    for b := range 6 {
        for d := range 4 {
			if _,ok := trans[Point{b,d}]; ok {
                continue
			}
            xy := boxint[b]
			for _,rule := range rules {
				dxy := Point{rule[0],rule[1]}
				md := rule[2]
				od := rule[3]
				if _,ok := trans[Point{b,md}]; ok {
                    continue
				}
				xy0 := xy.Add(dxy)
				b0 := slices.Index(boxint, xy0)
                if b0 < 0 {
                    continue
				}
				if _,ok := trans[Point{b,md}]; !ok {
					trans[Point{b,md}] = Point{b0,od}
				}
				if _,ok := trans[Point{b0,od^2}]; !ok {
                    trans[Point{b0,od^2}] = Point{b,md^2}
				}
			}
		}
	}

    return trans
}

// Find the box ordinal that contains the point x,y.

func findbox(boxes []Point, xy Point) int {
	for bn, bxy := range boxes {
		if tools.Between(bxy.X, xy.X, bxy.X+BOX) && tools.Between(bxy.Y, xy.Y, bxy.Y+BOX) {
            return bn
		}
	}
    return -1
}

// Right to up: y becomes x
// Up to right
// Left to down
// Down to left

// \ d2 
//  \        R       D       L       U
//d1 \ sets  y       x       y       x
//-------------------------------------------
// R  |      y      N-y     N-y      y
//    |
// D  |     N-x      x       x      N-x
//    |
// L  |     N-y      y       y      N-y
//    |
// U  |      x      N-x     N-x      x

// This implements the truth table, but I don't think this is either
// easier to read nor more efficient than an if/elif chain.

func edgeover( d1 int, d2 int, pt Point) Point {
	var xy int
	if d1 == R || d1 == L {
        xy = pt.Y
    } else {
        xy = pt.X
	}
	if d1^d2 == 1 || d1^d2 == 2 {
        xy = BOX - 1 - xy
	}

    pt.X = 0
	pt.Y = 0
    if d2 == R || d2 == L {
		if d2 == L {
			pt.X = BOX-1
		}
        pt.Y = xy
    } else {
		pt.X = xy
		if d2 == U {
			pt.Y = BOX-1
		}
	}

    return pt
}


func part2( mymap []string, codes string ) int {
	boxes := findLayout(mymap)
    trans := find_cube(mymap,boxes)

    // Pad the rows.

    padlines( mymap )

    direc := 0

    // Find the start.

    xy := boxes[0]
    box := findbox(boxes, xy)

	instr := make(chan int)
	go instruct(codes, instr)

    for code := range instr {
        if DEBUG {
            fmt.Println("---",code)
		}
        if code == 'L' {
            direc = (direc + 3) % 4
        } else if code == 'R' {
            direc = (direc + 1) % 4
        } else {
            for _ = range code {
				xy0 := xy.Add(directions[direc])

                if box == findbox(boxes,xy0) {
                    if mymap[xy0.Y][xy0.X] == '#' {
                        break
					}
                    xy = xy0
                    continue
				}

				newbd := trans[Point{box,direc}]
				newbox := newbd.X
				newdir := newbd.Y

				xyoff := xy0.Sub(boxes[box])

                if DEBUG {
                    fmt.Println("FROM", box+1, "d",direc, xyoff, xy0)
				}
                xyoff = edgeover( direc, newdir, xyoff )
				xy0 = xyoff.Add(boxes[newbox])
                if DEBUG {
                    fmt.Println("  TO", newbox+1, "d",newdir, xyoff, xy0)
				}

                if mymap[xy0.Y][xy0.X] == '#' {
                    break
				}
				xy = xy0
				box = newbox
				direc = newdir
                if DEBUG {
                    fmt.Println(xy)
				}
			}
		}
	}

    if DEBUG {
        fmt.Println("final",xy)
	}
    return 1000*(xy.Y+1)+4*(xy.X+1)+direc
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	parts := strings.Split(input,"\n\n")
	data := strings.Split(parts[0],"\n") 
	codes := parts[1]
	// In both cases, the first line spans three sides.
	BOX = len(data[0])/3

	fmt.Println("Part 1:", part1(data,codes) )
	fmt.Println("Part 2:", part2(data,codes) )
}
