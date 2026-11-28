package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2`[1:]

//go:embed day03.txt
var live string


// Pass 1, determine the size;

// Returns an empty XxY matrix.

func makematrix( x, y int ) [][]int {
	matrix := make([][]int,y)
    for n := range y {
		matrix[n] = make([]int, x)
	}
    return matrix
}

func maxi( nums [][]int ) (int,int) {
    maxx := 0
    maxy := 0
    for _, row := range nums {
        if DEBUG {
            fmt.Println( row )
		}
		maxx = max(maxx, row[1] + row[3])
		maxy = max(maxy, row[2] + row[4])
	}
    return maxx, maxy
}

func fill( mat [][]int, nums [][]int ) [][]int {
	for _,row := range nums {
        for dx := range(row[3]) {
            for dy := range(row[4]) {
                mat[row[2]+dy][row[1]+dx] ++
			}
		}
	}
    return mat
}


func part1( mat [][]int ) int {
    tot := 0
    for _,row := range(mat) {
        for _,col := range(row) {
            if col > 1 {
                tot ++
			}
		}
	}
    return tot
}

func part2( mat [][]int, data [][]int) int {
    for _,row := range data {
        winner := true
        for dx := range row[3] {
            for dy := range row[4] {
                if mat[row[2]+dy][row[1]+dx] > 1 {
                    winner = false
                    break
				}
			}
            if ! winner {
                break
			}
		}
        if winner {
            return row[0]
		}
	}
    return -1
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

    data := tools.GetNumbers[int]( input )

	w,h := maxi( data )
	mat := makematrix( w, h )
	fill( mat, data )

	fmt.Println("Part 1:", part1(mat))
	fmt.Println("Part 2:", part2(mat, data))
}

