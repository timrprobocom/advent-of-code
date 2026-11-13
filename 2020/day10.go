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

var test0 = `
16
10
15
5
1
11
7
19
6
12
4`[1:]

var test1 = `
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3`[1:]

var test = test1

//go:embed day10.txt
var live string


var diffs []int

func part1(data []int) int {
	fmt.Println(data)
	diffs = []int{}
	ones := 0
	threes := 0
	for i := range len(data)-1 {
		delta := data[i+1]-data[i]
		if delta == 1 {
			ones ++
		} else if delta == 3 {
			threes ++
		}
		diffs = append( diffs, delta )
	}

	if DEBUG {
		fmt.Println( diffs )
		fmt.Println( ones, threes )
		fmt.Println( tools.Count( diffs, 1 ))
		fmt.Println( tools.Count( diffs, 3 ))
	}

	return ones*threes
}

// Two 1s can be 2 ways     1 1 or 2
// Three 1s can be 4 ways:  1 1 1 or 2 1 or 1 2 or 3
// Four 1s can be 7 ways:   1 1 1 1 or 1 1 2 or 1 2 1 or 2 1 1 or 1 3 or 3 1 or 2 2
// Five 1s can be 13 ways:  1 1 1 1 1 or 2 1 1 1 or 1 2 1 1 or 1 1 2 1 or 1 1 1 2 or 2 2 1 or 2 1 2 or 1 2 2 or
//                            3 1 1 or 1 3 1 or 1 1 3 or 3 2 or 2 3
// +1 +2 +3 +6 

func part2x(data []int) int {

	mapping := map[int]int{ 2:2, 3:4, 4:7, 5:13 }

    // Count sequences of 1s.

	sequences := []int{}
	this := 0
	for _,i := range diffs {
		if i == 1 {
			this ++
		} else {
			if this >= 2 {
				sequences = append(sequences, this)
			}
			this = 0
		}
	}

	prod := 1
	for _,i := range sequences {
		prod *= mapping[i]
	}

	if DEBUG {
		fmt.Println(sequences)
	}

    return prod
}


// Why does this work?  
// It says the ways to get to N is the sum of the ways to get to the past 3.
// Is this dynamic programming?  I think this works because there are ONLY
// gaps of 1 and 3.

func part2( data []int ) int {
    adapters := make([]int, data[len(data)-1]+1)
    adapters[0] = 1
    for _,n := range data[1:] {
		if n == 1 {
		    adapters[n] = adapters[n-1]
		} else if n == 2 {
			adapters[n] = adapters[n-2] + adapters[n-1]
		} else {
			adapters[n] = adapters[n-3] + adapters[n-2] + adapters[n-1]
		}
	}
	return adapters[len(adapters)-1]
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	data := []int{0}
	for _,line := range strings.Fields(input) {
		data = append(data, tools.StrToInt(line))
	}
	slices.Sort(data)
	data = append(data, tools.Max(data)+3)

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
