package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var live = []int{0,20,7,16,1,18,15}

// Given the starting numbers 0,3,6, the 2020th number spoken is 465.
// Given the starting numbers 1,3,2, the 2020th number spoken is 1.
// Given the starting numbers 2,1,3, the 2020th number spoken is 10.
// Given the starting numbers 1,2,3, the 2020th number spoken is 27.
// Given the starting numbers 2,3,1, the 2020th number spoken is 78.
// Given the starting numbers 3,2,1, the 2020th number spoken is 438.
// Given the starting numbers 3,1,2, the 2020th number spoken is 1836.

// Given 0,3,6, the 30000000th number spoken is 175594.
// Given 1,3,2, the 30000000th number spoken is 2578.
// Given 2,1,3, the 30000000th number spoken is 3544142.
// Given 1,2,3, the 30000000th number spoken is 261214.
// Given 2,3,1, the 30000000th number spoken is 6895259.
// Given 3,2,1, the 30000000th number spoken is 18.
// Given 3,1,2, the 30000000th number spoken is 362.


func part1(data []int, count int) int {
	found := make([]int, count)
	for i := range count {
		found[i] = -1
	}
    for i,t := range data[:len(data)-1] {
        found[t] = i+1
	}
    nextx := data[len(data)-1]
	for tape := len(data); tape < count; tape++ {
        if DEBUG && tape % 1000000 == 0 {
            fmt.Printf( "  %d%%\r", tape * 100 / count )
		}
		lastx := tape
		if found[nextx] >= 0 {
			lastx = found[nextx]
		}
        found[nextx] = tape
        nextx = tape - lastx
	}

    return nextx
}

func main() {
	var input []int
	TEST, DEBUG, input = tools.Setup(live, live)

	fmt.Println("Part 1:", part1(input,2020))
	fmt.Println("Part 1:", part1(input,30000000))
}





