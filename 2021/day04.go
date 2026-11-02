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

var test = `
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7`[1:]

//go:embed day04.txt
var live string


// Check for bingo winner.
func check( board []int ) bool {
    for row := range 5 {
        if tools.Sum(board[row*5:row*5+5]) == -5 {
            return true
		}
		down := 0
		for i := range 5 {
			down += board[row+i*5]
		}
		if down == -5 {
			return true
		}
	}
    return false
}


func all( vals []bool ) bool {
	for _,b := range vals {
		if !b {
			return false
		}
	}
	return true
}


func part1(part int, boardin [][]int, calls []int) int {

	// Make a copy, since we modify it.
	
	boards := make([][]int, len(boardin))
	for i := range boardin {
		boards[i] = make([]int, len(boardin[i]) )
		copy( boards[i], boardin[i] )
	}

	done := make([]bool,len(boards))

    for _,call := range calls {
        for bno,board := range boards {
            if board[0] == 100 {
                continue
			}
			i := slices.Index(board, call)
			if i >= 0 {
                board[i] = -1
                if check(board) {
                    if DEBUG {
                        fmt.Println("WINNER", call, bno, board)
					}
                    done[bno] = true
                    if part == 1 || all(done) {
						sumx := 0
						for _,x := range board {
							if x > 0 {
								sumx += x
							}
						}
                        return sumx * call
					}
				}
			}
		}
	}
	return 0
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	boards := [][]int{}
	calls := []int{}
	for i,block := range strings.Split(input,"\n\n") {
		if i == 0 {
			calls = tools.GetNumbers[int](block)[0]
		} else {
			board := tools.GetNumbers[int](strings.ReplaceAll( block, "\n"," "))[0]
			boards = append( boards, board )
		}
	}

	fmt.Println("Part 1:", part1(1, boards, calls)) // 34506
	fmt.Println("Part 2:", part1(2, boards, calls)) // 7686
}

