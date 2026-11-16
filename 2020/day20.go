package main

import (
	"fmt"
	"math"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)


var DEBUG bool = false
var TEST bool = false

//go:embed test20.txt
var test string

//go:embed day20.txt
var live string


// Which edge is it?  
// 0 = N
// 1 = S
// 2 = E
// 3 = W
// 4 = N rev
// 5 = S rev
// 6 = E rev
// 7 = W rev

// Contains the list of tiles that contain the edge string.
var edges map[string][]int
// Contains the set of tiles that adjoin this tile.
var matches map[int]map[int]bool
// Contains the strings for each rotation.
var rotations map[int][]string

var gridsize int


func record( tno int, reflect int, edge string ) {
	_,ok := rotations[tno]
    if ! ok {
        rotations[tno] = make([]string,8)
	}
    rotations[tno][reflect] = edge
	edges[edge] = append( edges[edge], tno )
}

func reverse(s string) string {
	out := []byte{}
	for i := len(s)-1; i >= 0; i-- {
		out = append(out,s[i])
	}
	return string(out)
}

/*
func prod[T tools.Number]( nums []T ) T {
	var p T = 1
	for _,i := range nums {
		p *= i
	}
	return p
}
*/


func part1() int {
	p := 1
	for t, tlist := range matches {
		fmt.Println(t,tlist)
		if len(tlist) == 2 {
			p *= t
		}
	}
	return p
}

// How do we stitch this together?
// The 2s have to be corners.  The 3s are edges.  The 4s are centers.

func findgrid( ) [][]int {
	grid := make([][]int, gridsize)
	for i := range gridsize {
		grid[i] = make([]int, gridsize)
	}

    placed := make(map[int]bool)

    // So, pick one of the 2s.  This will be a corner

    for e,tlist := range matches {
        if len(tlist) == 2 {
            grid[0][0] = e
            placed[e] = true
            break
		}
	}

    // We can fill out the row by just picking the first match.

	for col := 1; col < gridsize-1; col++ {
        for e,tlist := range matches {
			if !placed[e] && len(tlist) == 3 && tlist[grid[0][col-1]] {
                grid[0][col] = e
                placed[e] = true
                break
			}
		}
	}

    // Pick a right corner, a match where len = 2.

	for e,_ := range matches[grid[0][gridsize-2]] {
        if !placed[e] && len(matches[e]) == 2 {
            grid[0][gridsize-1] = e
            placed[e] = true
            break
		}
	}
    
    // Now do middle rows.
	// Middle row tlists will be 3, 4, 4, ..., 4, 3.

	for row := 1; row < gridsize-1; row++ {
        for e,tlist := range matches {
            if !placed[e] && len(tlist) == 3 && tlist[grid[row-1][0]] {
                grid[row][0] = e
                placed[e] = true
                break
			}
		}

		for col := 1; col < gridsize-1; col++ {
            for e,tlist := range matches {
                if !placed[e] && len(tlist) == 4 && tlist[grid[row][col-1]] && tlist[grid[row-1][col]] {
                    grid[row][col] = e
                    placed[e] = true
                    break
				}
			}
		}

        for e,tlist := range matches {
			if !placed[e] && len(tlist) == 3 && tlist[grid[row-1][gridsize-1]] {
                grid[row][gridsize-1] = e
                placed[e] = true
                break
			}
		}
	}
		
    // Now do last row.

    for e,tlist := range matches {
		if !placed[e] && len(tlist) == 2 && tlist[grid[gridsize-2][0]] {
            grid[gridsize-1][0] = e
            placed[e] = true
            break
		}
	}

	for col := 1; col < gridsize-1; col++ {
        for e,tlist := range matches {
			if !placed[e] && len(tlist) == 3 && tlist[grid[gridsize-2][col]] { // checking [-1]col-1] not needed?
                grid[gridsize-1][col] = e
                placed[e] = true
                break
			}
		}
	}

	// There should be only one left.
    for e,tlist := range matches {
		if !placed[e] && len(tlist) == 2 && 
			tlist[grid[gridsize-1][gridsize-2]] && tlist[grid[gridsize-2][gridsize-1]] {
            grid[gridsize-1][gridsize-1] = e
			placed[e] = true
            break
		}
	}

	if DEBUG {
		fmt.Println(grid)
	}
    return grid
}

func r_hflip( tile []string ) []string {
	// Horizontal flip.
	out := []string{}
	for _,ln := range tile {
		out = append(out, reverse(ln))
	}
	return out
}

func r_vflip( tile []string ) []string {
    // Vertical flip.
	out := []string{}
	for i := len(tile)-1; i >= 0; i-- {
		out = append(out, tile[i])
	}
	return out
}

func r_rot90cw( tile []string ) []string {
    // Clockwise rotation.
	llen := len(tile)
	out := []string{}
	for nrow := range llen {
		row := []byte{}
		for ncol := range llen {
			row = append( row, tile[llen-ncol-1][nrow] )
		}
		out = append( out, string(row) )
	}
	return out
}

const (
	N = iota
	S
	E
	W
)

