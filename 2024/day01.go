package main

import (
	"fmt"
	"sort"
)

import _ "embed";

import "aoc/tools"

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

func part1(one []int, two []int) int {
    sumx := 0
    for i, p1 := range one {
          sumx += tools.AbsDiffInt(p1, two[i])
    }
    return sumx
}

func part2(one []int, two []int) int {
    sumx := 0
    for _, p1 := range one {
        sumx += p1 * tools.Count(two, p1)
    }
    return sumx
}

func main() {
    var input string
    TEST, DEBUG, input = tools.Setup(test,live)
    data := tools.Parse(input)

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
