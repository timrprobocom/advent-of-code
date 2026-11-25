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
....#
#..#.
#..##
..#..
#....`[1:]

var live = `
...#.
#.##.
#..##
#.###
##...`[1:]

type Point = tools.Point

func makegrid( data []string ) [][]int8 {
    grid := make([][]int8,5)
	// '.' is 46, '#' is 35.
    for y,ln := range data {
		grid[y] = make([]int8,5)
		for x := range(len(ln)) {
			if ln[x] == '#' {
				grid[y][x] = 1
			}
		}
	}
    return grid
}

func rating( grid [][]int8 ) int {
	sum := 0
	for i := range 25 {
	    c := grid[i/5][i%5]
		sum += int(c) << i
	}
	return sum
}

var valid = []int{0,1,2,3,4}

var checks = []Point{{-1,0},{1,0},{0,-1},{0,1}}

func cycle( grid [][]int8 ) [][]int8 {
    newgrid := make([][]int8, len(grid))
    for y := range len(grid) {
		newgrid[y] = make([]int8, len(grid[0]))
        for x := range len(grid[0]) {
			pt := Point{x,y}
			var neighbors int8 = 0
			for _,dxy := range checks {
				ptx := pt.Add(dxy)
			    if tools.Between(0, ptx.X, 5) && tools.Between(0, ptx.Y, 5) {
					neighbors += grid[ptx.Y][ptx.X]
				}
            }
            if neighbors == 1 || (neighbors == 2 && grid[y][x] == 0) {
                newgrid[y][x] = 1
			}
		}
	}
    return newgrid
}


func printgrid( grid [][]int8) {
	for _,row := range grid {
		out := make([]byte,5)
		for i := range len(row) {
			out[i] = ".#"[row[i]]
		}
		fmt.Println(string(out))
	}
}


func part1(grid [][]int8) int {
	values := make(map[int]int)
	r := rating(grid)
	values[r] = 0

	for i := 1; true; i++ {
		grid = cycle(grid)
		r = rating(grid)
		if DEBUG {
			printgrid( grid )
			fmt.Println( i, r )
		}
		if values[r] > 0 {
			if DEBUG {
				fmt.Println( r )
			}
			break
		}
		values[r] = i
	}
	return r
}


// Part 1 and part 2 really are very different.


//     |     |         |     |     
// 0,0 | 1,0 |   2,0   | 3,0 | 4,0 
//     |     |         |     |     
//-----+-----+---------+-----+-----
//     |     |         |     |     
// 0,1 | 1,1 |   2,1   | 3,1 | 4,1 
//     |     |         |     |     
//-----+-----+---------+-----+-----
//     |     |A|B|C|D|E|     |     
//     |     |-+-+-+-+-|     |     
//     |     |F|G|H|I|J|     |     
//     |     |-+-+-+-+-|     |     
// 0,2 | 1,2 |K|L|?|N|O| 3,2 | 4,2 
//     |     |-+-+-+-+-|     |     
//     |     |P|Q|R|S|T|     |     
//     |     |-+-+-+-+-|     |     
//     |     |U|V|W|X|Y|     |     
//-----+-----+---------+-----+-----
//     |     |         |     |     
// 0,3 | 1,3 |   2,3   | 3,3 | 4,3 
//     |     |         |     |     
//-----+-----+---------+-----+-----
//     |     |         |     |     
// 0,4 | 1,4 |   2,4   | 3,4 | 4,4 
//     |     |         |     |     
//Tile 19 has four adjacent tiles: 14, 18, 20, and 24.
//Tile G has four adjacent tiles: B, F, H, and L.
//Tile D has four adjacent tiles: 8, C, E, and I.
//Tile E has four adjacent tiles: 8, D, 14, and J.
//Tile 14 has eight adjacent tiles: 9, E, J, O, T, Y, 15, and 19.
//Tile N has eight adjacent tiles: I, O, S, and five tiles within the sub-grid marked ?.