// rotations (right, down)
//  E S == nothing
//  E N == v flip
//  W S == h flip
//  W N == h flip, v flip
//  N E == rot 90 cw
//  N W == h flip, rot 90 cw
//  S E == h flip, v flip, rot 90 cw
//  S W == v flip, rot 90 cw

// So, if the right side was the E edge and the bottom side was the S edge, no rotation.

type Pair struct {
    right int
	down  int
}

type Rotate = func([]string)[]string

var rotate_mapping = map[Pair][]Rotate{
    Pair{E,S}: []Rotate{},
    Pair{E,N}: []Rotate{r_vflip,},
    Pair{W,S}: []Rotate{r_hflip,},
    Pair{W,N}: []Rotate{r_hflip, r_vflip},
    Pair{N,E}: []Rotate{r_rot90cw,},
    Pair{N,W}: []Rotate{r_hflip, r_rot90cw},
    Pair{S,E}: []Rotate{r_vflip, r_rot90cw},
    Pair{S,W}: []Rotate{r_hflip, r_vflip, r_rot90cw},
}

func rotate_cell( tiles map[int][]string, target int, found1, found2 int ) {
	for _,xform := range rotate_mapping[Pair{found1,found2}] {
        tiles[target] = xform(tiles[target])
	}
}

func rotate_grid( tiles map[int][]string, grid [][]int ) {
    // For each element, find which one they have in common, right and down.
    for row := range gridsize-1 {
        for col := range gridsize-1 {
            target := grid[row][col]
            // Find the grid matches.
			if DEBUG {
				fmt.Println( row, col, target, grid[row][col+1], grid[row+1][col] )
			}
			found1 := -1
			found2 := -1
            for m,ms := range rotations[target][:4] {
				if slices.Contains( rotations[grid[row][col+1]], ms ) {
                    found1 = m
                    break
				}
			}
            for m,ms := range rotations[target][:4] {
				if slices.Contains( rotations[grid[row+1][col]], ms ) {
                    found2 = m
                    break
				}
			}
            rotate_cell( tiles, target, found1, found2 )
		}
	}

    // Do the right column.  Check left and down.
    col := gridsize-1
    for row := range gridsize-1 {
        target := grid[row][col]
		if DEBUG {
			fmt.Println( row, gridsize-1, target, grid[row][col-1], grid[row+1][col] )
		}
		found1 := -1
		found2 := -1
		for m,ms := range rotations[target][:4] {
			if slices.Contains( rotations[grid[row][col-1]], ms ) {
                found1 = m ^ 1
                break
			}
		}
		for m,ms := range rotations[target][:4] {
			if slices.Contains( rotations[grid[row+1][col]], ms ) {
                found2 = m
                break
			}
		}
        rotate_cell( tiles, target, found1, found2 )
	}

    // Do the bottom row.  Check right and up.
    row := gridsize-1
    for col := range gridsize-1 {
        target := grid[row][col]
		if DEBUG {
			fmt.Println( row, col, target, grid[row][col-1], grid[row][col-1] )
		}
		found1 := -1
		found2 := -1
		for m,ms := range rotations[target][:4] {
			if slices.Contains( rotations[grid[row][col+1]], ms ) {
                found1 = m 
                break
			}
		}
		for m,ms := range rotations[target][:4] {
			if slices.Contains( rotations[grid[row-1][col]], ms ) {
                found2 = m ^ 1
                break
			}
		}
        rotate_cell( tiles, target, found1, found2 )
	}

    // Do the final cell, do up and left.
	col = gridsize-1
	row = gridsize-1
    target := grid[row][col]
	found1 := -1
	found2 := -1
	if DEBUG {
		fmt.Println( gridsize-1, gridsize-1, target, grid[row][col-1], grid[col-1][row] )
	}
    for m,ms := range rotations[target][:4] {
		if slices.Contains( rotations[grid[row][col-1]], ms ) {
            found1 = m ^ 1
            break
		}
	}
    for m,ms := range rotations[target][:4] {
		if slices.Contains( rotations[grid[row-1][col]], ms ) {
            found2 = m ^ 1
            break
		}
	}
    rotate_cell( tiles, target, found1, found2 )
}


func stitchgrid( tiles map[int][]string, grid [][]int) []string {
	biggrid := []string{}
    subrows := len(tiles[grid[0][0]])
	fmt.Println("subrows",subrows)
	for _,row := range grid {
		for y := 1; y < subrows-1; y++ {
            line := ""
            for _,col := range row {
				line += tiles[col][y][1:subrows-1]
			}
            biggrid = append( biggrid, line )
		}
	}
    return biggrid
}

/*
01234567890123456789
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
*/

type Point struct {
	Y int
	X int
}

var monster = []Point{
    Point{0,18},
    Point{1,0},Point{1,5},Point{1,6},Point{1,11},Point{1,12},Point{1,17},Point{1,18},Point{1,19},
    Point{2,1},Point{2,4},Point{2,7},Point{2,10},Point{2,13},Point{2,16},
}

var msize = Point{3,20}

// TODO
// We COULD flip/rotate this map instead of 8 loops.

