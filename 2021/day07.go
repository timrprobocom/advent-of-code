package main

import (
	"fmt"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
16,1,2,0,4,2,7,1,2,14`[1:]

//go:embed day07.txt
var live string

var cost []int

func cost1( k int ) int {
	return k
}
func cost2( k int ) int {
	return cost[k]
}

func part1( data []int) int {
	return 0
}

var abs = tools.AbsInt[int]

func part2( data []int, cost func(int)int ) int {
    mf := 10000000000
	for avg := range tools.Max(data) {
		f := 0
		for _,k := range data {
			f += cost(abs(k-avg))
		}
        if f > mf {
            return mf
		}
        mf = f
	}
	return -1
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := tools.GetPosNumbers[int](input)[0]

	for i := range 2000 {
		cost = append( cost, i*(i+1)/2 )
	}

	fmt.Println("Part 1:", part2(data,cost1))
	fmt.Println("Part 2:", part2(data,cost2))
}
