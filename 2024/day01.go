package main

import (
	"fmt"
	"os"
	"sort"
)

import _ "embed";

var DEBUG bool = false
var TEST bool = false
var test = `3   4
4   3
2   5
1   3
3   9
3   3`

//go:embed day01.txt
var live string

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

func Count(haystack []int, needle int) int {
    count := 0
    for _, i := range haystack {
        if i == needle {
           count += 1
	}
    }
    return count
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
        result = append( result, append( row, sign*accum ) )
    }
    return result
}

// End tools.

func part1(one []int, two []int) int {
    sumx := 0
    for i, p1 := range one {
          sumx += absDiffInt(p1, two[i])
    }
    return sumx
}

func part2(one []int, two []int) int {
    sumx := 0
    for _, p1 := range one {
        sumx += p1 * Count(two, p1)
    }
    return sumx
}

func main() {
    input := setup()
    data := parse(input)

    var one []int
    var two []int
    for _, row := range data {
        one = append( one, row[0] )
        two = append( two, row[1] )
    }

    sort.Ints(one)
    sort.Ints(two)
    fmt.Println("Part 1:", part1(one, two))
    fmt.Println("Part 2:", part2(one, two))
}