//  0,0 has 4:  (1,2,-1)  (2,1,-1)  (1,0,0)  (0,1,0)
//  1,0 has 4:  (0,0,0)   (2,1,-1)  (2,0,0)  (1,1,0)
//  2,0 has 4:  (1,0,0)   (2,1,-1)  (3,0,0)  (2,1,0)
//  3,0 has 4:  (2,0,0)   (2,1,-1)  (4,0,0)  (3,1,0)
//  4,0 has 4:  (3,0,0)   (2,1,-1)  (3,2,-1) (4,1,0)

//  0,1 has 4:  (1,2,-1)  (0,0,0)   (1,1,0)  (0,2,0)
//  1,1 has 4:  (0,1,0)   (1,0,0)   (2,1,0)  (1,2,0)
//  2,1 has 8:  (1,1,0)   (2,0,0)   (3,1,0)  (*,0,1)
//  3,1 has 4:  (2,1,0)   (3,0,0)   (4,1,0)  (3,2,0)
//  4,1 has 4:  (3,1,0)   (4,0,0)   (3,2,-1) (4,2,0)

//  0,2 has 4:  (1,2,-1)  (0,1,0)   (1,2,0)  (0,3,0)
//  1,2 has 8:  (0,2,0)   (1,1,0)   (0,*,0)  (1,2,0)
//  2,2 has 1:  (2,2,0)
//  3,2 has 8:  (4,*,0)   (3,1,0)   (4,2,0)  (3,3,0)
//  4,2 has 4:  (3,2,0)   (4,1,0)   (1,2,-1) (4,3,0)

//  0,3 has 4:  (1,2,-1)  (0,2,0)   (1,3,0)  (0,4,0)
//  1,3 has 4:  (0,1,0)   (1,2,0)   (2,3,0)  (1,4,0)
//  2,3 has 8:  (1,1,0)   (2,2,0)   (3,3,0)  (*,0,1)
//  3,3 has 4:  (2,1,0)   (3,2,0)   (4,3,0)  (3,4,0)
//  4,3 has 4:  (3,1,0)   (4,2,0)   (3,2,-1) (4,4,0)

//  0,4 has 4:  (1,2,-1)  (0,3,0)   (1,4,0)  (2,3,-1)
//  1,4 has 4:  (0,4,0)   (1,3,0)   (2,4,0)  (2,3,-1)
//  2,4 has 4:  (1,4,0)   (2,3,0)   (3,4,0)  (2,3,-1)
//  3,4 has 4:  (2,4,0)   (3,3,0)   (4,4,0)  (2,3,-1)
//  4,4 has 4:  (3,4,0)   (4,3,0)   (3,2,-1) (2,3,-1)

type Point3 struct {
	x	int
	y	int
	z	int
}