// VFLIP replaces Y,X with  maxY-1-Y,X
// HFLIP replaces Y,X with  Y, maxX-1-X
// ROT90CW replaces Y,X with X,Y

func makeRotatedMonsters() [][]Point {
	monsters := [][]Point{monster}

	// H flip that.
	mrow := []Point{}
	for _,pt := range monsters[len(monsters)-1] {
		mrow = append( mrow, Point{pt.Y, msize.X-pt.X-1} )
	}
	monsters = append(monsters, mrow)

	// V flip that.
	mrow = []Point{}
	for _,pt := range monsters[len(monsters)-1] {
		mrow = append( mrow, Point{msize.Y-pt.Y-1, pt.X} )
	}
	monsters = append(monsters, mrow)

	// H flip that.
	mrow = []Point{}
	for _,pt := range monsters[len(monsters)-1] {
		mrow = append( mrow, Point{pt.Y, msize.X-pt.X-1} )
	}
	monsters = append(monsters, mrow)

	// Rotate that.
	mrow = []Point{}
	for _,pt := range monsters[len(monsters)-1] {
		mrow = append( mrow, Point{pt.Y, pt.X} )
	}
	monsters = append(monsters, mrow)

	// H flip that.
	mrow = []Point{}
	for _,pt := range monsters[len(monsters)-1] {
		mrow = append( mrow, Point{pt.Y, msize.X-pt.X-1} )
	}
	monsters = append(monsters, mrow)

	// V flip that.
	mrow = []Point{}
	for _,pt := range monsters[len(monsters)-1] {
		mrow = append( mrow, Point{msize.Y-pt.Y-1, pt.X} )
	}
	monsters = append(monsters, mrow)

	// H flip that.
	mrow = []Point{}
	for _,pt := range monsters[len(monsters)-1] { 
		mrow = append( mrow, Point{pt.Y, msize.X-pt.X-1} )
	}
	monsters = append(monsters, mrow)
	fmt.Println(monsters)

	return monsters
}


func checkMonster( biggrid []string, row, col int, monster []Point ) bool {
	for _,dxy := range monster {
		if biggrid[row+dxy.Y][col+dxy.X] != '#' {
			return false
		}
	}
	return true
}

func search( biggrid []string ) int {
    // Once we find one, the rest will be in the same orientation.
    count := 0
    found := 0
    bglen := len(biggrid)

    monsters := makeRotatedMonsters()
	// The first 4 are 20x3.  The last 4 are 3x20.

	for n,monster := range monsters {
		if found != 0 && found != n {
			continue
		}
		rowlim := msize.Y
		collim := msize.X
		if n >= 4 {
			rowlim = msize.X
			collim = msize.Y
		}

		for row := range bglen-rowlim {
			for col := range bglen-collim {
				if checkMonster( biggrid, row, col, monster ) {
					count ++
					found = n
					if DEBUG {
						fmt.Println( "FOUND", n  )
					}
				}
			}
		}
	}

    return count
}



func part2( tiles map[int][]string, count int ) int {
	grid := findgrid()
	rotate_grid(tiles, grid)
	biggrid := stitchgrid( tiles, grid )

	if DEBUG {
		for _,ln := range biggrid {
			fmt.Println( ln )
		}
	}

	ogres := search(biggrid)
	return count - 15 * ogres
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n\n")

	edges = make(map[string][]int)
	matches = make(map[int]map[int]bool)
	rotations = make(map[int][]string)
	 
	count := 0
	tiles := make(map[int][]string)
	for _,tile := range data {
		grid := strings.Split(tile, "\n")
		tileno := tools.StrToInt(grid[0][5:len(grid[0])-1])
		grid = grid[1:]
		matches[tileno] = make(map[int]bool)
		tiles[tileno] = grid

		for _,t := range grid[1:len(grid)-1] {
			count += strings.Count(t[1:len(t)-1], "#")
		}

		// Record all possible reflections.

		col0 := []byte{}
		col9 := []byte{}
		for _,g := range grid {
			col0 = append(col0, g[0])
			col9 = append(col9, g[len(g)-1])
		}
		g1 := string(col0)
		g2 := string(col9)

		record( tileno, 0, grid[0] )
		record( tileno, 4, reverse(grid[0]) )
		record( tileno, 1, grid[len(grid)-1] )
		record( tileno, 5, reverse(grid[len(grid)-1]) )
		record( tileno, 3, g1 )
		record( tileno, 7, reverse(g1) )
		record( tileno, 2, g2 )
		record( tileno, 6, reverse(g2) )
	}

	// Which tiles have edges in common?

	fmt.Println(edges)
	for _,tlist := range edges {
		if len(tlist) > 1 {
			matches[tlist[0]][tlist[1]] = true
			matches[tlist[1]][tlist[0]] = true
		}
	}

	// Test is 3x3, count is 303.
	// Live is 12x12, count is 2806 - 15 * 12.

	gridsize = int(math.Sqrt(float64(len(data))))
	fmt.Println( gridsize, count )

	fmt.Println("Part 1:", part1() )
	fmt.Println("Part 2:", part2(tiles, count))
}

