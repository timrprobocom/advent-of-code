package main

import (
	"fmt"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = []int{ 111111, 223450, 123789, 112233, 123444, 111122 }
var live = []int{ 254032,789860 }

func valid(pw int, part int ) bool {
	dig := fmt.Sprintf("%06d", pw)
    cnts := make([]int,10)
    for c := range 6 {
        if c < 5 && dig[c] > dig[c+1] {
            return false
		}
        cnts[dig[c]-'0'] ++
	}

    if part == 1 {
		// part 1
		for _,k := range cnts {
			if k >= 2 {
				return true
			}
		}
		return false
	} else {
		// part 2
        return slices.Contains(cnts, 2)
	}
	return false
}

func part1( part int, ranges []int ) int {
	cnt := 0
	for r := ranges[0]; r <= ranges[1]; r++ {
		if valid(r, part) {
			cnt++
		}
	}
	return cnt
}

func main() {
	var input []int
	TEST, DEBUG, input = tools.Setup(test, live)

    if TEST {
		for part := range 2 {
			for _,t := range input {
				fmt.Printf("Part %d: %d %t\n", part+1, t, valid(t,part+1) )
			}
		}
	} else {
		fmt.Println("Part 1:", part1(1, input))
		fmt.Println("Part 2:", part1(2, input))
	}
}