var coords = [][][]Point3{
//         W         N         E        S
    {
     { {1,2,-1}, {2,1,-1}, {1,0,0}, {0,1,0}},
     { {0,0,0},  {2,1,-1}, {2,0,0}, {1,1,0}},
     { {1,0,0},  {2,1,-1}, {3,0,0}, {2,1,0}},
     { {2,0,0},  {2,1,-1}, {4,0,0}, {3,1,0}},
     { {3,0,0},  {2,1,-1}, {3,2,-1},{4,1,0}},
    },
    {
     { {1,2,-1}, {0,0,0},  {1,1,0}, {0,2,0}},
     { {0,1,0},  {1,0,0},  {2,1,0}, {1,2,0}},
     { {1,1,0},  {2,0,0},  {3,1,0},          {0,0,1}, {1,0,1}, {2,0,1}, {3,0,1}, {4,0,1}},
     { {2,1,0},  {3,0,0},  {4,1,0}, {3,2,0}},
     { {3,1,0},  {4,0,0},  {3,2,-1},{4,2,0}},
    },
    {
     { {1,2,-1}, {0,1,0},  {1,2,0}, {0,3,0}},
     { {0,2,0},  {1,1,0},           {1,3,0}, {0,0,1}, {0,1,1}, {0,2,1}, {0,3,1}, {0,4,1}},
     { {2,2,0}, },
     {           {3,1,0},  {4,2,0}, {3,3,0}, {4,0,1}, {4,1,1}, {4,2,1}, {4,3,1}, {4,4,1}}, 
     { {3,2,0},  {4,1,0},  {3,2,-1},{4,3,0}},
    },
    {
     { {1,2,-1}, {0,2,0},  {1,3,0}, {0,4,0}},
     { {0,3,0},  {1,2,0},  {2,3,0}, {1,4,0}},
     { {1,3,0},            {3,3,0}, {2,4,0}, {0,4,1}, {1,4,1}, {2,4,1}, {3,4,1}, {4,4,1}},
     { {2,3,0},  {3,2,0},  {4,3,0}, {3,4,0}},
     { {3,3,0},  {4,2,0},  {3,2,-1},{4,4,0}},
    },
    {
     { {1,2,-1}, {0,3,0},  {1,4,0}, {2,3,-1}},
     { {0,4,0},  {1,3,0},  {2,4,0}, {2,3,-1}},
     { {1,4,0},  {2,3,0},  {3,4,0}, {2,3,-1}},
     { {2,4,0},  {3,3,0},  {4,4,0}, {2,3,-1}},
     { {3,4,0},  {4,3,0},  {3,2,-1},{2,3,-1}},
    },
}


func makegrids( depth int ) [][][]int8 {
	grid := make([][][]int8, depth+1)
	for lvl := range depth+1 {
		grid[lvl] = make([][]int8, 5)
		for y := range 5 {
			grid[lvl][y] = make([]int8, 5)
		}
	}
    return grid
}

func onelevel( grid [][][]int8, lvl int ) [][]int8 {
    depth := len(grid)
    newgrid := make([][]int8,5)
    for y := range 5 {
        newgrid[y] = make([]int8,5)
        for x := range 5 {
			var nbrs int8 = 0
			for _,dxy := range coords[y][x] {
			    if tools.Between(0, lvl+dxy.z, depth) {
					nbrs += grid[lvl+dxy.z][dxy.y][dxy.x] 
				}
			}
            if nbrs == 1 || (nbrs == 2 && grid[lvl][y][x] == 0) {
                newgrid[y][x] = 1
			}
		}
	}
    return newgrid
}

func doall( grid [][][]int8 ) [][][]int8 {
	newgrid := make([][][]int8, len(grid))
	for lvl := range len(grid) {
		newgrid[lvl] = onelevel(grid,lvl)
	}
    return newgrid
}

func fancyrow( depth int, level int, subgrids [][][]int8 ) int {
	if DEBUG {
		for ii := range len(subgrids) {
			fmt.Printf( "    %4d", level+ii-depth)
		}
		fmt.Println()
	}

	sumx := 0
	for y := range 5 {
		s := []byte{}
		for _,g := range subgrids {
			s = append( s, []byte("   ")... )
			for x := range 5 {
				s = append( s, ".#"[g[y][x]])
				sumx += int(g[y][x])
			}
		}
		if DEBUG {
			fmt.Println(string(s))
		}
	}
	if DEBUG {
		fmt.Println()
	}

    return sumx
}

func fancyprint(grid [][][]int8) int {
    depth := len(grid) / 2
    sumx := 0
	for i := 0; i < len(grid); i+=10 {
        sumx += fancyrow( depth, i, grid[i:min(i+10,len(grid))] )
	}
    return sumx
}

func part2( center [][]int8, depth int ) int {
    grids := makegrids( depth )
    grids[depth/2] = center
    for range(depth) {
        grids = doall(grids)
	}
    return fancyprint(grids)
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n")

	grid := makegrid(data)
	if DEBUG {
		printgrid( grid )
		fmt.Println( rating( grid) )
	}

	depth := 200
	if TEST {
		depth = 10
	}

	fmt.Println( "Part 1:", part1(grid))
	fmt.Println( "Part 2:", part2(grid, depth))
}


