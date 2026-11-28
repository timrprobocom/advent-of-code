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

//
// OK, on a 350x350 grid
// Find the distance from each point in the grid to each point in the 
//

var test = `
1 1
1 6
8 3
3 4
5 5
8 9`[1:]

//go:embed day06.txt
var live string

var SQ int
var TARGET int
var MAXD int

var abs = tools.AbsInt[int]

// Create a square grid of size sq containing -1.

func create( sq int, data [][]int) [][]int {
	mat := make([][]int, sq)
    for i := range sq {
		mat[i] = tools.Repeat( -1, sq )
	}
    for i,p := range data {
        mat[p[1]][p[1]] = i
	}
    return mat
}


func hamming(x0, y0, x1, y1 int) int {
    return abs(x0-x1) + abs(y0-y1)
}

func update( mat [][]int, data [][]int) {
	for y := range SQ {
		for x := range SQ {
			mind := 9999
			minxy := []int{}
			for i,pts := range data {
				man := hamming( x, y, pts[0], pts[1] )
				if man == mind {
					minxy = append( minxy, i )
				} else if man < mind {
					mind = man
					minxy = []int{i}
				}
			}
			if len(minxy) == 1 {
				mat[y][x] = minxy[0]
			}
		}
	}
}

func printgrid( mat [][]int ) {
    for y := range min(SQ,80) {
        s := []byte{}
		for x := range min(SQ,80) {
            c := mat[y+50][x+50]
            if c < 0 {
                s = append(s, '.')
            } else {
                s = append(s, byte(64+c) )
			}
		}
        fmt.Println(string(s))
	}
}



// Part 1

func part1( data [][]int, mat [][]int ) int {
	tots := make([]int,len(data))
	for y := range SQ {
		for x := range SQ {
            if mat[y][x] >= 0 {
                tots[mat[y][x]] ++
			}
		}
	}

    for n := range SQ {
        if mat[n][0] >= 0 {
			tots[mat[n][0]] = 0
		}
        if mat[n][SQ-1] >= 0 {
			tots[mat[n][SQ-1]] = 0
		}
        if mat[0][n] >= 0 {
			tots[mat[0][n]] = 0
		}
        if mat[SQ-1][n] >= 0 {
			tots[mat[SQ-1][n]] = 0
		}
	}
    if DEBUG {
        fmt.Println(tots)
	}
    return slices.Max(tots)
}

// Part 2

func part2( data [][]int ) int {
    knt := 0
	for y := -MAXD; y < MAXD; y++ {
        if DEBUG {
            fmt.Print(y,"\r")
		}
		for x := -MAXD; x < MAXD; x++ {
            sumh := 0
			for _,pt := range data {
                sumh += hamming(x,y,pt[0],pt[1])
                if sumh >= TARGET {
                    break
				}
			}
            if sumh < TARGET {
                if DEBUG {
                    fmt.Println(x,y)
				}
                knt ++
			}
		}
	}
    return knt
}

func choose( chk bool, ttt int, fff int ) int {
	if chk {
		return ttt
	}
	return fff
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, strings.TrimSpace(live))

	SQ     = choose(TEST, 10, 360)
	TARGET = choose(TEST, 32, 10000)
	MAXD   = choose(TEST, 25, 500)

	data := tools.GetNumbers[int](input)
	mat := create(SQ, data)
	update( mat, data )

	fmt.Println("Part 1:", part1(data, mat))
	fmt.Println("Part 2:", part2(data))
}
