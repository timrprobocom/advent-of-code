package main

import (
	"fmt"
	"os"
)

import _ "embed"

// Tools.

func absInt(x int) int {
    return absDiffInt(x, 0)
}

func absDiffInt(x, y int) int {
    if x < y {
        return y - x
    }
    return x - y
}

func remove( row []int, index int ) []int {
    clone := append( row[:0:0], row...)
    return append( clone[0:index], clone[index+1:]... )
}

func setup() string {
    for _, arg := range os.Args {
        if arg == "debug" {
            DEBUG = true
        }
        if arg == "test" {
            TEST = true
        }
    }

    if TEST {
        return test
    } else {
        return live
    }
}

// Produce a matrix of ints from the input.

func parse( input string ) [][]int {
    result := make([][]int, 0)
    var row []int
    var accum int
    sign := 1
    last := '?'
    for _, c := range input {
        switch c {
        case '\n':
            row = append( row, sign*accum )
            result = append( result, row )
            row = make([]int, 0)
            accum = 0
            sign = 1
        case ' ':
            if last != ' ' {
                row = append( row, sign*accum )
                accum = 0
                sign = 1
            }
        case '-':
            sign = -1
        case '0','1','2','3','4','5','6','7','8','9':
            accum = accum * 10 + int(c) - '0';
        default:
            print("Unexpected ", c)
        }
        last = c
    }
    if len(row) > 0 {
        result = append( result, row )
    }
    return result
}

// End tools.

var DEBUG bool = false
var TEST bool = false

var test = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`

//go:embed day02.txt
var live string

func is_safe( row []int ) bool {
    for i := 0; i < len(row)-1; i++ {
        x := row[i]
        y := row[i+1]
        if (y-x) * (row[1]-row[0]) < 0 {
            return false
        }
        if absInt(y-x) < 1 || absInt(y-x) > 3 {
            return false
        }
    }
    return true
}


func part1( data [][]int  ) int {
    sumx := 0
    for _, row := range data {
        if is_safe(row) {
            sumx++
        }
    }
    return sumx
}

func part2( data [][]int ) int {
    safe := 0
    for _, row := range data {
        if is_safe(row) {
            safe++
        } else {
            for i := 0; i < len(row); i++ {
                if is_safe(remove(row,i)) {
                    safe++
                    break
                }
            }
        }
    }
    return safe
}


func main() {
    input := setup()

    data := parse( input )

    fmt.Println("Part 1:", part1(data))
    fmt.Println("Part 2:", part2(data))
}
